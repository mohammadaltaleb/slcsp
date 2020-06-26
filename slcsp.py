#  The MIT License (MIT)
#
#  Copyright (c) 2020 Mohammad Altaleb
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import csv

from argparse import ArgumentParser


def read_argument():
    """
    reads the zip codes passed to the script

    Returns:
        the passed zip codes as a list or None in no argument was passed
    """
    parser = ArgumentParser()
    parser.add_argument("zipcodes", nargs="?")
    args = parser.parse_args()
    if args.zipcodes:
        return args.zipcodes.split(",")
    return None


def get_rate_area_rates(file_path):
    """
    reads plans.csv file and returns the content as a dictionary

    Args:
        file_path: the path to plans.csv file

    Returns:
        a dictionary mapping each rate area for Silver plans into a set of
        rates
    """
    rate_area_rates = dict()
    with open(file_path, "r") as plans_file:
        csv_reader = csv.DictReader(plans_file, delimiter=",")
        for line in csv_reader:
            if line["metal_level"] != "Silver":
                continue

            rate = float(line["rate"])
            rate_area = f"{line['state']} {line['rate_area']}"

            if not rate_area in rate_area_rates:
                rate_area_rates[rate_area] = set()
            rate_area_rates[rate_area].add(rate)
    return rate_area_rates


def get_zip_rate_areas(file_path):
    """
    reads zips.csv file and returns the content as a dictionary

    Args:
        file_path: the path to zips.csv file
    
    Returns:
        a dictionary mapping each zip code into a set of rate areas
    """
    zip_rate_areas = dict()
    with open(file_path, "r") as zip_codes_file:
        csv_reader = csv.DictReader(zip_codes_file, delimiter=",")
        for line in csv_reader:
            zipcode = line["zipcode"]
            rate_area = f"{line['state']} {line['rate_area']}"

            if zipcode not in zip_rate_areas:
                zip_rate_areas[zipcode] = set()
            zip_rate_areas[zipcode].add(rate_area)
    return zip_rate_areas


def read_slcsp_zip_codes(file_path):
    """
    reads zip codes in slcsp.csv

    Args:
        file_path: the path to slcsp.csv file

    Returns:
        a list of the zip codes in the file
    """
    zip_codes = []
    with open(file_path, "r") as zip_codes_file:
        csv_reader = csv.DictReader(zip_codes_file, delimiter=",")
        for line in csv_reader:
            zip_codes.append(line["zipcode"])
    return zip_codes


def get_second_smallest(values):
    """
    returns the second lowest value in a list of numbers

    Args:
        values: a list of floats
    
    Returns:
        the second lowst number in values
    """
    smallest, second_smallest = float("inf"), float("inf")
    for value in values:
        if value <= smallest:
            smallest, second_smallest = value, smallest
        elif value < second_smallest:
            second_smallest = value
    return second_smallest


def find_and_print_slcsp(rate_area_rates, zip_rate_areas, slcsp_zip_codes):
    """
    finds and prints the slcsp for each zip code in a list

    Args:
        rate_area_rates: a dictionary mapping rate areas into rate sets
        zip_rate_areas: a dictionary mapping zip codes into rate area sets
        slcsp_zip_codes: a list of zip codes to find their slcsp
    """
    print("zipcode,rate")
    for code in slcsp_zip_codes:
        slcsp = ""
        if code in zip_rate_areas and len(zip_rate_areas[code]) == 1:
            rate_area = zip_rate_areas[code].pop()
            if rate_area in rate_area_rates:
                rates = rate_area_rates[rate_area]
                if len(rates) > 1:
                    slcsp = f"{get_second_smallest(rates):.2f}"
        print(f"{code},{slcsp}")


def main(slcsp_zip_codes):
    rate_area_rates = get_rate_area_rates("plans.csv")
    zip_rate_areas = get_zip_rate_areas("zips.csv")
    if not slcsp_zip_codes:
        slcsp_zip_codes = read_slcsp_zip_codes("slcsp.csv")
    find_and_print_slcsp(rate_area_rates, zip_rate_areas, slcsp_zip_codes)


if __name__ == "__main__":
    zipcodes = read_argument()
    main(zipcodes)
