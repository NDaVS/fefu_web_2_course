from server import *
from client import *


class App:

    def __init__(self):
        self.server_image = None
        self.client_image = None
        self.user_ip = None
        self._client_1 = None
        self._server = None
        self.bttn2 = None
        self.bttn1 = None
        self.txt = None
        self.window = None
        self.main_color = None
        self.height = None
        self.width = None
        print('INFO [+]: App created')

    def menu_start(self, ip):
        self.width = 812
        self.height = 812
        self.main_color = 'white'

        self.window = Tk()
        self.window.title("Menu")
        self.txt = Label(self.window, text=f"Ваш ip: {ip}")
        self.txt.pack(side=TOP)

        self.server_image = PhotoImage(file='data/server.png')
        self.bttn1 = Button(text='Я хост', width=200, height=200, image=self.server_image)
        self.bttn1["border"] = "0"
        self.bttn1.bind('<Button-1>', self.host_starter)
        self.bttn1.pack(side=LEFT)

        self.client_image = PhotoImage(file='data/client.png')
        self.bttn2 = Button(text='Я клиент', width=250, height=250, image=self.client_image)
        self.bttn2["border"] = "0"
        self.bttn2.bind('<Button-1>', self.close)
        self.bttn2.pack(side=LEFT)

        self.window.bind("<KeyPress-Escape>", self.close)
        print('INFO [+]: Menu window created')
        self.window.mainloop()

    def close(self, event):
        self.client_starter(event)
        print('INFO [+]: Menu closed')

    def host_starter(self, event):
        self._server = Server()
        self.window.destroy()
        self._server.server_window_start()

    def client_starter(self, event):
        self._client_1 = Client()
        self.window.destroy()
        self._client_1.client_window_start()

    def app(self):
        self.user_ip = socket.gethostbyname(socket.gethostname())
        print('INFO [+]: Menu Started')
        self.menu_start(self.user_ip)
