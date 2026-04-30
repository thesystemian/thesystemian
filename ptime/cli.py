#!/usr/bin/env python3
import subprocess, sys
from pathlib import Path

PROJECT_NAME = "ptime"
SCRIPT_PATH = r"/Users/dax/the-systemian/ptime/cli.py"
PTIME_CMD = "ptime"

def run():
    # 1. Start Tracking
    try:
        subprocess.run([PTIME_CMD, "start", PROJECT_NAME], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except: pass

    # 2. Run Tool
    try:
        ret = subprocess.run(["python3", SCRIPT_PATH] + sys.argv[1:])
        
        # 3. Stop Tracking
        subprocess.run([PTIME_CMD, "stop"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        sys.exit(ret.returncode if ret else 0)
    except KeyboardInterrupt:
        subprocess.run([PTIME_CMD, "stop"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Erreur: Script introuvable : {{SCRIPT_PATH}}")
        sys.exit(1)

if __name__ == "__main__":
    run()
