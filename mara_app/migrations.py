"""Automigration of sql alchemy models with alembic. Automigration means that no intermediate files are created,
 instead diffs are immediately applied. Use with care.
"""
import gc
import io
import sys

import alembic
import alembic.autogenerate
import alembic.migration
import alembic.operations
import sqlalchemy
import sqlalchemy.ext.declarative.api
import sqlalchemy_utils


def get_migration_ddl(engine: sqlalchemy.engine.Engine) -> [str]:
    """
    Creates a diff between the defined SQLAlchemy models and the current database and applies it.
    Prints the executed statements to stdout
    """
    combined_meta_data = sqlalchemy.MetaData()

    # merge all loaded SQL alchemy models into a single metadata object
    for declarative_base in (
            [obj for obj in gc.get_objects() if isinstance(obj, sqlalchemy.ext.declarative.api.DeclarativeMeta)]):
        for (table_name, table) in declarative_base.metadata.tables.items():
            combined_meta_data._add_table(table_name, table.schema, table)

    with engine.connect() as connection:
        output = io.StringIO()
        ddl = []

        diff_context = alembic.migration.MigrationContext(connection.dialect, connection, opts={})

        autogen_context = alembic.autogenerate.api.AutogenContext(diff_context,
                                                                  opts={'sqlalchemy_module_prefix': 'sqlalchemy.',
                                                                        'alembic_module_prefix': 'executor.'})

        execution_context = alembic.migration.MigrationContext(connection.dialect, connection,
                                                               opts={'output_buffer': output, 'as_sql': True})
        executor = alembic.operations.Operations(execution_context)

        # Step 1: create a diff between the meta data and the data base
        # operations is a list of MigrateOperation instances, e.g. a DropTableOp
        operations = alembic.autogenerate.produce_migrations(diff_context, combined_meta_data).upgrade_ops.ops

        for operation in operations:
            # Step 2: autogenerate a python statement from the operation, e.g. "executor.drop_table('bar')"
            renderer = alembic.autogenerate.renderers.dispatch(operation)
            statement = renderer(autogen_context, operation)
            if isinstance(statement, list):
                statement = statement[0]

            # Step 3: "execute" python statement and get sql from buffer, e.g. "DROP TABLE bar;"
            eval(statement)
            ddl.append(output.getvalue())
            output.truncate(0)
            output.seek(0)

    return ddl


def auto_migrate(engine: sqlalchemy.engine.Engine):
    """Compares the current database with all defined models and applies the diff"""
    try:
        if not sqlalchemy_utils.database_exists(engine.url):
            sqlalchemy_utils.create_database(engine.url)
            print(f'Created database "{engine.url}"')
    except Exception as e:
        print(f'Could not access or create database "{engine.url}":\n{e}', file=sys.stderr)
        return False

    ddl = get_migration_ddl(engine)

    with engine.begin() as connection:
        for statement in ddl:
            sys.stdout.write('\033[1;32m' + statement + '\033[0;0m')
            connection.execute(statement)
    return True
