import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser

# --- CONFIGURATION ---
APPLET_CONFIG = {
    'Miiverse': {
        'launcher_offset': 0x31DA8, 
        'banner_file': '3D/BannerAppletMvs.LZ', 
        'banner_offset': 0x1D7C,
        'bytes_len': 3
    },
    'Browser': {
        'launcher_offset': 0x31E84, 
        'banner_file': '3D/BannerAppletWeb.LZ', 
        'banner_offset': 0x1D7C,
        'bytes_len': 3
    },
    'Notifications': {
        'launcher_offset': 0x31F60, 
        'banner_file': '3D/BannerAppletNews.LZ', 
        'banner_offset': 0x1D7C,
        'bytes_len': 3
    },
    'Friends': {
        'launcher_offset': 0x3203C, 
        'banner_file': '3D/BannerAppletFriend.LZ', 
        'banner_offset': 0x1D7C,
        'bytes_len': 3
    },
    'Game Notes': {
        'launcher_offset': 0x32118, 
        'banner_file': '3D/BannerAppletMemo.LZ', 
        'banner_offset': 0x1D7C,
        'bytes_len': 3
    },
}

LAUNCHER_FILENAME = "launcher.lz"

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class RomfsHexEditor:
    def __init__(self, root):
        icon_path = resource_path("icon.ico")
        self.root = root
        self.root.title("3DS Applet Color Editor")
        self.root.geometry("600x400")
        self.root.iconbitmap(icon_path)
        
        self.romfs_dir = ""
        self.applet_data = {} # Holds Tkinter StringVar and Canvas elements

        self.create_widgets()

    def create_widgets(self):
        # Folder Selection Row
        folder_frame = tk.Frame(self.root, padx=10, pady=10)
        folder_frame.pack(fill='x')
        
        self.btn_select = tk.Button(folder_frame, text="Select decompressed RomFS folder", command=self.select_folder)
        self.btn_select.pack(side='left')
        
        self.lbl_folder = tk.Label(folder_frame, text="No folder selected", textvar=None, fg="gray", padx=10)
        self.lbl_folder.pack(side='left', fill='x', expand=True)

        # Applet Grid Frame
        self.grid_frame = tk.LabelFrame(self.root, text="Applet Colors", padx=10, pady=10)
        self.grid_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Save Button
        self.btn_save = tk.Button(self.root, text="Save Changes & Backup", command=self.save_changes, state='disabled', bg="#d4edda")
        self.btn_save.pack(fill='x', padx=10, pady=10)

    def select_folder(self):
        directory = filedialog.askdirectory(title="Select decompressed RomFS folder")
        if not directory:
            return
        
        # Verify launcher.lz exists as a basic check
        if not os.path.exists(os.path.join(directory, LAUNCHER_FILENAME)):
            messagebox.showerror("Error", f"Could not find '{LAUNCHER_FILENAME}' in the selected directory. Did you decompress?")
            return
            
        self.romfs_dir = directory
        self.lbl_folder.config(text=directory, fg="black")
        self.load_hex_values()
        self.btn_save.config(state='normal')

    def load_hex_values(self):
        # Clear any existing grid items if switching folders
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
            
        launcher_path = os.path.join(self.romfs_dir, LAUNCHER_FILENAME)
        
        for i, (name, cfg) in enumerate(APPLET_CONFIG.items()):
            # 1. Read current hex from launcher.lz
            current_hex = "FFFFFF" # Default fallback
            if os.path.exists(launcher_path):
                with open(launcher_path, "rb") as f:
                    f.seek(cfg['launcher_offset'])
                    color_bytes = f.read(cfg['bytes_len'])
                    current_hex = color_bytes.hex().upper()

            # Create UI tracking variables
            hex_var = tk.StringVar(value=current_hex)
            
            # Label
            lbl = tk.Label(self.grid_frame, text=name, font=('Arial', 10, 'bold'))
            lbl.grid(row=i, column=0, sticky='w', pady=5, padx=5)
            
            # Entry Box
            entry = tk.Entry(self.grid_frame, textvariable=hex_var, width=10, font=('Courier', 10))
            entry.grid(row=i, column=1, pady=5, padx=5)
            
            # Color Preview Box
            preview = tk.Canvas(self.grid_frame, width=30, height=20, borderwidth=1, relief="solid")
            preview.grid(row=i, column=2, pady=5, padx=5)
            self.update_preview(preview, current_hex)
            
            # Trace entry modifications to update preview live
            hex_var.trace_add("write", lambda *args, p=preview, v=hex_var: self.update_preview(p, v.get()))

            # Color Picker Button
            btn_pick = tk.Button(self.grid_frame, text="🎨 Pick", command=lambda v=hex_var: self.pick_color(v))
            btn_pick.grid(row=i, column=3, pady=5, padx=5)
            
            # Store references
            self.applet_data[name] = {'hex_var': hex_var, 'cfg': cfg}

    def update_preview(self, canvas, hex_str):
        # Ensure it's a valid 6-character hex string for the preview canvas
        if len(hex_str) == 6:
            try:
                canvas.config(bg=f"#{hex_str}")
            except tk.TclError:
                canvas.config(bg="white") # Fallback on invalid hex syntax
        else:
            canvas.config(bg="white")

    def pick_color(self, hex_var):
        # Open color picker dialog
        initial_color = f"#{hex_var.get()}" if len(hex_var.get()) == 6 else "#FFFFFF"
        color_code = colorchooser.askcolor(title="Choose Applet Color", initialcolor=initial_color)
        if color_code[1]: # color_code[1] returns hex format '#RRGGBB'
            hex_var.set(color_code[1].replace("#", "").upper())

    def save_changes(self):
        launcher_path = os.path.join(self.romfs_dir, LAUNCHER_FILENAME)
        
        # 1. Create backups first if they don't already exist
        try:
            if not os.path.exists(launcher_path + ".bak"):
                shutil.copy2(launcher_path, launcher_path + ".bak")
            
            for name, data in self.applet_data.items():
                b_file = os.path.join(self.romfs_dir, data['cfg']['banner_file'])
                if os.path.exists(b_file) and not os.path.exists(b_file + ".bak"):
                    shutil.copy2(b_file, b_file + ".bak")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backups:\n{e}")
            return

        # 2. Write new hex values to files using the 7-byte structure
        try:
            with open(launcher_path, "r+b") as f_launch:
                for name, data in self.applet_data.items():
                    hex_str = data['hex_var'].get()
                    if len(hex_str) != 6: # 6 hex chars = 3 bytes (RGB)
                        raise ValueError(f"Invalid hex length for {name}. Must be 6 characters.")
                    
                    new_rgb = bytes.fromhex(hex_str)
                    
                    # --- Update launcher.lz ---
                    # First, read the existing 7 bytes to preserve the alpha byte
                    f_launch.seek(data['cfg']['launcher_offset'])
                    original_7_bytes = f_launch.read(7)
                    
                    if len(original_7_bytes) == 7:
                        alpha_byte = original_7_bytes[3:4] # Extract the 4th byte (Alpha)
                        # Construct payload: [RGB] (3 bytes) + [Alpha] (1 byte) + [RGB] (3 bytes)
                        launcher_payload = new_rgb + alpha_byte + new_rgb
                        
                        f_launch.seek(data['cfg']['launcher_offset'])
                        f_launch.write(launcher_payload)

                    # --- Update individual banner LZ file ---
                    banner_path = os.path.join(self.romfs_dir, data['cfg']['banner_file'])
                    if os.path.exists(banner_path):
                        with open(banner_path, "r+b") as f_banner:
                            f_banner.seek(data['cfg']['banner_offset'])
                            original_banner_bytes = f_banner.read(7)
                            
                            if len(original_banner_bytes) == 7:
                                banner_alpha = original_banner_bytes[3:4]
                                banner_payload = new_rgb + banner_alpha + new_rgb
                                
                                f_banner.seek(data['cfg']['banner_offset'])
                                f_banner.write(banner_payload)
                            
            messagebox.showinfo("Success", "Colors updated successfully! Secondary and banner colors matched.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving:\n{e}")

root = tk.Tk()
app = RomfsHexEditor(root)
root.mainloop()
