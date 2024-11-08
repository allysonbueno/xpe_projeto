# Start from the official Python 3.12 slim image
FROM apache/airflow:2.10.0

# Set the owner label
LABEL owner="allyson"

# Set environment variable to ignore Python warnings
ENV PYTHONWARNINGS="ignore"

# Copy DAGs, plugins, logs, and configuration files
COPY dags /opt/airflow/dags
COPY plugins /opt/airflow/plugins
COPY logs /opt/airflow/logs
COPY config/airflow.cfg /opt/airflow/airflow.cfg
COPY config/requirements.txt /opt/airflow/requirements.txt
COPY config/gspread/gspread /home/airflow/.local/lib/python3.8/site-packages/gspread
COPY config/gspread/gspread-5.10.0.dist-info /home/airflow/.local/lib/python3.8/site-packages/gspread-5.10.0.dist-info

# Install Python dependencies
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt
RUN pip install apache-airflow-providers-postgres

USER root
# Set permissions on DAGs directory (replace * with actual subdirectories if needed)
RUN chmod -R 755 /opt/airflow/dags
RUN chmod -R 755 /opt/airflow/logs
RUN chmod -R 755 /opt/airflow/plugins
RUN chmod -R 755 /opt/airflow/scheduler

# Create the airflow user and group if they don't exist
RUN groupadd -g 999 airflow || true && \
    useradd -r -u 999 -g airflow airflow || true

# Debugging: Check if the user and group were created successfully
RUN id airflow

# Ensure the installed binaries are available for the airflow user
RUN mkdir -p /home/airflow/.cache/ms-playwright && \
    chown -R 999:999 /home/airflow/.cache/ms-playwright

# Initialize Airflow database
RUN airflow db init

# Set the default user to airflow
USER airflow
