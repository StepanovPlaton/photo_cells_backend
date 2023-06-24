import os
from pathlib import Path
from typing import TypedDict
from dotenv import load_dotenv # type: ignore

class EnvSettings(TypedDict):
    GALLERY_DATABASE_URL: str
    GALLERY_ADMIN_PASSWORD: str
    GALLERY_PREVIEW_TARGET_SIZE: int

class EnvClass:
    def __init__(self):
        self.env: EnvSettings = {
            "GALLERY_DATABASE_URL": "sqlite:///./database.db",
            "GALLERY_ADMIN_PASSWORD": "password",
            "GALLERY_PREVIEW_TARGET_SIZE": 921600,
        }

        if (Path().parent / '.env').exists():
            load_dotenv(Path().parent / '.env')

        current_env = dict(os.environ.items())
        for key in self.env.keys():
            if(key in current_env.keys()):
                try:
                    self.env[key] = int(current_env[key])
                except:
                    self.env[key] = current_env[key]
            else:
                print(f'{key} didn\'t find in environment. Use default value - {self.env[key]}')
        
