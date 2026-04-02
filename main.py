import argparse
import tempfile
import sys
import os
from pathlib import Path
from src.config import PATH_RHUBARB, PATH_GODOT
from src.format_factory import tsv_to_json, to_mp4
from src.subprocess_run import sp_run
from src.output_filename import get_unique_filename

def main(
        audio_input: str,
        video_output: str
    ) -> int:

    """
    Orchestrates the process of generating a lip-sync video from an audio input.

    This function performs the following steps:
    1. Generates a TSV file with lip-sync data using RHUBARB.
    2. Converts the TSV data to a JSON file.
    3. Renders an AVI video using Godot based on the JSON data.
    4. Converts the AVI video to MP4, incorporating the original audio.

    Args:
        audio_input (str): The file path to the input audio file.
        video_output (str): The file path for the resulting MP4 video file.

    Returns:
        int: 0 if the video generation is successful, 1 if an error occurs at any stage.
    """

    print(f"[INFO] Starting video generation process for audio: '{audio_input}'")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path: Path = Path(tmp_dir)

        tmp_tsv: str = str(tmp_path / "lip_sync.tsv")
        tmp_json: str = str(tmp_path / "lip_sync.json")
        tmp_avi: str = str(tmp_path / "video.avi")

        command_rhubarb: list[str] = [
            PATH_RHUBARB,
            audio_input,
            "-o", tmp_tsv,
            "-f", "tsv"
        ]

        if sp_run(
            command=command_rhubarb,
            label=f"Generating lip-sync data with RHUBARB for '{audio_input}'"
        ): return 1

        if tsv_to_json(
            tsv_input=tmp_tsv,
            json_output=tmp_json,
            hex_background="#ffffffff",
            language="es"
        ): 
            print(f"[ERROR] TSV to JSON conversion failed for '{tmp_tsv}'")
            return 1
        print(f"[SUCCESS] TSV to JSON conversion completed: '{tmp_json}'")

        command_godot: list[str] = [
            PATH_GODOT,
            "--path",        "./13263ch-render",
            "--fixed-fps",   "24",
            "--write-movie", tmp_avi,
            "--", tmp_json
        ]

        if sp_run(
            command=command_godot,
            label=f"Rendering AVI video with Godot from '{tmp_json}'"
        ): return 1

        if to_mp4(
            video_input=tmp_avi,
            audio_input=audio_input,
            video_output=video_output
        ): 
            print(f"[ERROR] AVI to MP4 conversion failed for '{tmp_avi}'")
            return 1
        print(f"[SUCCESS] Video successfully converted to MP4: '{video_output}'")

    print(f"[SUCCESS] Video generation process completed for '{video_output}'")
    return 0

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a lip-sync video from an audio file."
    )
    parser.add_argument(
        "audio_input",
        type=str,
        help="Path to the input audio file (.wav)."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Path for the output video file (.mp4). If not specified,     "
             "it will be generated in the same directory as the audio file "
             "with a .mp4 extension and an incremental suffix if it exists."
    )

    args = parser.parse_args()

    audio_path = Path(args.audio_input)
    if not audio_path.is_file():
        print(f"[ERROR] Audio input file not found: {audio_path}")
        sys.exit(1)

    video_output_path: Path
    if args.output:
        video_output_path = Path(args.output)
    else:
        base_video_name = audio_path.stem
        base_video_path = audio_path.parent / f"{base_video_name}.mp4"
        video_output_path = get_unique_filename(base_video_path, ".mp4")

    print(f"[INFO] Audio input: {audio_path}")
    print(f"[INFO] Video output: {video_output_path}")

    sys.exit(
        main(
            audio_input=str(audio_path),
            video_output=str(video_output_path)
        )
    )


    
