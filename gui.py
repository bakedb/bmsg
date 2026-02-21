import tkinter as tk
import configparser as cfg
from tkinter import ttk, filedialog
from ttkthemes import ThemedTk
import crypt, startup, re, sys, json, os, webbrowser

# Variables
version = "0.2"
configfile = "config.ini"

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

# Parse config
config = cfg.ConfigParser()
if os.path.exists(configfile):
    config.read(configfile)
else:
    config['config'] = {
        'language': 'English (US)',
        'dev': '0',
        'theme': 'breeze'
    }
    config['keys'] = {
        'public': '',
        'private': ''
    }
    with open(configfile, "w") as f:
        config.write(f)

t = Translator(config['config']['language'])
current_language = config['config']['language']

# Skip startup sequence for dev versions
if config['config']['dev'] != "1":
    startup.startup()

# Set up tkinter
root = ThemedTk()
theme = config['config']['theme']
root.set_theme(theme)
notebook = ttk.Notebook(root)
root.title(f"bmsg {version}")

# Functions
def clipboard(input):
    root.clipboard_clear()
    root.clipboard_append(input)
    top = tk.Toplevel()
    top.geometry("210x60")
    ttk.Label(top, text=t.t("clipboard.label")).grid()
    ttk.Button(top, text="Ok", command=top.destroy).grid()   

def save_both_keys_to_file(public, private):
    f = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if f:
        content = f"{public}\n{private}"
        # no need to use an "open as" here
        f.write(content)
        f.close()

def save_keys_to_file(key):
    f = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if f:
        f.write(key)

