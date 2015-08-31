import os, sys, getopt, csv
from street_list import StreetList

def main(argv):
    usage_string = 'python tools/street_finder --streets_dir data/streets'
    streets_dir = ''

    try:
        opts, args = getopt.getopt(argv,"h", ["streets_dir="])
    except getopt.GetoptError:
        print usage_string
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print usage_string
        elif opt == '--streets_dir':
            streets_dir = arg

    if not os.path.exists(streets_dir):
        print "streets dir missing"
        sys.exit(2)

    with open('{}/street_segments.csv'.format(streets_dir), 'wb') as csvfile:
        headers = ['id','street_name','bounds','borough_code','zip_code','kml_id']
        csv_writer = csv.DictWriter(csvfile, fieldnames=headers)
        csv_writer.writeheader()
        print 'reading streets.kml'
        street_list = StreetList(streets_dir)
        for street in street_list:
            print street
            print street['street_name']
            if street['borough_code'] == '1':
                csv_writer.writerow(street)

if __name__ == "__main__":
    main(sys.argv[1:])
