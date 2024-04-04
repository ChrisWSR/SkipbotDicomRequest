import cv2
import numpy as np
import os
import pydicom
import subprocess
import requests  # Importa requests
from datetime import datetime

class DicomVideoConverterSend:
    def __init__(self, dicom_directory, server_url, video_path='salida_orientada.mp4'):
        self.dicom_directory = dicom_directory
        self.video_path = video_path  # Este será el primer video que luego será eliminado.
        self.server_url = server_url  # URL del servidor donde se subirá el video.
        self.data = None
        self.uploaded_video_id = None
        self.load_dicom_images()
        self.load_dicom_images()

    def load_dicom_images(self):
        dicom_files = [os.path.join(self.dicom_directory, f) for f in os.listdir(self.dicom_directory) if f.endswith('.dcm')]
        dicom_files.sort(key=lambda x: pydicom.dcmread(x).InstanceNumber)
        first_image = pydicom.dcmread(dicom_files[0]).pixel_array
        is_color = len(first_image.shape) == 3 and first_image.shape[2] == 3
        self.data = np.zeros((len(dicom_files), first_image.shape[0], first_image.shape[1]), dtype=np.float32 if is_color else first_image.dtype)

        for i, file in enumerate(dicom_files):
            dicom_data = pydicom.dcmread(file)
            image = dicom_data.pixel_array
            if is_color:
                image = image.mean(axis=2)
            self.data[i, :, :] = image

    def create_video(self):
        frames, height, width = self.data.shape
        if frames <= 10:
            fps = 1
        else:
            fps = frames / (frames / 2)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(self.video_path, fourcc, fps, (width, height), isColor=False)

        for i in range(frames):
            frame = self.data[i, :, :]
            norm_frame = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX)
            uint8_frame = np.uint8(norm_frame)
            video.write(uint8_frame)

        video.release()
        print("Video creado exitosamente en:", self.video_path)

    def convert_video(self):
        # Obtén el sello de tiempo actual y formatealo
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_video = f'salida_compatible_{timestamp}.mp4'

        ffmpeg_command = [
            'ffmpeg',
            '-i', self.video_path,
            '-vcodec', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-profile:v', 'baseline',
            '-level', '3.0',
            '-acodec', 'aac',
            output_video
        ]

        subprocess.run(ffmpeg_command, check=True)
        print("Video convertido y guardado como:", output_video)

        # Subir el video al servidor
        self.upload_video(output_video)

        # Eliminar los videos después de la subida
        os.remove(self.video_path)
        self.upload_video(output_video)

        os.remove(output_video)
        print(f"Los videos locales han sido eliminados.")
        
    def upload_video(self, video_path):
        url = self.server_url  # Usa la URL pasada al constructor

        url = 'https://server-production-c354.up.railway.app/ultrasonography/upload'  # Tu URL correcta
        headers = {'Authorization': 'Bearer *****'}  # Ejemplo de cabecera de autorización

# Abre el archivo aquí para poder cerrarlo después correctamente
        with open(video_path, 'rb') as file_to_upload:
            files = {'file': (os.path.basename(video_path), file_to_upload, 'video/mp4')}
        

            try:
                response = requests.post(url, files=files, headers=headers)
                # Asegúrate de que la solicitud fue exitosa
                if response.status_code == 200:
                    # Procesa la respuesta JSON
                    response_data = response.json()
                    self.uploaded_video_id = response_data.get('_id')
                    print(f"Respuesta del servidor: {response_data}")
                    # Extrae el _id del objeto subido, asumiendo que el servidor lo devuelve en la respuesta
                    uploaded_video_id = response_data.get('_id')  # Ajusta esta clave según tu respuesta específica
                    print(f"ID del video subido: {uploaded_video_id}")
                    return uploaded_video_id
                else:
                    print(f"Error en la subida. Código de estado: {response.status_code}, Respuesta: {response.text}")
            except Exception as e:
                print(f"Error al subir el video: {e}")



# Ejemplo de uso

#converter = DicomVideoConverterSend('/ruta/a/tus/archivos/dicom', 'http://tu-servidor.com/upload')
#converter.create_video()
#converter.convert_video()
