# Duplicate File Finder & Learning Sandbox

A modern, dark-themed desktop application built in Python using **Tkinter** and **Pillow (PIL)** to locate and safely remove duplicate files. This repository also serves as a playground for learning Python fundamentals, including file handling, cryptography hashing, and Tkinter GUI development.

---

## 🔍 Duplicate File Finder

The primary application (`duplicate_finder.py` or `learn_tkinter.py`) is a GUI tool that scans directories and detects duplicate files based on their actual content (MD5 hashes), rather than just file names.

### Key Features
* **MD5 Content Hashing:** Uses MD5 verification. Even if two files have different names, they will be flagged as duplicates if their content is identical.
* **Finder-like Interface:** Uses a `ttk.Treeview` layout showing File Name, Size, Type, Path, and Status.
* **Color-Coded Grouping:** Automatically groups duplicate sets with distinct, harmonic colors to make them easy to differentiate.
* **Safe Deletion:** Supports multiple selections and prompts the user with confirmation dialogs to prevent accidental file deletion.
* **Responsive Dark Theme:** Styled with a premium dark palette (`#232f3e` Amazon Dark Blue) to be easy on the eyes.

---

## 🛠 Setup & Installation

### 1. Requirements
Ensure you have Python 3 installed. You will also need to install the **Pillow** library for image handling:

```bash
pip install Pillow
```

### 2. Run the Application
Run the main script from your terminal:

```bash
python3 duplicate_finder.py
```

---

## 📂 Repository Structure

| File | Description |
| :--- | :--- |
| **`duplicate_finder.py`** | The main duplicate finder utility with full Treeview features. |
| **`learn_tkinter.py`** | An experimental canvas used to study Tkinter widgets (Labels, Entries, Buttons, positioning). |
| **`file_handling.py`** | Helper script exploring directory traversal (`os.chdir`, `os.getcwd`) and string/byte hashing. |
| **`Sets.py`** | Small script practicing Python Set operations. |

---

## 🧠 Core Python Concepts Explored

### 1. File Hashing (MD5)
To identify duplicates efficiently without loading entire files into memory at once, the app reads files in binary chunks (`8192` bytes) and updates an MD5 hasher:
```python
def get_file_md5(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()
```

### 2. Geometry Managers
Understanding the layout capabilities of Tkinter using:
* **`.pack()`**: Stacking elements and handling margins (`padx`, `pady`).
* **`.grid()`**: Creating structured row/column alignment.
* **`.place()`**: Positioning elements using exact or relative coordinates (`x`, `y`, `relx`, `rely`).

### 3. Tkinter Sub-Modules
* **`ttk`**: Used to implement the native-themed widgets like `Treeview` (tables).
* **`filedialog`**: Invokes the OS's native folder and file selection dialogs.
* **`messagebox`**: Delivers warnings, errors, and confirmation popups (`yes/no`).
