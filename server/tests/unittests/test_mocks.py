# tests/test_make_db_config.py
from calorimeter.server.utils.psql_executor import make_db_config

def test_make_db_config():
    db_config = make_db_config()
    expected_config = {
        "dbname": "calorimeter_db",
        "user": "calorimeter_robot",
        "host": "localhost",
        "port": 5432,
        "password": "password_mock",
    }
    assert db_config == expected_config
