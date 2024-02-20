import tkinter as tk
import ttkbootstrap as ttk

def say_hello():
    print("Hello!")

root = tk.Tk()
root.geometry("200x100")

# 创建一个PhotoImage对象来加载图标
icon = tk.PhotoImage(file="./floodfill.gif")

menubutton = ttk.Menubutton(root, text="", image=icon, compound="left")
menu = tk.Menu(menubutton, tearoff=False)

# 添加带图标的菜单项
menu.add_command(label="", command=say_hello, image=icon, compound="left", activebackground="white")
menu.add_command(label="", command=say_hello, image=icon, compound="left", activebackground="white")
menu.add_separator()
menu.add_command(label="", command=root.quit, image=icon, compound="left", activebackground="white")

menubutton.config(menu=menu)
menubutton.pack()

root.mainloop()
