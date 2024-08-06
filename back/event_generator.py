import pandas as pd
import numpy as np
import random
import pickle
from sklearn.svm import SVR
import json


df = pd.read_pickle('coords_tuple.pkl')
print(df.columns)
list_of_tuples = df['AB_pair']
total_count = len(list_of_tuples)
probabilities = [1 / total_count] * total_count

events_list = []
with open('svm_model_dmg.pkl', 'rb') as f:
    dmg_model = pickle.load(f)
with open('svm_model_dead.pkl', 'rb') as f:
    dead_model = pickle.load(f)
with open('svm_model_mag.pkl', 'rb') as f:
    mag_model = pickle.load(f)

def generate_events(count):
    if count == 1:
        print("HIT")
        random_tuples = np.random.choice(list_of_tuples, p=probabilities)
        mag_prediction = mag_model.predict([random_tuples])[0]
        dead_prediction = dead_model.predict([random_tuples])[0]
        dmg_prediction = dmg_model.predict([random_tuples])[0]
        print(random_tuples)
        print(mag_prediction)
        print(dead_prediction)
        print(dmg_prediction)   
        event = {
            "Location": random_tuples,
            "Damage": float(dmg_prediction),
            "Magnitude": float(mag_prediction),
            "MissingorDead": float(dead_prediction)
        }
        
        if len(events_list) >= 10:
            # Remove the oldest event (the first event in the list)
            events_list.pop(0)
        events_list.append(event)
        with open('events.json', 'w') as f:
            f.write(json.dumps(events_list))
    return

if __name__ == '__main__':
    random.seed()

        
    count = 0
    while True:
        random_number = random.randint(1, 2000000)
        generate_events(random_number)