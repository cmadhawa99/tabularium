import json
import os

SETTINGS_FILE = "config.json"

# Default Settings (if no file exists)
DEFAULTS = {
    "general": {
        "language": "English",
        "theme": "dark",
        "page_size": 50
    },
    "backup": {
        "auto_backup": False,
        "backup_path": os.path.expanduser("~/Documents/ArchiveBackups")
    },
    "master_data": {
        "sectors": ["Land Division", "Accounts", "Administration", "Planning", "Samurdhi"],
        "subjects": ["L-01", "L-02", "AC-55", "AD-10", "PL-99"],
        "file_types": ["Normal", "Special (විශේෂ)", "Confidential"]
    }
}

class SettingsManager:
    def __init__(self):
        self.settings = self.load_settings()

    def load_settings(self):
        if not os.path.exists(SETTINGS_FILE):
            return DEFAULTS
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except:
            return DEFAULTS

    def save_settings(self):
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get(self, category, key):
        return self.settings.get(category, {}).get(key, DEFAULTS[category][key])

    def set(self, category, key, value):
        if category not in self.settings:
            self.settings[category] = {}
        self.settings[category][key] = value
        self.save_settings()

# Create a singleton instance
settings = SettingsManager()