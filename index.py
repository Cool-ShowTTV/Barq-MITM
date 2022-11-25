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
logOut = False
version = "1.1.1"

@app.route('/<path:text>', methods=['GET', 'POST'])
def all_routes(text):
    headers = {
        "authorization": request.headers.get('authorization'),
        "Content-Type": request.headers.get('content-type'),
        "user-agent": "Barq MITM",
        "x-app-version": request.headers.get('x-app-version')
    }
    print(Fore.GREEN)
    print({
        "user-agent": "Barq MITM",
        "x-app-version": "1.0.0"
    })

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

    # Only needed if they send a requests to the root
    # But I haven't seen it yet
    """
    print(Fore.GREEN)
    print({
        "user-agent": "Barq MITM",
        "x-app-version": "1.0.0"
    })

    print(Fore.RED)
    print(request.data)
    print("\n\n")
    """

    # This is used for the feed back on the Dev page
    #  You can set "host" and "version" to whatever you want and it will show up on the Dev page
    return '{"host":"MITM by @Cool_Show","hostname":"MITM by @Cool_Show","version":"MITM V'+version+'","buildVersion":"MITM V'+version+'"}'



# run flask i guess
if __name__ == '__main__':
    port=5000
    print(Fore.GREEN + Style.BRIGHT + f'Barq MITM v{version} running on {localIP}:{port}' + Style.RESET_ALL)
    app.run(port=port, host=localIP)
