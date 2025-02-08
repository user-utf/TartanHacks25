import pandas as pd
import random
import requests
import re
import json

class data_handler:
    def __init__(self, file_name, categories = ["The Cloisters","Arms and Armor","Egyptian Art", "Greek and Roman Art", "Asian Art", "Islamic Art", "Modern and Contemporary Art", "European Paintings", "Musical Instruments", "Arts of Africa, Oceania, and the Americas","European Sculpture and Decorative Arts"], quiz_names = ["Rembrandt", "Renoir", "Cézanne", "Gogh"]) -> None:
        self.dfs = self.read(file_name, categories)
        self.quiz_list = [self.dfs[7][self.dfs[7]["Artist Display Name"].str.contains(name)] for name in quiz_names] 
        self.quiz_names = quiz_names
        self.categories = categories
        self.elements = ["Title"]

    def read(self, file_name, categories):
        data = pd.read_csv(file_name, sep=',', quotechar='"', skipinitialspace=True, low_memory=False) #, delimiter=','
        # data = data.dropna(subset=["Artist Wikidata URL", "Object Wikidata URL","Title","Artist Display Name"], how='any')
        data = data.dropna(subset=["Object Wikidata URL","Title","Artist Display Name","Medium"], how='any')
        data = data[data["Is Public Domain"]]
        self.header = data.columns

        out = [data[data["Department"] == cat] for cat in categories]
        return out

    def get_url(self, base):
        if "https:" not in base:
            return "no"
        if base[0] == "|":
            base = base[1:]
        print("Base URL:", base)
        base = base.split("|")[0]
        print("Parsed URL:", base)

        reply = requests.get(base).text

        class_start = reply.find('<meta property="og:image" content="https://upload.wikimedia.org/wikipedia/commons/')

        start = reply[class_start:].find('https://upload.wikimedia.org')
        end = reply[class_start+start:].find('"')
        return reply[class_start+start:class_start+start+end]

    def get_description(self, base):
        ID = base[base.rfind("/")+1:]
        # print(ID)
        text = requests.get("https://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + ID + "&format=json").text
        # print(text)
        reply = json.loads(text)
        try:
            return reply["entities"][ID]["descriptions"]["en"]["value"]
        except KeyError:
            return "no"  


    def get_quiz_image(self, data):
        url = self.get_url(data["Object Wikidata URL"])
        
        if url == "":
            return self.get_image(self.random_item())
        
        pattern = re.compile(r'[^a-zA-Z0-9\s.,;:!?()\"\'\-]')
        filter = pattern.sub('', data["Title"]).replace("　","")
        split = filter.split('"')
        if len(split) > 1:
            split = split[1]
        else:
            split = split[0]
        title = re.sub("[\(\[].*?[\)\]]", "", split)
        return [url, title]


    def get_image(self, data, cat = -1):
        artist_photo = "no"
        descriptions = "no"
        print(data["Artist Wikidata URL"])
        print(data["Object Wikidata URL"])
        if not pd.isnull(data["Artist Wikidata URL"]):
            artist_photo = self.get_url(data["Artist Wikidata URL"])
            descriptions = self.get_description(data["Artist Wikidata URL"])

        url = self.get_url(data["Object Wikidata URL"])
        
        if url == "":
            if cat == -1:
                return self.get_image(self.random_item())
            else:
                return self.random_image_from_dep(cat)
        # print(rtn,reply[class_start:class_start+start+end+10])
        pattern = re.compile(r'[^a-zA-Z0-9\s.,;:!?()\"\'\-]')
        filter = pattern.sub('', data["Title"]).replace("　","")
        split = filter.split('"')
        if len(split) > 1:
            split = split[1]
        else:
            split = split[0]
        title = re.sub("[\(\[].*?[\)\]]", "", split)
        return [url, title, data["Artist Display Name"].split("|")[0], data["Department"],data["Medium"], artist_photo, descriptions]

    def get_item(self, category, idx):
        return self.dfs[category].iloc[idx]
    
    def random_item(self):
        cat = random.randint(0, len(self.categories)-1)
        # print(cat,self.categories[cat],len(self.dfs[cat]))
        index = random.randint(0, len(self.dfs[cat])-1)
        # print(index)
        return self.get_item(cat, index)

    def random_image_from_dep(self, cat):
        print("Random IMG from Dep:", self.categories[cat],cat)
        index = random.randint(0, len(self.dfs[cat])-1)
        return self.get_image(self.get_item(cat, index),cat)

    def random_image_from_dep_name(self, dep):
        if dep[1:-1] not in self.categories:
            print("NOT FOUND CAT \n\n")
            return self.get_image(self.random_item())
        cat = self.categories.index(dep[1:-1])
        return self.random_image_from_dep(cat)

    def find_with_medium(self, dep, medium):
        medium = medium[:-1]
        mask = self.dfs[dep]["Medium"].str.contains(medium)
        valid = self.dfs[dep][mask]
        idx = random.randint(0, len(valid)-1)
        return valid.iloc[idx]

    def similar(self, info):
        info = info[1:-1]
        [dep, medium] = info.split("|")
        medium = medium.split(",")[0].split(" ")[0]

        if dep not in self.categories:
            print("NOT FOUND\n\n")
            return self.get_image(self.random_item())
        
        cat = self.categories.index(dep)

        data = self.find_with_medium(cat, medium)

        return self.get_image(data)
    
    def find_with_artist(self, dep, artist):
        artist = artist[:-1]
        mask = self.dfs[dep]["Artist Display Name"].str.contains(artist)
        valid = self.dfs[dep][mask]
        print(valid,artist)
        idx = random.randint(0, len(valid)-1)
        return valid.iloc[idx]
    
    def same_artist(self, info):
        info = info[1:-1]
        [dep, artist] = info.split("|")

        if dep not in self.categories:
            print("NOT FOUND\n\n")
            return self.get_image(self.random_item())
        
        cat = self.categories.index(dep)

        data = self.find_with_artist(cat, artist)

        return self.get_image(data)
    
    def quiz(self):
        artist = random.randint(0, len(self.quiz_list)-1)
        # print(cat,self.categories[cat],len(self.dfs[cat]))
        index = random.randint(0, len(self.quiz_list[artist])-1)
        print("QUIZ:",self.quiz_list[artist].iloc[index])
        return self.get_quiz_image(self.quiz_list[artist].iloc[index])



if __name__ == "__main__":
    met = data_handler('MetObjects.csv')
    met.get_image(met.random_item())
    met.get_image(met.random_item())
    met.get_image(met.random_item())
    met.get_image(met.random_item())