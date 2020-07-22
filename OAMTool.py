# -*- coding: UTF-8 -*-

from my_view import Gui
from my_util import Init


def start():
    gui = Gui()

    """ 环境核查并初始化 """
    if not Init.init():
        return

    gui.pack()

    gui.mainloop()


if __name__ == '__main__':
    start()
