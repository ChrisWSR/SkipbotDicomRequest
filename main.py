from get import *
from image import *
from remove import * 
from videoToSever import *
def main():
    base_url = 'https://a401-2806-261-417-5512-6590-e2e0-186b-8ce8.ngrok-free.app'
    patient_id = '4cf8daab-2ae2a98c-64548873-588522ae-74252fc2'
    url_server='https://server-production-c354.up.railway.app/ultrasonography/upload'
    downloader = DicomDownloader(base_url, patient_id)
    print('download',downloader)
    archive_path = downloader.download_series_archive()
    print("ARCHIVEPATH",archive_path)
    extraction_dir= downloader.extract_archive(archive_path)
    print(extraction_dir)
    # Aquí deberías incluir tu lógica para procesar/convertir los archivos DICOM según sea necesario.
    # Por ejemplo, podrías llamar a otra clase o función que procese los archivos en `extraction_dir`.
    # Configurar las rutas de los directorios
    output_directory = os.getcwd()+'/'+'outimages'  # Ruta donde se guardarán las imágenes JPEG
    
# Crear una instancia de la clase y ejecutar la conversión
    dicom_to_jpeg_converter = DicomToJpegConverter(extraction_dir, output_directory)
    # Uso de la clase
    #converter = DicomVideoConverter(extraction_dir,)
    #converter.create_video()
    #converter.convert_video(output_directory+'/'+patient_id+'.mp4')
    converter = DicomVideoConverterSend(extraction_dir, url_server)
    converter.create_video()
    converter.convert_video()
    # Accede al _id del video subido
    uploaded_video_id = converter.uploaded_video_id
    print(f"El _id del video subido es: {uploaded_video_id}")
    # Limpieza (opcional, descomenta si quieres usarlo)
    clean_up(archive_path, extraction_dir)


if __name__ == '__main__':
    main()
