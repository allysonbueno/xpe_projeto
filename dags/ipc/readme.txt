pip install uritemplate
pip install openpyxl


- Master table creation
CREATE TABLE finance.global_ipc (
    country text NULL,
    current_rate float8 NULL,
    previous_rate text NULL,
    "date" text NULL,
    created_date timestamp NULL,
    CONSTRAINT global_ipc_uid UNIQUE (country, date))

- Temp table creation
CREATE TABLE finance.temp_global_ipc (
    country text NULL,
    current_rate float8 NULL,
    previous_rate text NULL,
    "date" text NULL,
    created_date timestamp NULL)