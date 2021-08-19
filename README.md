# generic-chat-client
A very simple chat client made in Python with Tkinter, with support to nicknames and embedding images (GIFs aren't supported yet) from links. It also comes with an server to host it by yourself.

# How to compile and host a server by yourself
First, you need [Python](https://www.python.org/downloads/) installed.

(If you're in Linux, you may need ``python-tk`` to run the client. In debian-based, you can just type ``sudo apt install python-tk``. In Arch Linux-based, ``pacman -S python-tk``.)

And then, if you want to clone the repository from a terminal, you will need Git installed on your computer. Otherwise, you can just download a .zip of the repository. But cloning is recommended.

Open CMD/Powershell (If you're on Windows) or your Terminal (if you are in MacOS/Linux) and clone (download) the repository to the desired folder that you want:
```
git clone https://github.com/pvini07BR/generic-chat-client.git
```
Go to the ``src`` folder:
```
cd src/
```
And finally run the server:
```
python server.py
```
And then it will prompt you the IP adress and port that you will use to host your server.
If you see "Server is starting..." on the console, means that the server is sucefully running and listening for new connections.

Now open the client:
```
python client.py
```
Insert your nickname, and if you want to connect to the server that is hosted in your localhost, you can keep the default values. Otherwise you can use an Public IP that is port fowarded with an server already running. Then press the "Connect to chat" button, or press Enter.

If a chat screen appears, congrats! You are sucefully running your own server and connected to it.

Anyways, if you want to compile the .py files as an .exe file, you can install and use pyinstaller:
```
pip install pyinstaller
```
And then compile them:

Client:
```
pyinstaller --onefile -w client.py
```

Server:
```
pyinstaller --onefile server.py
```
- ``--onefile``: This will pack the entire .py file and its dependencies into one single .exe file.
- ```-w``: This will make the .exe file to not open an command prompt window when running it.
- ``client.py``/``server.py``: The target .py file to be compiled.
