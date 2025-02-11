import yaml
import psycopg2

def get_db_connection():
    """
    Creates and returns a connection to the PostgreSQL database.
    """
    # Load DB configuration from config file
    with open("config.yml", "r") as config_file:
        config = yaml.safe_load(config_file)
        db_config = config["database"]
    
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=db_config["name"],
        user=db_config["user"],
        password=db_config["password"],
        host=db_config["host"],
        port=db_config["port"]
    )

    return conn
