"""Mara admin command line interface"""

import click
from mara_app import migrations
from mara_db import dbs
import mara_db.config


@click.command()
def migrate():
    """Compares the current database with all defined models and applies the diff"""
    migrations.auto_migrate(dbs.engine(mara_db.config.mara_db_alias()))
