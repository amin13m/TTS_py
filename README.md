# TTS Python

A Python-based Text-to-Speech project for generating and processing speech audio, with support for multiple TTS engines and Persian voice models.

The project is designed to keep **source code and configuration in Git**, while large ML models, generated audio, virtual environments, logs, and temporary files remain outside the repository.

---

## Features

* Text-to-Speech generation
* Persian TTS support
* Multiple TTS engines/environments
* XTTS v2 support
* F5-TTS support
* Audio processing and merging
* JSON-based input
* Voice management
* GPU/CUDA support
* Separate Python environments for different TTS engines
* Large model files stored outside Git

---

# Requirements

## Operating System

The project is primarily developed and tested on:

* Windows 10/11
* PowerShell

Linux/macOS may work with modifications, but the commands in this README use Windows PowerShell syntax.

---

## Hardware

For GPU-based TTS:

* NVIDIA GPU
* CUDA-compatible PyTorch installation
* Sufficient VRAM for the selected model

CPU execution may be possible for some components, but inference can be significantly slower.

---

# Python

Use a supported Python version compatible with the selected TTS environment.

It is strongly recommended to use **separate virtual environments** for different TTS engines.

The project currently uses:

```text
f5env/
env_xtts/
indextts_env/
```

These environments are intentionally excluded from Git.

---

# Project Structure

```text
tts_py/
│
├── failed/                 # Failed/generated processing results
├── input/                  # Input JSON files
│   ├── Ep1.json
│   └── Ep2.json
│
├── logs/                   # Application logs
│   └── project.log
│
├── models/                 # Local ML models (NOT stored in Git)
│
├── output/                 # Generated audio (NOT stored in Git)
│
├── requirements/
│   ├── common.txt          # Shared dependencies
│   ├── f5env.txt           # F5-TTS environment
│   └── env_xtts.txt        # XTTS environment
│
├── src/
│   ├── audio/
│   ├── core/
│   ├── engine/
│   ├── models/
│   ├── quality/
│   ├── utils/
│   ├── audio_merge.py
│   ├── dubber_engine.py
│   ├── f5tts.py
│   ├── gpu.py
│   ├── json_reader.py
│   ├── tts_engine.py
│   └── voice_manager.py
│
├── temp/                   # Temporary files
├── voices/                 # Voice/reference files
│
├── .gitignore
├── main.py
├── requirements.txt
├── run.bat
├── test_xtts_fa.py
└── README.md
```

---

# Installation

## 1. Clone the Repository

```powershell
git clone https://github.com/amin13m/TTS_py.git
cd TTS_py
```

---

# 2. Create the Virtual Environments

Do not commit virtual environments to Git.

### F5-TTS Environment

```powershell
python -m venv f5env
```

Activate it:

```powershell
.\f5env\Scripts\Activate.ps1
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install dependencies:

```powershell
pip install -r requirements\f5env.txt
```

---

## 3. XTTS Environment

Deactivate the previous environment first:

```powershell
deactivate
```

Create the XTTS environment:

```powershell
python -m venv env_xtts
```

Activate it:

```powershell
.\env_xtts\Scripts\Activate.ps1
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install dependencies:

```powershell
pip install -r requirements\env_xtts.txt
```

---

# PowerShell Execution Policy

If PowerShell prevents activation of the virtual environment with an execution-policy error, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then reopen PowerShell and activate the environment again.

---

# CUDA / PyTorch

The current environments use CUDA 12.6 builds of PyTorch.

Expected versions:

```text
torch       2.12.1+cu126
torchaudio  2.11.0+cu126
torchvision 0.27.1+cu126
```

For F5-TTS:

```text
torchcodec 0.14.0
```

After installation, verify PyTorch and CUDA:

```powershell
python -c "import torch; print('PyTorch:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('CUDA version:', torch.version.cuda)"
```

A working GPU installation should report:

```text
CUDA available: True
```

You can also check the NVIDIA driver from PowerShell:

```powershell
nvidia-smi
```

If CUDA is unavailable, check:

1. NVIDIA driver installation
2. PyTorch CUDA build
3. Active virtual environment
4. GPU compatibility
5. Python/PyTorch compatibility

---

# Models

## Important

The `models/` directory is intentionally **not stored in Git**.

Large model files can exceed GitHub's file-size limits and should not be committed to the source repository.

The local directory may contain files such as:

```text
models/
├── persian_vits/
├── piper_fa/
└── xtts_v2/
```

Model files can be hundreds of megabytes or larger.

The repository therefore follows this structure:

```text
Source Code     → GitHub
Requirements    → GitHub
Configuration   → GitHub
Models          → Local / external storage
Generated Audio → Local
Virtual Env     → Local
```

