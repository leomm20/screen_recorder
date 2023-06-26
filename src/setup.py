from cx_Freeze import setup, Executable


options = {
    'build_exe': {
        'includes': ['avi2mp4'],
        'bin_path_includes': [r'C:\Python\Lib\site-packages\cv2'],
        'include_files': [r'opencv_videoio_ffmpeg470_64.dll'],
        'zip_include_packages': ['moviepy~=1.0.3', 'opencv-python~=4.7.0.72', 'PyAutoGUI~=0.9.53', 'pydub~=0.25.1',
                                 'soundfile~=0.12.1', 'pynput~=1.7.6', 'numpy~=1.24.1'],
    }
}

setup(
    name="PQAQC_screenrecorder",
    version="1.0",
    author='Leonardo Maggiotti',
    description="Screen Recorder con posibilidad de grabar audio",
    executables=[Executable("main.py")],
)

# python setup.py build
