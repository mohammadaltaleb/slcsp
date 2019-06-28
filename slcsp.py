"""
slcsp.py

Author: Mohammad Altaleb
Email: mohammadaltaleb@gmail.com

This scripts finds the slcsp for a given set of Zip Codes
"""

import csv

from argparse import ArgumentParser


def read_argument():
    """
    reads the zip codes passed to the script

    Returns:
        the passed zip codes as a list or None in no argument was passed
    """
    parser = ArgumentParser()
    parser.add_argument('zipcodes', nargs='?')
    args = parser.parse_args()
    if(args.zipcodes):
        return args.zipcodes.split(',')
    return None


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


def get_second_smallest(values):
    """
    This function returns the second lowest value in a list of numbers

    Args:
        values: a list of floats
    
    Returns:
        the second lowst number in values
    """
    smallest, second_smallest = float('inf'), float('inf')
    for value in values:
        if value <= smallest:
            smallest, second_smallest = value, smallest
        elif value < second_smallest:
            second_smallest = value
    return second_smallest


def find_and_print_slcsp(rate_area_rates, zip_rate_areas, slcsp_zip_codes):
    """
    This function finds and prints the slcsp for each zip code in a list

    Args:
        rate_area_rates: a dictionary mapping rate areas into rate sets
        zip_rate_areas: a dictionary mapping zip codes into rate area sets
        slcsp_zip_codes: a list of zip codes to find their slcsp
    """
    print('zipcode,rate')
    for code in slcsp_zip_codes:
        slcsp = ''
        if code in zip_rate_areas and len(zip_rate_areas[code]) == 1:
            rate_area = zip_rate_areas[code].pop()
            if rate_area in rate_area_rates:
                rates = rate_area_rates[rate_area]
                if len(rates) > 1:
                    slcsp = f'{get_second_smallest(rates):.2f}'
        print(f'{code},{slcsp}')


def main(slcsp_zip_codes):
    rate_area_rates = get_rate_area_rates('plans.csv')
    zip_rate_areas = get_zip_rate_areas('zips.csv')
    if not slcsp_zip_codes:
        slcsp_zip_codes = read_slcsp_zip_codes('slcsp.csv')
    find_and_print_slcsp(rate_area_rates, zip_rate_areas, slcsp_zip_codes)


if __name__ == '__main__':
    zipcodes = read_argument()
    main(zipcodes)
