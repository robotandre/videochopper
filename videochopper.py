import os 
import string
import pathlib

#### 'True' or 'False' Case-Sensitive. ####
make_vclip = True
delete_clip = False
####

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



start_time = "00:00"
stop_time = "00:00"


videoqueue = getVideoQueue()

for video_filename in videoqueue:
    timestamps = getTimestamps(os.path.splitext(video_filename)[0] + ".txt")

    timestamp_counter = 0
    timestamp_length = len(timestamps)

    while timestamp_counter < timestamp_length:
        start_time = timestamps[timestamp_counter]

        if (timestamp_counter + 1) >= timestamp_length:
            break

        stop_time = timestamps[timestamp_counter+1]

        output_name = f"clip_{start_time.replace(':', '-')}_{stop_time.replace(':', '-')}_{video_filename[:-4]}.mp4"
        os.system(f"ffmpeg -ss {start_time} -to {stop_time} -i \"{video_filename}\" \"{output_name}\"")
        
        if make_vclip:
            os.system(f"ffmpeg -i \"{output_name}\" -vf \"split[original][copy];[copy]scale=-1:ih*(16/9)*(16/9),crop=w=ih*9/16,gblur=sigma=20[blurred];[blurred][original]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2\" \"v{output_name}\"")

        if delete_clip:
            os.remove(pathlib.Path(f"{output_name}"))
            
        timestamp_counter += 2
