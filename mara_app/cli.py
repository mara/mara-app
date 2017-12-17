"""Mara admin command line interface"""

import click
import mara_db.config
import mara_db.sqlalchemy
import sys
from mara_app import migrations


@click.command()
def migrate():
    """Compares the current database with all defined models and applies the diff"""
    if not migrations.auto_migrate(mara_db.sqlalchemy.engine(mara_db.config.mara_db_alias())):
        sys.exit(-1)
