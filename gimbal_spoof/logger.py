# logger.py

import os
import time
import json
from datetime import datetime

# --- Configurable ---
INTERFACE_NAME = "hci0"
DEVICE_ADDRESS = None
LOG_DIR = os.path.expanduser("~/gatt_logs")
os.makedirs(LOG_DIR, exist_ok=True)

timestamp_str = datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S')
LOG_PATH = os.path.join(LOG_DIR, f"ble_log_{timestamp_str}.jsonl")

# --- ANSI colors ---
COLOR_MAP = {
    "READ": "\033[94m",            # Blue
    "WRITE": "\033[92m",           # Green
    "START_NOTIFY": "\033[93m",    # Yellow
    "STOP_NOTIFY": "\033[93m",
    "CCCD_WRITE": "\033[93m",
    "START_INDICATE": "\033[95m",  # Purple
    "STOP_INDICATE": "\033[95m",
}
RESET = "\033[0m"

def set_device_address(mac: str):
    global DEVICE_ADDRESS
    DEVICE_ADDRESS = mac

def log_event(event_type, uuid, path, payload=b''):
    ns = time.time_ns()
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(ns // 1_000_000_000)) + f".{ns % 1_000_000_000:09d}Z"

    event = {
        "timestamp": timestamp,
        "event": event_type,
        "uuid": uuid,
        "path": path,
        "payload_hex": payload.hex(),
        "payload_utf8": payload.decode('utf-8', errors='replace'),
        "interface": INTERFACE_NAME,
        "device_address": DEVICE_ADDRESS,
    }

    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")

    # --- Color console output ---
    color = COLOR_MAP.get(event_type, "\033[91m")  # Red fallback for unknown
    print(f"{color}[{timestamp}] {event_type} - UUID: {uuid} - PATH: {path}{RESET}")
    if payload:
        print(f"{color}           └─ TEXT: {payload.decode('utf-8', errors='replace')}{RESET}")
