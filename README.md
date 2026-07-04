# 13263ch - Automated Lip-Sync Video Generator

**Version:** 2.25.1a
**Developed by:** dlemo-kun

---

## What's New

* **Version Flag:** Added the `--version` flag to quickly check the current version of the tool.
* **Character Selection:** Added the `--character` argument to specify which character you want to use.
* **Background Color:** Added the `--color` argument to customize the background color.
* **New Default Character:** Introduced a new default character named `None Female (nofe)`.
* **Python Path Specification:** You can now explicitly specify the path of the Python version you want to utilize.

---

## Tutorial

### What is this?
**13263ch** is an automated tool designed to generate lip-sync videos from an audio file. It orchestrates a workflow that analyzes speech and renders a character's mouth movements in a video format.

### How to Run

#### 1. Prerequisites
Ensure you have the following tools installed and accessible in your system path:
- **Python 3.x**
- **Godot Engine 4.x**
- **Rhubarb Lip Sync**
- **FFmpeg**

#### 2. Installation
Clone the repository and install the Python dependencies:
```bash
git clone https://github.com/dlemo-kun/13263ch.git
cd 13263ch
pip install -r requirements.txt
```

#### 3. Configuration
Create a `.env` file in the root directory (copy the existing `.env` template) and set the paths to your executables:
```env
PATH_PYTHON="C:/path/to/python.exe"
PATH_RHUBARB="C:/path/to/rhubarb.exe"
PATH_GODOT="C:/path/to/godot.exe"
PATH_FFMPEG="C:/path/to/ffmpeg.exe"
```

#### 4. Execution
Run the main script providing an input audio file and the desired output video name:
```bash
python ./main.py ./test/test.wav --output ./test/test.mp4
```

## Characters

The `--character` argument to specify which character you want to use.

### Options:

* **None:**
    * **ID:** none
    * **Name:** None
    * **Creator/s:** dlemo-kun and Nano Banana
    * **Use:** `--character none`

* **None Female:**
    * **ID:** nofe
    * **Name:** None Female
    * **Creator/s:** Elytra and Nano Banana Pro
    * **Use:** `--character nofe`