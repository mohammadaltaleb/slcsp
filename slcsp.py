"""
slcsp.py

Author: Mohammad Altaleb
Email: mohammadaltaleb@gmail.com

This scripts finds the slcsp for a given set of Zip Codes
"""

import csv


def get_rate_area_rates(file_path):
    """
    This function reads plans.csv file and parses its data into 
    a dictionary

    Args:
        file_path: the path to plans.csv file
    
    Returns:
        a dictionary mapping each rate area for Silver plans into a set of 
        rates
    """
    rate_area_rates = dict()
    with open(file_path, 'r') as plans_file:
        csv_reader = csv.DictReader(plans_file, delimiter=',')
        for line in csv_reader:
            if line['metal_level'] != 'Silver':
                continue

            rate = (float)(line['rate'])
            rate_area = f"{line['state']} {line['rate_area']}"
            
            if not rate_area in rate_area_rates:
                rate_area_rates[rate_area] = set()
            rate_area_rates[rate_area].add(rate)
    return rate_area_rates


def get_zip_rate_areas(file_path):
    """
    This function reads zips.csv file and parses its data into
    a dictionary

    Args:
        file_path: the path to zips.csv file
    
    Returns:
        a dictionary mapping each zip code into a set of rate areas
    """
    zip_rate_areas = dict()
    with open(file_path, 'r') as zip_codes_file:
        csv_reader = csv.DictReader(zip_codes_file, delimiter=',')
        for line in csv_reader:
            zipcode = line['zipcode']
            rate_area = f"{line['state']} {line['rate_area']}"

            if not zipcode in zip_rate_areas:
                zip_rate_areas[zipcode] = set()
            zip_rate_areas[zipcode].add(rate_area)
    return zip_rate_areas


def read_slcsp_zip_codes(file_path):
    """
    This function reads zip codes in slcsp.csv

    Args:
        file_path: the path to slcsp.csv file

    Returns:
        a list of the zip codes in the file
    """
    zip_codes = []
    with open(file_path, 'r') as zip_codes_file:
        csv_reader = csv.DictReader(zip_codes_file, delimiter=',')
        for line in csv_reader:
            zip_codes.append(line['zipcode'])
    return zip_codes


def find_slcsp(rate_area_rates, zip_rate_areas, slcsp_zip_codes):
    """
    This function finds and prints the slcsp for each zip code in a list

    Args:
        rate_area_rates: a dictionary mapping rate areas into rate sets
        zip_rate_areas: a dictionary mapping zip codes into rate area sets
        slcsp_zip_codes: a list of zip codes to find their slcsp
    """
    for code in slcsp_zip_codes:
        slcsp = ''
        if len(zip_rate_areas[code]) == 1:
            rate_area = zip_rate_areas[code].pop()
            if rate_area in rate_area_rates:
                rates = sorted(rate_area_rates[rate_area])
                if len(rates) > 1:
                    slcsp = rates[1]
        print(f'{code},{slcsp}')


def main():
    rate_area_rates = get_rate_area_rates('plans.csv')
    zip_rate_areas = get_zip_rate_areas('zips.csv')
    slcsp_zip_codes = read_slcsp_zip_codes('slcsp.csv')
    find_slcsp(rate_area_rates, zip_rate_areas, slcsp_zip_codes)


if __name__ == '__main__':
    main()