---

# Model Setup

Before running an engine that requires a local model, make sure its model files exist in the expected location.

Example:

```text
models/
└── xtts_v2/
    ├── config.json
    ├── dvae.pth
    ├── mel_stats.pth
    ├── model.pth
    ├── speakers_xtts.pth
    └── vocab.json
```

Other engines may require their own model directories.

Do not place virtual environments or generated files inside the model directories.

---

# Installing Models

Model files are intentionally distributed separately from the Git repository.

When setting up a new machine:

1. Clone the repository.
2. Create the required Python environment.
3. Install the corresponding requirements.
4. Download or copy the required model files.
5. Place them under the expected `models/` directory.
6. Run the appropriate test script.

> Always obtain model files from their official/original distribution source and follow the corresponding model license.

---

# Input Files

Input data is stored in:

```text
input/
```

The project supports JSON-based input.

Example files:

```text
input/Ep1.json
input/Ep2.json
```

The exact JSON schema should match what is expected by the project's JSON reader and processing pipeline.

Before processing a large batch, test with a small input file first.

---

# Running the Project

The main entry point is:

```text
main.py
```

Run it from an activated environment:

```powershell
python main.py
```

Alternatively, if the project configuration supports it:

```powershell
.\run.bat
```

---

# XTTS Testing

A dedicated XTTS test script is available:

```text
test_xtts_fa.py
```

Activate the XTTS environment:

```powershell
.\env_xtts\Scripts\Activate.ps1
```

Then run:

```powershell
python test_xtts_fa.py
```

This is useful for verifying:

* Python environment
* XTTS installation
* Model availability
* CUDA/GPU availability
* Persian TTS functionality
* Audio generation

---

# F5-TTS

Activate the F5 environment:

```powershell
.\f5env\Scripts\Activate.ps1
```

Then run the project or the appropriate F5-TTS component:

```powershell
python main.py
```

The F5-TTS implementation is located in:

```text
src/f5tts.py
```

---

# Switching Between Environments

Only one environment should be active at a time.

### XTTS

```powershell
.\env_xtts\Scripts\Activate.ps1
```

### F5-TTS

```powershell
deactivate
.\f5env\Scripts\Activate.ps1
```

Check which Python is currently active:

```powershell
python -c "import sys; print(sys.executable)"
```

This is especially important when debugging dependency conflicts.

---

# Dependency Separation

The project intentionally keeps engine-specific dependencies separate.

## Common

```text
requirements/common.txt
```

Contains dependencies shared between environments.

## F5-TTS

```text
requirements/f5env.txt
```

Contains dependencies specific to the F5-TTS environment.

Important versions include:

```text
coqui-tts       0.27.5
transformers   4.53.3
tokenizers     0.21.4
numpy           2.4.4
```

## XTTS

```text
requirements/env_xtts.txt
```

Contains dependencies specific to the XTTS environment.

Important versions include:

```text
coqui-tts       0.25.3
transformers   4.46.2
tokenizers     0.20.3
numpy           1.26.4
```

Do not blindly merge the two environments into one virtual environment.

Some dependency versions are intentionally different.

---

# Audio Output

Generated audio is written to:

```text
output/
```

Temporary processing files are stored in:

```text
temp/
```

Failed processing results may be stored in:

```text
failed/
```

These directories are ignored by Git.

---

# Voices

Reference voices and voice-related files are stored under:

```text
voices/
```

Unlike generated output and model binaries, this directory is not automatically excluded by the project's `.gitignore`.

Do not commit large or private voice files unless they are intentionally part of the project.

---

# Logs

Application logs are stored under:

```text
logs/
```

Example:

```text
logs/project.log
```

Logs are ignored by Git and should normally not be committed.

---

# Git Rules

The repository intentionally excludes:

```text
f5env/
env_xtts/
indextts_env/
models/
output/
failed/
temp/
logs/
__pycache__/
```

It also excludes large model/audio files such as:

```text
*.wav
*.mp3
*.flac
*.pt
*.pth
*.ckpt
*.safetensors
*.bin
*.onnx
```

This keeps the Git repository lightweight and focused on source code.

---

# Why Models Are Not in Git

GitHub has a strict file-size limit for normal Git objects.

Large ML models can easily exceed that limit.

For example, a single model may be hundreds of megabytes or more.

Keeping models outside Git provides several advantages:

* Faster cloning
* Smaller repository
* Faster Git operations
* Cleaner version history
* Easier model replacement
* No accidental upload of huge binary files

The source repository remains fully usable as long as the required models are obtained separately.

---

# Git LFS

Git LFS can be used for large files when they intentionally need to be version-controlled.

However, the current project is designed so that the large files under:

```text
models/
```

