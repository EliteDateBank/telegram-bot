import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Send request to Google
response = requests.get("https://www.google.com")

# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")
title = soup.title.string
preview = soup.get_text()[:300]

# Print to console
print("Status:", response.status_code)
print("Page Title:", title)
print("\nPreview of content:")
print(preview)

# Create a filename with date and time
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"google_output_{timestamp}.txt"

# Save the output to a text file
with open(filename, "w", encoding="utf-8") as f:
    f.write(f"Status: {response.status_code}\n")
    f.write(f"Page Title: {title}\n\n")
    f.write("Preview of content:\n")
    f.write(preview)

print(f"\n✅ Output saved to {filename}")
