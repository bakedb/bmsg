import tkinter as tk
import configparser as cfg
from tkinter import ttk, filedialog, scrolledtext, messagebox
from tkinter.font import Font
from ttkthemes import ThemedTk
import crypt, startup, re, sys, json, os, webbrowser

# Variables
version = "0.4"
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
config_file_exists = os.path.exists(configfile)

if config_file_exists:
    config.read(configfile)
else:
    # Create default config structure
    config['config'] = {
        'language': 'English (US)',
        'dev': '0',
        'theme': 'arc',
        'key-security': '1024 (default)'
    }
    config['keys'] = {
        'public': '',
        'private': ''
    }
    # Try to write the config file
    try:
        with open(configfile, "w") as f:
            config.write(f)
    except (OSError, IOError):
        # Config file might not be writable in bundled environment/windows binary
        pass

# Ensure required sections exist
if 'config' not in config:
    config['config'] = {
        'language': 'English (US)',
        'dev': '0', 
        'theme': 'arc'
    }
if 'keys' not in config:
    config['keys'] = {
        'public': '',
        'private': ''
    }

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

# Functions n' stuff

def handle_crash(exc_type, exc_value, exc_traceback):
    import traceback
    error_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f"Unhandled exception: {error_details}")  # Log to console
    messagebox.showwarning(title=t.t("crash.title"), message=t.t("crash.message"))

sys.excepthook = handle_crash

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
    f = filedialog.asksaveasfile(defaultextension=".bmsg", filetypes=[("Encrypted Messages", "*.bmsg"), ("All Files", "*.*")])
    if f:
        content = str(message)
        # no need to use an "open as" here
        f.write(content)
        f.close()

def load_message_from_file():
    f = filedialog.askopenfile(defaultextension=".bmsg", filetypes=[("Encrypted Messages", "*.bmsg"), ("All Files", "*.*")])
    if f:
        content = f.read()
        decrypted_entry.insert(0, content)

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

def get_keys_wrapper():
    length = config['config']['key-security']
    if length == "1024 (default)":
        get_keys(1024)
    elif length == "2048 (secure, slower)":
        get_keys(2048)

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

def save_key_to_config(key, type, clear_type=None):
    def clear_key(key):
        if key == "public":
            config['keys']['public'] = ""
        elif key == "private":
            config['keys']['private'] = ""
        with open(configfile, "w") as f:
            config.write(f)
        warn_popup.destroy()
    if key != "":
        if type == "public":
            config['keys']['public'] = key
        elif type == "private":
            config['keys']['private'] = key
    else:
        if type == "clear":
            warn_popup = tk.Toplevel(root)
            warn_popup.title(t.t("managekeys.popup.title"))
            ttk.Label(warn_popup, text=t.t("managekeys.popup.info")).grid(column=0, row=0)
            ttk.Button(warn_popup, text=t.t("global.yes"), command=lambda: clear_key(clear_type)).grid(column=0, row=1)
            ttk.Button(warn_popup, text=t.t("global.cancel"), command=warn_popup.destroy).grid(column=0, row=2)
    with open(configfile, "w") as f:
        config.write(f)

def save_config():
    save_language()
    save_theme()
    save_security()
    save_popup = tk.Toplevel(root)
    save_popup.title(t.t("settings.savepopup.title"))
    ttk.Label(save_popup, text=t.t("settings.savepopup.message")).grid(column=0, row=0)
    ttk.Button(save_popup, text=t.t("global.close"), command=save_popup.destroy).grid(column=0, row=1)

def save_security():
    value = key_security_setting.get()
    config['config']['key-security'] = value
    with open(configfile, "w") as f:
        config.write(f)

def test_crash():
    try:
        raise Exception("Test crash triggered intentionally")
    except Exception as e:
        handle_crash(type(e), e, e.__traceback__)

def test_crash_continue():
    # raise Exception("Test crash triggered intentionally")
    sys.exit(1)

