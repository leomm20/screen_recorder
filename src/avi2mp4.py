import os

import moviepy.editor as moviepy


def convert_avi2mp4(video):
    clip = moviepy.VideoFileClip(video)
    filename = video[:-4] + '.mp4'
    clip.write_videofile(filename)
    return filename


if __name__ == '__main__':
    convert_avi2mp4('block.avi')
