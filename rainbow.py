import hashlib
import subprocess
import random
import string
from parse import get_args
from table import RainbowTable


# MD5hash = '21232f297a57a5a743894a0e4a801fc3'
# SHA256hash = 'b1dff32c41ff49d3c05a9e4e2abe95acfadd6212c0cd763f25369972a2a09b43'

# def find_hash_type(hash: str) -> str:
#     types = subprocess.check_output(['python3 hash-id.py ' + hash], shell=True).strip()
#     types = str(types)
#     index = types.find(']')
#     types = types[index + 2:]


#     hash_type = ''
#     counter = 0
#     while True:
#         if types[counter] == '[':
#             break
#         hash_type = hash_type + types[counter]
#         counter += 1

#     hash_type = hash_type[0:-2]

#     return hash_type

# def enter_hash_type():
#     type = input('Enter hash type: ')
#     return type

# hash_type = enter_hash_type()
# print(hash_type)
# hash_type = find_hash_type(MD5hash)
# print(hash_type)


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
        plaintextKey = (int(hash, 16) * col) % (26 ** n)
        plaintext = ""
        for _ in range(n):
            plaintext += string.ascii_lowercase[plaintextKey % 26]
            plaintextKey //= 26
        return plaintext
    return result

def reduce_upper(n):
    def result(hash, col):
        plaintextKey = (int(hash, 16) * col) % (26 ** n)
        plaintext = ""
        for _ in range(n):
            plaintext += string.ascii_uppercase[plaintextKey % 26]
            plaintextKey //= 26
        return plaintext
    return result

def reduce_letters(n):
    def result(hash, col):
        plaintextKey = (int(hash, 16) * col) % (52 ** n)
        plaintext = ""
        for _ in range(n):
            plaintext += string.ascii_letters[plaintextKey % 52]
            plaintextKey //= 52
        return plaintext
    return result

def reduce_special_chars(n):
    def result(hash, col):
        plaintextKey = (int(hash, 16) * col) % (100 ** n)
        plaintext = ""
        for _ in range(n):
            plaintext += string.printable[plaintextKey % 100]
            plaintextKey //= 100
        return plaintext
    return result

def reduce_alphanumeric(n):
    def result(hash, col):
        plaintextKey = (int(hash, 16) * col) % (62 ** n)
        plaintext = ""
        for _ in range(n):
            plaintext += (string.ascii_letters + string.digits)[plaintextKey % 62]
            plaintextKey //= 62
        return plaintext
    return result

def reduce_all(n):
    def result(hash, col):
        plaintextKey = (int(hash, 16) * col) % (110 ** n)
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
    elif input == 'alphanumeric':
        return reduce_alphanumeric(n), gen_alphanumeric(n)
    elif input == 'all':
        return reduce_all(n), gen_all(n)
    else:
        print("This reduction function is not supported")
        exit(1)
    

args = get_args()

print(args.mode)

if args.mode == "crack":
    print("cracking mode")
    
    
    
elif args.mode == "gen":
    print("generating mode")
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
    print(hashing_alg('hello'.encode('utf-8')).hexdigest())
    
    reduction_func, gen_func = get_reduction_func(args.restrictions, args.length)
    print(reduction_func('21232f297a57a5a743894a0e4a801fc3', 1), gen_func())
    
    table = RainbowTable(hashing_alg, args.length, args.restrictions, reduction_func, gen_func)
    table.gen_table(1000)
    
    table.load_table("table.pickle")
    
    table.export_csv()