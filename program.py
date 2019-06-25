def get_rate_area_rates():
    rate_area_rates = dict()
    with open('plans.csv', 'r') as plans_file:
        next(plans_file)
        for line in plans_file:
            plan_parts = line.strip().split(',')
            if plan_parts[2] != 'Silver':
                continue

            rate = (float)(plan_parts[3])
            rate_area = f'{plan_parts[1]} {plan_parts[4]}'
            
            if not rate_area in rate_area_rates:
                rate_area_rates[rate_area] = set()
            rate_area_rates[rate_area].add(rate)
    return rate_area_rates


def get_zip_rate_areas():
    zip_rate_areas = dict()
    with open('zips.csv', 'r') as zip_codes_file:
        next(zip_codes_file)
        for line in zip_codes_file:
            zip_code_parts = line.strip().split(',')
            zipcode = zip_code_parts[0]
            rate_area = f'{zip_code_parts[1]} {zip_code_parts[4]}'

            if not zipcode in zip_rate_areas:
                zip_rate_areas[zipcode] = set()
            zip_rate_areas[zipcode].add(rate_area)
    return zip_rate_areas


def read_slcsp_zip_codes():
    zip_codes = []
    with open('slcsp.csv', 'r') as zip_codes_file:
        next(zip_codes_file)
        for line in zip_codes_file:
            zip_codes.append(line.strip().split(',')[0])
    return zip_codes


def main():
    rate_area_rates = get_rate_area_rates()
    zip_rate_areas = get_zip_rate_areas()
    test_data = read_slcsp_zip_codes()
    for code in test_data:
        slcsp = ''
        if len(zip_rate_areas[code]) == 1:
            rate_area = zip_rate_areas[code].pop()
            if rate_area in rate_area_rates:
                rates = sorted(rate_area_rates[rate_area])
                if len(rates) > 1:
                    slcsp = rates[1]
        print(f'{code},{slcsp}')


if __name__ == '__main__':
    main()
