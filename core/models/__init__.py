from peewee import *
from playhouse.pool import PooledPostgresqlExtDatabase
# We want to use the PooledPostgresqlExtDatabase database class here
# PooledPostgresqlExtDatabase provides connection pooling https://docs.peewee-orm.com/en/latest/peewee/playhouse.html#pool
# as well as extended Postgresql support for things like json, hstore, etc. https://docs.peewee-orm.com/en/latest/peewee/playhouse.html#postgres-ext
# 
db = PooledPostgresqlExtDatabase(
        'test_db',
        user='test_user',
        password='test_password',
        host='localhost',
        port=5432,
        max_connections=1,
        stale_timeout=300 # 5 min
    )

class CaseInsensitiveField(CharField):
    def db_value(self, value):
        return value.lower() if value else None

    def python_value(self, value):
        return value

class BaseExtModel(Model):
    class Meta:
        database=db
