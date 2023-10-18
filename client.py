import socket
import time
from tkinter import *


class Client:

    def __init__(self):
        self.port_txt = None
        self.ip_txt = None
        self.ip = '192.168.25.62'
        self.port = 1234
        self.number = 404
        self.lbl = None
        self.data = None
        self.activity_flag = False
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.window = None
        print('INFO [+]: Client created')

    def close(self, event):
        self.window.destroy()

    def reconnect(self, event):
        self.window.destroy()
        print('INFO [+]: Reconnect')
        self.client_window_start()

    def save_data(self, event):
        self.port = int(self.port_txt.get())
        self.ip = self.ip_txt.get()
        print('INFO [+]: Take data')
        self.activity_flag = True
        self.window.destroy()
        self.client_up()

    def client_window_start(self):
        self.window = Tk()
        self.window.title("Нейронка думает...")
        self.window.geometry('400x250')

        self.ip_txt = Entry(self.window, width=20)
        self.ip_txt.pack(side=TOP)

        self.port_txt = Entry(self.window, width=20)
        self.port_txt.pack(side=TOP)

        self.window.bind('<KeyPress-Return>', self.save_data)

        self.lbl = Label(self.window, text='( ._.)', font=("Arial Bold", 140))
        self.window.bind("<KeyPress-Escape>", self.close)
        self.lbl.pack(side=BOTTOM)
        print('INFO [+]: Client window created')
        self.window.mainloop()

    def client_up(self):
        try:
            self.client.connect((self.ip, self.port))
            self.window = Tk()
            self.window.title("Нейронка думает что это...")
            self.window.geometry('400x250')

            self.lbl = Label(self.window, text=str(self.number), font=("Arial Bold", 150))
            self.window.bind("<KeyPress-Escape>", self.close)
            self.lbl.pack(side=BOTTOM)

            print('INFO [+]: Client up  created')
            self.lbl.after(500, self.client_check, self.client)
            self.window.mainloop()
        except Exception as e:
            print('INFO [+]: Server is down')
            self.window = Tk()
            self.window.title("Нейронка не думает ( ._.)")
            self.window.geometry('1000x100')

            self.lbl = Label(self.window, text="Проверьте правильность внесенных данных \nДля продолжения нажмите Ввод",
                             font=("Arial Bold", 32))

            self.window.bind("<KeyPress-Escape>", self.close)
            self.window.bind("<KeyPress-Return>", self.reconnect)
            self.lbl.pack(side=BOTTOM)
            self.window.mainloop()

    def client_check(self, client):
        try:
            self.data = client.recv(1024).decode('utf-8').lower()
            self.lbl.config(text=self.data)
            print(f'INFO [+]: Client data changed: {self.data}')
            self.lbl.after(500, self.client_check, self.client)
        except Exception as e:
            print('INFO [+]: Client disconnected')
            self.lbl.config(text='404')
            time.sleep(2)
            self.lbl.after(500, self.client_check, self.client)
