import os
import importlib

def load_modules_from_folder(folder):
    for filename in os.listdir(folder):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            importlib.import_module(f"{folder}.{module_name}")
