import requests
from bs4 import BeautifulSoup
import re

# Base URL for the course discourse page
base_url = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34"

# Fetch the page
response = requests.get(base_url)
if response.status_code != 200:
    print("Failed to fetch the page")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

# Find all thread links (Discourse often uses 'tr.topic-list-item' or similar)
threads = soup.select('tr.topic-list-item a.title')
if not threads:
    # Fallback: try another selector if the above doesn't work
    threads = soup.select('a.raw-link.raw-topic-link')

# Collect thread titles and links
thread_data = []
for thread in threads:
    title = thread.text.strip()
    link = thread['href']
    # Ensure link is absolute
    if not link.startswith('http'):
        link = f"https://discourse.onlinedegree.iitm.ac.in{link}"
    thread_data.append((title, link))

# Print thread data
for idx, (title, link) in enumerate(thread_data, 1):
    print(f"{idx}. {title}\n   {link}\n")

# Optional: Scrape content of a thread (example for the first thread)
if thread_data:
    example_thread_url = thread_data[0][1]
    thread_response = requests.get(example_thread_url)
    if thread_response.status_code == 200:
        thread_soup = BeautifulSoup(thread_response.text, 'html.parser')
        # Extract post content (Discourse uses 'div.post' or similar)
        posts = thread_soup.select('div.post')
        for post in posts:
            # Extract username and content if available
            username_elem = post.select_one('span.username')
            username = username_elem.text.strip() if username_elem else "Unknown"
            content_elem = post.select_one('div.post-body')
            content = content_elem.text.strip() if content_elem else "[No content]"
            print(f"User: {username}\n{content}\n---")
