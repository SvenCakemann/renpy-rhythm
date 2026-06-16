import os
import sys

import librosa


def get_onset_times(file_path):
    # Load audio at original sample rate
    y, sr = librosa.load(file_path, sr=None, mono=True)

    # Detect onset frames
    onset_frames = librosa.onset.onset_detect(
        y=y,
        sr=sr,
        units="frames"
    )

    # Convert frames to seconds
    onset_times = librosa.frames_to_time(
        onset_frames,
        sr=sr
    )

    return onset_times.tolist()


def process_file(file_path):
    onset_times = get_onset_times(file_path)

    file_name_no_extension, _ = os.path.splitext(file_path)
    output_name = file_name_no_extension + ".beatmap.txt"

    with open(output_name, "wt", encoding="utf-8") as f:
        f.write("\n".join(f"{t:.4f}" for t in onset_times))

    print(f"{file_path} => {output_name}")


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python generate_beatmap.py [input]\n"
            "Generate my_music.beatmap.txt from my_music.mp3\n"
            "[input] can be a file or directory containing audio files"
        )
        return

    path = sys.argv[1]

    if os.path.isdir(path):
        valid_exts = {
            ".mp3",
            ".wav",
            ".ogg",
            ".flac",
            ".m4a",
            ".aac"
        }

        files = [
            os.path.join(path, f)
            for f in os.listdir(path)
            if os.path.splitext(f)[1].lower() in valid_exts
        ]
    else:
        files = [path]

    for file_path in files:
        try:
            process_file(file_path)
        except Exception as e:
            print(f"Error processing {file_path}")
            print(e)


if __name__ == "__main__":
    main()