# IFVE - Image from video extraction

IFVE is a simple Python application that allows you to extract frames from a video and save them as images. Ideal for Stable Diffusion training.

This is just a hobby project to exercise my beginner python skills more

## Features 
-  Select a video file to extract frames from
- Choose a folder to save the extracted frames
- Select the number of frames to extract
- Optionally resize the frames to 512x512 or 768x768
- The script automatically skips the first 10 minutes and the last 10 minutes if the video is over 60 minutes long in order to avoid studio intro scenes and credit scenes.

## Installation
1. Clone the repository
2. Install the dependencies

## Usage
1. Run the application
2. Click on the "Select video" button to choose a video file
3. Click on the "Select folder to save images" button to choose a folder to save the extracted frames
4. Enter the number of frames you want to extract in the "Select how many images you need" field
5. Select a resize option from the "Select image size option" dropdown menu (optional)
6. Click on the "Continue" button to start the extraction process
7. The images will be saved in the folder.
