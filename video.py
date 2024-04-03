import cv2
import numpy as np
import os
import pydicom
import subprocess

class DicomVideoConverter:
    def __init__(self, dicom_directory, video_path='salida_orientada.mp4'):
        self.dicom_directory = dicom_directory
        self.video_path = video_path  # Este será el primer video que luego será eliminado.
        self.data = None
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

    def convert_video(self, output_video='salida_compatible.mp4'):
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

        # Eliminar el video original después de la conversión
        os.remove(self.video_path)
        print(f"El video original {self.video_path} ha sido eliminado.")


