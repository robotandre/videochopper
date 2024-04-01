import os 
import string
import pathlib

#####
# Directions:
# Make .txt file with same name as video file with timestamps formatted 
# 0:10; 0:20; outputTitle.mp4; Metadata Title; Track#
### Example:
### videofile.mp4
### videofile.txt
# 0:10; 0:20; 1_outputTitle.mp4; Metadata Title; 1
# 0:20; 0:30; 2_outputTitle.mp4; Second Metadata Title; 2
###
# This will make a clip from 0:10 to 0:20, and another for 0:20 to 0:30. 
####

def getTitles(title_filename):
    with open(title_filename, 'r') as file_handle:
        titlenames = file_handle.read().strip().split('\n')
    return titlenames

def getTimestamps(timestamp_filename):
    with open(timestamp_filename, 'r') as file_handle:
        timestamps = file_handle.read().strip().split('\n')
    return timestamps

def getVideoQueue():
    all_filenames = os.listdir()
    videoqueue = []

    for file in all_filenames:

        if file.endswith(".txt"):
            continue 

        basename = os.path.splitext(file)[0]
        timestamp_file = basename + ".txt"

        if timestamp_file in all_filenames:
            videoqueue.append(file)

    return videoqueue

startTime = "00:00"
stopTime = "00:00"

videoQueue = getVideoQueue()

for videoFilename in videoQueue:
    timestamps = getTimestamps(os.path.splitext(videoFilename)[0] + ".txt")
    
    timestampCounter = 0
    timestampLength = len(timestamps)

    while timestampCounter < timestampLength:
       currentTimestamp = timestamps[timestampCounter].split(";")
       # 0:00; 1:00; filename.mp4; File Title; 1
       # Start; Stop; filename.mp4; File Title; File Track #

       startTime = currentTimestamp[0].strip()
       stopTime = currentTimestamp[1].strip()

       # Temporary name incase no input.
       outputFilename = f"clip_{startTime.replace(':', '-')}_{stopTime.replace(':', '-')}_{videoFilename[:-4]}.mp4"
       outputMetadata = ""

       if len(currentTimestamp) > 2:
           outputFilename = currentTimestamp[2].strip()
       
       if len(currentTimestamp) > 3:
           outputMetadata += f" -metadata title=\"{currentTimestamp[3].strip()}\""

       if len(currentTimestamp) > 4:
           outputMetadata += f" -metadata track=\"{currentTimestamp[4].strip()}\""


       if len(currentTimestamp) < 4:
           os.system(f"ffmpeg -ss {startTime} -to {stopTime} -i \"{videoFilename}\" \"{outputFilename}\"")
       else:
           os.system(f"ffmpeg -ss {startTime} -to {stopTime} -i \"{videoFilename}\" \"tmp_{outputFilename}\"")
           os.system(f"ffmpeg -i \"tmp_{outputFilename}\" -codec copy{outputMetadata} \"{outputFilename}\"")
           os.system(f"rm \"tmp_{outputFilename}\"")

       timestampCounter += 1
