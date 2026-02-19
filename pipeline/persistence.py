import json
import os
import uuid
from datetime import datetime

if os.name == "nt":  # Windows
    _DATA_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "reasoning_lab")
else:  # Linux / macOS
    _DATA_DIR = os.path.join(os.path.expanduser("~"), ".local", "share", "reasoning_lab")
_SETTINGS_FILE = os.path.join(_DATA_DIR, "settings.json")
_CHATS_DIR = os.path.join(_DATA_DIR, "chats")


def _ensure_dirs():
    os.makedirs(_CHATS_DIR, exist_ok=True)


def save_settings(settings: dict):
    _ensure_dirs()
    with open(_SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)


def load_settings() -> dict:
    try:
        with open(_SETTINGS_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def list_chats() -> list:
    _ensure_dirs()
    chats = []
    for fname in os.listdir(_CHATS_DIR):
        if fname.endswith(".json"):
            try:
                with open(os.path.join(_CHATS_DIR, fname)) as f:
                    chats.append(json.load(f))
            except Exception:
                pass
    chats.sort(key=lambda c: c.get("updated_at", ""), reverse=True)
    return chats


def save_chat(chat: dict):
    _ensure_dirs()
    chat["updated_at"] = datetime.now().isoformat()
    with open(os.path.join(_CHATS_DIR, f"{chat['id']}.json"), "w") as f:
        json.dump(chat, f, indent=2)


def delete_chat(chat_id: str):
    path = os.path.join(_CHATS_DIR, f"{chat_id}.json")
    if os.path.exists(path):
        os.remove(path)


def new_chat_record() -> dict:
    now = datetime.now()
    return {
        "id": str(uuid.uuid4()),
        "name": now.strftime("Chat \u2013 %b %d, %H:%M"),
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "messages": [],
    }
