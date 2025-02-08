from flask import Flask, render_template, request
from data_handler import data_handler

app = Flask(__name__)
collection = data_handler('MetObjects.csv')


@app.route("/")
def index():
    return render_template("index.html",img_url="https://upload.wikimedia.org/wikipedia/commons/c/c0/Douglas_adams_portrait_cropped.jpg")

@app.route('/random')
def random():
    data = collection.get_image(collection.random_item())
    return render_template("index.html",img_url=data[0], title = data[1], artist = data[2], department = data[3], medium = data[4], artist_photo = data[5], descriptions = data[6])

@app.route('/department<dep>')
def department(dep):
    print(dep)
    data = collection.random_image_from_dep_name(dep)
    return render_template("index.html",img_url=data[0], title = data[1], artist = data[2], department = data[3], medium = data[4], artist_photo = data[5], descriptions = data[6])

@app.route('/similar<info>')
def similarity(info):
    print(info)
    data = collection.similar(info)
    return render_template("index.html",img_url=data[0], title = data[1], artist = data[2], department = data[3], medium = data[4], artist_photo = data[5], descriptions = data[6])

@app.route('/artist<info>')
def artist(info):
    data = collection.same_artist(info)
    return render_template("index.html",img_url=data[0], title = data[1], artist = data[2], department = data[3], medium = data[4], artist_photo = data[5], descriptions = data[6])

@app.route('/quiz.html')
def quiz():
    data = collection.quiz()
    return render_template("quiz.html",img_url=data[0], title = data[1])


if __name__ == '__main__':
    app.run()