import os 
import string
import pathlib

#####
# Directions:
# Make .txt file with same name as video file with timestamps formatted "(start)\n(stop)\n" 
# Example (No spaces):
### videofile.txt
# 0:10
# 0:20
# 0:30
# 0:40
###
# This will make a clip from 0:10 to 0:20, and another for 0:30 to 0:40. 
####

###########################################
#### 'True' or 'False' Case-Sensitive. ####
make_vclip = False  # Vertical, phone resolution.
delete_clip = False # Delete normal clip, keep Vclip.
has_titles = False
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



start_time = "00:00"
stop_time = "00:00"


videoqueue = getVideoQueue()

for video_filename in videoqueue:
    timestamps = getTimestamps(os.path.splitext(video_filename)[0] + ".txt")
    
    title_counter = 0
    if has_titles: 
        titles = getTitles(os.path.splitext(video_filename)[0] + ".title")
        title_length = len(titles)

    timestamp_counter = 0
    timestamp_length = len(timestamps)

    while timestamp_counter < timestamp_length:
        start_time = timestamps[timestamp_counter]

        if (timestamp_counter + 1) >= timestamp_length:
            break

        stop_time = timestamps[timestamp_counter+1]

        output_metadata = ""
        output_name = f"clip_{start_time.replace(':', '-')}_{stop_time.replace(':', '-')}_{video_filename[:-4]}.mp4"
        os.system(f"ffmpeg -ss {start_time} -to {stop_time}{output_metadata} -i \"{video_filename}\" \"{output_name}\"")
        ## Note that {output_metadata} starts as "" and any spaces will be appended if metadata exists.
        ## Example: ' -metadata title="Movie Title"'
        
        if has_titles:
            output_metadata += f" -metadata title=\"{titles[title_counter]}\""
            output_metadata += f" -metadata track=\"{title_counter+1}\""
            os.system(f"ffmpeg -i \"{output_name}\" -codec copy{output_metadata} \"m{output_name}\"")

        if make_vclip:
            os.system(f"ffmpeg -i \"{output_name}\" -vf \"split[original][copy];[copy]scale=-1:ih*(16/9)*(16/9),crop=w=ih*9/16,gblur=sigma=20[blurred];[blurred][original]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2\" \"v{output_name}\"")

        if delete_clip:
            os.remove(pathlib.Path(f"{output_name}"))
            
        timestamp_counter += 2
        title_counter += 1
