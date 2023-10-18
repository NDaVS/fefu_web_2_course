import socket
from tkinter import *
from PIL import Image
from NumberRecognizer import *


def save_as_png(canvas, file_name):
    canvas.postscript(file=file_name + '.ps')
    Image.open(file_name + '.ps').save(file_name + '.png', 'png')


class Server:
    def __init__(self):
        self.num = None
        self.address = None
        self.connection = None
        self.server = None
        self.screen = None
        self.window = None
        self.n = None
        self.text = None
        self.main_color = None
        self.color = None
        self.points = None
        self.height = None
        self.width = None
        self.brush_size = None
        self.activity_flag = True
        self.number = None
        print('INFO [+]: Server created')

    def data(self, put='none'):
        if put != 'none':
            self.text = put
        else:
            return self.text
        print('INFO [+]: Server data changed')

    def server_window_start(self):
        self.server_up()
        self.width = 812
        self.height = 812

        self.points = []
        self.brush_size = 70
        self.color = 'black'
        self.main_color = 'white'
        self.window = Tk()
        self.window.title("Рисунок нейронке")

        self.screen = Canvas(self.window,
                             width=self.width,
                             height=self.height,
                             bg=self.main_color)
        self.screen.bind("<B1-Motion>", self.paint)
        self.screen.bind("<Button-2>", self.paint)
        self.screen.bind('<ButtonRelease-1>', self.save)
        self.screen.pack()
        self.window.bind("<KeyPress-BackSpace>", self.clear)
        self.window.bind("<KeyPress-Escape>", self.close)
        print('INFO [+]: Server window created')
        self.window.mainloop()

    def paint(self, event):
        x1 = event.x + self.brush_size
        x2 = event.x - self.brush_size
        y1 = event.y + self.brush_size
        y2 = event.y - self.brush_size

        self.screen.create_oval(x1, y1, x2, y2, fill='black', outline='black')

        self.points.append((event.x, event.y))
        if len(self.points) > 2:
            self.screen.create_line(self.points[-3:], fill=self.color, width=self.brush_size, smooth=1)
        # print('INFO [+]: Server painted')

    def save(self, event):
        self.points.clear()
        save_as_png(self.screen, 'img/data')
        self.n = NumberRecognizer()
        self.n.init()
        self.n.load()
        self.number = self.n.recognize('img/data.png')
        print('INFO [+]: Image saved')
        self.connection.send(str(self.number).encode("utf-8"))

    def clear(self, event):
        self.screen.delete("all")
        print('INFO [+]: Window cleared')

    def close(self, event):
        self.window.destroy()
        print('INFO [+]: Window closed')

    def server_up(self):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', 1234))
        self.server.listen(1)

        self.connection, self.address = self.server.accept()
        print('INFO [+]: Server up')
