"""
Program for controlling the IMU connected to Pi_1
"""

import picamera
from pathlib import Path
import os

def ensure_dir(file_path):
    #Creates a directory if it doesn't exist from a Path variable
    if not file_path.parent.exists():
        file_path.parent.mkdir(parents=True)
    

class PiCam():
    
    def __init__(self):
        self.resolution = (640,480)
        self.images_dir = Path(os.path.dirname(__file__)) / 'PiCam_Img'
        self.videos_dir = Path(os.path.dirname(__file__)) / 'PiCam_Vid'
        #Check the videos and images directories exist
        ensure_dir(self.images_dir)
        ensure_dir(self.videos_dir)
        #When None videos will be recorded as one file, otherwise it is cut into
        #segments based on the value of video_cut in seconds
        self.video_cut = None
    
    def video(self, length, file_name):
        '''Records a video for the given length of time (in seconds) and saves to a file'''
        if self.video_cut == None:
            self._one_video(length, file_name)
        else:
            self._cut_video(length, file_name)
    
    def _cut_video(self, length, file_name):
        '''Records a video of the given length cur into segments'''
        n = 1
        file_name = 'PiCam_Vid/{}_{}.h264'.format(file_name,n)
        n += 1
        camera = picamera.Picamera(resolution=self.resolution)
        camera.start_recording(file_name)
        total_time = 0
        while (total_time - self.video_cut) >= 0:
            camera.wait_recording(self.video_cut)
            camera.split_recording('PiCam_Vid/{}_{}.h264'.format(file_name,n))
            n += 1
            total_time += self.video_cut
        camera.wait_recording(length - total_time)
        camera.stop_recording()
        
        
    def _one_video(self, length, file_name):
        '''Record a video and store as one file'''
        file_name = '{}.h264'.format(file_name)
        camera = picamera.Picamera(resolution=self.resolution)
        camera.start_recording(file_name)
        camera.wait_recording(length)
        camera.stop_recording()