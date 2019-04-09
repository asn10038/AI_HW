'''This is a simple ngrams calculator'''
import sys
import pprint
# size of the ngrams
NGRAMS = 1
# sliding window size
SLIDING_WINDOW = 1 


def usage():
    use_string = ''' python3 ngrams.py [file1][file2] ... '''
    print(use_string)

def get_ngram_counts(filename):
    res = {}
    with open(filename, "rb") as inp:
        ba = bytearray(inp.read())
    for byte in ba:
        if byte in res:
            res[byte] += 1
        else:
            res[byte] = 1
    return res

def process_files():
    res = {} 
    for filename in sys.argv[1:]:
        counts = get_ngram_counts(filename)
        res[filename] = counts
    return res

def dump_counts(counts):
    pp = pprint.PrettyPrinter(indent=6, depth=5) 
    pp.pprint(counts)

def create_csv(counts):
    '''creates a csv of the counts of the files where each row is a file'''
    headers = []
    for x in range(256):
        headers.append(str(hex(x)))
    with open('/tmp/counts.csv', 'w') as out:
        out.write(','.join(headers))
        out.write('\n')
        for f in counts:
            out.write(','.join(str(x) for x in counts[f].values()))
            out.write('\n')
    print("wrote to: /tmp/counts.csv")


def main():
    counts = process_files()
    dump_counts(counts)
    create_csv(counts)

if __name__=='__main__':
    print("Starting the main method;")
    main()
