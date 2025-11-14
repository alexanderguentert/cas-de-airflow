import os
import pendulum
from airflow.decorators import dag
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

# Zugangsdaten in .env
google_api_token = os.environ.get("GOOGLE_API")
ckan_base_url  = os.environ.get("CKAN_BASE_URL_INT")
ckan_api_key = os.environ.get("CKAN_API_KEY_INT")

@dag(
    dag_id="update_sar_hauptarchiv_dag",
    start_date=pendulum.datetime(2025, 11, 1),
    schedule=None,
    catchup=False,
    description="Erstelle Tabelle mit Inventar des Hauptarchivs und erstelle Zusammenfassungen",
)
def update_sar_hauptarchiv_taskflow():
    
    # gemeinsam genutztes Verzeichnis. Hier werden Dateien zwischengespeichert
    shared_mount = Mount(source="airflow_shared_data", target="/app/data", type="volume")

    # Task 1: Container erzeugt eine Parquet-Datei
    download_sru_table = DockerOperator(
        task_id="download_sru_table",
        image="ghcr.io/alexanderguentert/cas-de-airflow-container:latest",
        command="python /app/download_sru.py",
        docker_url="unix://var/run/docker.sock",
        auto_remove="force",
        network_mode="bridge",
        mounts=[shared_mount],  
        mount_tmp_dir=False, 
        force_pull=False,
    )

    # Task 2: Container prüft/erstellt Zusammen und speicher csv/parquet
    process_summaries = DockerOperator(
        task_id="process_summaries",
        image="ghcr.io/alexanderguentert/cas-de-airflow-container:latest",
        command="python /app/manage_summaries.py",
        docker_url="unix://var/run/docker.sock",
        auto_remove="force",
        network_mode="bridge",
        mounts=[shared_mount],
        mount_tmp_dir=False, 
        environment={
        "GOOGLE_API": google_api_token,
        },
    )
    
    # Task 3: Lade CSV auf CKAN: 
    upload_csv = DockerOperator(
        task_id="upload_csv",
        image="ghcr.io/alexanderguentert/cas-de-airflow-container:latest",
        command="python /app/upload_resource_to_ckan_with_patch.py --file /app/data/sar_inventar_hauptarchiv.csv --dataset int_dwh_sar_inventar_hauptarchiv",
        docker_url="unix://var/run/docker.sock",
        auto_remove="force",
        network_mode="bridge",
        mounts=[shared_mount],
        mount_tmp_dir=False, 
        environment={
        "CKAN_BASE_URL": ckan_base_url,
        "CKAN_API_KEY": ckan_api_key
        },
    )
    
    # Task 4: Lade parquet auf CKAN: 
    upload_parquet = DockerOperator(
        task_id="upload_parquet",
        image="ghcr.io/alexanderguentert/cas-de-airflow-container:latest",
        command="python /app/upload_resource_to_ckan_with_patch.py --file /app/data/sar_inventar_hauptarchiv.parquet --dataset int_dwh_sar_inventar_hauptarchiv",
        docker_url="unix://var/run/docker.sock",
        auto_remove="force",
        network_mode="bridge",
        mounts=[shared_mount],
        mount_tmp_dir=False, 
        environment={
        "CKAN_BASE_URL": ckan_base_url,
        "CKAN_API_KEY": ckan_api_key
        },
    )
    
    # Task 5: Lade metadaten auf CKAN: 
    upload_metadata = DockerOperator(
        task_id="upload_metadata",
        image="ghcr.io/alexanderguentert/cas-de-airflow-container:latest",
        command="python /app/update_metadata.py --dataset int_dwh_sar_inventar_hauptarchiv",
        docker_url="unix://var/run/docker.sock",
        auto_remove="force",
        network_mode="bridge",
        mounts=[shared_mount],
        mount_tmp_dir=False, 
        trigger_rule="all_success",
        environment={
        "CKAN_BASE_URL": ckan_base_url,
        "CKAN_API_KEY": ckan_api_key
        },
    )

    # Reihenfolge: erst erzeugen, dann verarbeiten, dann upload, dann metadaten aktualisieren
    download_sru_table >> process_summaries >> [upload_csv, upload_parquet] >> upload_metadata


# DAG muss am Ende aufgerufen werden
update_sar_hauptarchiv_taskflow()
