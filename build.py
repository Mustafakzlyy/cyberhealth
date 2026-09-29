import os
import subprocess
import sys

def build():
    print("🚀 CyberHealth Desktop derleme işlemi başlatılıyor...")

    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name=CyberHealthDesktop",
        "--collect-all=customtkinter",
        "main.py"
    ]

    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Derleme tamamlandı! Çıktı klasörü: dist/CyberHealthDesktop")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Derleme sırasında hata oluştu: {e}")

if __name__ == "__main__":
    build()
