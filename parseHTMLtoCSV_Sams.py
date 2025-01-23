import csv
import time
import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    """Fetch the HTML content from the given URL."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise ValueError(f"Failed to fetch the URL. HTTP Status Code: {response.status_code}")

def parse_sams_club_addresses_to_csv_from_url(url, output_csv):
    start_time = time.time()  # Start timing

    # Fetch HTML content from the URL
    print("Fetching HTML content from the web...")
    html_content = fetch_html(url)

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the table by its ID
    table = soup.find('table', id='tablepress-37')
    if not table:
        raise ValueError("Table with id 'tablepress-37' not found in the fetched HTML content.")
    
    # Initialize a list to store the addresses
    addresses = []
    total_rows = 0
    valid_rows = 0
    
    # Iterate through the rows in the table's body
    print("Parsing table data...")
    for row in table.find('tbody').find_all('tr'):
        total_rows += 1
        # Extract columns for each row
        columns = row.find_all('td')
        if len(columns) >= 5:  # Ensure there are enough columns
            store_name = columns[0].get_text(strip=True)
            street = columns[1].get_text(strip=True)
            city = columns[2].get_text(strip=True)
            state = columns[3].get_text(strip=True)
            zip_code = columns[4].get_text(strip=True)
            
            # Append the address as a dictionary
            addresses.append({
                "Store Name": store_name,
                "Street": street,
                "City": city,
                "State": state,
                "Zip Code": zip_code,
            })
            valid_rows += 1
    
    # Write addresses to a CSV file
    print(f"Writing data to {output_csv}...")
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Store Name", "Street", "City", "State", "Zip Code"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(addresses)
    
    # End timing
    end_time = time.time()
    time_taken = end_time - start_time
    
    # Logging summary
    print("Summary of Extraction:")
    print(f" - Total rows processed: {total_rows}")
    print(f" - Valid rows extracted: {valid_rows}")
    print(f" - Required field coverage: {100 * valid_rows / total_rows:.2f}%")
    print(f" - Time taken: {time_taken:.2f} seconds")
    print(f" - Output CSV file: {output_csv}")

# Example usage
url = "https://brilliantmaps.com/us-locations/sams-club-locations/"
output_csv = "sams_club_locations.csv"
try:
    parse_sams_club_addresses_to_csv_from_url(url, output_csv)
except Exception as e:
    print(f"Error: {e}")
