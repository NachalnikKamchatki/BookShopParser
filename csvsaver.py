import csv

def csv_write_books_data(data):
    if data and isinstance(data, list):
        with open('books_data.csv', 'w', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(data[0].keys())
            for item in data:
                csv_writer.writerow(item.values())
    else:
        print('data is incorrect!!!')

