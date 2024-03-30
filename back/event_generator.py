import pandas as pd
import numpy as np
import random

df = pd.read_pickle('coords_tuple.pkl')
print(df.columns)
list_of_tuples = df['AB_pair']
total_count = len(list_of_tuples)
probabilities = [1 / total_count] * total_count


def generate_events(count):
    if count == 1:
        print("HIT")
    random_tuples = np.random.choice(list_of_tuples, p=probabilities)
    #print(random_tuples)
    #print(count)
    return

if __name__ == '__main__':
    random.seed()

    count = 0
    while True:
        random_number = random.randint(1, 30000)
        generate_events(random_number)