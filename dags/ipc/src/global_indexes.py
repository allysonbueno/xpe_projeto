from ipc.src.db_actions import SupaBase
import pandas as pd
from ipc.src.parameters import DATA_BASE_CONFIG
import http.client, json
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class Global_Indexes:    
    def __init__(self):
        self.rapidapi_host = DATA_BASE_CONFIG["external"]["rapidapi_host"]
        self.rapidapi_key  = DATA_BASE_CONFIG["external"]["rapidapi_key"]     

    def request_rapid_api(self):
        api_param = 'inflation-rate-around-the-world.p.rapidapi.com'
        print(f'....Data Request From: {api_param}')
        
        conn = http.client.HTTPSConnection(api_param)
        headers = {'x-rapidapi-key': self.rapidapi_key, 'x-rapidapi-host': self.rapidapi_host}
        conn.request("GET", "/world", headers=headers)
        res = conn.getresponse()
        data = res.read()
        json_data = json.loads(data)
        return json_data

    def __get_global_indexes(self):
        temp_table_name = 'temp_global_indexes'
        sb = SupaBase()
        sb.truncate_table(temp_table_name)

        json_data = self.request_rapid_api()
        
        print('....Data Transformation')
        df = pd.DataFrame(pd.json_normalize(json_data))
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        df = df.rename(columns={
            'countryname': 'country',
            'lastinflation': 'current_rate',
            'previousinflation': 'previous_rate'})
        df['date'] = pd.to_datetime(df['date'], format='%b/%y').dt.strftime('%Y-%m')
        df = df.drop(columns=['unit'])        
        df['created_date'] = pd.Timestamp.now()
        df['created_date'] = df['created_date'].astype(str)
        if not df.empty:
            inserted_data = sb.insert_df_to_supabase(df, temp_table_name)
            print("Inserted Data:", inserted_data)

    def get_global_indexes(self):        
        self.__get_global_indexes()