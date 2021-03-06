import pandas as pd
import app_Lib.manage_directories as md
import parameters.parameters as pm
import os
import app_Lib.functions as funcs


def d000(source_output_path, source_name, Table_mapping, STG_tables, BKEY):
    file_name = funcs.get_file_name(__file__)
    f = open(source_output_path + "/" + file_name + ".sql", "w+")

    for table_maping_index, table_maping_row in Table_mapping[Table_mapping['Source'] == source_name].iterrows():
        prcess_type = "TXF"
        layer = str(table_maping_row['Layer'])
        process_name = prcess_type + "_" + layer + "_" + str(table_maping_row['Mapping name'])
        target_table = str(table_maping_row['Target table name'])
        Historization_algorithm = str(table_maping_row['Historization algorithm'])

        f.write("delete from " + pm.automation_db + "." + pm.etl_process_table + " where process_name = '" + process_name + "';\n")
        f.write("insert into " + pm.automation_db + "." + pm.etl_process_table + "(SOURCE_NAME, PROCESS_TYPE, PROCESS_NAME, BASE_TABLE, APPLY_TYPE, RECORD_ID)\n")
        f.write("VALUES ('" + source_name + "', '" + prcess_type + "', '" + process_name + "', '" + target_table + "', '" + Historization_algorithm + "', NULL)" + ";\n")
        f.write("\n")

    for STG_tables_index, STG_tables_row in STG_tables.loc[(STG_tables['Source system name'] == source_name) & (STG_tables['Key set name'].notnull())].iterrows():
        Key_set_name = STG_tables_row['Key set name']
        Key_domain_name = STG_tables_row['Key domain name']
        Table_name = STG_tables_row['Table name']
        Column_name = STG_tables_row['Column name']
        prcess_type = "BKEY"
        target_table = ""
        Historization_algorithm = "INSERT"

        for BKEY_index, BKEY_row in BKEY.loc[(BKEY['Key set name'] == Key_set_name) & (BKEY['Key domain name'] == Key_domain_name)].iterrows():
            Key_set_id = int(BKEY_row['Key set ID'])
            Key_domain_ID = int(BKEY_row['Key domain ID'])
            Physical_table = BKEY_row['Physical table']
            # print(Table_name, Column_name, Key_set_id,Key_domain_ID,Physical_table)
            process_name = "BK_" + str(Key_set_id) + "_" + Table_name + "_" + Column_name + "_" + str(Key_domain_ID)

            f.write("delete from " + pm.automation_db + "." + pm.etl_process_table + " where process_name = '" + process_name + "';\n")
            f.write("insert into " + pm.automation_db + "." + pm.etl_process_table + "(SOURCE_NAME, PROCESS_TYPE, PROCESS_NAME, BASE_TABLE, APPLY_TYPE, RECORD_ID)\n")
            f.write("VALUES ('" + source_name + "', '" + prcess_type + "', '" + process_name + "', '" + target_table + "', '" + Historization_algorithm + "', NULL)" + ";\n")
            f.write("\n")

    f.close()
