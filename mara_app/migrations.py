"""Automigration of sql alchemy models with alembic. Automigration means that no intermediate files are created,
 instead diffs are immediately applied. Use with care.
"""
import copy
import io
import sys

import alembic
import alembic.autogenerate
import alembic.migration
import alembic.operations
import sqlalchemy.engine
import sqlalchemy_utils
from sqlalchemy import *  # unfortunately needed to get the eval part further down working


def get_migration_ddl(engine: sqlalchemy.engine.Engine) -> [str]:
    """
    Creates a diff between the defined SQLAlchemy models and the current database and applies it.
    Prints the executed statements to stdout
    """

    # merge all loaded SQL alchemy models into a single metadata object
    combined_meta_data = MetaData()

    for name, module in copy.copy(sys.modules).items():
        if 'MARA_AUTOMIGRATE_SQLALCHEMY_MODELS' in dir(module):
            for table in getattr(module, 'MARA_AUTOMIGRATE_SQLALCHEMY_MODELS'):
                for t in table.metadata.tables.values():
                    t.tometadata(combined_meta_data)

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
            statements = renderer(autogen_context, operation)
            if not isinstance(statements, list):
                statements = [statements]

            for statement in statements:
                # Step 3: "execute" python statement and get sql from buffer, e.g. "DROP TABLE bar;"
                try:
                    eval(statement)
                except Exception as e:
                    print('statement: ' + statement)
                    raise(e)
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
