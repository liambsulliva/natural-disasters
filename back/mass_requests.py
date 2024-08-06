import requests
import csv
import concurrent.futures

def fetch_and_write(item_id):
    url = f"https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/earthquakes/{item_id}"
    response = requests.get(url)
    data = response.json()

    # List of keys to skip
    keys_to_skip = ['comments']

    # Create a new dictionary without the skipped keys
    filtered_data = {k: v for k, v in data.items() if k not in keys_to_skip}

    with open('output.csv', 'a', newline='') as csvfile:
        fieldnames = filtered_data.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if item_id == 1:  # Write headers only once
            writer.writeheader()
        writer.writerow(data)

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_and_write, item_id) for item_id in range(1, 6413)]
        concurrent.futures.wait(futures)