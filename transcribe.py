#!/home/artemka/AI_transcribation/venv/bin/python3
"""
Transcriber Console Application
--------------------------------
A versatile terminal-based Python script to transcribe audio or video files 
into text using OpenAI Whisper models. It supports various model sizes 
(tiny, base, small, medium), automatic audio extraction from video (via ffmpeg),
and convenient language selection for both English and Russian.

Requirements:
    - Python 3.7+ 
    - ffmpeg (system-wide installation)
    - Torch 
    - Whisper 
    - (Optional) Rich for colored console output

Usage Examples:
    1) Transcribe an MP3 audio file to screen:
       $ python transcriber.py /path/to/audio.mp3

    2) Transcribe an MP4 video file, specifying an output text file and Russian language:
       $ python transcriber.py /path/to/video.mp4 --output result.txt --lang rus

    3) Select a specific Whisper model (e.g., 'medium'):
       $ python transcriber.py /path/to/audio.mp3 --model medium

Background:
    - OpenAI Whisper is a general-purpose speech recognition model. 
    - This script demonstrates how to preprocess input (video/audio), load the 
      chosen Whisper model, and then output transcribed text in an accessible 
      format. 
"""

import os
import sys
import subprocess
import argparse
import warnings

try:
    import torch
except ImportError:
    print("[ERROR] PyTorch is required but not installed. Please install it via 'pip install torch'.")
    sys.exit(1)

try:
    import whisper
except ImportError:
    print("[ERROR] Whisper is required but not installed. Please install it via 'pip install whisper'.")
    sys.exit(1)


# Suppress future warnings from PyTorch/Whisper
warnings.filterwarnings("ignore", category=FutureWarning)


def extract_audio(video_path: str, audio_path: str) -> None:
    """
    Extracts audio from a given video file and saves it as a WAV file with 
    the specified audio path. Uses ffmpeg via subprocess to convert the file.

    :param video_path: Path to the input video file (e.g., .mp4)
    :param audio_path: Path to the temporary audio file (e.g., temp_audio.wav)
    """
    try:
        command = [
            "ffmpeg", "-i", video_path, "-vn", 
            "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", 
            audio_path
        ]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode("utf-8", errors="ignore")
        print(f"[ERROR] Failed to extract audio: {error_msg}")
        sys.exit(1)


def transcribe_audio(audio_path: str, device: str, language: str, model_size: str) -> str:
    """
    Loads the specified Whisper model on the chosen device (CPU or GPU), 
    then transcribes the audio file.

    :param audio_path: Path to the audio file to be transcribed.
    :param device: 'cuda' if GPU is available, otherwise 'cpu'.
    :param language: The language code (e.g., 'en', 'ru').
    :param model_size: Model size to load (tiny, base, small, medium).
    :return: The transcribed text as a string.
    """
    # Load the model
    print(f"[INFO] Loading Whisper model: {model_size} on device: {device}")
    model = whisper.load_model(model_size, device=device)

    # Perform the transcription
    print("[INFO] Starting transcription...")
    result = model.transcribe(audio_path, language=language, verbose=False)
    return result["text"]


def valid_file_path(path: str) -> str:
    """
    Checks if the provided file path is a valid file. Used by argparse 
    for argument validation.

    :param path: File path string.
    :return: The same path if valid, otherwise raises an exception.
    """
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"File '{path}' does not exist.")
    return path


def parse_arguments() -> argparse.Namespace:
    """
    Sets up the command-line argument parser and returns the parsed arguments.

    :return: A Namespace object with parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description=(
            "A console application to transcribe audio or video files into text "
            "using OpenAI Whisper models. Supports multiple model sizes, "
            "languages, and output options."
        )
    )

    # Positional argument: input file
    parser.add_argument(
        "input_file",
        type=valid_file_path,
        help="Path to the input file (audio/video). Supported formats: mp3, m4a, wav, mp4."
    )

    # Optional argument: output file
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Optional path to save the transcription text. If omitted, prints to console."
    )

    # Optional argument: language selection
    parser.add_argument(
        "-l", "--lang",
        type=str,
        choices=["eng", "rus"],
        default="rus",
        help="Language for transcription: 'eng' or 'rus'. Default is 'rus'."
    )

    # Optional argument: model size
    parser.add_argument(
        "-m", "--model",
        type=str,
        choices=["tiny", "base", "small", "medium"],
        default="small",
        help=(
            "Whisper model size to use: 'tiny', 'base', 'small', or 'medium'. "
            "Default is 'small'. Larger models are more accurate but heavier."
        )
    )

    # Optional argument: force device
    parser.add_argument(
        "-d", "--device",
        type=str,
        choices=["cpu", "cuda"],
        default=None,
        help="Force device to 'cpu' or 'cuda'. By default, auto-detects GPU if available."
    )

    return parser.parse_args()


def main() -> None:
    """
    Main function that orchestrates the console application flow:
    1. Parse CLI arguments.
    2. Validate file extension.
    3. Extract audio if needed.
    4. Transcribe using the chosen Whisper model.
    5. Save or print the result.
    """
    args = parse_arguments()

    # Map short language codes to Whisper-compatible codes
    language_map = {"eng": "en", "rus": "ru"}
    language = language_map[args.lang]

    # Determine the device
    if args.device is not None:
        device = args.device
    else:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    input_file = args.input_file
    output_file = args.output
    model_size = args.model

    _, ext = os.path.splitext(input_file)
    ext = ext.lower()

    audio_path = input_file  # If already an audio file

    # If it's a video file, extract audio first
    if ext == ".mp4":
        print("[INFO] Detected video file. Extracting audio...")
        audio_path = "temp_audio.wav"
        extract_audio(input_file, audio_path)
    elif ext not in [".mp3", ".m4a", ".wav"]:
        print("[ERROR] Unsupported file format. Please provide mp3, mp4, m4a, or wav.")
        sys.exit(1)

    # Transcribe
    transcribed_text = transcribe_audio(
        audio_path=audio_path, 
        device=device, 
        language=language, 
        model_size=model_size
    )

    # Clean up temporary audio file if we extracted from video
    if ext == ".mp4" and os.path.exists(audio_path):
        os.remove(audio_path)

    # Output handling
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(transcribed_text)
        print(f"\n[INFO] Transcription saved to: {output_file}")
    else:
        print("\n[TRANSCRIPTION OUTPUT]")
        print(transcribed_text)


if __name__ == "__main__":
    main()
