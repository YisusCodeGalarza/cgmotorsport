import os
import subprocess
import tarfile
from datetime import datetime

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = '/var/www/cgmotorsport'
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
VENV_PYTHON = os.path.join(BASE_DIR, 'venv/bin/python')
MANAGE_PY = os.path.join(BASE_DIR, 'manage.py')

# Retención de respaldos (días)
RETENTION_DAYS = 14 

def run_backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    fecha_hoy = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_db_path = os.path.join(BACKUP_DIR, f'db_{fecha_hoy}.json')
    tar_output_path = os.path.join(BACKUP_DIR, f'backup_completo_{fecha_hoy}.tar.gz')

    print(f"[{datetime.now()}] Iniciando proceso de backup...")

    # 1. Exportar la base de datos a JSON
    print("Exportando base de datos a JSON...")
    cmd_dump = [
        VENV_PYTHON, MANAGE_PY, 'dumpdata',
        '--natural-foreign', '--natural-primary',
        '-e', 'contenttypes', '-e', 'auth.Permission',
        '--indent', '4'
    ]
    
    try:
        with open(json_db_path, 'w', encoding='utf-8') as f:
            subprocess.run(cmd_dump, stdout=f, check=True)
        print("Base de datos exportada con éxito.")
    except Exception as e:
        print(f"Error al exportar la base de datos: {e}")
        return

    # 2. Empaquetar JSON + Carpeta media/
    print("Empaquetando DB + carpeta media...")
    try:
        with tarfile.open(tar_output_path, "w:gz") as tar:
            tar.add(json_db_path, arcname=os.path.basename(json_db_path))
            if os.path.exists(MEDIA_DIR):
                tar.add(MEDIA_DIR, arcname='media')
        
        print(f"Backup creado exitosamente: {tar_output_path}")
        
        # Eliminar el JSON suelto
        if os.path.exists(json_db_path):
            os.remove(json_db_path)
            
    except Exception as e:
        print(f"Error al comprimir respaldo: {e}")

    # 3. Limpieza de respaldos antiguos (> RETENTION_DAYS)
    print("Limpiando respaldos antiguos...")
    now = datetime.now()
    for archivo in os.listdir(BACKUP_DIR):
        archivo_path = os.path.join(BACKUP_DIR, archivo)
        if os.path.isfile(archivo_path) and archivo.startswith('backup_completo_'):
            estat = os.stat(archivo_path)
            dias_antiguedad = (now - datetime.fromtimestamp(estat.st_mtime)).days
            if dias_antiguedad >= RETENTION_DAYS:
                os.remove(archivo_path)
                print(f"Respaldo antiguo eliminado: {archivo}")

    print(f"[{datetime.now()}] Proceso finalizado.")

if __name__ == '__main__':
    run_backup()