from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from seu_script import enviar_emails_aniversario

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 22),
    'email': ['seu_email@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'enviar_emails_aniversario',
    default_args=default_args,
    description='Envia e-mails de aniversário para clientes',
    schedule_interval='@daily',
)

tarefa_enviar_emails = PythonOperator(
    task_id='enviar_emails',
    python_callable=enviar_emails_aniversario,
    dag=dag,
)

tarefa_enviar_emails
