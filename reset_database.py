from core.models import admin_db, view_db
from core.models.rpSoftware import RPSoftware
from core.models.software import Software
from core.models.rps import RPS
from core.models.aiSoftwareInfo import AISoftwareInfo
from core.models.api import API
from core.parseSpiderOutput import parse_spider_output
from core.db_logic.createRpTable import update_rp_table, create_rp_table_records
from core.db_logic.createSoftwareTable import update_software_table, create_software_table_records
from core.db_logic.createRPSoftwareTable import update_rp_software_table, create_rp_software_table_records
from core.db_logic.createAISoftwareTable import create_ai_software_table_records, update_ai_software_table


@admin_db.connection_context()
def recreate_tables():
    main_tables = [RPS, Software, API]   # RPS with no foreign key fields
    dependant_tables = [RPSoftware, AISoftwareInfo] # RPS with foreign key fields
    admin_db.drop_tables(dependant_tables)
    admin_db.drop_tables(main_tables)
    admin_db.create_tables(main_tables+dependant_tables)


if __name__=="__main__":
    recreate_tables()

    rp_table_records = create_rp_table_records()
    update_rp_table(rp_table_records)
    print("RP table updated")

    spider_output = parse_spider_output()

    # Write table info to file for testing purposes
    # with open("spider_output.txt", "w") as so:
    #     so.writelines(str(spider_output))

    columns={'Software',"Software Description","Software's Web Page","Software Documentation","Example Software Use"}
    software_table_records = create_software_table_records(columns,spider_output)
    update_software_table(software_table_records)
    print("Software table updated")

    rp_software_records = create_rp_software_table_records(spider_output)
    update_rp_software_table(rp_software_records)

    print("RPSoftware table updated")

    # Write table info to file for testing purposes
    with view_db:
        rp_software = RPSoftware.select()
    with open('rp_sftw_text.txt', 'w') as rst:
        for rp_s in rp_software:
            rst.writelines(f"\nrp: {rp_s.rp_id.rp_name}, \
                software: {rp_s.software_id.software_name}, \
                ver: {rp_s.software_versions},"
                )

    columns={'Software','✨Research Area', '✨Example Use', '✨Software Class', '✨Research Field', '✨Core Features', '✨Research Discipline', '✨AI Description', '✨Software Type', '✨General Tags'}
    ai_software_records = create_ai_software_table_records(columns)
    update_ai_software_table(ai_software_records)
    print("AISoftwareRecords table updated")

    # Write table info to file for testing purposes
    with view_db:
        ai_software = AISoftwareInfo.select()
    with open('ai_sftw_text.txt', 'w') as ast:
        for ai_s in ai_software:
            ast.writelines(f"\nsoftware: {ai_s.software_id.software_name}, \
                desc: {ai_s.ai_description}, \
                s_type: {ai_s.ai_software_type},\
                s_class: {ai_s.ai_software_class},\
                r_field: {ai_s.ai_research_field},\
                r_area: {ai_s.ai_research_area},\
                r_discipline: {ai_s.ai_research_discipline},\
                c_features: {ai_s.ai_core_features},\
                g_tags: {ai_s.ai_general_tags},\
                e_use: {ai_s.ai_example_use}"
                )