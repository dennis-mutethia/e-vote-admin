import pdfplumber, uuid

# from utils.db import Db

# db = Db()

# def extract_data_from_pdf(pdf_path):
#     with pdfplumber.open(pdf_path) as pdf:        
#         county_id_old = ''
#         constituency_id_old = ''
#         ward_id_old = ''
#         polling_station_id_old = ''
#         for page in pdf.pages:
#             # Extract tables from each page
#             tables = page.extract_tables()
#             for table in tables:
#                 for row in table[2:]:  # Skip header if present
#                     print(row)
#                     county_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, (f'{int(row[0])}')))
#                     constituency_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, (f'{county_id}-{int(row[2])}')))
#                     ward_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, (f'{constituency_id}-{int(row[4])}')))
#                     polling_station_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, (f'{ward_id}-{int(row[6])}')))
#                     if county_id != county_id_old:
#                         db.insert_county(county_id, int(row[0]), row[1].upper())
#                         county_id_old = county_id
#                     if constituency_id != constituency_id_old:
#                         db.insert_constituency(constituency_id, int(row[2]), county_id, row[3].upper())
#                         constituency_id_old = constituency_id
#                     if ward_id != ward_id_old:
#                         db.insert_ward(ward_id, int(row[4]), constituency_id, row[5].upper())
#                         ward_id_old = ward_id
#                     if polling_station_id != polling_station_id_old:
#                         db.insert_polling_station(polling_station_id, int(row[6]), ward_id, row[7].upper())
#                         db.create_partition('voters', polling_station_id)
#                         db.create_partition('votes', polling_station_id)
#                         db.create_partition('sms_codes', polling_station_id)
#                         polling_station_id_old = polling_station_id

def extract_data_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:        
        county_id_old = ''
        constituency_id_old = ''
        ward_id_old = ''
        polling_station_id_old = ''
        for page in pdf.pages:
            # Extract tables from each page
            tables = page.extract_tables()
            for table in tables:
                for row in table[2:]:  # Skip header if present
                    print(row)
                    county_code = int(row[1])
                    county_name = row[1].upper()
                    county_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f'{county_code}'))
                    constituency_code = int(row[2])
                    constituency_name = row[3].upper()
                    constituency_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f'{county_id}-{constituency_code}'))
                    ward_code = int(row[4])
                    ward_name = row[5].upper()
                    ward_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, (f'{constituency_id}-{ward_code}')))
                    polling_station_code = int(row[6])
                    polling_station_name = row[7].upper()
                    polling_station_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, (f'{ward_id}-{polling_station_code}')))

if __name__ == '__main__':
    pdf_path = 'polling_stations.pdf'
    extract_data_from_pdf(pdf_path)
