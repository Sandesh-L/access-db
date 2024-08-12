from peewee import *
from playhouse.pool import PooledPostgresqlExtDatabase
from dotenv import load_dotenv
import os
# We want to use the PooledPostgresqlExtDatabase database class here
# PooledPostgresqlExtDatabase provides connection pooling https://docs.peewee-orm.com/en/latest/peewee/playhouse.html#pool
# as well as extended Postgresql support for things like json, hstore, etc. https://docs.peewee-orm.com/en/latest/peewee/playhouse.html#postgres-ext

load_dotenv()

# Database config
DB_NAME = os.getenv("DB_NAME", "ara_db")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_MAX_CONN = os.getenv("DB_MAX_CONN", 10)
DB_CONN_TIMEOUT = os.getenv("DB_CONN_TIMEOUT", 300) # default 5 min

# DB user credentails
ADMIN_USER = os.getenv('DB_ADMIN_USER')
ADMIN_PASS = os.getenv('DB_ADMIN_PASS')
EDIT_USER = os.getenv('DB_EDIT_USER')
EDIT_PASS = os.getenv('DB_EDIT_PASS')
VIEW_USER = os.getenv('DB_VIEW_USER')
VIEW_PASS = os.getenv('DB_VIEW_PASS')

admin_db = PooledPostgresqlExtDatabase(DB_NAME, user=ADMIN_USER,
                                       password=ADMIN_PASS, host=DB_HOST,
                                       port=DB_PORT, max_connections=DB_MAX_CONN,
                                       stale_timeout=DB_CONN_TIMEOUT)

edit_db = PooledPostgresqlExtDatabase(DB_NAME, user=EDIT_USER,
                                       password=EDIT_PASS, host=DB_HOST,
                                       port=DB_PORT, max_connections=DB_MAX_CONN,
                                       stale_timeout=DB_CONN_TIMEOUT)

view_db = PooledPostgresqlExtDatabase(DB_NAME, user=VIEW_USER,
                                       password=VIEW_PASS, host=DB_HOST,
                                       port=DB_PORT, max_connections=DB_MAX_CONN,
                                       stale_timeout=DB_CONN_TIMEOUT)

class CaseInsensitiveField(CharField):
    def db_value(self, value):
        return value.lower() if value else None

    def python_value(self, value):
        return value

class BaseExtModel(Model):
    class Meta:
        database=admin_db   # default database is set to admin_db
