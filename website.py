from flask import Flask, render_template, request
from data_handler import data_handler

app = Flask(__name__)
collection = data_handler('MetObjects.csv')


@app.route("/")
def index():
    return render_template("index.html",img_url="https://upload.wikimedia.org/wikipedia/commons/c/c0/Douglas_adams_portrait_cropped.jpg")

@app.route('/random')
def hello():
    data = collection.get_image(collection.random_item())
    print(data)
    return render_template("index.html",img_url=data[0], title = data[1], artist = data[2], department = data[3])

if __name__ == '__main__':
    app.run()