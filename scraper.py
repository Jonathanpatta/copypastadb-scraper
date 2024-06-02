import requests
from bs4 import BeautifulSoup

def get_href_links(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the <div> with the class "entry-content"
        entry_content_div = soup.find("div", class_="entry-content")

        # If the <div> is found
        if entry_content_div:
            # Find the first child <div> within the "entry-content" <div>
            child_div = entry_content_div.find("div")

            # If a child <div> is found
            if child_div:
                # Find the <p> tag within the child <div>
                p_tag = child_div.find("p")

                # If a <p> tag is found
                if p_tag:
                    # Find all <a> tags within the <p> tag
                    a_tags = p_tag.find_all("a")

                    # List to store the href links
                    href_links = []

                    # Iterate over the <a> tags and extract the href links
                    for a_tag in a_tags:
                        href = a_tag.get("href")
                        href_links.append(href)

                    # Return the list of href links
                    return href_links
                else:
                    print("No <p> tag found within the child <div> of the <div> with class 'entry-content'")
            else:
                print("No child <div> found within the <div> with class 'entry-content'")
        else:
            print("No <div> with class 'entry-content' found on the webpage")
    else:
        print(f"Failed to fetch webpage. Error code: {response.status_code}")

    # Return an empty list if no href links were found
    return []



import string
import pickle

base_url = "https://copypastadb.com/database/"
all_href_links = []
failed_urls = []

# Iterate through all letters from 'a' to 'z'
for letter in string.ascii_lowercase:
    url = f"{base_url}{letter}/"
    print(f"Fetching links from: {url}")
    
    href_links = get_href_links(url)
    
    if not href_links:
        failed_urls.append(url)
        print(f"Warning: No links found for {url}")
    else:
        all_href_links.extend(href_links)

print("All href links:")
print(len(all_href_links))

if failed_urls:
    print("\nFailed URLs:")
    for failed_url in failed_urls:
        print(failed_url)

# Save all_href_links to a pickle file
with open("data/all_href_links.pkl", "wb") as f:
    pickle.dump(all_href_links, f)
    print("\nAll href links saved to 'all_href_links.pkl'")