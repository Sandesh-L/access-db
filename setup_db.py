from models import db
from models.rps import RPS

# Connect to the db and create tables
@db.connection_context() # opens a db connectionon function call, conn is closed on function return
def setup_db():
    db.drop_tables([RPS])
    db.create_tables([RPS])

@db.connection_context()
def add_rp(rp_data):
    """
    rp_data {list}: a list of objects...
    """
    rp =RPS.insert_many(rp_data).execute()

@db.connection_context()
def get_all_rps():
    rps = RPS.select()
    return rps

if __name__ == "__main__":
    setup_db()

    rp_data = [
        {"rp_name":"aces", "rp_sftw_docs_links":"this is a link", "rp_has_individual_sftw_docs":0},
        {"rp_name":"hello", "rp_sftw_docs_links":"www.hello.com", "rp_has_individual_sftw_docs":1},
        {"rp_name":"hello", "rp_sftw_docs_links":"potatoes.po", "rp_has_individual_sftw_docs":1}
        ]

    add_rp(rp_data)

    rps = get_all_rps()
    for rp in rps:
        print(f'rp: {rp.rp_name}, links: {rp.rp_sftw_docs_links}, rp_has_individual_sftw_docs: {rp.rp_has_individual_sftw_docs}')

