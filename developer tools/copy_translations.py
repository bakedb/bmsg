# This file was vibe coded
# LANG_DIR will probably need to be modified if venv is not activated
import json, os, re

LANG_DIR = "languages"
SOURCE = "English (US).json"

key_re = re.compile(r'^\s*"([^"]+)"\s*:')

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()

def save_lines(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)

source_data = load_json(os.path.join(LANG_DIR, SOURCE))
source_keys = list(source_data.keys())

for filename in os.listdir(LANG_DIR):
    if filename == SOURCE or not filename.endswith(".json"):
        continue

    path = os.path.join(LANG_DIR, filename)
    lines = load_lines(path)

    existing_keys = []
    key_to_line = {}

    # Scan file for keys and remember their line numbers
    for i, line in enumerate(lines):
        m = key_re.match(line)
        if m:
            key = m.group(1)
            existing_keys.append(key)
            key_to_line[key] = i

    # Remove keys that no longer exist
    for key in existing_keys:
        if key not in source_keys:
            idx = key_to_line[key]
            lines[idx] = None  # mark for deletion

    # Insert missing keys in the correct order
    for i, key in enumerate(source_keys):
        if key not in existing_keys:
            # Insert after the previous key in the file
            if i == 0:
                insert_at = 0
            else:
                prev_key = source_keys[i - 1]
                if prev_key in key_to_line:
                    insert_at = key_to_line[prev_key] + 1
                else:
                    insert_at = len(lines)

            new_line = f'    "{key}": "{source_data[key]}",\n'
            lines.insert(insert_at, new_line)

            # Recalculate line numbers
            lines = [l for l in lines if l is not None]
            key_to_line = {}
            for j, line in enumerate(lines):
                m = key_re.match(line)
                if m:
                    key_to_line[m.group(1)] = j

    # Remove deleted lines
    lines = [l for l in lines if l is not None]

    save_lines(path, lines)
    print(f"Updated {filename}")
