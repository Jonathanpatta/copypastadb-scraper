import pandas as pd
import pickle
import json


def loadpkl(filename):
    with open(filename,"rb") as f:
        data = pickle.load(f)
    return data

def convert_to_json(filename):
    data = loadpkl(filename)
    json_arr = []
    for dat in data:
        json_arr.append(json.loads(dat))
    return json_arr

def process_json_data(json_data):
   errored_data = []
   normal_data = []

   for id,data in enumerate(json_data):
       if 'error' in data.keys() and 'url' in data.keys():
           errored_data.append({'id':str(id),'error': data['error'], 'url': data['url']})
       elif 'title' in data.keys() and 'content' in data.keys():
           normal_data.append({'id':str(id),'title': data['title'], 'content': data['content']})

   errored_df = pd.DataFrame(errored_data)
   errored_df.to_csv('data/csv/errored.csv', index=False)

   normal_df = pd.DataFrame(normal_data)
   normal_df.to_csv('data/csv/data.csv', index=False)


all_data = []

for i in range(1,398):
    json_data = convert_to_json("data/batch"+str(i))
    all_data += json_data    

print(len(all_data))

process_json_data(all_data)