class TextEditor:
    def __init__(self, window):
        self.window = window
        editor_window = tk.Toplevel(root)
        self.text_entry = scrolledtext.ScrolledText(editor_window, wrap=tk.WORD)
        self.text_entry.grid(column=0, row=0)
        tk.Button(editor_window, text=t.t("global.save"), command=lambda: TextEditor.save(self.text_entry.get(1.0, tk.END).strip(), editor_window)).grid(column=0, row=1)
    def save(input, window):
        encrypted_entry.insert(0, input)
        window.destroy()

def openeditor():
    editor = TextEditor(encrypt_tab)

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

ttk.Button(encrypt_tab, text=t.t("encrypt.openeditor"), command=lambda: openeditor()).grid(column=2, row=0)
ttk.Button(encrypt_tab, text=t.t("encrypt.button"), command=lambda: encrypt(encrypted_entry, public_key_entry)).grid(column=2, row=1)

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
ttk.Button(decrypt_tab, text=t.t("decrypt.openfile"), command=lambda: load_message_from_file()).grid(column=1, row=2)

# Key generator tab
key_tab = ttk.Frame(notebook)
notebook.add(key_tab, text=t.t("getkeys.tab"))
generate_keys_button = ttk.Button(key_tab, text=t.t("getkeys.button"), command=lambda: get_keys(get_keys_wrapper())).grid(column=0, row=0)
key_label = ttk.Label(key_tab, text=t.t("getkeys.notgenerated"))
key_label.grid(column=0, row=1)

# Manage keys tab
manage_keys_tab = ttk.Frame(notebook)
notebook.add(manage_keys_tab, text=t.t("managekeys.tab"))
ttk.Label(manage_keys_tab, text=t.t("managekeys.copylabel")).grid(column=0, row=0)
ttk.Button(manage_keys_tab, text=t.t("managekeys.copypublic"), command=lambda: clipboard(config['keys']['public'])).grid(column=1, row=0)
ttk.Button(manage_keys_tab, text=t.t("managekeys.copyprivate"), command=lambda: clipboard(config['keys']['private'])).grid(column=2, row=0)
ttk.Label(manage_keys_tab, text=t.t("managekeys.deletelabel")).grid(column=0, row=1)
ttk.Button(manage_keys_tab, text=t.t("managekeys.deletepublic"), command=lambda: save_key_to_config("", "clear", "public")).grid(column=1, row=1)
ttk.Button(manage_keys_tab, text=t.t("managekeys.deleteprivate"), command=lambda: save_key_to_config("", "clear", "private")).grid(column=2, row=1)

# Settings tab
settings_tab = ttk.Frame(notebook)
notebook.add(settings_tab, text=t.t("settings.tab"))
ttk.Label(settings_tab, text=t.t("settings.language")).grid(column=0, row=0)
language_options = ttk.Combobox(settings_tab, values=["English (US)", "Engwish (owo)"])
language_options.set(current_language)
language_options.grid(column=0, row=1)
ttk.Label(settings_tab, text=t.t("settings.theme")).grid(column=0, row=2)
theme_selection = ttk.Combobox(settings_tab, values=["adapta", "aquativo", "arc", "black", "blue", "breeze", "clearlooks", "elegance", "equilux", "itft1", "keramik", "kroc", "plastik", "smog", "ubuntu", "winxpblue", "yaru"])
theme_selection.set(theme)
theme_selection.grid(column=0, row=3)
ttk.Button(settings_tab, text=t.t("settings.themeinfo"), command=lambda: webbrowser.open("https://ttkthemes.readthedocs.io/en/latest/themes.html")).grid(column=1, row=3)
ttk.Label(settings_tab, text=t.t("settings.securitylabel")).grid(column=0, row=4)
key_security_setting = ttk.Combobox(settings_tab, values=["1024 (default)", "2048 (secure, slower)"])
key_security_setting.set(config['config']['key-security'])
key_security_setting.grid(column=0, row=5)
ttk.Button(settings_tab, text=t.t("global.save"), command=lambda: save_config()).grid(column=0, row=6)

# Dev tab
dev_tab = ttk.Frame(notebook)
notebook.add(dev_tab, text=t.t("devoptions.tab"))
ttk.Button(dev_tab, text=t.t("devoptions.testcrash"), command=lambda: test_crash()).grid(column=0, row=0)

notebook.grid()

tk.mainloop()