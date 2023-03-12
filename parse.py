import argparse
import sys

def get_args():
    parser = argparse.ArgumentParser(description='Supported modes - crack, gen. For more details enter crack -h or gen -h')
    parser.add_argument('mode', metavar='mode', type=str, choices=['crack', 'gen'], help='Select a function - crack/gen')
    if len(sys.argv) < 2:
        print('Plese select a mode - options: crack, gen')
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

    args = parser.parse_args()
    return args

