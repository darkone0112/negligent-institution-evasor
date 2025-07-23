import os
import sys

def get_config_path():
    """Get the correct path for config.json whether running as script or executable"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = sys._MEIPASS
    else:
        # Running as script
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, 'config.json')
