import socket
import threading
import urllib
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk,Image
import os
import urllib.request
import io
import re

global write_thread
global receive_thread

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

images = []
hdr = {'User-Agent':user_agent,}
isPortValid = False

def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

def exit():
    os._exit(0)

def connect():
    try:
        portTemp = int(portEntry.get())
        isPortValid = True
    except:
        isPortValid = False
        messagebox.showerror(title="Error", message="The port you inserted is invalid. Please check and try again.")
    if not nickEntry.get() == "" and not ipEntry == "" and not portEntry == "" and isPortValid == True:
        nickname = nickEntry.get()

        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(5)
            client.connect((ipEntry.get(), portTemp))
            client.settimeout(None)

            gui.destroy()
            global chatgui
            chatgui = Tk()
            chatgui.attributes('-alpha', 0.0)
            chatgui.title("Generic Chat Client v1.0")
            chatgui.columnconfigure(1, weight=1)
            #chatgui.geometry("640x480")
            global chatInterface
            #chatInterface = ScrolledText(chatgui, padx=5,pady=5, state=DISABLED)
            #chatInterface.grid(row=0, column=1, sticky=W+E+S+N, padx=10, pady=10)

            container = ttk.Frame(chatgui)
            canvas = Canvas(container)
            scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

            canvas.configure(yscrollcommand=scrollbar.set, bg="white")

            container.pack(fill="both", expand=True, padx=5, pady=5)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            global chatTyping
            chatTyping = Entry(chatgui)
            def writeHandle(event):
                write()
            chatTyping.bind("<Return>", func=writeHandle)
            chatTyping.pack(fill="x", padx=5, pady=5)

            center(chatgui)
            chatgui.attributes('-alpha', 1.0)

            def FindURL(string):
                regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
                url = re.findall(regex, string)
                return [x[0] for x in url]

            def receive():
                while True:
                    try:
                        message = client.recv(1024).decode('utf-8')
                        if message == 'NICK':
                            client.send(nickname.encode('utf-8'))
                        else:
                            messageFrame = Frame(scrollable_frame)
                            messageFrame.config(bg="white")
                            messageFrame.pack(fill="x")
                            msgText = Label(messageFrame, text=message)
                            if "[SERVER]:" in message:
                                msgText.config(fg="blue", bg="white")
                            else:
                                msgText.config(fg="black", bg="white")
                            msgText.pack(anchor="w")

                            availableUrls = FindURL(message)

                            if not len(availableUrls) == 0:
                                for i in availableUrls:
                                    requestImage = urllib.request.Request(str(i), headers=hdr)

                                    try:
                                        raw_data = urllib.request.urlopen(requestImage).read()
                                        im = Image.open(io.BytesIO(raw_data))
                                        image = ImageTk.PhotoImage(im)
                                        label1 = Label(messageFrame, image=image)
                                        label1.pack(anchor="w")

                                        images.append(image)

                                        scrollable_frame.bind(
                                            "<Configure>",
                                            lambda e: canvas.configure(
                                                scrollregion=canvas.bbox("all")
                                            )
                                        )

                                        if canvas.yview()[1] >= 0.9:
                                            while not canvas.yview()[1] == 1.0:
                                                canvas.yview_moveto(1.0)
                                    except:
                                        pass

                            scrollable_frame.bind(
                                "<Configure>",
                                lambda e: canvas.configure(
                                    scrollregion=canvas.bbox("all")
                                )
                            )

                            if canvas.yview()[1] >= 0.9:
                                while not canvas.yview()[1] == 1.0:
                                     canvas.yview_moveto(1.0)


                    except Exception as e:
                        messagebox.showerror("Error", "An error ocurred when receiving an message.\n\n" + str(e))
                        print(e)
                        client.close()
                        break

            def write():
                if not chatTyping.get() == "":
                    message = f'[{nickname}]: {chatTyping.get()}'
                    client.send(message.encode('utf-8'))
                    chatTyping.delete(0, END)
                    scrollable_frame.bind(
                        "<Configure>",
                        lambda e: canvas.configure(
                            scrollregion=canvas.bbox("all")
                        )
                    )

                    if canvas.yview()[1] >= 0.9:
                        while not canvas.yview()[1] == 1.0:
                            canvas.yview_moveto(1.0)

            receive_thread = threading.Thread(target=receive)
            receive_thread.start()

            write_thread = threading.Thread(target=write)
            write_thread.start()

            chatgui.protocol("WM_DELETE_WINDOW", exit)
            chatgui.mainloop()
        except Exception as e:
            messagebox.showerror(title="Error", message="Failed to connect to the specified chat server. Please check if the server is up and running, check your firewall or your internet connection.\n\n" + str(e))
            print(e)
    else:
        if nickEntry.get() == "" and not ipEntry == "" and not portEntry == "":
            messagebox.showwarning(title="Warning", message="You cannot use an empty nickname.")
        elif nickEntry.get() == "" and ipEntry == "" and not portEntry == "":
            messagebox.showwarning(title="Warning", message="You forgot to set a nickname and an IP to connect.")
        elif nickEntry.get() == "" and ipEntry == "" and portEntry == "":
            messagebox.showwarning(title="Warning", message="You forgot to set a nickname and an IP and port to connect.")

def connectHandle(event):
    connect()

global gui
gui = Tk()
gui.attributes('-alpha', 0.0)
gui.title("Generic Chat Client v1.0")
title = Label(gui, text="Generic Chat Client", font=('Helvetica 18 bold', 40)).pack()

nickText = Label(gui, text="Enter your nickname:").pack(pady=10)
nickEntry = Entry(gui, width=50, borderwidth=5)
nickEntry.pack(padx=50, pady=8)

ipEntry = Entry(gui, width=20, borderwidth=5)
ipText = Label(gui, text="Enter the IP to connect to:").pack(pady=3)
ipEntry.insert(0, "127.0.0.1")
ipEntry.pack(padx=50, pady=3)

portEntry = Entry(gui, width=20, borderwidth=5)
portText = Label(gui, text="Enter the port to connect to:").pack(pady=3)
portEntry.insert(0, "55555")
portEntry.pack(padx=50, pady=3)

nickButton = Button(gui, text="Connect to chat", command=connect)
nickButton.pack(pady=10)

gui.bind("<Return>", func=connectHandle)

center(gui)
gui.attributes('-alpha', 1.0)

gui.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))
gui.mainloop()