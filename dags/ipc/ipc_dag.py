from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from ipc.src.global_indexes import Global_Indexes
from ipc.src.db_actions import SupaBase

args = {
    'owner': 'Allyson Bueno',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 1),
    'email': 'allyson_bueno@gmail.com',
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'global-financial-indexes-dag',
    default_args=args,
    catchup=False,
    tags=['indices', 'ipc', 'global'],
    schedule_interval='0 20 5,15,25 * *',
    start_date=datetime(2023, 8, 1),
) as dag:

    sb = SupaBase()
    
    truncate_table = PythonOperator(
        task_id='truncate_table',
        python_callable=sb.truncate_table,
        op_args=['temp_global_indexes'],
    )

    idx = Global_Indexes()
    get_global_indexes = PythonOperator(
        task_id='get_global_indexes',
        python_callable=idx.get_global_indexes,
    )

    upsert_global_indexes = PythonOperator(
        task_id='upsert_global_indexes',
        python_callable=sb.upsert_global_indexes,
    )

    truncate_table >> get_global_indexes >> upsert_global_indexes
