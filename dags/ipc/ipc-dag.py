from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
# from airflow.providers.postgres.operators.postgres import PostgresOperator
# from airflow.operators.email import EmailOperator
from ipc.src.global_indexes import Global_Indexes

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
    'global-financial-indexes-dag',
    default_args=args,
    catchup=False,
    tags=['indices', 'ipc', 'global'],
    schedule_interval='0 20 5,15,25 * *',
)
dag.is_paused_upon_creation = True

def get_global_indexes():
    print('TEST OK')

with dag:

    # truncate_temp_global_ipc = PostgresOperator(
    #     task_id='truncate_temp_global_ipc',
    #     postgres_conn_id='postgres_local',
    #     sql='TRUNCATE TABLE ipc.temp_global_ipc;',
    # )
    
    idx = Global_Indexes()
    # get_global_indexes = PythonOperator(
    #     task_id='get_global_indexes',
    #     python_callable=idx.get_global_indexes,
    # )

    get_global_indexes = PythonOperator(
        task_id='get_global_indexes',
        python_callable=get_global_indexes,
    )

    # upsert_global_indexes = PostgresOperator(
    #     task_id='upsert_global_indexes',
    #     postgres_conn_id='postgres_local',
    #     sql="""
    #     INSERT INTO ipc.global_ipc (country, current_rate, previous_rate, "date", created_date)
    #     SELECT country, current_rate, previous_rate, "date", created_date FROM ipc.temp_global_ipc
    #     ON CONFLICT (country, "date") DO UPDATE SET
    #         current_rate = EXCLUDED.current_rate,
    #         previous_rate = EXCLUDED.previous_rate,
    #         created_date = EXCLUDED.created_date;
    #     """,
    # )

    # send_email = EmailOperator(
    #     task_id      = 'send_email',
    #     to           = alerts_mail, 
    #     subject      = 'DAG global-financial-indexes-dag Success',
    #     html_content ='<p>The global-financial-indexes-dag has completed successfully.</p>',
    # )

    # truncate_temp_global_ipc >> get_global_indexes >> upsert_global_indexes >> send_email
    get_global_indexes
