import requests

class DicomDownloader:
    def __init__(self, base_url, patient_id):
        self.base_url = base_url    
        self.patient_id = patient_id

    def get_series_image_urls(self):
        # Obtener estudios del paciente y seleccionar el primer estudio
        response = requests.get(f'{self.base_url}/patients/{self.patient_id}/studies')
        studies = response.json()
        listImages = []  # Lista para almacenar URLs de imágenes

        for study in studies:
            for series in study['Series']:
                # Obtener imágenes de la serie
                response = requests.get(f'{self.base_url}/series/{series}/instances')
                if response.status_code == 200:
                    instances = response.json()
                    for instance in instances:
                        # Construir URL de la imagen (preview o imagen decodificada)
                        image_url = f'{self.base_url}/instances/{instance["ID"]}/preview'  # O usar otro endpoint según necesidad
                        listImages.append(image_url)
                else:
                    print(f'Error al obtener imágenes de la serie {series}. Código de estado: {response.status_code}')
        
        if listImages:
            print(f'Se encontraron {len(listImages)} imágenes.')
        else:
            print('No se encontraron imágenes.')
        
        return listImages

# Usar la clase para obtener URLs de imágenes
base_url = 'https://a401-2806-261-417-5512-6590-e2e0-186b-8ce8.ngrok-free.app'
patient_id = '4cf8daab-2ae2a98c-64548873-588522ae-74252fc2'
downloader = DicomDownloader(base_url, patient_id)
image_urls = downloader.get_series_image_urls()

print('URLs de las imágenes:', image_urls)
