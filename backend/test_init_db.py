from flask import cli
from flask.cli import AppGroup
from app import create_app, db 
from flask_sqlalchemy import SQLAlchemy
import subprocess
import click 

# Define CLI group for database commands
db_cli = AppGroup('db', help='Database management commands')

# Create Flask app instance using create_app function
app = create_app()

@click.command()  # Use click's command decorator
def init_db():
    with app.app_context():
        db.create_all()

# Define CLI group for background tasks
background_cli = AppGroup('background', help='Background task management commands')

@background_cli.command('start')
def start_background_task():
    """Start background task."""
    background_process = subprocess.Popen(["python", "initapp.py"])
    print('Background task started')

@background_cli.command('stop')
def stop_background_task():
    """Stop background task."""
    # Terminate background process
    # Add logic to properly terminate the background task
    print('Background task stopped')

# Register CLI groups
app.cli.add_command(db_cli)
app.cli.add_command(background_cli)

if __name__ == '__main__':
    cli.main()