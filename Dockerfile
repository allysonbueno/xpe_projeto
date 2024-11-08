# Use the official Apache Airflow image as base
FROM apache/airflow:2.10.0-python3.9

# Set environment variables
ENV AIRFLOW_HOME=/opt/airflow
ENV AIRFLOW_UID=50000
ENV PYTHON_VERSION=3.9

# Copy requirements file
COPY config/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure the necessary directories exist and have the correct permissions
RUN mkdir -p $AIRFLOW_HOME/logs/scheduler && \
    mkdir -p $AIRFLOW_HOME/logs/webserver && \
    mkdir -p $AIRFLOW_HOME/dags && \
    mkdir -p $AIRFLOW_HOME/plugins && \
    chown -R ${AIRFLOW_UID}:0 $AIRFLOW_HOME/logs && \
    chown -R ${AIRFLOW_UID}:0 $AIRFLOW_HOME/dags && \
    chown -R ${AIRFLOW_UID}:0 $AIRFLOW_HOME/plugins

# Set working directory
WORKDIR $AIRFLOW_HOME

# Switch to airflow user to avoid running as root
USER ${AIRFLOW_UID}:0

# Expose necessary ports for webserver and flower (as per your docker-compose.yml setup)
EXPOSE 5000 5555

# Copy the DAGs and configuration files (optional)
COPY dags/ $AIRFLOW_HOME/dags/
COPY config/airflow.cfg $AIRFLOW_HOME/airflow.cfg
COPY config/pg_hba.conf /etc/postgresql/pg_hba.conf

# Set entrypoint for airflow to start required services like webserver, scheduler, or worker
ENTRYPOINT ["bash", "-c"]

# The command will be passed by docker-compose (e.g., 'webserver', 'scheduler', etc.)
