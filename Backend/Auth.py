from flask import Flask

app = Flask('__main__')

@app.route('/')
def mainpage():
    file = open('./Vista/Paginalogin.html')
    html = file.read()
    return html

