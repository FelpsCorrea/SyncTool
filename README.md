# 🔄 Sync Tool - File Synchronization with Progress Bar

A command-line tool to **synchronize missing or modified files** between two directories. It shows a live progress bar while copying and optionally logs errors to a text file. Can be compiled into a standalone `.exe` to run on any Windows machine **without Python installed**.

---

## Features

- Recursively scans source and destination folders
- Creates missing folders in the destination
- Copies only missing or modified files (based on file size)
- Displays a progress bar per file
- Logs copy errors to a file (optional)
- Cross-platform (Windows, macOS, Linux)
- Can be packaged as a `.exe` with no Python required

---

## How to Use (Python)

### 1. Install Python

Download from: https://www.python.org/downloads/  
Ensure `python` and `pip` are in your system PATH.

---

### 2. Download the script

Save the file as `sync_tool.py`.

---

### 3. Run from terminal or command prompt:

```bash
python sync_tool.py /path/to/source /path/to/destination --log custom_log.txt
```

- Replace `/path/to/source` with your source folder
- Replace `/path/to/destination` with your target folder
- `--log` is optional. Default: `transfer_errors.txt`

---

### Example Commands

**Windows:**
```bash
python sync_tool.py "D:\Photos" "E:\Backup" --log "backup_errors.txt"
```

**macOS/Linux:**
```bash
python sync_tool.py "/Volumes/MainDrive" "/Volumes/Backup" --log "errors.txt"
```

---

## Creating a Standalone `.exe` (No Python Needed)

### 1. Install PyInstaller:

```bash
pip install pyinstaller
```

---

### 2. Generate the executable:

```bash
pyinstaller --onefile sync_tool.py
```

Your `.exe` will be located in the `dist/` folder:

```
dist/
  sync_tool.exe  
```

---

### 3. Run the `.exe`:

```bash
sync_tool.exe "D:\Photos" "E:\Backup" --log "error_log.txt"
```

 It works on any Windows system — no Python required!

---
