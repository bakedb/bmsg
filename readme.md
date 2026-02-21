# bmsg
bmsg (b message) is a simple message encryption and decryption tool using RSA and a Tkinter GUI.

## Usage
Install:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Run:
```bash
python gui.py
```

## TODO:
- profiles for different keys
- security slider (key length, 1024 for speed, 2048 for security. Put performance warning for values >2048)
- hashing
- more languages
- website
- add screenshots to readme
- Add versioning to config.ini and a popup asking to update the config
- Save button on generate keys tab with all save options
- Add "manage keys" tab
- Add password to private key
- Actual theme selector