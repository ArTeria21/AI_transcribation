# Transcribe: CLI Speech-to-Text with OpenAI Whisper

[![Python 3.7+](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready terminal application for high-accuracy audio/video transcription using OpenAI's Whisper AI models.

## 🚀 Features

| Feature                | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| Multi-format Support   | Process MP3, WAV, M4A, MP4 files                                           |
| Model Selection        | Choose from tiny/base/small/medium Whisper models                          |
| GPU Acceleration       | Automatic CUDA detection with fallback to CPU                               |
| Language Support       | English (`eng`) and Russian (`rus`) translations                            |
| Clean Output           | Console display or file output with proper encoding                        |
| Video Handling         | Automatic audio extraction from video files via FFmpeg                     |

## 📦 Installation

### System Requirements
```
sudo apt update && sudo apt install ffmpeg python3-venv
```

### Python Environment Setup
```
# Create dedicated virtual environment
python3 -m venv ~/.local/venv/transcribe
source ~/.local/venv/transcribe/bin/activate

# Install dependencies
pip install torch whisper rich
deactivate
```

### Application Deployment
```
# 1. Make script executable
chmod +x transcribe.py

# 2. Create global symlink
mkdir -p ~/.local/bin
ln -s $(pwd)/transcribe.py ~/.local/bin/transcribe

# 3. Update PATH (add to ~/.bashrc)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## 🖥️ Usage

### Basic Syntax
```
transcribe [INPUT_FILE] [OPTIONS]
```

### Common Options
| Option          | Description                           | Default     |
|-----------------|---------------------------------------|-------------|
| `-o, --output`  | Output file path                      | Console     |
| `-l, --lang`    | Language (eng/rus)                    | rus         |
| `-m, --model`   | Whisper model size                    | small       |
| `-d, --device`  | Force compute device (cpu/cuda)      | auto-detect |

### Usage Examples
```
# Transcribe video with medium model
transcribe lecture.mp4 --model medium -o transcript.txt

# English transcription forcing CPU
transcribe interview.mp3 --lang eng --device cpu

# Show help menu
transcribe --help
```

## 🛠️ Technical Details

### Model Performance
| Model   | VRAM Usage | Relative Speed | Accuracy |
|---------|------------|----------------|----------|
| tiny    | ~1 GB      | 16x            | Basic    |
| base    | ~1.5 GB    | 8x             | Good     |
| small   | ~5 GB      | 1x             | Excellent|
| medium  | ~10 GB     | 0.5x           | Best     |

### File Processing Pipeline
1. Input validation → 2. Audio extraction (if video) → 3. Model loading → 4. Transcription → 5. Cleanup → 6. Output

## 🔍 Troubleshooting

**Common Issues:**
- `ffmpeg not found`: Reinstall via `sudo apt install ffmpeg`
- CUDA out of memory: Use smaller model or `--device cpu`
- Encoding errors: Ensure files are in supported formats

**Verification:**
```
# Check installation
which transcribe && transcribe --version

# Test GPU detection
python3 -c "import torch; print(torch.cuda.is_available())"
```

## 🙏 Acknowledgments
- OpenAI for the Whisper model
- PyTorch team for deep learning framework
- FFmpeg community for audio processing