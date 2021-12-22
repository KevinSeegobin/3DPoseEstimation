import os
import json
from os import listdir
from os.path import isfile, join

def InitVids(path):

    files = [f for f in listdir(path) if isfile(join(path, f))]
    
    for f in files:
        cmd = "bin\\OpenposeDemo.exe --video %s --write_json output\\%s --display 0 --render_pose 0 --part_candidates"%(join(path, f), f[:-4])
        #print(cmd)
        os.system(cmd)

def InitIms(path):
    cmd = "bin\\OpenposeDemo.exe --image_dir %s --write_json output\\images --display 0 --render_pose 0 --part_candidates"%(path)
    os.system(cmd)

def ProcessIm(path):
    parts = dict()

    with open(path) as f:
        data = json.load(f)
        data = dict(data["people"][0])["pose_keypoints_2d"]
    
    for i in range(int(len(data)/3)):
        parts[i] = data[i*3: i*3+3]

    for i in list(reversed(parts.keys())):
        parts[i] = [(parts[i][0] - parts[0][0]), (parts[i][1] - parts[0][1]), parts[i][2]]

    return parts

def ProcessVid(path):
    files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
    frame = dict()
    frames = dict()

    for file in range(len(files)):
        with open(files[file]) as f:
            data = json.load(f)
            data = dict(data["people"][0])["pose_keypoints_2d"]

        for i in range(int(len(data)/3)):
            frame[i] = data[i*3 : i*3+3]

        for i in list(reversed(frame.keys())):
            frame[i] = [(frame[i][0] - frame[0][0]), (frame[i][1] - frame[0][1]), frame[i][2]] ##fix this maybe

        frames["frame%s"%file] = frame

    return frames

InitVids(".\\UCF101")


#openpose\bin\OpenPoseDemo.exe --video openpose\examples\media\video.avi --write_json output/Vid1/ --display 0 --render_pose 0