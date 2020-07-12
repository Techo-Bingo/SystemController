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

# 设置窗口宽高固定
window.resizable(0, 0)
 
# 定义列的名称
tree = ttk.Treeview(window, show = "tree")
_img = tk.PhotoImage(file="..\\image\\oam.png")
myid=tree.insert('','end',text="中国China",image=_img,tags=('ttk1s', 'simple'))  # ""表示父节点是根
tree.tag_configure('ttk1s', foreground='yellow', font=('黑体', 12, 'bold'))
myidx1=tree.insert(myid,'end',"广东",text="中国广东",values=("2"))  # text表示显示出的文本，values是隐藏的值
myidx2=tree.insert(myid,'end',"江苏",text="中国江苏",values=("3"))
myidx3=tree.insert(myid,'end',"aaa",text="中国aa",values=("3"))
myidy=tree.insert('','end',"美国",text="美国USA",values=("4"))
myidy1=tree.insert(myidy,'end',"加州",text="美国加州",values=("5"))

#tree.tag_bind('font_1', 'aa_1')
# 鼠标选中一行回调
def selectTree(event):
    for item in tree.selection():
        item_text = tree.item(item, "values")
        print(item_text)
     
# 选中行
tree.bind('<<TreeviewSelect>>', selectTree)
 
tree.pack(expand = True, fill = tk.BOTH)
 
window.mainloop()