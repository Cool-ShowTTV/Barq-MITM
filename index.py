from flask import Flask, request
import requests
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if input("Do you want auto local IP (has problems)? (y/n): ") == "y":
    localIP = __import__("socket").gethostbyname(__import__("socket").gethostname())
else:
    localIP = input("What is a local IP that this divice has?: ") # "192.168.1.168"


from colorama import Fore, Back, Style, init
init()

url = "https://api.barq.app"
logOut = True
version = "1.1.2"
userAgent = "Barq MITM"	

@app.route('/<path:text>', methods=['GET', 'POST'])
def all_routes(text):
    headers = {
        "authorization": request.headers.get('authorization'),
        "Content-Type": request.headers.get('content-type'),
        "user-agent": userAgent,
        "x-app-version": request.headers.get('x-app-version')
    }
    data = ""
    data = data + (Fore.GREEN)+"\n"
    data = data + (str(request.headers))+"\n"

    data = data + (Fore.RED)+"\n"
    data = data + (f'{request.method} {url}/{text} {request.data}')+"\n"
    #open text file and write to it
    with open("barq.txt", "w") as f:
        f.write(request.data.decode())
    if request.method == 'POST':
        rq = requests.post(f'{url}/{text}', data=request.data, headers=headers).text
    else:
        rq = requests.get(f'{url}/{text}', headers=headers).text
    if logOut:
        print(data)
        print(Fore.RESET + "\n")
        print(rq)
    print("\n\n")
    return rq

@app.route('/', methods=['GET', 'POST'])
def home():
    APIVersion = requests.get('https://api.barq.app',headers={
        "authorization": request.headers.get('authorization'),
        "Content-Type": request.headers.get('content-type'),
        "user-agent": userAgent,
        "x-app-version": request.headers.get('x-app-version')
    }).json()['version']

    # This is used for the feed back on the Dev page
    #  You can set "host" and "version" to whatever you want and it will show up on the Dev page
    return f'{{"host":"MITM by @Cool_Show","hostname":"MITM by @Cool_Show","version":"MITM v{version}\nAPI: v{APIVersion}","buildVersion":"MITM v{version}\nAPI: v{APIVersion}"}}'

@app.route('/favicon.ico', methods=['GET', 'POST'])
def favicon():
    return ''

# run flask i guess
if __name__ == '__main__':
    port=5000
    print(Fore.GREEN + Style.BRIGHT + f'Barq MITM v{version} running on http://{localIP}:{port}' + Style.RESET_ALL)
    app.run(port=port, host=localIP)
