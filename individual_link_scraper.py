import requests
from bs4 import BeautifulSoup
import json

def extract_data(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        entry_content_div = soup.find('div', class_='entry-content')


        for child_div in entry_content_div.find_all('div'):
            if 'copypasta' in child_div.get('class', []):
                p_tag = child_div.p
                if p_tag:
                    content = p_tag.get_text()

        
        title_class_name = 'has-text-align-left customposttitle wp-block-post-title'
        title_h1 = soup.find('h1', class_=title_class_name)
        title = title_h1.get_text()


        # Create a dictionary with the extracted data
        data = {
            'title': title,
            'content': content
        }

        # Convert the dictionary to a JSON string
        json_data = json.dumps(data)

        return json_data

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching the URL: {e}")
        return json.dumps({"error":str(e),"url":url})
    except Exception as e:
        print(f"An error occurred: {e}")
        return json.dumps({"error":str(e),"url":url})



import concurrent.futures
import pickle
import threading
import time


def save_data_to_file(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

with open("data/all_href_links.pkl", "rb") as f:
    urls = pickle.load(f)


print(len(urls))
batch_size = 1000
batch_no = 164
urls = urls[batch_no*batch_size:]
all_data = []


def process_urls(urls, extract_data,start_batch_no, batch_size=1000):
    all_data = []
    failed_urls = []
    lock = threading.Lock()
    errored_urls = 0
    start = time.time()
    batch_no = start_batch_no

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_results = [executor.submit(extract_data, url) for url in urls]
        num_urls_processed = 0

        for future in concurrent.futures.as_completed(future_results):
            json_data = future.result()
            if json_data:
                with lock:
                    all_data.append(json_data)
            
            else:
                with lock:
                    failed_urls.append()

            num_urls_processed += 1
            if num_urls_processed % batch_size == 0:
                with lock:
                    batch_no += 1
                    save_data_to_file(all_data, "data/batch"+str(batch_no))
                    print("saved file:","batch"+str(batch_no))
                    all_data = []  # Clear the list after saving
                print(f"Processed {num_urls_processed} URLs")

            if num_urls_processed % 100 == 0:
                print(f"Processed {num_urls_processed} URLs in {time.time()-start} seconds")

        # Save remaining data if any
        if num_urls_processed % batch_size != 0:
            with lock:
                batch_no += 1
                save_data_to_file(all_data, "data/batch"+str(batch_no))
                print("saved file:","batch"+str(batch_no))
        
        

    print(len(all_data))

process_urls(urls, extract_data,batch_size=batch_size,start_batch_no=batch_no)