import os
import shutil
import threading
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

# Dosya kategorileri ve uzantılar
EXTENSIONS = {
    "Resimler": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"],
    "Belgeler": [".pdf", ".docx", ".doc", ".xlsx", ".pptx", ".txt"],
    "Videolar": [".mp4", ".mkv", ".mov", ".avi"],
    "Müzikler": [".mp3", ".wav", ".flac"],
    "Arşivler": [".zip", ".rar", ".7z", ".tar"],
    "Kurulumlar": [".exe", ".msi"],
    "Minecraft Modları": [".jar"],
}


def clean_downloads():
    # Butonu işlem bitene kadar devre dışı bırak
    btn_clean.config(state="disabled", text="Düzenleniyor...")
    status_label.config(text="Dosyalar taranıyor ve taşınıyor...", fg="#f39c12")
    root.update()

    downloads_path = Path.home() / "Downloads"

    if not downloads_path.exists():
        messagebox.showerror("Hata", "İndirilenler klasörü bulunamadı!")
        btn_clean.config(state="normal", text="İndirilenleri Temizle 🚀")
        return

    moved_count = 0

    for item in downloads_path.iterdir():
        if item.is_file():
            # Kendi exe dosyamızı veya scripti taşımayalım
            if item.name.startswith("script1") or item.name.startswith(
                "DownloadCleaner"
            ):
                continue

            file_ext = item.suffix.lower()
            target_folder_name = "Diğer"

            for folder_name, ext_list in EXTENSIONS.items():
                if file_ext in ext_list:
                    target_folder_name = folder_name
                    break

            target_folder = downloads_path / target_folder_name
            target_folder.mkdir(exist_ok=True)

            try:
                shutil.move(str(item), str(target_folder / item.name))
                moved_count += 1
            except Exception as e:
                print(f"Hata ({item.name}): {e}")

    # İşlem tamamlandığında arayüzü güncelle
    status_label.config(
        text=f"Tamamlandı! Toplam {moved_count} dosya düzenlendi.", fg="#2ecc71"
    )
    btn_clean.config(state="normal", text="İndirilenleri Temizle 🚀")
    messagebox.showinfo(
        "Başarılı", f"İndirilenler temizlendi!\n{moved_count} dosya taşındı."
    )


def start_cleaning_thread():
    # Arayüz donmasın diye işlemi arkada çalıştırır
    threading.Thread(target=clean_downloads, daemon=True).start()


# --- Pencere Tasarımı ---
root = tk.Tk()
root.title("Download Cleaner")
root.geometry("400x260")
root.resizable(False, False)
root.configure(bg="#1e1e2e")

# Başlık
title_label = tk.Label(
    root,
    text="📁 Download Cleaner",
    font=("Segoe UI", 16, "bold"),
    fg="#cdd6f4",
    bg="#1e1e2e",
)
title_label.pack(pady=(25, 5))

desc_label = tk.Label(
    root,
    text="İndirilenler klasörünü tek tıkla kategorilere ayırır.",
    font=("Segoe UI", 9),
    fg="#a6adc8",
    bg="#1e1e2e",
)
desc_label.pack(pady=(0, 20))

# Temizleme Butonu
btn_clean = tk.Button(
    root,
    text="İndirilenleri Temizle 🚀",
    font=("Segoe UI", 11, "bold"),
    bg="#89b4fa",
    fg="#11111b",
    activebackground="#b4befe",
    relief="flat",
    padx=15,
    pady=8,
    cursor="hand2",
    command=start_cleaning_thread,
)
btn_clean.pack(pady=10)

# Durum Yazısı
status_label = tk.Label(
    root, text="Hazır", font=("Segoe UI", 9), fg="#a6adc8", bg="#1e1e2e"
)
status_label.pack(pady=(15, 0))

root.mainloop()
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
