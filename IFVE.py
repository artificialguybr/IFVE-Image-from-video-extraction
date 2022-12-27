import sys
import cv2
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLineEdit, QLabel, QMessageBox, QComboBox, QProgressBar
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('IFVE - Image from video extraction')

        self.video_button = QPushButton('Select video', self)
        self.video_button.clicked.connect(self.select_video)
        self.video_button.move(0, 50)

        self.save_folder_button = QPushButton('Select folder to save images', self)
        self.save_folder_button.clicked.connect(self.select_save_folder)
        self.save_folder_button.move(0, 100)

        self.num_images_label = QLabel('Select how many images you need:', self)
        self.num_images_label.move(0, 150)
        self.num_images_box = QLineEdit(self)
        self.num_images_box.move(180, 150)

        self.resize_label = QLabel('Select image size option:', self)
        self.resize_label.move(0, 200)
        self.resize_options = QComboBox(self)
        self.resize_options.addItem("Do Not resize")
        self.resize_options.addItem("Resize to 512x512")
        self.resize_options.addItem("Resize to 768x768")
        self.resize_options.move(150, 200)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(100, 50, 200, 25)

        self.continue_button = QPushButton('Continue', self)
        self.continue_button.clicked.connect(self.validate_inputs)
        self.continue_button.move(100, 250)
        
    def select_video(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, 'Select video', '', 'Videos (*.mp4 *.mov *.avi *.wmv)', options=options)
        if file_name:
            print(f'Setting selected_video')
            self.selected_video = file_name
            print(f'Selected_video: {self.selected_video}')
            QMessageBox.information(self, 'Success', 'Video selected successfully')
        else:
            QMessageBox.warning(self, 'Error', 'No video was selected')
    def select_save_folder(self):
        self.selected_save_folder = str(QFileDialog.getExistingDirectory(self, 'Select folder to save images'))
        if self.selected_save_folder:
            QMessageBox.information(self, 'Success', 'Folder to save images selected successfully')
        else:
            QMessageBox.warning(self, 'Error', 'No folder was selected')
        
    def validate_inputs(self):
        try:
            print(f'Setting num_images...')
            self.num_images = int(self.num_images_box.text())
            print(f'num_images: {self.num_images}')
            if self.selected_video and self.selected_save_folder:
                QMessageBox.information(self, 'Success', 'Extraction started')
                self.progress_bar.setMaximum(self.num_images)
                # Load the video
                video = cv2.VideoCapture(self.selected_video)
                print(f'Video: {video}')
                # Get the video duration in minutes
                duration = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) / video.get(cv2.CAP_PROP_FPS) / 60
                print(f'Duration: {duration}')
                # Ignore the first 10 and last 10 minutes if the video is longer than 60 minutes
                if duration > 60:
                    duration = duration - 20
                    video.set(cv2.CAP_PROP_POS_MSEC, 600000)
                    print(f'New duration: {duration}')
                # Extract and save the images
                for i in range(self.num_images):
                    # Generate a random frame number between 0 and the duration of the video in seconds multiplied by the video FPS and make them proportionally spaced apart. Generate a new frame if the frame is already taken or if the frame are too close to each other.
                    frame_num = random.randint(0, int(duration * 60 * video.get(cv2.CAP_PROP_FPS)))
                    print(frame_num)
                    # Set the video position to the selected frame
                    video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                
                    # Read and save the image with the filename of the video name and the frame number.
                    success, image = video.read()
                    if success:
                        print(f'Saving image {i+1}...')
                        result = cv2.imwrite(f'{self.selected_save_folder}/{self.selected_video.split("/")[-1].split(".")[0]}_{frame_num}.png', image)
                        self.progress_bar.setValue(i+1)
                    # Check the resize option and resize the image if needed.
                    if self.resize_options.currentText() == 'Resize to 512x512':
                        print('Resizing to 512x512')
                        image = Image.open(f'{self.selected_save_folder}/{self.selected_video.split("/")[-1].split(".")[0]}_{frame_num}.png')
                        image = image.resize((512, 512), Image.Resampling.LANCZOS)
                        image.save(f'{self.selected_save_folder}/{self.selected_video.split("/")[-1].split(".")[0]}_{frame_num}.png')
                    elif self.resize_options.currentText() == 'Resize to 768x768':
                        print('Resizing to 768x768')
                        image = Image.open(f'{self.selected_save_folder}/{self.selected_video.split("/")[-1].split(".")[0]}_{frame_num}.png')
                        image = image.resize((768, 768), Image.Resampling.LANCZOS)
                        image.save(f'{self.selected_save_folder}/{self.selected_video.split("/")[-1].split(".")[0]}_{frame_num}.png')
                QMessageBox.information(self, 'Success', 'Extraction finished')
            else:
                QMessageBox.warning(self, 'Error', 'Please select a video and a folder to save images')
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Please enter a valid number of images')

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


