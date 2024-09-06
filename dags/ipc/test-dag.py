from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

alerts_mail = 'teste@teste.com'

args = {
    'owner': 'Allyson Bueno',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 1),
    'email': [alerts_mail],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'test-dag',
    default_args=args,
    catchup=False,
    tags=['indices', 'ipc', 'global'],
    schedule_interval='0 20 5,15,25 * *',
)
dag.is_paused_upon_creation = True

def get_global_indexes():
    print('teste')

with dag:

    
    get_global_indexes = PythonOperator(
        task_id='get_global_indexes',
        python_callable=get_global_indexes,
    )


    get_global_indexes
