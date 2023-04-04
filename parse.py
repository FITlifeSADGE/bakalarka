import argparse
import sys

def get_args():
    parser = argparse.ArgumentParser(description='Supported modes - crack, gen, search, load. For more details enter crack -h, gen -h,search -h or load-h', add_help=False )
    parser.add_argument('mode', metavar='mode', type=str, choices=['crack', 'gen', 'search', 'load'], help='Select a function - crack/gen/search')
    if len(sys.argv) < 2:
        print('Plese select a mode - options: crack, gen, search, load')
        exit(1)
    if sys.argv[1] == 'crack':
        parser.add_argument('hash', metavar='hash', type=str, help='Enter the hash you want to crack')
        parser.add_argument('table', metavar='table', type=str, help='Enter the name of a table you want to use')
        parser.add_argument('-p', '--path', metavar='path', type=str, help='Enter the path to the table', default='/usr/share/collections/RTables/')
        if len(sys.argv) < 4:
            print('''hash algorithms implemented: 
                  md5 HashLen=16
                  sha1 HashLen=20
                  sha256 HashLen=32
                  sha512 HashLen=64
                  
                  examples:
                  python3 rainbow.py crack 098f6bcd4621d373cade4e832627b4f6 table.csv [-p path]''')
    elif sys.argv[1] == 'gen':
        parser.add_argument('algorithm', metavar='hash_algorithm', type=str, help='Select a hashing algorihm, e.g. md5, sha1, sha256, sha512')
        parser.add_argument('restrictions', metavar='charset', type=str, choices=['lowercase', 'uppercase', 'letters', 'special', 'alphanum', 'all', 'test'] , help='Enter password restrictions - lowercase, uppercase, lettters, special, alphanum, all')
        parser.add_argument('length_min', metavar='plaintext_length_min', type=int, help='Enter the min length of plaintext password')
        parser.add_argument('length_max', metavar='plaintext_length_max', type=int, help='Enter the max length of plaintext password')
        parser.add_argument('columns', metavar='chain_len', type=int, help='Enter the length of a chain')
        parser.add_argument('rows', metavar='chain_num', type=int, help='Enter the amount of rows')
        parser.add_argument('filename', metavar='filename', type=str, help='Enter the name of a file you want to save the table to', default='table.csv')
        if len(sys.argv) < 9:
            print('''hash algorithms implemented: 
                  md5 HashLen=16
                  sha1 HashLen=20
                  sha256 HashLen=32
                  sha512 HashLen=64
                  
                  examples:
                  python3 rainbow.py gen md5 lowercase 5 10 1000 1000 table.csv''')
    elif sys.argv[1] == 'search':
        parser.add_argument('algorithm', metavar='hash_algorithm', type=str, help='Select a hashing algorihm, e.g. md5, sha1, sha256, sha512')
        parser.add_argument('restrictions', metavar='charset', type=str, choices=['lowercase', 'uppercase', 'letters', 'special', 'alphanum', 'all'] , help='Enter password restrictions - lowercase, uppercase, lettters, special, alphanum, all')
        parser.add_argument('length_min', metavar='plaintext_length_min', type=int, help='Enter the max length of plaintext password')
        parser.add_argument('length_max', metavar='plaintext_length_max', type=int, help='Enter the max length of plaintext password')
        if len(sys.argv) < 6:
            print('''hash algorithms implemented: 
                  md5 HashLen=16
                  sha1 HashLen=20
                  sha256 HashLen=32
                  sha512 HashLen=64
                  
                  examples:
                  python3 rainbow.py search md5 lowercase 5 10''')
    elif sys.argv[1] == 'load':
        parser.add_argument('path', metavar='path', type=str, help='Enter the path to the table you want to download')
        parser.add_argument('ID', metavar='ID', type=str, help='Enter the ID of the table you want to download')
        if len(sys.argv) < 4:
            print('''
                  examples:
                  python3 rainbow.py load . 1''')
    args = parser.parse_args()
    return args

