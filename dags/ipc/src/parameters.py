# import os
# from dotenv import load_dotenv

# try:
#     load_dotenv('creds.env')
#     password     = os.getenv("DB_PASSW")
#     rapidapi_key = os.getenv('RAPIDAPI_KEY')
#     supabase_url = os.getenv('SUPABASE_URL')
#     supabase_pwd = os.getenv('SUPABASE_URL_PASSW')
# except: pass

# try:
from airflow.models import Variable
password     = Variable.get("DB_PASSW")
rapidapi_key = Variable.get('RAPIDAPI_KEY')
supabase_url = Variable.get('SUPABASE_URL')
supabase_pwd = Variable.get('SUPABASE_URL_PASSW')
# except: pass    

DATA_BASE_CONFIG = {
    'database': {
        'host'          : '127.0.0.1',
        'user'          : 'postgres',
        'password'      : password,
        'supabase_url' : supabase_url,
        'supabase_pwd' : supabase_pwd,
    },
    'external': {
        'rapidapi_host' : 'inflation-rate-around-the-world.p.rapidapi.com',
        'rapidapi_key'  : rapidapi_key,     
    },
}