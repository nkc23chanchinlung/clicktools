import tkinter as tk
from tkinter import filedialog
import threading
import time
import random
import pyautogui

tasks = []  # (path, seconds)
running = False

# 画像追加
def add_image():
    path = filedialog.askopenfilename()
    if path:
        try:
            sec = float(entry.get())
        except:
            sec = 1

        tasks.append((path, sec))
        listbox.insert(tk.END, f"{path.split('/')[-1]} : {sec}s")

# 削除
def delete_selected():
    selected = listbox.curselection()
    if not selected:
        return
    index = selected[0]
    listbox.delete(index)
    tasks.pop(index)

# 開始
def start():
    global running
    if running:
        return
    running = True
    threading.Thread(target=run).start()

# 停止
def stop():
    global running
    running = False

# 画像検索（リトライ付き）
def find_image(path, tries=5):
    for _ in range(tries):
        pos = pyautogui.locateCenterOnScreen(path, confidence=0.7)
        if pos:
            return pos
        time.sleep(0.5)
    return None

# 実行処理
def run():
    global running

    while running:
        for path, sec in tasks:
            if not running:
                break

            # 時間ランダムズレ
            delay = sec + random.uniform(-0.5, 0.5)
            time.sleep(max(0, delay))

            print(f"{path} 探索中...")

            pos = find_image(path)

            if pos:
                # 位置ランダムズレ
                x = pos.x + random.randint(-5, 5)
                y = pos.y + random.randint(-5, 5)

                pyautogui.moveTo(x, y, duration=random.uniform(0.1, 0.3))
                pyautogui.click()
                print("クリック成功")
            else:
                print("見つからない")

        if not loop_var.get():
            break

    running = False

# GUI
root = tk.Tk()
root.title("完成版クリックツール")

entry = tk.Entry(root)
entry.insert(0, "2")
entry.pack()

btn_add = tk.Button(root, text="画像追加", command=add_image)
btn_add.pack()

btn_delete = tk.Button(root, text="削除", command=delete_selected)
btn_delete.pack()

listbox = tk.Listbox(root, width=50)
listbox.pack()

loop_var = tk.BooleanVar()
loop_check = tk.Checkbutton(root, text="ループ", variable=loop_var)
loop_check.pack()

btn_start = tk.Button(root, text="開始", command=start)
btn_start.pack()

btn_stop = tk.Button(root, text="停止", command=stop)
btn_stop.pack()

root.mainloop()