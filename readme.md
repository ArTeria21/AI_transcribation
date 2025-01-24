# Transcribe: A Console Application for Speech-to-Text using Whisper

**Transcribe** is a user-friendly command-line tool for converting audio and video files into text using [OpenAI Whisper](https://github.com/openai/whisper). It supports multiple model sizes (tiny, base, small, medium), automatic GPU/CPU detection, language selection (English/Russian), and flexible output options. The script also offers transparent audio extraction from video files using `ffmpeg`.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Prerequisites and Requirements](#prerequisites-and-requirements)
4. [Installation](#installation)
   - [1. Download the Code](#1-download-the-code)
   - [2. Install Dependencies](#2-install-dependencies)
   - [3. Make the Script Executable](#3-make-the-script-executable)
   - [4. Make It Accessible System-Wide](#4-make-it-accessible-system-wide)
5. [Usage](#usage)
   - [Command Examples](#command-examples)
   - [Language Codes](#language-codes)
   - [Model Sizes](#model-sizes)
6. [Uninstallation or Removal](#uninstallation-or-removal)
7. [How It Works](#how-it-works)
8. [Troubleshooting](#troubleshooting)
9. [Contributing](#contributing)
10. [License](#license)
11. [Acknowledgments](#acknowledgments)

---

## Project Overview

**Transcribe** is a single Python script that harnesses the power of [OpenAI Whisper](https://github.com/openai/whisper) to accurately transcribe audio and video files into text. Whether you have `.mp3`, `.wav`, `.m4a`, or `.mp4` files, this tool will detect whether you need audio extraction (for video files) and then apply a chosen Whisper model to convert speech to text.

### Why Use This Tool?

1. **Convenient**: One-stop solution for both audio and video transcription in the terminal.  
2. **Flexible**: Choose from multiple Whisper model sizes, switch between English (`eng`) and Russian (`rus`), and save outputs to files or display them on-screen.  
3. **Optimized**: Automatically detects if a GPU is available (and falls back to CPU if not).  
4. **Friendly**: Uses Python’s `argparse` to give clear usage instructions.

---

## Key Features

- **Audio Extraction**: Automatically extracts audio from MP4 video files using `ffmpeg`.  
- **Multiple Language Support**: Currently supports English (`eng`) and Russian (`rus`), mapped to Whisper’s recognized codes (`en`, `ru`).  
- **Model Selection**: Choose from `tiny`, `base`, `small`, or `medium` Whisper models.  
- **Device Auto-Detection**: Uses CUDA if available; otherwise defaults to CPU. You can also force a device (`--device cpu` or `--device cuda`).  
- **Output Options**:  
  - Print transcription text to the console.  
  - Save transcription text to a file.  
- **Error Handling**: Gracefully handles missing dependencies, unsupported file types, and other runtime errors.  

---

## Prerequisites and Requirements

1. **Linux Environment**: Script is built and tested on Linux.  
2. **Python 3.7+**: Ensure you have Python 3.7 or higher.  
3. **System-Wide `ffmpeg`**: Required for extracting audio from video files.  
   - Install on Debian/Ubuntu:  
     ```bash
     sudo apt-get update && sudo apt-get install ffmpeg
     ```
   - Install on Fedora/CentOS:  
     ```bash
     sudo dnf install ffmpeg
     ```
4. **`pip`**: A Python package manager for installing dependencies.  
5. **CUDA-Capable GPU** (Optional): If you want GPU acceleration. Otherwise, CPU is sufficient.

---

## Installation

### 1. Download the Code

You can clone this repository (or download the single `transcriber.py` file directly):

```bash
git clone https://github.com/ArTeria21/AI_transcribation
cd AI_transcribation
```

*(Replace the above URL with your own if you host this somewhere else.)*

### 2. Install Dependencies

Use the included `requirements.txt` file to install necessary Python packages. (If you prefer a virtual environment, activate it before installing.)

```bash
pip install -r requirements.txt
```

This installs:
- **torch** (PyTorch)  
- **whisper**  
- **rich** *(optional but recommended for nicer console output)*  

> **Note**: Depending on your system, installing PyTorch may require additional steps to match your CUDA version. For more details, see the [PyTorch Installation Guide](https://pytorch.org/get-started/locally/).

> **Note**: If you are using venv, you need to replace shebang line in the script with the path to your venv! 

### 3. Make the Script Executable

Grant executable permissions to the script:

```bash
chmod +x transcribe.py
```

### 4. Make It Accessible System-Wide

To call the script from any directory using `transcribe`, you can create a symbolic link (symlink) in a directory like `/usr/local/bin`, which is usually in your `$PATH`.

```bash
sudo ln -s /full/path/to/transcribe.py /usr/local/bin/transcribe
```

> **Replace** `/full/path/to/transcribe.py` with the actual path to your script (e.g., `/home/user/AI_transcribation/transcribe.py`).

Now you can run `transcribe` from any directory in your terminal. If you receive a `Permission denied` error, ensure that `transcribe.py` has executable permissions set.

---

## Usage

Once installed, you can invoke the application by typing:

```bash
transcribe --help
```

You should see a helpful message describing all available arguments:

```
usage: transcribe [-h] [-o OUTPUT] [-l {eng,rus}] [-m {tiny,base,small,medium}] [-d {cpu,cuda}] input_file

A console application to transcribe audio or video files into text using OpenAI Whisper models.

positional arguments:
  input_file            Path to the input file (audio/video). Supported formats: mp3, m4a, wav, mp4.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Optional path to save the transcription text. If omitted, prints to console.
  -l {eng,rus}, --lang {eng,rus}
                        Language for transcription: 'eng' or 'rus'. Default is 'rus'.
  -m {tiny,base,small,medium}, --model {tiny,base,small,medium}
                        Whisper model size to use: 'tiny', 'base', 'small', or 'medium'. Default is 'small'.
  -d {cpu,cuda}, --device {cpu,cuda}
                        Force device to 'cpu' or 'cuda'. By default, auto-detects GPU if available.
```

### Command Examples

1. **Transcribe an MP3 file, print to console**:
   ```bash
   transcribe /path/to/file.mp3
   ```

2. **Transcribe an MP4 video, save output to a text file**:
   ```bash
   transcribe /path/to/video.mp4 --output transcript.txt
   ```

3. **Use English language and force CPU**:
   ```bash
   transcribe /path/to/audio.wav --lang eng --device cpu
   ```

4. **Select the medium Whisper model**:
   ```bash
   transcribe /path/to/audio.wav --model medium
   ```

### Language Codes
- `eng` -> **English**  
- `rus` -> **Russian**

*(Mapped internally to the Whisper language codes `en` and `ru`.)*

### Model Sizes

Choose one of the following Whisper models:
- `tiny`
- `base`
- `small` (default)
- `medium`

**Note**: Larger models typically provide better accuracy but require more VRAM and processing power.

---

## Uninstallation or Removal

If you want to remove the global `transcribe` command:

```bash
sudo rm /usr/local/bin/transcribe
```

Then you can remove or archive the project folder.

---

## How It Works

1. **Input Validation**: The script checks if your provided file exists and that it’s a supported format (mp3, m4a, wav, mp4).  
2. **Audio Extraction** (for video only): If the file is `.mp4`, `ffmpeg` extracts the audio track and outputs a temporary `temp_audio.wav`.  
3. **Model Loading**: It checks if you have CUDA available; if yes, it uses `cuda`; otherwise, it defaults to CPU (unless overridden by `--device`).  
4. **Transcription**: The chosen Whisper model transcribes the audio data, returning raw text.  
5. **Cleanup**: If `temp_audio.wav` was created, it’s deleted after use.  
6. **Output**: The final text is either printed to your terminal or saved to a file, depending on the `--output` argument.

---

## Troubleshooting

- **PyTorch Installation Errors**: Verify you installed the correct PyTorch build for your Linux distribution and CUDA version.  
- **`ModuleNotFoundError: No module named 'whisper'`**: Make sure you installed dependencies via `pip install whisper` or `pip install -r requirements.txt`.  
- **`ffmpeg` Not Found**: You must install `ffmpeg` via your system’s package manager. Confirm installation by running `ffmpeg -version`.  
- **GPU Memory Issues**: If you encounter out-of-memory errors on a GPU, try a smaller Whisper model (e.g., `tiny` or `base`), or switch to CPU (`--device cpu`).  

---

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition.  
- [PyTorch](https://pytorch.org/) for deep learning capabilities.  
- [ffmpeg](https://ffmpeg.org/) for audio extraction from videos.  

*Thank you for using **Transcribe**! If you have any questions or suggestions, please reach out or open an issue.*