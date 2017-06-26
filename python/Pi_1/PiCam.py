"""
Program for controlling the IMU connected to Pi_1
"""

import picamera
from pathlib import Path
import os
import multiprocessing


def ensure_dir(file_path):
    # Creates a directory if it doesn't exist from a Path variable
    if not file_path.exists():
        file_path.mkdir(parents=True)


class PiCam():

    def __init__(self):
        self.active = False
        self.resolution = (640, 480)
        self.framerate = 20
        self.images_dir = Path(os.path.dirname(__file__)) / 'PiCam_Img'
        self.videos_dir = Path(os.path.dirname(__file__)) / 'PiCam_Vid'
        # Check the videos and images directories exist
        ensure_dir(self.images_dir)
        ensure_dir(self.videos_dir)
        # When None videos will be recorded as one file, otherwise it is cut into
        # Segments based on the value of video_cut in seconds
        self._processes = []
        self._flags = []

    def background_record_process(self, file_name, cut_length=None):
        '''Start a background process constantly recording video'''
        self.active = True
        flag = multiprocessing.Value('i', 0)
        if cut_length is None:
            p = multiprocessing.Process(target=self._video_process,
                                        args=(file_name, flag))
        else:
            p = multiprocessing.Process(target=self._cut_video_process,
                                        args=(file_name, cut_length, flag))

        self._processes.append(p)
        self._flags.append(flag)
        p.start()

    def end_background_process(self):
        '''End all background processes'''
        self.active = False
        # Tell the processes to stop recording
        for flag in self._flags:
            with flag.get_lock():
                flag.value = 1
        # Wait for each process to finish
        for i, process in enumerate(self._processes):
            process.join('Camera Process {} joined'.format(i))

    def _cut_video_process(self, file_name, cut_length, flag):
        '''Records a video of the given length cur into segments'''
        camera = picamera.PiCamera(resolution=self.resolution,
                                   framerate=self.framerate)
        n = 1
        camera.start_recording('PiCam_Vid/{}_{}.h264'.format(file_name, n))
        with flag.get_lock():
            local_flag = flag.value

        while local_flag == 0:
            camera.wait_recording(self.video_cut)
            n += 1
            camera.split_recording('PiCam_Vid/{}_{}.h264'.format(file_name, n))
            with flag.get_lock():
                local_flag = flag.value
        camera.stop_recording()

    def _video_process(self, file_name, flag):
        '''Record a video and store as one file'''
        file_name = '{}.h264'.format(file_name)
        camera = picamera.PiCamera(resolution=self.resolution,
                                   framerate=self.framerate)
        with flag.get_lock():
            local_flag = flag.value
        camera.start_recording(file_name)
        while local_flag == 0:
            camera.wait_recording(0.5)
            with flag.get_lock():
                local_flag = flag.value
        camera.stop_recording()
