import pandas as pd
import random
import requests
import re

class data_handler:
    def __init__(self, file_name, categories = ["The Cloisters","Arms and Armor","Egyptian Art", "Greek and Roman Art", "Asian Art", "Islamic Art", "Modern and Contemporary Art", "European Paintings", "Musical Instruments", "Arts of Africa, Oceania, and the Americas","European Sculpture and Decorative Arts"]) -> None:
        self.dfs = self.read(file_name, categories)
        self.categories = categories
        self.elements = ["Title"]

    def read(self, file_name, categories):
        data = pd.read_csv(file_name, sep=',', quotechar='"', skipinitialspace=True, low_memory=False) #, delimiter=','
        # data = data.dropna(subset=["Artist Wikidata URL", "Object Wikidata URL","Title","Artist Display Name"], how='any')
        data = data.dropna(subset=["Object Wikidata URL","Title","Artist Display Name","Medium"], how='any')
        data = data[data["Is Public Domain"]]
        self.header = data.columns
        # print(data["Department"].unique())
        # print(data[data["Department"] == '"Arts of Africa, Oceania, and the Americas"'])
        out = [data[data["Department"] == cat] for cat in categories]
        # print(len(out[8]))
        return out

    def get_image(self, data):
        url = data["Object Wikidata URL"]
        # print(data)
        # print(data["Medium"])
        # print(data["Artist Wikidata URL"])
        # print(data["Artist Display Bio"])
        reply = requests.get(url).text

        class_start = reply.find('<meta property="og:image" content="https://upload.wikimedia.org/wikipedia/commons/')

        start = reply[class_start:].find('https://upload.wikimedia.org')
        end = reply[class_start+start:].find('"')
        rtn = reply[class_start+start:class_start+start+end]
        if rtn == "":
            return self.get_image(self.random_item())
        print(rtn,reply[class_start:class_start+start+end+10])
        pattern = re.compile(r'[^a-zA-Z0-9\s.,;:!?()\"\'\-]')
        filter = pattern.sub('', data["Title"]).replace("　","")

        return [rtn, filter, data["Artist Display Name"].split("|")[0], data["Department"],data["Medium"]]

    def get_item(self, category, idx):
        return self.dfs[category].iloc[idx]
    
    def random_item(self):
        cat = random.randint(0, len(self.categories)-1)
        # print(cat,self.categories[cat],len(self.dfs[cat]))
        index = random.randint(0, len(self.dfs[cat])-1)
        # print(index)
        return self.get_item(cat, index)
    
    def random_image_from_dep(self, dep):
        if dep[1:-1] not in self.categories:
            return self.get_image(self.random_item())
        cat = self.categories.index(dep[1:-1])
        index = random.randint(0, len(self.dfs[cat])-1)
        return self.get_image(self.get_item(cat, index))

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



if __name__ == "__main__":
    met = data_handler('MetObjects.csv')
    met.get_image(met.random_item())
    met.get_image(met.random_item())
    met.get_image(met.random_item())
    met.get_image(met.random_item())