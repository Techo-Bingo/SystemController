# -*- coding:utf-8-*-
import tkinter as tk
import tkinter.ttk as ttk
class App(ttk.Frame):
    def __init__(self, parent=None, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        # Create Treeview 
        self.tree = ttk.Treeview(self, column=('A','B'), selectmode='none', height=7)
        self.tree.grid(row=0, column=0, sticky='nsew')
        # Setup column heading
        self.tree.heading('#0', text=' Pic directory', anchor='center')
        self.tree.heading('#1', text=' A', anchor='center')
        self.tree.heading('#2', text=' B', anchor='center')
        # #0, #01, #02 denotes the 0, 1st, 2nd columns
        # Setup column
        self.tree.column('A', anchor='center', width=100)
        self.tree.column('B', anchor='center', width=100)
        # Insert image to #0 
        self._img = tk.PhotoImage(file="20190116115007169.gif") #change to your file path
        self.tree.insert('', 'end', text="#0's text", image=self._img,
                         value=("A's value", "B's value"))
 
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('450x180+300+300')
    app = App(root)
    app.grid(row=0, column=0, sticky='nsew')
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.mainloop()
