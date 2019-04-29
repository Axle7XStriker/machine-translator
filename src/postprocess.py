import sys
import random
import string
from collections import defaultdict

def postprocessing(corpus_files):
    '''
        Removes the special characters from the parallel corpus 
        obtained after reordering it. 
    '''
    for corpus_file in corpus_files:
        data = []
    
        # Read from language corpus file 
        with open(corpus_file, 'r') as  inp:
            for index, line in enumerate(inp):
                if len(line) > 0:
                    line = line.strip()
                    data.append(line.translate(str.maketrans("", "", string.punctuation)))
        data.append("")
    
        # Update language corpus file 
        with open(corpus_file, 'w') as f:
            f.write('\n'.join(data))
    
    return


if __name__ == "__main__":
    # Parameter checking 
    if len(sys.argv) < 2:
        print("Usage: python postprocess.py [file_path(s)]")
        sys.exit(0)
    
    postprocessing(sys.argv[1:])
