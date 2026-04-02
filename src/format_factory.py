import os
import json
import subprocess
import math
# # # # # # # # # # # # # # # # # # # # # # # # # # #
# BL in this case is an abbreviation for src.blink  #
# I don't mean Boy's Love.                          #
#                                                   #
import src.blink as bl                              #
#                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # #
from src.config import PATH_FFMPEG
from src.lsm import lsm_selector
from src.subprocess_run import sp_run

def tsv_to_json(
        tsv_input: str, 
        json_output: str, 
        hex_background: str = "#fff", 
        language: str = "en_US",
        fps: int = 24
    ) -> int:
    
    """
    Reads a TSV (Tab-Separated Values) file containing timestamps and characters, 
    maps the characters to specific mouth shape indices based on language, 
    and exports the sequence data as a JSON file.

    Args:
        tsv_input (str): The file path to the source TSV file.
        json_output (str): The file path for the resulting JSON file.
        hex_background (str, optional): Background hex color. Defaults to "#fff".
        language (str, optional): Target language for shape mapping. Defaults to "en_US".

    Returns:
        int: 0 if the conversion is successful, 1 if an error occurs.
    """
    
    print(f"[INFO] Starting process: TSV to JSON conversion")
    print(f"[INFO] Loading shape map for language: '{language}'")
    
    try:
        lio_shape_map: dict[str, int] = lsm_selector(language)
    except Exception as e:
        print(f"[ERROR] Failed to load shape map: {e}")
        return 1
    
    events: list[tuple[float, int]] = []
    
    print(f"[INFO] Reading input file: '{tsv_input}'")
    try:
        with open(tsv_input, "r", encoding="utf-8") as file:
            lines: list[str] = file.readlines()

            for line_index, line in enumerate(lines, start=1):
                line = line.strip()
                if not line: 
                    continue
                
                parts: list[str] = line.split("\t")
                if len(parts) == 2:
                    try:
                        time: float = float(parts[0])
                    except ValueError:
                        print(f"[WARNING] Line {line_index}: '{parts[0]}' is not a valid float. Skipping line.")
                        continue

                    char: str = parts[1]
                    num: int = lio_shape_map.get(char, 0)
                    events.append((time, num))
                else:
                    print(f"[WARNING] Line {line_index}: Expected 2 columns. Skipping line.")

    except FileNotFoundError:
        print(f"[ERROR] Input file not found: '{tsv_input}'")
        return 1
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred while reading the file: {e}")
        return 1

    events.sort(key=lambda x: x[0])

    final_list: list[list] = []
    frame_duration: float = 1.0 / fps
    last_event_time: float = events[-1][0]
    
    total_frames: int = math.ceil(last_event_time * fps)
    
    current_event_idx: int = 0
    current_num: int = 0
    
    print(f"[INFO] Generating constant {fps} FPS sequence...")
    
    for frame_index in range(total_frames + 1):
        current_frame_time = frame_index * frame_duration
        
        while current_event_idx < len(events) and events[current_event_idx][0] <= current_frame_time:
            current_num = events[current_event_idx][1]
            current_event_idx += 1
            
        name_png: str = f"none_{bl.blink_state()}{current_num}"
        
        frame_data: list = [round(current_frame_time, 4), name_png, hex_background]
        final_list.append(frame_data)

    print(f"[INFO] Successfully generated {len(final_list)} frames.")

    print(f"[INFO] Writing data to JSON output: '{json_output}'")
    try:
        output_dir = os.path.dirname(json_output)
        if output_dir and not os.path.exists(output_dir):
            print(f"[INFO] Creating directory: '{output_dir}'")
            os.makedirs(output_dir)

        with open(json_output, "w", encoding="utf-8") as json_file:
            json.dump(final_list, json_file, indent=4)
        
        print(f"[SUCCESS] JSON file successfully saved to '{json_output}'")
        return 0

    except IOError as e:
        print(f"[ERROR] Failed to write JSON file '{json_output}': {e}")
        return 1
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred while saving JSON: {e}")
        return 1


def to_mp4(
        video_input: str, 
        audio_input: str, 
        video_output: str
    ) -> int:
    
    """
    Merges a video file and an audio file, converting them into an MP4 format using FFmpeg.
    The video is re-encoded using H.264 and the audio using AAC.

    Args:
        video_input (str): The file path to the source video.
        audio_input (str): The file path to the source audio.
        video_output (str): The file path for the resulting MP4 video.

    Returns:
        int: 0 if the conversion is successful, 1 if an error occurs.
    """
    
    print(f"[INFO] Starting process: Muxing video '{video_input}' and audio '{audio_input}'")
    
    command_ffmpeg: list[str] = [
        PATH_FFMPEG,
        "-y",
        "-i",        video_input,
        "-i",        audio_input,
        "-map",      "0:v:0",
        "-map",      "1:a:0",
        "-c:v",      "libx264",   # Codec H.264
        "-preset",   "slow",
        "-crf",      "22",        # 18-28
        "-c:a",      "aac",       # Codec AAC
        "-b:a",      "192k",
        "-pix_fmt",  "yuv420p",
        "-shortest",
        video_output
    ]

    print(f"[INFO] Running FFmpeg command: {' '.join(command_ffmpeg)}")

    try:
        if sp_run(
            command=command_ffmpeg,
            label=""
        ): return 1
        
        print(f"[SUCCESS] Video successfully saved to '{video_output}'")
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] FFmpeg process failed with error code {e.returncode}")
        return 1
        
    except FileNotFoundError:
        print(f"[ERROR] FFmpeg executable not found at '{PATH_FFMPEG}'. Please check your paths.")
        return 1
