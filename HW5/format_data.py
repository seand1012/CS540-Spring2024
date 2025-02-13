import csv

def main():
    data = load_data('Frozen Lake Data.csv')
    format_data(data, 'hw5.csv')
    

def load_data(filepath):
    with open(filepath, newline = '') as csvfile:
        reader = csv.DictReader(csvfile)
        next(reader)
        data = list(reader) 
    return data
    
    #return data

def format_data(data, output_file):
    cleaned_data = []
    
    start_year = 1855
    end_year = 2021
    
    for row in data:
        year = int(row['Winter'][:4])
        days = row['Days of Ice Cover']
        # checks if year is within year range,
        # days is not null, and if days is not a range
        if start_year <= year <= end_year and days and days != '-':
            cleaned_data.append([year, int(days)])
    
    aggregate_data = {}
    
    for row in cleaned_data:
        year, days = row
        if year in aggregate_data:
            aggregate_data[year] += days
        else:
            aggregate_data[year] = days
    
    with open(output_file, 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(['year', 'days'])
        for year, days in aggregate_data.items():
            writer.writerow([year,days])

if __name__ == "__main__":
    main()