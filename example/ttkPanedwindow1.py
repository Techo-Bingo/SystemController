import tkinter as tk
from tkinter import ttk, scrolledtext


root = tk.Tk()

# 添加水平方向（HORIZONTAL）的推拉窗组件
# paned_win_h = ttk.Panedwindow(root, orient=tk.HORIZONTAL)
# 添加垂直方向（VERTICAL）的推拉窗组件
paned_win_v = ttk.Panedwindow(root, orient=tk.VERTICAL)
# paned_win_h.grid(row=0, column=0, sticky=tk.NSEW)
paned_win_v.grid(row=1, column=0, sticky=tk.NSEW)
a = scrolledtext.ScrolledText(paned_win_v,
                          bd=2,
                          relief='ridge',
                          height=10,
                          width=100)
a.pack()
b = scrolledtext.ScrolledText(paned_win_v,
                          bd=2,
                          relief='ridge',
                          height=10,
                          width=100)
b.pack()
# 往推拉窗中添加text组件，并设置权重
paned_win_v.add(a, weight=2)
paned_win_v.add(b, weight=1)
root.mainloop()
