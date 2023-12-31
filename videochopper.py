import os 
import string

# For every file in directory, check if there's a txt file with the same name.

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

        output_name = f"{start_time.replace(':', '-')}_{stop_time.replace(':', '-')}_{video_filename}"
        os.system(f"ffmpeg -ss {start_time} -i \"{video_filename}\" -to {stop_time} -c copy \"{output_name}\"")
            
        timestamp_counter += 1

