# 🕷️ SPYSTEALER - Advanced Modular Stealer & Crypter Toolkit

![SPYSTEALER Banner](https://img.shields.io/badge/status-active-success?style=flat-square)

---

## 🚀 About

**SPYSTEALER** is a full-featured modular information stealer combined with an optional crypter for enhanced stealth.  
Designed for red teamers, penetration testers, or educational research.

SPYSTEALER can:
- Build a highly modular and customizable **stealer executable**.
- **Crypt** and **pack** any `.exe` into a FUD (Fully Undetectable) executable.
- Automatically **upload stolen data** to your **Discord webhook**.

---

## 🛠️ Features

### 💻 Stealer Core (`stub.py`)

- **System Recon**: Collect PC name, username, OS info, local and external IP, ISP, location.
- **Browser Theft**:
  - Passwords
  - Cookies
  - Credit cards
  - Autofill forms
  - Browser extensions
  - Browser sessions
- **Files & Documents Theft**:
  - DOC, DOCX, PDF, TXT files from Desktop
- **Credential Dumpers**:
  - Windows Credential Manager (cmdkey /list)
  - FileZilla saved credentials
- **Network Theft**:
  - Wi-Fi BSSID + basic geolocation
- **Screenshots & Webcam Spy**:
  - Take a live screenshot
  - Capture webcam image
- **Browser Master Key Dump**:
  - Extract Chrome-based browser master decryption keys
- **Silent UAC Bypass**:
  - Attempt privilege escalation using `fodhelper.exe`
- **Automatic Zipping + Upload**:
  - Collect all stolen files
  - Zip and send them to your Discord webhook instantly

---

### 🛡️ Crypter Core (`crypter.py`)

- **Payload Encryption**:
  - XOR encrypt your `.exe` payload with random keys
- **Loader Obfuscation**:
  - Randomize import names
  - Insert junk functions
  - VM detection + sandbox evasion (basic)
- **Memory Execution**:
  - Executes the decrypted payload **directly in memory**
- **Automatic Packing**:
  - Optional UPX ultra-brute compression
- **Automatic Compilation**:
  - From Python → Onefile Windows executable
- **Self-Cleaning**:
  - Deletes temporary `.spec`, build folders, and intermediate files

---

## 📦 Setup Instructions

> **Recommended Python Version:**  
> `Python 3.10 - 3.12` (Windows)

### Install Requirements:

```bash
pip install -r requirements.txt
```
or manually:
```bash
pip install pyinstaller psutil pillow pycryptodome requests pyperclip opencv-python
```

---

## 📋 Usage

### Step 1: Inject Your Webhook

```bash
python spystealer.py
```
- Select `1️⃣` Inject Webhook
- Enter your **Discord Webhook URL**

---

### Step 2: Build Stealer EXE

- Select `2️⃣` Build Stub
- Name your output EXE
- (Optional) Add an `.ico` file for legit look
- Stealer `.exe` will be generated inside `/build/`

---

### Step 3: Crypt Payload (Optional but Recommended)

- Select `3️⃣` Stub Crypter
- Provide the path to the stub `.exe`
- Enter a new name for your **final FUD executable**

Result:  
- New crypted `.exe` inside `/build_output/`

---

## 🔥 Example Terminal Preview

```
[ + ] Developed by AnonSpyDir

[ 🔗 ] Webhook Status: Injected ✅

[ 1️⃣ ] Inject Webhook
[ 2️⃣ ] Build Stub (.exe only)
[ 3️⃣ ] Stub Cryptor (FUD a .exe)
[ 4️⃣ ] Exit
```

---

## ⚙️ Example Commands Behind the Scenes

- Building Stealer:
  ```bash
  pyinstaller --onefile --noconsole --icon=myicon.ico stub.py
  ```

- Building Crypted Payload:
  ```bash
  pyinstaller --onefile --noconsole loader_payload.py
  upx --ultra-brute dist/loader_payload.exe
  ```

---

## ❗ Disclaimer

> This project is strictly for **educational** and **authorized penetration testing** use only.  
>  
> I am **NOT responsible** for any misuse, damage, or illegal activities caused by this software.  
>  
> Always ensure you have **explicit permission** before running this software on any machine.

---

## 👨‍💻 Credits

- Developed by [AnonSpyDir] 🕷️
- Thanks to Open Source Communities
- Inspired by modern stealth techniques

---

# 🕷️ Stay stealthy. Stay smart.  
# **SPYSTEALER - Tactical Recon at its Finest**
