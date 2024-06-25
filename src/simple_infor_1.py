# tạo giao diện người dùng hiển thị thông tin pokemon

import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import pandas as pd
import tkinter.messagebox as messagebox

# Đọc data1
data1 = pd.read_csv("data/pokemon_data.csv")

# Hàm tra cứu thông tin Pokemon theo ID hoặc tên
def search_pokemon():
    query = search_entry.get().lower()  # Chuyển đổi query thành chữ thường để so sánh
    try:
        # Tra cứu thông tin từ data1 dựa trên ID hoặc tên
        if query.isdigit():  # Nếu query là số, tìm theo ID
            pokemon_info = data1.loc[int(query)]
        else:  # Nếu không, tìm theo tên
            pokemon_info = data1[data1['NAME'].str.lower() == query]
        
        # Chuyển đổi dữ liệu thành cột ngang trước khi hiển thị thông tin
        pokemon_info_transposed = pokemon_info.to_frame().transpose()

        # Hiển thị thông tin Pokemon
        messagebox.showinfo("Pokemon Info", pokemon_info_transposed.to_string(index=False))  # Hiển thị thông tin dưới dạng text
    except:
        messagebox.showerror("Error", "Pokemon not found")


# Tạo một từ điển ánh xạ từ ID của Pokemon thành tên của ảnh
id_to_image_name = {}
for index, row in data1.iterrows():
    id_to_image_name[row['ID']] = row['NAME'].lower() + '.png'



# Hàm hiển thị hình ảnh Pokemon
def show_pokemon_image():
    try:
        # Đọc ID hoặc tên Pokemon từ ô nhập liệu
        query = search_entry.get().lower()
        if query.isdigit():  # Nếu query là số, tìm theo ID
            pokemon_id = int(query)
            image_name = id_to_image_name.get(pokemon_id)
        else:  # Nếu không, tìm theo tên
            image_name = query + '.png'

        # Đường dẫn đến hình ảnh Pokemon
        image_path = "images/{image_name}"  # Tên ảnh được lưu trong thư mục images

        # Mở và hiển thị hình ảnh
        img = Image.open(image_path)
        img = img.resize((200, 200), Image.ANTIALIAS)  # Resize hình ảnh để hiển thị trong giao diện
        img = ImageTk.PhotoImage(img)

        # Hiển thị thông tin và hình ảnh Pokemon trong cùng một hộp thoại
        pokemon_info = search_pokemon(query)  # Lấy thông tin Pokemon
        messagebox.showinfo("Pokemon Info", pokemon_info, image=img)  # Hiển thị thông tin và hình ảnh

    except:
        messagebox.showerror("Error", "Image not found")


# Tạo cửa sổ
root = tk.Tk()
root.title("Pokemon Viewer")

# Điều chỉnh kích thước cửa sổ
root.geometry("800x600")  # kích thước là pixel

# Tạo và định vị các widget
search_label = tk.Label(root, text="Enter Pokemon ID or Name:")
search_label.pack()
search_entry = tk.Entry(root)
search_entry.pack()

search_button = tk.Button(root, text="Search", command=search_pokemon)
search_button.pack()

image_label = tk.Label(root)
image_label.pack()

show_image_button = tk.Button(root, text="Show Pokemon Image", command=show_pokemon_image)
show_image_button.pack()

# Chạy ứng dụng
root.mainloop()