import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from PIL import Image
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Đường dẫn đến các tệp dữ liệu
data1_path = "data/pokemon_data.csv"
data2_path = "data/images/"

# Đọc dữ liệu từ file CSV vào DataFrame
data1 = pd.read_csv(data1_path)

def display_pokemon_info(pokemon_name_or_id):
    # Kiểm tra xem pokemon_name_or_id có phải là một số hay không
    if pokemon_name_or_id.isdigit():
        # Nếu là số, tìm trong cột 'ID'
        pokemon_info = data1[data1['ID'] == int(pokemon_name_or_id)]
    else:
        # Nếu không phải là số, tìm trong cột 'NAME'
        pokemon_info = data1[data1['NAME'].str.lower() == pokemon_name_or_id.lower()]
    
    if pokemon_info.empty:
        messagebox.showerror("Lỗi", "Không tìm thấy thông tin cho Pokemon này.")
        return
    
    pokemon_info = pokemon_info.iloc[0]  # Chọn hàng đầu tiên nếu có nhiều hơn một kết quả
    
    # Hiển thị hình ảnh của Pokemon và radar chart
    image_path = os.path.join(data2_path, f"{pokemon_info['NAME'].lower()}.png")
    
    stats_labels = ['HP', 'ATTACK', 'DEFENSE', 'SP.ATK', 'SP.DEF', 'SPEED']
    stats_values = [pokemon_info[label] for label in stats_labels]
    
    angles = np.linspace(0, 2 * np.pi, len(stats_labels), endpoint=False).tolist()
    stats_values += stats_values[:1]
    angles += angles[:1]
    
    fig = plt.figure(figsize=(12, 6))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])

    if os.path.exists(image_path):
        pokemon_image = Image.open(image_path)
        pokemon_image = pokemon_image.resize((400, 400))  # Điều chỉnh kích thước hình ảnh
        ax0 = plt.subplot(gs[0])
        ax0.imshow(pokemon_image)
        ax0.axis('off')
    else:
        messagebox.showerror("Lỗi", "Không tìm thấy hình ảnh cho Pokemon này.")
    
    ax1 = plt.subplot(gs[1], polar=True)
    ax1.fill(angles, stats_values, color='red', alpha=0.25)
    ax1.set_yticklabels([])
    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(stats_labels)
    
    for angle, value, label in zip(angles, stats_values, stats_labels):
        ax1.text(angle, value + 1, f'{value}', horizontalalignment='center', size=10, color='red', weight='semibold')
    
    plt.title(f"Các chỉ số chiến đấu của {pokemon_info['NAME']}", size=15, color='red', y=1.1)
    plt.show()
    
    # Hiển thị evolution chart
    pre_evo = pokemon_info['PRE.EVO']
    post_evo = pokemon_info['POST.EVO']
    
    evolution_chain = []
    
    # Tìm pre.evo của Pokemon
    if not pd.isna(pre_evo) and pre_evo != "":
        evolution_chain.append(pre_evo)
    else:
        # Nếu không có pre.evo, tìm post.evo của pokemon trong data1
        post_evo_pokemon = data1[data1['POST.EVO'] == pokemon_info['NAME']]
        if not post_evo_pokemon.empty:
            evolution_chain.append(post_evo_pokemon.iloc[0]['NAME'])
    
    # Thêm Pokemon hiện tại
    evolution_chain.append(pokemon_info['NAME'])
    
    # Tìm post.evo của Pokemon (nếu có)
    if not pd.isna(post_evo) and post_evo != "":
        evolution_chain.append(post_evo)
    
    if evolution_chain:
        fig, ax = plt.subplots(1, len(evolution_chain), figsize=(12, 4))
        for i, pokemon_name in enumerate(evolution_chain):
            evolution_image_path = os.path.join(data2_path, f"{pokemon_name.lower()}.png")
            if os.path.exists(evolution_image_path):
                evolution_image = Image.open(evolution_image_path)
                evolution_image = evolution_image.resize((150, 150))  # Điều chỉnh kích thước hình ảnh
                ax[i].imshow(evolution_image)
                ax[i].axis('off')
                ax[i].set_title(pokemon_name, size=10)
            else:
                messagebox.showerror("Lỗi", f"Không tìm thấy hình ảnh cho {pokemon_name}.")
        plt.show()

# Tạo giao diện Tkinter
def search_pokemon():
    pokemon_name_or_id = entry.get()
    if pokemon_name_or_id:
        display_pokemon_info(pokemon_name_or_id)
    else:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên hoặc ID của Pokemon.")


root = tk.Tk()
root.title("Thông tin Pokemon")

# Đặt kích thước cửa sổ
root.geometry("800x400")

frame = ttk.Frame(root, padding="40")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Điều chỉnh các thuộc tính của label
label = ttk.Label(frame, text="Nhập tên hoặc ID của Pokemon:", font=("Helvetica", 12))
label.grid(row=0, column=0, padx=20, pady=20)

# Điều chỉnh các thuộc tính của entry
entry = ttk.Entry(frame, width=30, font=("Helvetica", 12))
entry.grid(row=0, column=1, padx=20, pady=20)

# Điều chỉnh các thuộc tính của button
button = ttk.Button(frame, text="Tìm kiếm", command=search_pokemon, width=20)
button.grid(row=0, column=2, padx=20, pady=20)

root.mainloop()