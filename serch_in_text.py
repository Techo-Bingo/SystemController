"""Search in text."""


from tklib import *

str = """Up until now, we've just dealt with plain text. 
Now it's time to look at how to add special formatting, such as bold, italic, 
strikethrough, background colors, font sizes, and-libin much more. Tk's text widget 
implements these using a feature called tags.
"""


def highlight():
    sel = App.text.tag_ranges('sel')
    if len(sel) > 0:
        App.text.tag_add('highlight', *sel)


def search(a=None, event=None):
    App.text.tag_remove("highlight", "1.0", "end")
    start = 1.0
    while True:
        pattern = App.re.get()
        pos = App.text.search(pattern, start, stopindex='end', regexp=True)
        if not pos:
            break
        print(pos)
        end = '%s.%s'%(pos.split('.')[0], len(pattern) + int(pos.split('.')[1]))
        App.text.tag_add('highlight', pos, end)
        start = pos + '+1c'


class Demo(App):
    def __init__(self):
        super().__init__()
        Label("Search with regexp", font="Arial 18")

        App.text = Text(str, height=10, width=50)
        App.text.tag_configure('highlight', background='red')

        App.re = Entry('search', search)


Demo().run()
