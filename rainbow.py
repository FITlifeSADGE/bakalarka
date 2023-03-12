import hashlib
import random
import string
from parse import get_args
from table import RainbowTable
import time

# Word generator functions
def gen_lower(n):
    def result():
        password = ""
        for _ in range(n):
            password += random.choice(string.ascii_lowercase)
        return password
    return result

def gen_upper(n):
    def result():
        password = ""
        for _ in range(n):
            password += random.choice(string.ascii_uppercase)
        return password
    return result

def gen_letters(n):
    def result():
        password = ""
        for _ in range(n):
            password += random.choice(string.ascii_letters)
        return password
    return result

def gen_special_chars(n):
    def result():
        password = ""
        for _ in range(n):
            password += random.choice(string.printable)
        return password
    return result

def gen_alphanumeric(n):
    def result():
        password = ""
        for _ in range(n):
            password += random.choice(string.ascii_letters + string.digits)
        return password
    return result

def gen_all(n):
    def result():
        password = ""
        for _ in range(n):
            password += random.choice(string.digits + string.printable)
        return password
    return result


# Reduction functions
def reduce_lower(n):
    def result(hash, col):
        plaintextKey = (int(hash, 16) ^ col) % (26 ** n)
        plaintext = ""
        for _ in range(n):
            plaintext += string.ascii_lowercase[plaintextKey % 26]
            plaintextKey //= 26
        return plaintext
    return result

def reduce_upper(n):
    def result(hash, col):
        plaintextKey = (int(hash, 16) ^ col) % (26 ** n)
        plaintext = ""
        for _ in range(n):
            plaintext += string.ascii_uppercase[plaintextKey % 26]
            plaintextKey //= 26
        return plaintext
    return result

def reduce_letters(n):
    def result(hash, col):
        plaintextKey = (int(hash, 16) ^ col) % (52 ** n)
        plaintext = ""
        for _ in range(n):
            plaintext += string.ascii_letters[plaintextKey % 52]
            plaintextKey //= 52
        return plaintext
    return result

def reduce_special_chars(n):
    def result(hash, col):
        plaintextKey = (int(hash, 16) ^ col) % (100 ** n)
        plaintext = ""
        for _ in range(n):
            plaintext += string.printable[plaintextKey % 100]
            plaintextKey //= 100
        return plaintext
    return result

def reduce_alphanumeric(n):
    def result(hash, col):
        plaintextKey = (int(hash, 16) ^ col) % (62 ** n)
        plaintext = ""
        for _ in range(n):
            plaintext += (string.ascii_letters + string.digits)[plaintextKey % 62]
            plaintextKey //= 62
        return plaintext
    return result

def reduce_all(n):
    def result(hash, col):
        plaintextKey = (int(hash, 16) ^ col) % (110 ** n)
        plaintext = ""
        for _ in range(n):
            plaintext += (string.printable + string.digits)[plaintextKey % 110]
            plaintextKey //= 110
        return plaintext
    return result

def get_hashing_alg(input: str):
    if input == 'md5':
        return hashlib.md5
    elif input == 'sha1':
        return hashlib.sha1
    elif input == 'sha256':
        return hashlib.sha256
    elif input == 'sha512':
        return hashlib.sha512
    else:
        print("This hashing algorithm is not supported")
        exit(1)
        
def get_reduction_func(input: str, n: int):
    if input == 'lowercase':
        return reduce_lower(n), gen_lower(n)
    elif input == 'uppercase':
        return reduce_upper(n), gen_upper(n)
    elif input == 'letters':
        return reduce_letters(n), gen_letters(n)
    elif input == 'special':
        return reduce_special_chars(n), gen_special_chars(n)
    elif input == 'alphanum':
        return reduce_alphanumeric(n), gen_alphanumeric(n)
    elif input == 'all':
        return reduce_all(n), gen_all(n)
    else:
        print("This reduction function is not supported")
        exit(1)
    

args = get_args()
if args.mode == "crack":
    table = RainbowTable(hashlib.md5, 10, reduce_lower(5), gen_lower(5), "md5", "lowercase", 5)
    table.load_from_cvs(filename=args.table)
    hashing_alg = get_hashing_alg(table.alg)
    reduction_func, _ = get_reduction_func(table.rest, table.len)
    table.hash_func = hashing_alg
    table.chain_len = int(table.get_chain_len())
    table.reduction_func = reduction_func
    
    print(table.crack(args.hash))
    
    
    
elif args.mode == "gen":
    if args.length < 1:
        print("Length must be greater than 0")
        exit(1)
    if args.columns < 1:
        print("Number of columns must be greater than 0")
        exit(1)
    if args.rows < 1:
        print("Number of rows must be greater than 0")
        exit(1)
    hashing_alg = get_hashing_alg(args.algorithm)
    reduction_func, gen_func = get_reduction_func(args.restrictions, args.length)
    
    table = RainbowTable(hashing_alg, args.columns, reduction_func, gen_func, args.algorithm, args.restrictions, args.length)
    table.gen_table(rows=args.rows, file="table.csv")
    #table.load_from_cvs(filename="lowercase_md5_5.csv")
    lowercase_md5_5 = ['8b712063688bfd433d3362f2633f9a0a', 'c67fe96a412465a5573125fb88ff5a65', '6656910800c58e1e9e6bc8230805a381', '181fddda8e43336070176f2df7c90a55']
    
    uppercase_md5_5 = ['c423ecf794014e15e584585eb0d9f150', '8abb5fdd82d4289310fb9396d9a61a6c', '7225950dd173633a9d577a8eb17c2706', '6ef15de7cf0589256fdc4bdddfabdeed']
    
    #python3 rainbow.py gen 5 5000 10000 lowercase 
    # for hash in lowercase_md5_5:
    #     start = time.time()
    #     print(table.crack(hash))
    #     print("""Found in {0} seconds""".format(time.time() - start))
    
    # python3 rainbow.py gen 5 10000 20000 uppercase md5
    # for hash in uppercase_md5_5:
    #     start = time.time()
    #     print(table.crack(hash))
    #     print("""Found in {0} seconds""".format(time.time() - start))
    