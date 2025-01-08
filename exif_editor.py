import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from exif import Image

def jpg_to_exif(filepath):
    with open(filepath, "rb") as img_file:
        img = Image(img_file)
    if img.has_exif:
        print(f"EXIF data found in {filepath}.")
    else:
        print(f"EXIF data not found in {filepath}.")
    return img

def clear_all_exif(img):
    img.delete_all()
    messagebox.showinfo("Success", "All EXIF data has been deleted.")
    update_exif_table(img)

def list_all_exif(img):
    exif_data = []
    for attr in img.list_all():
        try:
            value = getattr(img, attr)
            exif_data.append((attr, value))
        except Exception:
            exif_data.append((attr, "failed to get value"))
    return exif_data

def update_exif_table(img):
    exif_data = list_all_exif(img)
    for row in exif_tree.get_children():
        exif_tree.delete(row)
    for attr, value in exif_data:
        exif_tree.insert("", "end", values=(attr, value))

def change_exif(img, filepath):
    def update_exif():
        attr = attr_entry.get()
        value = value_entry.get()
        if hasattr(img, attr):
            try:
                setattr(img, attr, value)
                with open(filepath, "wb") as new_img_file:
                    new_img_file.write(img.get_file())
                messagebox.showinfo("Success", f"Attribute '{attr}' updated to: {value}.")
                update_exif_table(img)
                change_window.destroy()
            except ValueError as ve:
                messagebox.showerror("Error", f"Invalid value for attribute '{attr}': {ve}.")
                change_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update attribute '{attr}': {e}.")
                change_window.destroy()
        else:
            messagebox.showerror("Error", f"The image does not have an attribute '{attr}'.")
            change_window.destroy()



    change_window = tk.Toplevel(root)
    change_window.title("Change EXIF Data")

    tk.Label(change_window, text="Attribute Name:").grid(row=0, column=0, padx=10, pady=10)
    attr_entry = tk.Entry(change_window)
    attr_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(change_window, text="New Value:").grid(row=1, column=0, padx=10, pady=10)
    value_entry = tk.Entry(change_window)
    value_entry.grid(row=1, column=1, padx=10, pady=10)

    update_button = tk.Button(change_window, text="Update", command=update_exif)
    update_button.grid(row=2, columnspan=2, pady=10)

def save_file(img, filepath):
    with open(filepath, "wb") as new_img_file:
        new_img_file.write(img.get_file())
    messagebox.showinfo("Success", "EXIF data saved")

def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg;*.jpeg")])
    if filepath:
        img = jpg_to_exif(filepath)
        update_exif_table(img)
        clear_button.config(state=tk.NORMAL, command=lambda: clear_all_exif(img))
        change_button.config(state=tk.NORMAL, command=lambda: change_exif(img, filepath))
        save_button.config(state=tk.NORMAL, command=lambda: save_file(img, filepath))

root = tk.Tk()
root.title("EXIF Metadata Editor")

exif_frame = tk.Frame(root)
exif_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

exif_tree = ttk.Treeview(exif_frame, columns=("Attribute", "Value"), show="headings")
exif_tree.heading("Attribute", text="Attribute")
exif_tree.heading("Value", text="Value")
exif_tree.column("Attribute", width=200)
exif_tree.column("Value", width=400)
exif_tree.pack(fill=tk.BOTH, expand=True)

button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, padx=10, pady=10)

open_button = tk.Button(button_frame, text="Open File", command=open_file)
open_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Clear All EXIF Data", state=tk.DISABLED)
clear_button.pack(side=tk.LEFT, padx=5)

change_button = tk.Button(button_frame, text="Change EXIF Data", state=tk.DISABLED)
change_button.pack(side=tk.LEFT, padx=5)
save_button = tk.Button(button_frame, text="Save EXIF Data", state=tk.DISABLED)
save_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
