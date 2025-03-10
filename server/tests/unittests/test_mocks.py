# tests/test_make_db_config.py
from server.utils.psql_executor import make_db_config

def test_make_db_config():
    # Call the function that builds the DB config.
    db_config = make_db_config()

    # Based on your patch_config fixture, the test config is:
    # {
    #     "db": {
    #         "name": "calorimeter_db",
    #         "user": "calorimeter_robot",
    #         "host": "localhost",
    #         "port": 5432,
    #         "pswd_secret_id": "id1"   # (Ensure your test config uses "id1" so it matches the patch_fetch_secret mapping)
    #     },
    #     ... (other keys)
    # }
    #
    # And patch_fetch_secret returns "test_secret_value_1" for secret id "id1".
    #
    # Therefore, we expect make_db_config() to output:
    expected_config = {
        "name": "calorimeter_db",
        "user": "calorimeter_robot",
        "host": "localhost",
        "port": 5432,
        "pswd_secret_id": "id1",  # or it might be removed if your implementation omits it
        "password": "test_secret_value_1",
    }
    assert db_config == expected_config
