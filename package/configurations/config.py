import os
import urllib
from os import environ

# from urllib.parse import quote_plus
from dotenv import load_dotenv

# from package.azure_database import connection_string

load_dotenv()

# For AZURE SQL DB CONNECTION
driver = "{ODBC Driver 17 for SQL Server}"
username = os.environ.get("USER_NAME")
password = os.environ.get("PASSWORD")
database = os.environ.get("DB_NAME")
server = environ.get("SERVER")
# authentication = environ.get("AUTHENTICATION")

# Connection string from AZURE SQLDB
# password_encoded = quote_plus(password)

# server = "<server-name>.database.windows.net"
# database = "<db-name>"
# user = "<db-user>"
# password = "<db-password>"

conn = f"""Driver={driver};Server=tcp:{server},1433;Database={database};
        Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"""

params = urllib.parse.quote_plus(conn)
conn_str = "mssql+pyodbc:///?autocommit=true&odbc_connect={}".format(params)


class Config:
    # App secret key
    SECRET_KEY = environ.get("SECRET_KEY", "dev-key")
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


config_by_name = {
    "dev": DevelopmentConfig
    # "prod": ProductionConfig,
}
