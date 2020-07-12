# -*- coding:utf-8-*-
import tkinter as tk
import tkinter.ttk as ttk
class App(ttk.Frame):
    def __init__(self,parent=None, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        # Create Treeview 
        self.tree = ttk.Treeview(self,column=('A','B'),selectmode='none',height=7)
        self.tree.grid(row=0, column=0, sticky='nsew')
        # Setup column heading
        self.tree.heading('#0',text=' Pic directory',anchor='center')
        self.tree.heading('#1', text=' A',anchor='center')
        self.tree.heading('#2', text=' B', anchor='center')
        # Setup column
        self.tree.column('A', anchor='center', width=100)
        self.tree.column('B', anchor='center', width=100)
        # Insert image to #0 
        #self._img = tk.PhotoImage(file="timg.gif") #change to your file path
        #self.tree.insert('', 'end', text="#0's text", image=self._img, value=("A's value", "B's value"))

def test1():
    dict1 = {'ViewText': '操作维护', 'PageName': 'NA', 'PageType': 'NA', 'Shell': 'NA', 'SubTree': [{'ViewText': '快速日志采集', 'PageName': 'QuickLogPage', 'PageType': ['OPTION_DOWNLOAD', ['PLT进程日志', 'MDC进程日志', 'UDC进程日志', '系统相关日志']], 'Shell': 'collect_quick_logs.sh', 'SubTree': []}, {'ViewText': '时区夏令时配置', 'PageName': 'TimezonePage', 'PageType': ['SELF'], 'Shell': 'set_timezone.sh', 'SubTree': []}]}

    print(dict1['ViewText'])
    print(isinstance(dict1, dict))
    import time
    _now = time.time()
    print(_now)
    aa='OPTION_DOWNLOAD'
    aa = aa.replace('\\{', '(').replace('\\}', ')').replace('{', '').replace('}', '').replace(',', '')
    a, b = aa.split()[0], aa.split()[1:]
    print(a, b)
    print(time.time())


if __name__ == '__main__':
    test1()
    root = tk.Tk()
    root.geometry('450x180+300+300')
    app = App(root)
    app.grid(row=0, column=0, sticky='nsew')
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.mainloop()
