import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def process_image(filepath, thickness=2):
    image = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)

    #alfa kanalı (seffaflık bilgisi) varsa (RGBA bilgisi var) kanaldan bir maske cıkarılır ve seffaf olmayan bolgeler 255 olur
    if image.shape[2] == 4: #görselin rgba olup olmadığının kontrolü
        alpha = image[:, :, 3]
        binary = cv2.threshold(alpha, 1, 255, cv2.THRESH_BINARY)[1] #gorunur piksellere 255(beyaz) atanır
    #alfa kanalı yoksa (RGBA bilgisi yok) gorsel grıye cevrılır,
    # 240 uzeri pikseller terslenip kenarlar bulunur (SIYAH BG BEYAZ FG)
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    #kenardaki bosluklar kapatılarak duzgun kontur elde edilir
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    #en dıştaki çizgiler bulunur (dıs kontur)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #bos seffaf rgba oluturulur
    h, w = binary.shape
    result = np.zeros((h, w, 4), dtype=np.uint8)


    #kucuk gurultuler filtrelenir
    min_area = 5000
    epsilon_ratio = 0.002

    filtered = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

    #filtrelenmiş konturlardan en büyük olanı seçilip düzgün hale getirilir ve thicknessa göre opak çizilir
    if filtered:
        largest = max(filtered, key=cv2.contourArea)
        epsilon = epsilon_ratio * cv2.arcLength(largest, True)
        approx = cv2.approxPolyDP(largest, epsilon, True)
        cv2.drawContours(result, [largest], -1, (0, 0, 0, 255), thickness=thickness)

    #yeni dosya kaydedilir
    out_path = filepath.replace(".png", "_R.png")
    cv2.imwrite(out_path, result)
    return out_path

def select_file():
    global original_path
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if not file_path:
        return

    original_path = file_path

    try:
        img = Image.open(original_path)
        img.thumbnail((400, 400))
        tk_img = ImageTk.PhotoImage(img)

        input_panel.config(image=tk_img)
        input_panel.image = tk_img

    except Exception as e:
        messagebox.showerror("Hata", f"Preview could not be loaded:\n{e}")

def detect_edges():
    if not original_path:
        messagebox.showwarning("Uyarı", "Please select a PNG file first.")
        return

    try:
        thickness = int(thickness_var.get())
        if thickness < 1 or thickness > 20:
            raise ValueError("Enter a value between 1 and 20.")
    except Exception:
        messagebox.showerror("Hata", "Enter a valid thickness (e.g., 2, 5)")
        return

    try:
        result_path = process_image(original_path, thickness)

        img = Image.open(result_path)
        img.thumbnail((400, 400))
        tk_img = ImageTk.PhotoImage(img)

        output_panel.config(image=tk_img)
        output_panel.image = tk_img

        messagebox.showinfo("Okay", f"Processed image has been saved:\n{result_path}")

    except Exception as e:
        messagebox.showerror("Hata", f"Processing failed:\n{e}")

#region Interface
root = tk.Tk()
root.title("Edge Detector App")
root.geometry("850x600")
root.configure(bg="#dcdcdc")

# Üst: Dosya seç + kalınlık + buton
top_frame = tk.Frame(root, bg="#dcdcdc")
top_frame.pack(pady=10)

btn = tk.Button(top_frame, text="📁 Choose a PNG File", command=select_file, font=("Segoe UI", 12), bg="#4CAF50", fg="white")
btn.pack(side="left", padx=10)

tk.Label(top_frame, text="Thickness:", font=("Segoe UI", 11), bg="#dcdcdc").pack(side="left", padx=5)
thickness_var = tk.StringVar(value="2")
thickness_entry = tk.Entry(top_frame, textvariable=thickness_var, width=5, font=("Segoe UI", 11))
thickness_entry.pack(side="left", padx=5)

detect_button = tk.Button(top_frame, text="🧠 Detect Edge", command=detect_edges, font=("Segoe UI", 12), bg="#2196F3", fg="white")
detect_button.pack(side="left", padx=10)

frame = tk.Frame(root, bg="#dcdcdc")
frame.pack(pady=10)

input_panel = tk.Label(frame, text="Original Image", bg="#dcdcdc", width=400, height=400)
input_panel.pack(side="left", padx=10)

output_panel = tk.Label(frame, text="Processed Image", bg="#dcdcdc", width=400, height=400)
output_panel.pack(side="right", padx=10)

original_path = None

#endregion
root.mainloop()
