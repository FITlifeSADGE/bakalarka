import argparse
import sys

def get_args():
    parser = argparse.ArgumentParser(description='Supported modes - crack, gen, search, load. For more details enter crack -h, gen -h,search -h or load-h' )
    parser.add_argument('mode', metavar='mode', type=str, choices=['crack', 'gen', 'search', 'load'], help='Select a function - crack/gen/search')
    if len(sys.argv) < 2:
        print('Plese select a mode - options: crack, gen, search, load')
        exit(1)
    if sys.argv[1] == 'crack':
        parser.add_argument('hash', metavar='hash', type=str, help='Enter the hash you want to crack')
        parser.add_argument('table', metavar='table', type=str, help='Enter the name of a table you want to use')
    elif sys.argv[1] == 'gen':
        parser.add_argument('length', metavar='length', type=int, help='Enter the max length of plaintext password')
        parser.add_argument('columns', metavar='columns', type=int, help='Enter the length of a chain')
        parser.add_argument('rows', metavar='rows', type=int, help='Enter the amount of rows')
        parser.add_argument('restrictions', metavar='restrictions', type=str, choices=['lowercase', 'uppercase', 'letters', 'special', 'alphanum', 'all'] , help='Enter password restrictions - lowercase, uppercase, lettters, special, alphanum, all')
        parser.add_argument('algorithm', metavar='algorithm', type=str, help='Select a hashing algorihm, e.g. md5, sha1, sha256, sha512')
        parser.add_argument('filename', metavar='filename', type=str, help='Enter the name of a file you want to save the table to', default='table.csv')
    elif sys.argv[1] == 'search':
        parser.add_argument('algorithm', metavar='algorithm', type=str, help='Select a hashing algorihm, e.g. md5, sha1, sha256, sha512')
        parser.add_argument('restrictions', metavar='restrictions', type=str, choices=['lowercase', 'uppercase', 'letters', 'special', 'alphanum', 'all'] , help='Enter password restrictions - lowercase, uppercase, lettters, special, alphanum, all')
        parser.add_argument('length', metavar='length', type=int, help='Enter the max length of plaintext password')
    elif sys.argv[1] == 'load':
        parser.add_argument('path', metavar='path', type=str, help='Enter the path to the table you want to download')
        parser.add_argument('ID', metavar='ID', type=str, help='Enter the ID of the table you want to download')
    args = parser.parse_args()
    return args

