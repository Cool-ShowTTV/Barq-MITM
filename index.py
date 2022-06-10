from flask import Flask, request
import requests
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

import socket
localIP = socket.gethostbyname(socket.gethostname())

from colorama import Fore, Back, Style, init
init()

url = "https://api.barq.social"
logOut = False

@app.route('/<path:text>', methods=['GET', 'POST'])
def all_routes(text):
    headers = {
        "authorization": request.headers.get('authorization'),
        "Content-Type": request.headers.get('content-type'),
        "user-agent": "Barq MITM",
        "x-app-version": "1.0.0"
    }
    print(Fore.GREEN)
    print(headers)

    print(Fore.RED)
    print(request.data)
    #open text file and write to it
    with open("barq.txt", "w") as f:
        f.write(str(request.data).replace("\\n", "\n"))    
    print("\n\n")
    if request.method == 'POST':
        rq = requests.post(f'{url}/{text}', data=request.data, headers=headers).text
        if logOut:
            print(rq)
        return rq
    else:
        rq = requests.get(f'{url}/{text}', headers=headers).text
        if logOut:
            print(rq)
        return rq

@app.route('/', methods=['GET', 'POST'])
def home():
    headers = {
        "authorization": request.headers.get('authorization'),
        "Content-Type": request.headers.get('content-type'),
        "user-agent": "Barq MITM",
        "x-app-version": "1.0.0"
    }
    print(Fore.GREEN)
    print(headers)

    print(Fore.RED)
    print(request.data)
    print("\n\n")
    if request.method == 'POST':
        rq = requests.post(f'{url}', data=request.data, headers=headers).text
        if logOut:
            print(rq)
        return rq
    else:
        rq = requests.get(f'{url}', headers=headers).text
        if logOut:
            print(rq)
        return rq



# run flask i guess
if __name__ == '__main__':
    
    print(Fore.GREEN + Style.BRIGHT + "Barq MITM running on " + localIP + ":80" + Style.RESET_ALL)
    app.run(port=80, host=localIP)
