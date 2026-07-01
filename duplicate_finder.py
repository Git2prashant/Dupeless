"""
Duplicate File Finder — A Tkinter GUI Application
Scans a selected folder and detects duplicate files using MD5 hashing.
Displays files in a Finder-like view with color-coded duplicate groups.
"""

import os
import hashlib
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk, Image

# ========================== CONFIGURATION ========================== #

DARK_BG = '#232f3e'          # Main background (Amazon dark blue)
DARKER_BG = '#1a2332'       # Darker shade for panels
ACCENT = '#ff9900'           # Amazon orange accent
TEXT_COLOR = '#e0e0e0'       # Light text
SECONDARY_TEXT = '#8899aa'   # Muted text
SUCCESS_GREEN = '#4caf50'    # Green for status
DANGER_RED = '#f44336'       # Red for delete
WHITE = '#ffffff'

# Colors for duplicate groups (to tell groups apart)
GROUP_COLORS = [
    '#ff9900',   # Orange
    '#00bcd4',   # Cyan
    '#e91e63',   # Pink
    '#8bc34a',   # Light green
    '#9c27b0',   # Purple
    '#ffeb3b',   # Yellow
    '#ff5722',   # Deep orange
    '#03a9f4',   # Light blue
    '#cddc39',   # Lime
    '#f06292',   # Pink light
]


# ========================== HELPER FUNCTIONS ========================== #

def format_file_size(size_bytes):
    """Convert bytes to human-readable format (KB, MB, GB)."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def get_file_md5(filepath):
    """Calculate MD5 hash of a file (reads in chunks for large files)."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(8192)    # Read 8KB at a time
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except (PermissionError, OSError):
        return None


def get_file_extension(filename):
    """Get file extension or 'No Extension' if none."""
    _, ext = os.path.splitext(filename)
    return ext.upper() if ext else 'No Ext'


# ========================== MAIN APPLICATION ========================== #

