import os

def load_magedb_config():
    return {
        'host': os.environ['MAGEDB_HOST'],
        'port': os.environ['MAGEDB_PORT'],
        'dbname': os.environ['MAGEDB_NAME'],
        'user': os.environ['MAGEDB_USER'],
        'password': os.environ['MAGEDB_PASSWORD'],
    }
