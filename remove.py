import os
def clean_up(archive_path, extraction_dir):
    if archive_path:
        os.remove(archive_path)  # Elimina el archivo ZIP
    if extraction_dir:
        for root, dirs, files in os.walk(extraction_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(extraction_dir)  # Elimina el directorio de descompresión
    print('Archivos residuales eliminados.')