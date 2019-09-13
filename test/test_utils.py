from alayatodo import app, DATABASE
from main import initialize_database, apply_schema_update


def initialize_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/alayatodo.db'
    client = app.test_client()
    with app.app_context():
        initialize_database()
        apply_schema_update()
    return client