def load_keys_from_file():
    f = filedialog.askopenfile(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if f:
        content = f.read()
        return content

def save_message_to_file(message):
    f = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if f:
        content = str(message)
        # no need to use an "open as" here
        f.write(content)
        f.close()

def get_keys(length):
    keys = str(crypt.generate_keys(length))
    re_output = re.findall(r'\w+\((.*?)\)', keys)
    public_key = re_output[0]
    private_key = re_output[1]
    key_label.configure(text=t.t("getkeys.label", public=public_key, private=private_key), wraplength=300, font=("default", 5))
    ttk.Button(key_tab, text=t.t("getkeys.copypublic"), command=lambda: clipboard(public_key)).grid(column=0, row=2)
    ttk.Button(key_tab, text=t.t("getkeys.copyprivate"), command=lambda: clipboard(private_key)).grid(column=0, row=3)
    ttk.Label(key_tab, text=t.t("getkeys.savemessage")).grid(column=0, row=4)
    ttk.Button(key_tab, text=t.t("getkeys.save"), command=lambda: save_keys_to_file(public_key)).grid(column=0, row=5)
    ttk.Button(key_tab, text=t.t("getkeys.savepublictoconfig"), command=lambda: save_key_to_config(public_key, "public")).grid(column=0, row=6)
    ttk.Button(key_tab, text=t.t("getkeys.saveprivatetoconfig"), command=lambda: save_key_to_config(private_key, "private")).grid(column=0, row=7)

def encrypt(entry, key):
    message = entry.get()
    key_string = key.get()
    try:
        public_key = crypt.return_keys(key_string)
    except ValueError as e:
        ttk.Label(encrypt_tab, text=t.t("global.error", e=e)).grid(column=2, row=1)
        return
    
    enc_message = crypt.encrypt(message, public_key)
    enc_popup = tk.Toplevel(root)
    enc_popup.title(t.t("encrypt.popup.title"))
    ttk.Label(enc_popup, text=t.t("encrypt.popup.output"), wraplength=200, anchor="center").grid(column=0, row=0)
    ttk.Label(enc_popup, text=t.t(enc_message), wraplength=200, font=("default", 5), anchor="center").grid(column=0, row=1)
    ttk.Button(enc_popup, text=t.t("encrypt.popup.copy"), command=lambda: clipboard(enc_message)).grid(column=0, row=2)
    ttk.Button(enc_popup, text=t.t("encrypt.popup.save"), command=lambda: save_message_to_file(enc_message)).grid(column=0, row=3)
    ttk.Button(enc_popup, text=t.t("global.close"), command=enc_popup.destroy).grid(column=0, row=4)

def decrypt(entry, key):
    message = entry.get()
    key_string = key.get()
    try:
        private_key = crypt.return_keys(key_string)
    except ValueError as e:
        ttk.Label(decrypt_tab, text=t.t("global.error", e=e)).grid(column=2, row=1)
        return
    
    dec_message = crypt.decrypt(message, private_key)
    dec_popup = tk.Toplevel(root)
    dec_popup.title(t.t("decrypt.popup.title"))
    ttk.Label(dec_popup, text=t.t("decrypt.popup.output", dec_message=dec_message), wraplength=200, anchor="center").grid(column=0, row=0)
    ttk.Button(dec_popup, text=t.t("decrypt.popup.copy"), command=lambda: clipboard(dec_message)).grid(column=0, row=1)
    ttk.Button(dec_popup, text=t.t("decrypt.popup.save"), command=lambda: save_message_to_file(dec_message)).grid(column=0, row=2)
    ttk.Button(dec_popup, text=t.t("global.close"), command=dec_popup.destroy).grid(column=0, row=3)

def save_language():
    config['config']['language'] = language_options.get()
    with open(configfile, "w") as f:
        config.write(f)

def save_theme():
    config['config']['theme'] = theme_selection.get()
    with open(configfile, "w") as f:
        config.write(f)

def save_key_to_config(key, type):
    if type == "public":
        config['keys']['public'] = key
    elif type == "private":
        config['keys']['private'] = key
    with open(configfile, "w") as f:
        config.write(f)

def save_config():
    save_language()
    save_theme()
    save_popup = tk.Toplevel(root)
    save_popup.title(t.t("settings.savepopup.title"))
    ttk.Label(save_popup, text=t.t("settings.savepopup.message")).grid(column=0, row=0)
    ttk.Button(save_popup, text=t.t("global.close"), command=save_popup.destroy).grid(column=0, row=1)

# GUI
frame = ttk.Frame(root)
frame.grid()

# Message encryption tab
encrypt_tab = ttk.Frame(notebook)
notebook.add(encrypt_tab, text=t.t("encrypt.title"))

ttk.Label(encrypt_tab, text=t.t("encrypt.label")).grid(column=0, row=0)
encrypted_entry = tk.Entry(encrypt_tab)
encrypted_entry.grid(column=1, row=0)

ttk.Label(encrypt_tab, text=t.t("encrypt.keylabel")).grid(column=0, row=1)
public_key_entry = tk.Entry(encrypt_tab)
public_key_entry.grid(column=1, row=1)

ttk.Button(encrypt_tab, text=t.t("encrypt.button"), command=lambda: encrypt(encrypted_entry, public_key_entry)).grid(column=2, row=0)

# Message decryption tab
decrypt_tab = ttk.Frame(notebook)
notebook.add(decrypt_tab, text=t.t("decrypt.title"))

ttk.Label(decrypt_tab, text=t.t("decrypt.label")).grid(column=0, row=0)
decrypted_entry = tk.Entry(decrypt_tab)
decrypted_entry.grid(column=1, row=0)

ttk.Label(decrypt_tab, text=t.t("decrypt.keylabel")).grid(column=0, row=1)
private_key_entry = tk.Entry(decrypt_tab)
private_key_entry.grid(column=1, row=1)

ttk.Button(decrypt_tab, text=t.t("decrypt.button"), command=lambda: decrypt(decrypted_entry, private_key_entry)).grid(column=2, row=0)
ttk.Button(decrypt_tab, text=t.t("decrypt.prefill"), command=lambda: private_key_entry.insert(0, config['keys']['private'])).grid(column=2, row=1)

# Key generator tab
key_tab = ttk.Frame(notebook)
notebook.add(key_tab, text=t.t("getkeys.tab"))
generate_keys_button = ttk.Button(key_tab, text=t.t("getkeys.button"), command=lambda: get_keys(1024)).grid(column=0, row=0)
key_label = ttk.Label(key_tab, text=t.t("getkeys.notgenerated"))
key_label.grid(column=0, row=1)

# Settings tab
settings_tab = ttk.Frame(notebook)
notebook.add(settings_tab, text=t.t("settings.tab"))
ttk.Label(settings_tab, text=t.t("settings.language")).grid(column=0, row=0)
language_options = ttk.Combobox(settings_tab, values=["English (US)", "Engwish (owo)"])
language_options.set(current_language)
language_options.grid(column=0, row=1)
ttk.Label(settings_tab, text=t.t("settings.theme")).grid(column=0, row=2)
theme_selection = ttk.Entry(settings_tab)
theme_selection.insert(0, theme)
theme_selection.grid(column=0, row=3)
ttk.Button(settings_tab, text=t.t("settings.themeinfo"), command=lambda: webbrowser.open("https://ttkthemes.readthedocs.io/en/latest/themes.html")).grid(column=1, row=3)
ttk.Button(settings_tab, text=t.t("global.save"), command=lambda: save_config()).grid(column=0, row=4)

notebook.grid()

# Crash handler
def on_crash(exec_type, exc, tb):
    tk.messagebox.showwarning(title=t.t("crash.title"), message=t.t("crash.message"))
sys.excepthook = on_crash

tk.mainloop()
