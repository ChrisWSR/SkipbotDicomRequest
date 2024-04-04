import cv2
import numpy as np
import os
import pydicom

class DicomToJpegConverter:
    def __init__(self, dicom_directory, output_directory):
        self.dicom_directory = dicom_directory
        self.output_directory = output_directory
        self.convert_dicom_to_jpeg()

    def convert_dicom_to_jpeg(self):
        # Asegurarse de que el directorio de salida existe
        os.makedirs(self.output_directory, exist_ok=True)

        # Leer todos los archivos DICOM en el directorio y ordenarlos
        dicom_files = [os.path.join(self.dicom_directory, f) for f in os.listdir(self.dicom_directory) if f.endswith('.dcm')]
        dicom_files.sort(key=lambda x: pydicom.dcmread(x).InstanceNumber)

        # Procesar cada archivo DICOM
        for i, file_path in enumerate(dicom_files):
            dicom_data = pydicom.dcmread(file_path)
            image = dicom_data.pixel_array
            
            # Convertir imágenes en color a escala de grises (si es necesario)
            if len(image.shape) == 3 and image.shape[2] == 3:
                image = image.mean(axis=2)
                
            # Normalizar el frame
            norm_image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
            uint8_image = np.uint8(norm_image)

            # Guardar la imagen como JPEG
            jpeg_filename = os.path.join(self.output_directory, f"image_{i:04d}.jpg")
            cv2.imwrite(jpeg_filename, uint8_image)

            print(f"Imagen DICOM guardada como JPEG: {jpeg_filename}")