remain outside the Git repository.

Therefore, model files should not be added to Git simply because Git LFS is installed.

---

# Troubleshooting

## `python` is not recognized

Verify Python installation:

```powershell
python --version
```

If Python is installed but not found, check your PATH configuration.

---

## Virtual environment activation fails

Try:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then:

```powershell
.\env_xtts\Scripts\Activate.ps1
```

or:

```powershell
.\f5env\Scripts\Activate.ps1
```

---

## Wrong Python environment is active

Check:

```powershell
python -c "import sys; print(sys.executable)"
```

The result should point to the expected environment.

For XTTS:

```text
...\tts_py\env_xtts\Scripts\python.exe
```

For F5-TTS:

```text
...\tts_py\f5env\Scripts\python.exe
```

---

## CUDA is not available

Run:

```powershell
python -c "import torch; print(torch.cuda.is_available())"
```

If it returns:

```text
False
```

also run:

```powershell
nvidia-smi
```

Then verify that the installed PyTorch build is the CUDA version required by the environment.

---

## Model not found

Check that the required model exists:

```powershell
Test-Path .\models
```

For a specific model:

```powershell
Test-Path .\models\xtts_v2\model.pth
```

If the result is:

```text
False
```

the model has not been installed or copied to the expected location.

---

## Dependency conflicts

Do not install packages randomly into the wrong environment.

First check:

```powershell
python -m pip list
```

Then verify the active environment:

```powershell
python -c "import sys; print(sys.executable)"
```

If necessary, recreate the environment instead of trying to repair a heavily modified environment.

---

# Clean Environment Reinstallation

If an environment becomes corrupted, remove and recreate it.

For XTTS:

```powershell
deactivate
Remove-Item -Recurse -Force .\env_xtts
python -m venv env_xtts
.\env_xtts\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements\env_xtts.txt
```

For F5-TTS:

```powershell
deactivate
Remove-Item -Recurse -Force .\f5env
python -m venv f5env
.\f5env\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements\f5env.txt
```

---

# Recommended Setup Order

For a new machine, use this order:

```text
1. Clone repository
        ↓
2. Install Python
        ↓
3. Create virtual environment
        ↓
4. Install requirements
        ↓
5. Verify PyTorch
        ↓
6. Verify CUDA
        ↓
7. Install/copy models
        ↓
8. Verify model files
        ↓
9. Run TTS test
        ↓
10. Run the main application
```

---

# Development Workflow

Before making changes:

```powershell
git status
```

Create or switch to the development branch:

```powershell
git checkout dev
```

Make changes and test them.

Then:

```powershell
git status
git add .
git commit -m "Describe your changes"
```

Push the development branch:

```powershell
git push origin dev
```

After testing, merge into `main`:

```powershell
git checkout main
git pull origin main
git merge dev
git push origin main
```

---

# Important Git Warning

Never use:

```powershell
git add .
```

without checking what is going to be committed when working with models, generated audio, virtual environments, or other large files.

Always check:

```powershell
git status
```

before committing.

If a large file accidentally appears in the staged changes, remove it from the Git index before committing.

---

# Repository Philosophy

This project follows a simple separation:

```text
┌─────────────────────────────┐
│          GitHub             │
│                             │
│  Source code               │
│  Requirements              │
│  Configuration             │
│  Documentation             │
│  Small project assets      │
└──────────────┬──────────────┘
               │
               │ setup
               ▼
┌─────────────────────────────┐
│       Local Machine         │
│                             │
│  Virtual environments       │
│  ML models                  │
│  Generated audio            │
│  Temporary files            │
│  Logs                       │
└─────────────────────────────┘
```

This keeps the repository manageable while allowing the complete TTS system to be reconstructed on a new machine.

---

# Quick Start

For an already configured machine:

```powershell
cd D:\Projects\tts_py
```

Activate the required environment.

For XTTS:

```powershell
.\env_xtts\Scripts\Activate.ps1
python test_xtts_fa.py
```

For F5-TTS:

```powershell
.\f5env\Scripts\Activate.ps1
python main.py
```

---

# Before Running

Make sure:

* [ ] Python is installed
* [ ] Correct virtual environment is active
* [ ] Requirements are installed
* [ ] PyTorch is installed
* [ ] CUDA is available if GPU inference is required
* [ ] Required model files exist
* [ ] Input JSON files are valid
* [ ] Output directories are writable
* [ ] Voice/reference files are available when required

---

# Notes

This repository contains the application code and dependency definitions.

Model availability, model licenses, GPU compatibility, and third-party package compatibility may change independently of this project.

For reproducible setups, use the pinned dependency versions provided in the `requirements/` directory and keep each TTS engine in its dedicated virtual environment.
