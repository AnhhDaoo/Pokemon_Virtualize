import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import tkinter as tk
from tkinter import ttk, messagebox

# Đường dẫn đến thư mục chứa hình ảnh
data2_path = "data/images/"

def display_first_10_images():
    # Lấy danh sách tất cả các tệp hình ảnh trong thư mục
    image_files = [f for f in os.listdir(data2_path) if os.path.isfile(os.path.join(data2_path, f))]
    
    # Sắp xếp danh sách theo thứ tự bảng chữ cái
    image_files.sort()
    
    # Chọn 10 tệp đầu tiên từ danh sách đã sắp xếp
    first_10_images = image_files[:10]
    
    # Hiển thị 10 bức ảnh đó
    fig, axes = plt.subplots(2, 5, figsize=(12, 4))
    axes = axes.flatten()
    
    for ax, image_file in zip(axes, first_10_images):
        image_path = os.path.join(data2_path, image_file)
        image = Image.open(image_path)
        ax.imshow(image)
        ax.axis('off')
        ax.set_title(os.path.splitext(image_file)[0], fontsize=10)
    
    plt.tight_layout()
    plt.show()

# Tạo giao diện Tkinter
def show_images():
    display_first_10_images()

root = tk.Tk()
root.title("Hiển thị 10 bức ảnh đầu tiên")

frame = ttk.Frame(root, padding="50")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

button = ttk.Button(frame, text="Hiển thị 10 bức ảnh đầu tiên", command=show_images)
button.grid(row=0, column=0, padx=50, pady=50)

root.mainloop()
