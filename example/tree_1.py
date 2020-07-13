import tkinter as tk
from tkinter import ttk
 
window = tk.Tk()
# 设置窗口大小
winWidth = 600
winHeight = 400
# 获取屏幕分辨率
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()
 
x = int((screenWidth - winWidth) / 2)
y = int((screenHeight - winHeight) / 2)
 
# 设置主窗口标题
window.title("TreeView参数说明")
# 设置窗口初始位置在屏幕居中
window.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
# 设置窗口图标
# window.iconbitmap("./image/icon.ico")
# 设置窗口宽高固定
window.resizable(0, 0)
 
# 定义列的名称
columns = ("name", "gender", "age")
tree = ttk.Treeview(window, show = "headings", columns = columns, selectmode = tk.BROWSE)
 
# 设置表格文字居中
tree.column("name", anchor = "center")
tree.column("gender", anchor = "center")
tree.column("age", anchor = "center")
 
# 设置表格头部标题
tree.heading("name", text = "姓名")
tree.heading("gender", text = "性别")
tree.heading("age", text = "年龄")
 
# 设置表格内容
lists = [{"name": "yang", "gender": "男", "age": "18"}, {"name": "郑", "gender": "女", "age": "25"}]
i = 0
for v in lists:
    tree.insert('', i, values = (v.get("name"), v.get("gender"), v.get("age")))
    i += 1
 
tree.pack(expand = True, fill = tk.BOTH)
 
 
# 获取当前点击行的值
def treeviewClick(event):  # 单击
    for item in tree.selection():
        item_text = tree.item(item, "values")
        print(item_text)
 
# 鼠标左键抬起
tree.bind('<ButtonRelease-1>', treeviewClick)
 
# 鼠标选中一行回调
def selectTree(event):
    for item in tree.selection():
        item_text = tree.item(item, "values")
        print(item_text)
     
# 选中行
#tree.bind('<<TreeviewSelect>>', selectTree)
 
window.mainloop()