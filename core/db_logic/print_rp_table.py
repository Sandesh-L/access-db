from ..models import db
from ..models.rps import RPS

rps = RPS.select()
for rp in rps:
    print(f'rp: {rp.rp_name}, links: {rp.rp_software_documentation_links}, rp_has_individual_sftw_docs: {rp.rp_has_individual_software_documentation}')

