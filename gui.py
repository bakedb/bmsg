import tkinter as tk
from tkinter import ttk, filedialog
import crypt, startup, re, sys, json

# Variables
version = "0.1"

# Skip startup sequence for dev versions
if "dev" not in version:
    startup.startup()

root = tk.Tk()
notebook = ttk.Notebook(root)
root.title(f"bmsg {version}")
root.geometry("500x500")

# Language translator (not mine)
class Translator:
    def __init__(self, lang="en"):
        with open(f"languages/{lang}.json", "r", encoding="utf-8") as f:
            self.strings = json.load(f)

    def t(self, key, **kwargs):
        text = self.strings.get(key, f"[{key}]")
        if kwargs:
            return text.format(**kwargs)
        return text

t = Translator("en")

# Functions
def clipboard(input):
    root.clipboard_clear()
    root.clipboard_append(input)
    top = tk.Toplevel()
    top.geometry("210x60")
    tk.Label(top, text=t.t("clipboard.label")).grid()
    tk.Button(top, text="Ok", command=top.destroy).grid()   

def save_keys_to_file(public, private):
    f = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if f:
        content = f"{public}\n{private}"
        # no need to use an "open as" here
        f.write(content)
        f.close()

def save_message_to_file(message):
    f = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if f:
        content = message
        # no need to use an "open as" here
        f.write(content)
        f.close()

def get_keys(length):
    keys = str(crypt.generate_keys(length))
    re_output = re.findall(r'\w+\((.*?)\)', keys)
    public_key = re_output[0]
    private_key = re_output[1]
    key_label.configure(text=t.t("getkeys.label", public=public_key, private=private_key), wraplength=300, font=("default", 5))
    tk.Button(key_tab, text=t.t("getkeys.copypublic"), command=lambda: clipboard(public_key)).grid(column=0, row=2)
    tk.Button(key_tab, text=t.t("getkeys.copyprivate"), command=lambda: clipboard(private_key)).grid(column=0, row=3)
    tk.Label(key_tab, text=t.t("getkeys.savemessage")).grid(column=0, row=4)
    tk.Button(key_tab, text=t.t("getkeys.save"), command=lambda: save_keys_to_file(public_key, private_key)).grid(column=0, row=5)

def encrypt(entry, key):
    message = entry.get()
    key_string = key.get()
    try:
        public_key = crypt.return_keys(key_string)
    except ValueError as e:
        tk.Label(encrypt_tab, text=t.t("encrypt.error", e=e)).grid(column=2, row=1)
        return
    
    enc_message = crypt.encrypt(message, public_key)
    tk.Label(encrypt_tab, text=t.t("encrypt.output", enc_message=enc_message)).grid(column=2, row=1)

# GUI
frame = tk.Frame(root)
frame.grid()

# Message encryption tab
encrypt_tab = ttk.Frame(notebook)
notebook.add(encrypt_tab, text=t.t("encrypt.title"))

tk.Label(encrypt_tab, text=t.t("encrypt.label")).grid(column=0, row=0)
encrypted_entry = tk.Entry(encrypt_tab)
encrypted_entry.grid(column=1, row=0)

tk.Label(encrypt_tab, text=t.t("encrypt.keylabel")).grid(column=0, row=1)
public_key_entry = tk.Entry(encrypt_tab)
public_key_entry.grid(column=1, row=1)

tk.Button(encrypt_tab, text=t.t("encrypt.button"), command=lambda: encrypt(encrypted_entry, public_key_entry)).grid(column=2, row=0)

# Key generator tab
key_tab = ttk.Frame(notebook)
notebook.add(key_tab, text=t.t("getkeys.tab"))
generate_keys_button = tk.Button(key_tab, text=t.t("getkeys.button"), command=lambda: get_keys(1024)).grid(column=0, row=0)
key_label = tk.Label(key_tab, text=t.t("getkeys.notgenerated"))
key_label.grid(column=0, row=1)

notebook.grid()

# Crash handler
def on_crash(exec_type, exc, tb):
    tk.messagebox.showwarning(title=t.t("crash.title"), message=t.t("crash.message"))
sys.excepthook = on_crash

tk.mainloop()
