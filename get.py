import requests
import zipfile
import os

class DicomDownloader:
    def __init__(self, base_url, patient_id):
        self.base_url = base_url    
        self.patient_id = patient_id

    def download_series_archive(self):
        # Obtener estudios del paciente y seleccionar el primer estudio
        response = requests.get(f'{self.base_url}/patients/{self.patient_id}/studies')
        studies = response.json()
        first_series_id = studies[0]['Series'][0]

        # Descargar el archivo ZIP de la serie
        response = requests.get(f'{self.base_url}/series/{first_series_id}/archive')
        if response.status_code == 200:
            filename = f'imagen_{first_series_id}.zip'
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f'Archivo DICOM guardado como {filename}')
            return filename
        else:
            print(f'Error al descargar el archivo DICOM. Código de estado: {response.status_code}')
            return None

    def extract_archive(self, archive_path):
        if archive_path:
            extraction_dir = f'./{archive_path.rstrip(".zip")}'
            os.makedirs(extraction_dir, exist_ok=True)
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extraction_dir)
            print(f'Archivos descomprimidos en {extraction_dir}')

            # Buscar el primer archivo DICOM en el directorio de extracción y sus subdirectorios
        # Buscar el primer archivo DICOM en el directorio de extracción y sus subdirectorios
            for root, dirs, files in os.walk(extraction_dir):
                for file in files:
                    if file.endswith('.dcm'):
                        # Obtiene el directorio que contiene el primer archivo DICOM encontrado
                        first_dicom_dir = root
                        relative_dir_path = os.path.relpath(first_dicom_dir, extraction_dir)
                        print(f'Path de la carpeta del primer archivo DICOM: {relative_dir_path}')
                        return extraction_dir+'/'+relative_dir_path
            # Si no se encuentra ningún archivo DICOM, retorna None
            print('No se encontraron archivos DICOM.')
            return None
        return None