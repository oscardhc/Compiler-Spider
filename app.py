from flask import Flask, render_template
import os
import _thread
import time
import datetime

app = Flask(__name__)

a = []
res = []

def hs(s):
    res = 0
    mod = 1000000007
    for c in s:
        res = (res * 233 + ord(c)) % mod
    return str(res)

def init():
    for url in a:
        h = hs(url)
        if not os.path.exists(h):
            os.system('mkdir ' + h + '; cd ' + h + '; git clone ' + url + r';')
    update()

def byStr(t):
    return t[1][0]

def update():
    global a, res, t
    _res = []
    for url in a:
        h = hs(url)
        os.system('cd ' + h + r'/*; git pull; git log --pretty=format:"%ad: %s" --date=format:"%Y-%m-%d %H:%M:%S" > ../log.txt')
        with open(h + r'/log.txt', 'r') as f:
            _res.append((url[19:], f.read().split('\n')))
    t = datetime.datetime.now()
    res = sorted(_res, key=byStr)
    res.reverse()
    time.sleep(60)

def backend():
    global a
    with open('urls.txt', 'r') as f:
        a = f.read().split('\n')
        a.remove('')
    print(a)
    init()
    while True:
        update()

@app.route('/')
def hello_world():
    # with open()
    return render_template('index.html', res=res, time=t)

_thread.start_new_thread(backend, ())
if __name__ == '__main__':
    t = datetime.datetime.now()
    app.run(host='0.0.0.0', port=80)
