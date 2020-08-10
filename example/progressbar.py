import time
import threading
from tkinter import *


class MyProgressBar(object):
    def __init__(self, master, width, height):
        self.canvas_bar = None
        self.canvas_shape = None
        self.canvas_text = None
        self.width = width
        self.height = height
        self.pack_frame(master)

    def pack_frame(self, master):
        self.canvas_bar = Canvas(master, width=self.width, height=self.height, bg='black')
        self.canvas_shape = self.canvas_bar.create_rectangle(0, 0, 0, self.height, fill='Green')
        self.canvas_text = self.canvas_bar.create_text(self.width/2, self.height/2+2, text='0%')
        self.canvas_bar.pack()

    def update(self, percent, change_color=False):
        prog_len = int(self.width * percent / 100) + 1
        color = 'Green'
        if change_color:
            if 60 <= percent < 70:
                color = 'Gold'
            elif 70 <= percent < 80:
                color = 'Coral'
            elif 80 <= percent < 90:
                color = 'OrangeRed'
            elif 90 <= percent <= 100:
                color = 'Red3'
        self.canvas_bar.coords(self.canvas_shape, (0, 0, prog_len, self.height+2))
        self.canvas_bar.itemconfig(self.canvas_text, text='%d%%' % percent)
        self.canvas_bar.itemconfig(self.canvas_shape, fill=color, outline=color)


def update_progress_bar():
    for percent in range(1, 101):
        #hour = int(percent/3600)
        #minute = int(percent/60) - hour*60
        #second = percent % 60
        #green_length = int(width * percent / 100)
        #canvas_progress_bar.coords(canvas_shape, (0, 0, green_length, 25))
        #canvas_progress_bar.itemconfig(canvas_text, text='%02d:%02d:%02d' % (hour, minute, second))
        #var_progress_bar_percent.set('%0.2f  %%' % percent)
        time.sleep(0.2)
        mybar.update(percent)



def run():
    th = threading.Thread(target=update_progress_bar)
    th.setDaemon(True)
    th.start()


top = Tk()
top.title('Progress Bar')
top.geometry('500x500+290+100')
top.resizable(False, False)
top.config(bg='#535353')

'''
# 进度条
width = 200
height = 16
canvas_progress_bar = Canvas(top, width=width, height=height)
canvas_shape = canvas_progress_bar.create_rectangle(0, 0, 0, 25, fill='green')
canvas_text = canvas_progress_bar.create_text(width/2, height/2)
canvas_progress_bar.itemconfig(canvas_text, text='00:00:00')
var_progress_bar_percent = StringVar()
var_progress_bar_percent.set('00.00  %')
label_progress_bar_percent = Label(top, textvariable=var_progress_bar_percent, fg='#F5F5F5', bg='#535353')
canvas_progress_bar.place(relx=0.45, rely=0.4, anchor=CENTER)
label_progress_bar_percent.place(relx=0.89, rely=0.4, anchor=CENTER)
'''
Label(top).pack()
mybar = MyProgressBar(top, 200, 18)

# 按钮
button_start = Button(top, text='开始', fg='#F5F5F5', bg='#7A7A7A', command=run, height=1, width=15, relief=GROOVE, bd=2, activebackground='#F5F5F5', activeforeground='#535353')
button_start.place(relx=0.45, rely=0.5, anchor=CENTER)

top.mainloop()

