"""CLI commands for the application."""
import click
from flask.cli import with_appcontext
from app.utils.logger import logger

@click.command('seed-db')
@with_appcontext
def seed_db_command():
    """Seed the database with sample data."""
    from scripts.seed_data import seed_data
    try:
        seed_data()
        click.echo('Successfully seeded database.')
    except Exception as e:
        logger.error(f"Error seeding database: {str(e)}")
        click.echo('Error seeding database. Check logs for details.')
        raise

def init_app(app):
    """Register CLI commands."""
    app.cli.add_command(seed_db_command)
