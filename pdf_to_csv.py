#import pdfplumber
import uuid
import csv

#county_id,county_code,county_name,constituency_id,constituency_code,constituency_name,ward_id,ward_code,ward_name,polling_station_id,polling_station_code,polling_station_name

def extract_data_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        polling_station_id_old = ''
        for page_num, page in enumerate(pdf.pages, 1):
            if page_num > 663:
                tables = page.extract_tables()
                county_data = {}
                
                for table in tables:
                    for row in table[2:]:  # Skip header if present
                        try:
                            county_code = int(row[0])
                            county_name = row[1].upper().replace('/', ' ')
                            county_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f'{county_code}'))
                            constituency_code = int(row[2])
                            constituency_name = row[3].upper()
                            constituency_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f'{county_id}-{constituency_code}'))
                            ward_code = int(row[4])
                            ward_name = row[5].upper()
                            ward_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, (f'{constituency_id}-{ward_code}')))
                            polling_station_code = int(row[6].replace('RSE ',''))
                            polling_station_name = row[7].upper()
                            polling_station_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, (f'{ward_id}-{polling_station_code}')))

                            if county_name not in county_data:
                                county_data[county_name] = []
                            
                            if polling_station_id_old != polling_station_id and county_name != 'NYAMIRA':
                                # Append data to the specific county's list
                                county_data[county_name].append({
                                    'county_id': county_id,
                                    'county_code': county_code,
                                    'county_name': county_name,
                                    'constituency_id': constituency_id,
                                    'constituency_code': constituency_code,
                                    'constituency_name': constituency_name,
                                    'ward_id': ward_id,
                                    'ward_code': ward_code,
                                    'ward_name': ward_name,
                                    'polling_station_id': polling_station_id,
                                    'polling_station_code': polling_station_code,
                                    'polling_station_name': polling_station_name
                                })
                                polling_station_id_old = polling_station_id
                        except Exception as e:
                            print(f"Error processing row on page {page_num}: {row} {e}")

                # Write data for each county after processing each page
                for county_name, records in county_data.items():
                    print(f"Processing page {page_num} [{county_name}]")
                    csv_file_path = f"data/{county_name}.csv"
                    mode = 'a' if page_num > 1 else 'w'  # Append if not the first page
                    try:
                        with open(csv_file_path, mode, newline='', encoding='utf-8') as csvfile:
                            fieldnames = ['county_id', 'county_code', 'county_name', 
                                        'constituency_id', 'constituency_code', 'constituency_name', 
                                        'ward_id', 'ward_code', 'ward_name', 
                                        'polling_station_id', 'polling_station_code', 'polling_station_name']
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            
                            if mode == 'w':  # Write header only for the first page
                                writer.writeheader()
                            for record in records:
                                writer.writerow(record)                        
                    except PermissionError:
                        print(f"Could not write to {csv_file_path}. Check if the file is open elsewhere.")
                    except Exception as e:
                        print(f"An error occurred while writing {county_name}: {e}")

if __name__ == '__main__':
    #pdf_path = 'polling_stations.pdf'
    #extract_data_from_pdf(pdf_path)
    voter_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f'27633615'))
    print(voter_id)
