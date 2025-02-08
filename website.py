from flask import Flask, render_template, request
from data_handler import data_handler

app = Flask(__name__)
collection = data_handler('MetObjects.csv')


@app.route("/")
def index():
    #https://upload.wikimedia.org/wikipedia/commons/c/c0/Douglas_adams_portrait_cropped.jpg
    return render_template("index.html",img_url="https://images.metmuseum.org/CRDImages/as/original/DP130155.jpg", title = "Under the Wave off Kanagawa, also known as The Great Wave", artist = "Katsushika Hokusai", department = "Asian Art", medium = "Pentaptych of woodblock prints; ink and color on paper", artist_photo = "https://upload.wikimedia.org/wikipedia/commons/1/1c/Hokusai_as_an_old_man.jpg", descriptions = "Japanese artist (1760-1849)", year = "1831")

@app.route('/random')
def random():
    data = collection.get_image(collection.random_item())
    return render_template("index.html",img_url=data[0], title = data[1], artist = data[2], department = data[3], medium = data[4], artist_photo = data[5], descriptions = data[6], year = data[7])

@app.route('/department<dep>')
def department(dep):
    print(dep)
    data = collection.random_image_from_dep_name(dep)
    return render_template("index.html",img_url=data[0], title = data[1], artist = data[2], department = data[3], medium = data[4], artist_photo = data[5], descriptions = data[6], year = data[7])

@app.route('/similar<info>')
def similarity(info):
    print(info)
    data = collection.similar(info)
    return render_template("index.html",img_url=data[0], title = data[1], artist = data[2], department = data[3], medium = data[4], artist_photo = data[5], descriptions = data[6], year = data[7])

@app.route('/artist<info>')
def artist(info):
    data = collection.same_artist(info)
    return render_template("index.html",img_url=data[0], title = data[1], artist = data[2], department = data[3], medium = data[4], artist_photo = data[5], descriptions = data[6], year = data[7])

@app.route('/quiz.html<info>')
def quiz(info):
    data = collection.quiz(info)
    return render_template("quiz.html",img_url=data[0], title = data[1], qwb = data[2], score = data[3], num = data[4], num2 = data[4]-1)


if __name__ == '__main__':
    app.run()