from flask import Flask, render_template
import os
import _thread
import time
import datetime
import matplotlib.pyplot as plt
import gc

app = Flask(__name__)

a = []
res = []

def hs(s):
    res = 0
    mod = 1000000007
    for c in s:
        res = (res * 233 + ord(c)) % mod
    return str(res)

def byStr(t):
    return t[1][0]

def square(a):
    return [i ** 0.5 for i in a]

def updateFigure():
    fig, ax = plt.subplots(1, figsize=(9, 4))

    tot = int(time.strftime('%W', time.localtime()))
    xt = []
    yt = []
    for i in range(tot):
        yt += [0]
        xt += [i]
    for i in res:
        y = []
        for _ in range(tot):
            y += [0]
        for itm in i[1]:
            t = int(time.strftime('%W', time.strptime(itm[0: 19], '%Y-%m-%d %H:%M:%S'))) - 1
            y[t] += 1
        y = square(y)
        for j in range(tot):
            yt[j] += y[j]
        ax.fill_between(xt, y, 0,
                 facecolor="orange", 
                 color='orange',       
                 alpha=0.1)         

    ax.plot(xt, yt, 'b-', label='sum of sqrt')
    ax.set_ylabel('square root of commit numbers')
    ax.set_xlabel('week number in 2020')
    ax.set_title('Commit Statistics')
    ax.legend()

    fig.savefig('static/graph.png',dpi=300,format='png')

    del fig
    del ax

def update():
    global a, res, t
    with open('urls.txt', 'r') as f:
        a = f.read().split('\n')
        a.remove('')
    _res = []
    for url in a:
        h = hs(url)
        if not os.path.exists(h):
            os.system('mkdir ' + h + '; cd ' + h + '; git clone ' + url + r';')
        os.system('cd ' + h + r'/*; git fetch --all; git reset --hard origin/master; git pull; git log --pretty=format:"%ad: %s" --date=format:"%Y-%m-%d %H:%M:%S" > ../log.txt')
        with open(h + r'/log.txt', 'r') as f:
            _res.append((url, f.read().split('\n')))
    t = datetime.datetime.now()
    res = sorted(_res, key=byStr)
    res.reverse()
    
    del _res

    updateFigure()
    gc.collect()

    time.sleep(60)

def backend():
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