class DuplicateFinderApp:
    """Main application class for the Duplicate File Finder."""

    def __init__(self, root):
        self.root = root
        self.root.title('Duplicate File Finder')
        self.root.geometry('950x650')
        self.root.minsize(800, 500)
        self.root.configure(bg=DARK_BG)

        # Try to set icon (skip if not found)
        try:
            self.root.iconbitmap('favicon.ico')
        except:
            pass

        # Store data
        self.selected_folder = StringVar(value='No folder selected')
        self.status_text = StringVar(value='Select a folder to begin scanning')
        self.file_count = StringVar(value='Files: 0')
        self.duplicate_count = StringVar(value='Duplicates: 0')
        self.all_files = []          # List of all scanned file paths
        self.duplicates = {}         # {hash: [file_paths]} for duplicates only

        # Build the UI
        self._create_header()
        self._create_toolbar()
        self._create_file_view()
        self._create_status_bar()

    # -------------------- HEADER -------------------- #

    def _create_header(self):
        """Create the top header with title."""
        header_frame = Frame(self.root, bg=DARKER_BG, height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)    # Prevent frame from shrinking

        # App title
        title_label = Label(
            header_frame,
            text='🔍 Duplicate File Finder',
            font=('Helvetica', 18, 'bold'),
            fg=ACCENT,
            bg=DARKER_BG
        )
        title_label.pack(side=LEFT, padx=20, pady=15)

        # File count badges (right side)
        stats_frame = Frame(header_frame, bg=DARKER_BG)
        stats_frame.pack(side=RIGHT, padx=20)

        Label(
            stats_frame,
            textvariable=self.file_count,
            font=('Helvetica', 11),
            fg=TEXT_COLOR,
            bg=DARKER_BG
        ).pack(side=LEFT, padx=(0, 15))

        Label(
            stats_frame,
            textvariable=self.duplicate_count,
            font=('Helvetica', 11, 'bold'),
            fg=DANGER_RED,
            bg=DARKER_BG
        ).pack(side=LEFT)

    # -------------------- TOOLBAR -------------------- #

    def _create_toolbar(self):
        """Create the toolbar with folder selector and action buttons."""
        toolbar_frame = Frame(self.root, bg=DARK_BG, pady=10)
        toolbar_frame.pack(fill='x', padx=15)

        # Folder path display
        path_frame = Frame(toolbar_frame, bg='#2d3e50', relief='solid', bd=1)
        path_frame.pack(side=LEFT, fill='x', expand=True, padx=(0, 10))

        Label(
            path_frame,
            text='📁',
            font=('Helvetica', 14),
            bg='#2d3e50',
            fg=ACCENT
        ).pack(side=LEFT, padx=(10, 5))

        Label(
            path_frame,
            textvariable=self.selected_folder,
            font=('Helvetica', 11),
            fg=TEXT_COLOR,
            bg='#2d3e50',
            anchor='w'
        ).pack(side=LEFT, fill='x', expand=True, padx=5, pady=8)

        # Browse button
        browse_btn = Button(
            toolbar_frame,
            text='Browse Folder',
            font=('Helvetica', 11, 'bold'),
            bg=ACCENT,
            fg='#000000',
            activebackground='#e68a00',
            activeforeground='#000000',
            relief='flat',
            padx=15,
            pady=6,
            cursor='hand2',
            command=self._browse_folder
        )
        browse_btn.pack(side=LEFT, padx=(0, 5))

        # Scan button
        scan_btn = Button(
            toolbar_frame,
            text='🔍 Scan',
            font=('Helvetica', 11, 'bold'),
            bg=SUCCESS_GREEN,
            fg=WHITE,
            activebackground='#388e3c',
            activeforeground=WHITE,
            relief='flat',
            padx=15,
            pady=6,
            cursor='hand2',
            command=self._scan_for_duplicates
        )
        scan_btn.pack(side=LEFT, padx=(0, 5))

        # Delete selected button
        delete_btn = Button(
            toolbar_frame,
            text='🗑 Delete Selected',
            font=('Helvetica', 11, 'bold'),
            bg=DANGER_RED,
            fg=WHITE,
            activebackground='#c62828',
            activeforeground=WHITE,
            relief='flat',
            padx=15,
            pady=6,
            cursor='hand2',
            command=self._delete_selected
        )
        delete_btn.pack(side=LEFT)

    # -------------------- FILE VIEW (TREEVIEW) -------------------- #

    def _create_file_view(self):
        """Create the Finder-like file list using Treeview."""
        # Container frame
        tree_frame = Frame(self.root, bg=DARK_BG)
        tree_frame.pack(fill='both', expand=True, padx=15, pady=(5, 0))

        # Style the Treeview to match dark theme
        style = ttk.Style()
        style.theme_use('default')

        style.configure('Custom.Treeview',
            background=DARKER_BG,
            foreground=TEXT_COLOR,
            fieldbackground=DARKER_BG,
            font=('Helvetica', 11),
            rowheight=28,
            borderwidth=0
        )
        style.configure('Custom.Treeview.Heading',
            background='#2d3e50',
            foreground=ACCENT,
            font=('Helvetica', 11, 'bold'),
            borderwidth=1,
            relief='flat'
        )
        style.map('Custom.Treeview',
            background=[('selected', '#3d5a80')],
            foreground=[('selected', WHITE)]
        )
        style.map('Custom.Treeview.Heading',
            background=[('active', '#3d5a80')]
        )

        # Create Treeview with columns
        columns = ('name', 'size', 'type', 'path', 'status')
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            style='Custom.Treeview',
            selectmode='extended'     # Allow selecting multiple rows
        )

        # Define column headings
        self.tree.heading('name', text='File Name', anchor='w')
        self.tree.heading('size', text='Size', anchor='center')
        self.tree.heading('type', text='Type', anchor='center')
        self.tree.heading('path', text='Path', anchor='w')
        self.tree.heading('status', text='Status', anchor='center')

        # Define column widths
        self.tree.column('name', width=220, minwidth=150, anchor='w')
        self.tree.column('size', width=80, minwidth=60, anchor='center')
        self.tree.column('type', width=70, minwidth=50, anchor='center')
        self.tree.column('path', width=350, minwidth=200, anchor='w')
        self.tree.column('status', width=120, minwidth=80, anchor='center')

        # Scrollbars
        y_scroll = Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        x_scroll = Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Pack: Treeview + scrollbars
        self.tree.pack(side=LEFT, fill='both', expand=True)
        y_scroll.pack(side=RIGHT, fill='y')
        x_scroll.pack(side=BOTTOM, fill='x')

        # Tag colors for duplicate groups
        for i, color in enumerate(GROUP_COLORS):
            self.tree.tag_configure(f'group_{i}', foreground=color)
        self.tree.tag_configure('unique', foreground=SECONDARY_TEXT)

    # -------------------- STATUS BAR -------------------- #

    def _create_status_bar(self):
        """Create the bottom status bar."""
        status_frame = Frame(self.root, bg=DARKER_BG, height=30)
        status_frame.pack(fill='x', side=BOTTOM)

        Label(
            status_frame,
            textvariable=self.status_text,
            font=('Helvetica', 10),
            fg=SECONDARY_TEXT,
            bg=DARKER_BG,
            anchor='w'
        ).pack(side=LEFT, padx=15, pady=5)

    # ==================== ACTIONS ==================== #

    def _browse_folder(self):
        """Open a folder selection dialog."""
        folder = filedialog.askdirectory(title='Select a Folder to Scan')
        if folder:
            self.selected_folder.set(folder)
            self.status_text.set(f'Folder selected: {folder}')
            self._load_files(folder)

    def _load_files(self, folder_path):
        """Load all files from the selected folder into the Treeview."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.all_files = []
        file_count = 0

        # Walk through the folder
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                # Skip hidden files (starting with .)
                if filename.startswith('.'):
                    continue

                filepath = os.path.join(dirpath, filename)
                try:
                    file_size = os.path.getsize(filepath)
                except OSError:
                    continue

                self.all_files.append(filepath)
                file_count += 1

                # Insert into Treeview
                self.tree.insert('', 'end', values=(
                    filename,
                    format_file_size(file_size),
                    get_file_extension(filename),
                    filepath,
                    'Not scanned'
                ), tags=('unique',))

        self.file_count.set(f'Files: {file_count}')
        self.duplicate_count.set('Duplicates: 0')
        self.status_text.set(f'Loaded {file_count} files. Click "Scan" to find duplicates.')

    def _scan_for_duplicates(self):
        """Scan all loaded files for duplicates using MD5 hashing."""
        if not self.all_files:
            messagebox.showwarning('No Files', 'Please select a folder first!')
            return

        self.status_text.set('Scanning for duplicates... Please wait.')
        self.root.update()    # Force UI update so the status message shows

        # Calculate MD5 hash for each file
        hash_map = {}    # {md5_hash: [filepath, filepath, ...]}

        for filepath in self.all_files:
            file_hash = get_file_md5(filepath)
            if file_hash:
                if file_hash not in hash_map:
                    hash_map[file_hash] = []
                hash_map[file_hash].append(filepath)

        # Filter to only groups with 2+ files (actual duplicates)
        self.duplicates = {
            h: paths for h, paths in hash_map.items() if len(paths) > 1
        }

        # Count total duplicate files
        total_duplicates = sum(len(paths) for paths in self.duplicates.values())

        # Update the Treeview with scan results
        # Clear and re-populate, putting duplicates at the top
        for item in self.tree.get_children():
            self.tree.delete(item)

        # First: Insert duplicates (grouped and color-coded)
        group_index = 0
        for file_hash, paths in self.duplicates.items():
            tag = f'group_{group_index % len(GROUP_COLORS)}'

            for filepath in paths:
                filename = os.path.basename(filepath)
                try:
                    file_size = os.path.getsize(filepath)
                except OSError:
                    file_size = 0

                self.tree.insert('', 'end', values=(
                    filename,
                    format_file_size(file_size),
                    get_file_extension(filename),
                    filepath,
                    f'⚠ Duplicate (Group {group_index + 1})'
                ), tags=(tag,))

            group_index += 1

        # Then: Insert unique files
        duplicate_paths = set()
        for paths in self.duplicates.values():
            duplicate_paths.update(paths)

        for filepath in self.all_files:
            if filepath not in duplicate_paths:
                filename = os.path.basename(filepath)
                try:
                    file_size = os.path.getsize(filepath)
                except OSError:
                    file_size = 0

                self.tree.insert('', 'end', values=(
                    filename,
                    format_file_size(file_size),
                    get_file_extension(filename),
                    filepath,
                    '✓ Unique'
                ), tags=('unique',))

        # Update status
        self.duplicate_count.set(f'Duplicates: {total_duplicates}')
        if total_duplicates > 0:
            self.status_text.set(
                f'Found {total_duplicates} duplicate files in {len(self.duplicates)} groups!'
            )
        else:
            self.status_text.set('No duplicates found. All files are unique!')

    def _delete_selected(self):
        """Delete the selected files from disk."""
        selected_items = self.tree.selection()

        if not selected_items:
            messagebox.showinfo('No Selection', 'Please select files to delete.')
            return

        # Get file paths of selected items
        files_to_delete = []
        for item in selected_items:
            values = self.tree.item(item, 'values')
            filepath = values[3]    # Path is the 4th column
            files_to_delete.append((item, filepath))

        # Confirm deletion
        count = len(files_to_delete)
        confirm = messagebox.askyesno(
            'Confirm Delete',
            f'Are you sure you want to permanently delete {count} file(s)?\n\n'
            'This action cannot be undone!'
        )

        if not confirm:
            return

        # Delete files
        deleted = 0
        for item, filepath in files_to_delete:
            try:
                os.remove(filepath)
                self.tree.delete(item)
                if filepath in self.all_files:
                    self.all_files.remove(filepath)
                deleted += 1
            except OSError as e:
                messagebox.showerror('Error', f'Could not delete:\n{filepath}\n\nReason: {e}')

        self.file_count.set(f'Files: {len(self.all_files)}')
        self.status_text.set(f'Deleted {deleted} file(s) successfully.')


# ========================== RUN THE APP ========================== #

if __name__ == '__main__':
    root = Tk()
    app = DuplicateFinderApp(root)
    root.mainloop()
