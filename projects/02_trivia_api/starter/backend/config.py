# from os import getenv
from dotenv import dotenv_values

dotenv_path = r".env"
env = dotenv_values(dotenv_path)


def get_config() -> dict:
    conf = dict()
    db_name = env.get('DB_NAME')
    db_user = env.get('DB_USER')
    db_pass = env.get('DB_PASSWD')
    db_host = env.get('DB_HOST')
    db_port = env.get('DB_PORT')
    db_credentials = f'{db_user}:{db_pass}'
    db_socket = f'{db_host}:{db_port}'
    conf["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{db_credentials}@{db_socket}/{db_name}'
    conf["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    return conf
    