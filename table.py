import time
import pickle
import csv
from tqdm import tqdm
from os import system, name

CSV_FIELDNAMES = ['start_point', 'endpoint_hash']

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

class RainbowTable:
    def __init__(self, hash_func, chain_len, reduction_func, gen_func, alg, restrictions, length):
        self.table = {}
        self.hash_func = hash_func
        self.chain_len = chain_len
        self.gen_func = gen_func
        self.reduction_func = reduction_func
        self.alg = alg
        self.rest = restrictions
        self.len = length
        
    def gen_table(self, file="table.csv", rows=1000):
        print("Generating table...")
        startTime = time.time()
        for i in tqdm(range(rows)):
            start = self.gen_func()
            plainText = start
            for col in range(self.chain_len):
                hashcode = self.hash_func(plainText.encode('utf-8')).hexdigest()
                plainText = self.reduction_func(hashcode, col)
            self.table[hashcode] = start
            
        self.table['chain_len'] = self.chain_len
        self.table['alg'] = self.alg
        self.table['rest'] = self.rest
        self.table['len'] = self.len
        
        with open(file, 'w') as table:
            writer = csv.DictWriter(table, fieldnames=CSV_FIELDNAMES) 
            writer.writeheader()
            for k, v in self.table.items():
                writer.writerow({CSV_FIELDNAMES[0]: v, CSV_FIELDNAMES[1]: k})
        
        elapsed = time.time() - startTime
        print("Done generating in {0} seconds.".format(elapsed), flush=True)
                
    def recreate_chain(self, hashedPassword, start):
        for col in range(self.chain_len):
            hash = self.hash_func(start.encode('utf-8')).hexdigest()
            if hash == hashedPassword:
                return start
            start = self.reduction_func(hash, col)
            
        return None

    def crack(self, hashedPassword):
        print("Searching for a match in Rainbow Table, progress bar represents worst case scenario...")
        if hashedPassword in self.table:
            traversalResult = self.recreate_chain(hashedPassword, self.table[hashedPassword])
            if traversalResult:
                return traversalResult
        for startCol in tqdm(range(self.chain_len-1, -1, -1)):
            candidate = hashedPassword
            for col in range(startCol, self.chain_len):
                candidate = self.hash_func(self.reduction_func(candidate, col-1).encode('utf-8')).hexdigest()
            if candidate in self.table:
                traversalResult = self.recreate_chain(hashedPassword, self.table[candidate])
                if traversalResult:

                    return traversalResult
 
    def load_from_cvs(self, filename="RainbowTable.csv"):
        self.table = {}
        with open(filename, 'r') as table:
            reader = csv.DictReader(table)
            for row in reader:
                self.table[row[CSV_FIELDNAMES[1]]] = row[CSV_FIELDNAMES[0]]
                
    def get_chain_len(self):
        return self.table['chain_len']