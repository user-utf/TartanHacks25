import pandas as pd
import random
import requests

class data_handler:
    def __init__(self, file_name, categories = ["Arms and Armor","Egyptian Art", "Greek and Roman Art", "Asian Art", "Islamic Art", "Modern and Contemporary Art"]) -> None:
        self.df = self.read(file_name, categories)
        self.shape = self.df.shape
        self.header = self.df.columns
        self.elements = ["Title"]
        print(self.df)

    def read(self, file_name, categories):
        data = pd.read_csv(file_name, delimiter=',',low_memory=False)
        print(data)
        data = data.dropna(subset=["Artist Wikidata URL", "Object Wikidata URL"], how='any')
        data = data[data["Is Public Domain"]]
        data = data[data["Department"].isin(categories)]
        return data

    def get_image(self, data):
        url = data["Object Wikidata URL"]
        reply = requests.get(url).text

        class_start = reply.find('<meta property="og:image" content="https://upload.wikimedia.org/wikipedia/commons/')

        start = reply[class_start:].find('https://upload.wikimedia.org')
        end = reply[class_start+start:].find('"')
        return reply[class_start+start:class_start+start+end]
#{{ img_url }}"

    def get_item(self, idx):
        return self.df.iloc[idx]
    
    def random_item(self):
        index  = random.randint(0, self.shape[1]-1)
        return self.get_item(index)




if __name__ == "__main__":
    met = data_handler('MetObjects.csv')
    met.get_image(met.random_item())
    met.get_image(met.random_item())
    met.get_image(met.random_item())
    met.get_image(met.random_item())