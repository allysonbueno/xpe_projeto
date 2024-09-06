from ipc.src.parameters import DATA_BASE_CONFIG
import pandas as pd
from supabase import create_client, Client


class SupaBase:
    def __init__(self):
        self.superbase_url      = DATA_BASE_CONFIG["database"]["supabase_url"]
        self.superbase_pwd      = DATA_BASE_CONFIG["database"]["supabase_pwd"]

    # Example: Fetch data from a table
    def fetch_data(self, table_name):
        supabase: Client = create_client(self.superbase_url, self.superbase_pwd)

        response = supabase.table(table_name).select('*').execute()
        return response.data

    # Example: Insert data into a table
    def insert_data(self, table_name, data):
        supabase: Client = create_client(self.superbase_url, self.superbase_pwd)        
        response = supabase.table(table_name).insert(data).execute()
        return response.data

    def insert_df_to_supabase(self, df: pd.DataFrame, table_name: str):
        print(df)

        data = df.to_dict(orient='records')
        print(data)
        
        # Insert data into Supabase
        supabase: Client = create_client(self.superbase_url, self.superbase_pwd)
        response = supabase.table(table_name).insert(data).execute()
        print("Supabase Response:", response)
        
        return response.data

# class DatabaseUsage:
#     def __init__(self):
#         self.host          = DATA_BASE_CONFIG["postgres"]["host"] 
#         self.user          = DATA_BASE_CONFIG["postgres"]["user"]            
#         self.password      = DATA_BASE_CONFIG["postgres"]["password"]
#         self.rapidapi_host = DATA_BASE_CONFIG["external"]["rapidapi_host"]
#         self.rapidapi_key  = DATA_BASE_CONFIG["external"]["rapidapi_key"]     
#         self.conn = psycopg2.connect(host = self.host, user = self.user, password = self.password)

#     def query_result(self, query):
#         conn = self.conn
#         cur = conn.cursor()
#         cur.execute(query)
#         result = cur.fetchall()
#         cur.close()
#         return result    

#     def commit_query(self, query):
#         conn = self.conn
#         cur = conn.cursor()
#         cur.execute(query)
#         conn.commit()
#         cur.close()
#         conn.close()

# class DataTypePatterns:
#     @staticmethod
#     def get_global_ipc_dtype_pattern():
#         print('....Setting data dtypes')
#         dtype_pattern = {
#             'country' : 'object',
#             'current_rate' : 'float64',
#             'previous_rate' : 'object',
#             'date' : 'object',
#             'created_date' : 'datetime64[ns, UTC]'
#             }
#         return dtype_pattern        
    

# class DataframeIngestion():
#     def __init__(self):
#         self.host          = DATA_BASE_CONFIG["postgres"]["host"] 
#         self.user          = DATA_BASE_CONFIG["postgres"]["user"]            
#         self.password      = DATA_BASE_CONFIG["postgres"]["password"]

#     def __send_data_to_db(self, dataframe, table_name):
#         df = pd.DataFrame(dataframe)
#         schema_name = 'finance'
#         print(f'....Sending data to {schema_name}.{table_name}')
#         engine = create_engine(f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}/postgres?options=-csearch_path%3Dschema,{schema_name}').connect()
#         df.to_sql(con=engine, name= table_name, if_exists='append', chunksize=1000, index=False)        
    
#     def convert_to_specified_dtype(self, df, dtype_pattern):
#         for col, dtype in dtype_pattern.items():
#             if 'datetime' in dtype: 
#                 if 'timezone-naive' in dtype.lower():  df[col] = df[col].dt.tz_localize(None)
#                 elif 'timezone-aware' in dtype.lower():
#                     timezone = dtype.split('timezone-aware')[1].strip()
#                     df[col] = df[col].dt.tz_convert(timezone)
#             elif 'int' in dtype:
#                 df[col] = df[col].astype(float) 
#                 df[col] = df[col].astype(dtype, errors='ignore')
#             else:
#                 df[col] = df[col].astype(dtype) 
#         return df    
        
#     def send_data_to_db(self, df, table_name, dtype_pattern=None):
#         print('....Sending data do DB')
#         if dtype_pattern: 
#             df = self.convert_to_specified_dtype(df, dtype_pattern)
#         self.__send_data_to_db(df, table_name)    