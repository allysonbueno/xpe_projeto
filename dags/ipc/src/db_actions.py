from ipc.src.parameters import DATA_BASE_CONFIG
import pandas as pd
from supabase import create_client, Client


class SupaBase:
    def __init__(self):
        self.supabase_url    = DATA_BASE_CONFIG["database"]["supabase_url"]
        self.supabase_key    = DATA_BASE_CONFIG["database"]["supabase_pwd"]
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)       
        
    # Executar comando no SupaBase para enviar comandos sql:
    # CREATE OR REPLACE FUNCTION execute_sql(query TEXT)
    #     RETURNS VOID AS $$
    #     BEGIN
    #         EXECUTE query;
    #     END;
    #     $$ LANGUAGE plpgsql;

    def truncate_table(self, table_name: str):
        query = f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;"
        try:
            response = self.supabase.rpc("execute_sql", {"query": query}).execute()
            print(f'Response: {response.data}')
        except Exception as e:
            print(f"An error occurred: {e}")

    def insert_df_to_supabase(self, df: pd.DataFrame, table_name: str):
        print('....Inserting data into SUPABASE')
        data_to_insert = df.to_dict(orient='records')        
        response = self.supabase.table(table_name).insert(data_to_insert).execute()
        return response.data

    def upsert_global_indexes(self):
        query = """
        insert into
            global_indexes (
                country,
                current_rate,
                previous_rate,
                date,
                created_date
            )
            select
            country,
            current_rate,
            previous_rate,
            date,
            created_date
            from
            temp_global_indexes
            on conflict (country, date) do
            update
            set
            current_rate = excluded.current_rate,
            previous_rate = excluded.previous_rate,
            created_date = excluded.created_date;
        """
        try:
            response = self.supabase.rpc("execute_sql", {"query": query}).execute()
            print(f'Response: {response.data}')
        except Exception as e:
            print(f"An error occurred: {e}")
