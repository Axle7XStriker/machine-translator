import sys
import random
import string
from collections import defaultdict

def preprocessing(bidict_files):
    '''
        Preprocess the one-many mapping of bilingual dictionary from source to 
        target into a one-one mapping from source to target 
    '''
    bilingual_dict = []
    src_dict = []
    trg_dict = []

    # Read from bilingual dictionary containing many target translations for each source word 
    for bidict_file in bidict_files:
        with open(bidict_file, 'r') as  inp:
            for line in inp:
                if len(line) > 0:
                    bimap = line.strip().split(':')
                    src_word = bimap[0]
                    trg_words = bimap[1].strip().split()
                    for trg_word in trg_words:
                        src_dict.append(src_word)
                        trg_dict.append(trg_word)
    src_dict.append("")
    trg_dict.append("")
    # Write the processed dictionary into two separate files corresponding to source and target 
    with open('./Dataset/raw/training_source.txt', 'a') as f:
        f.write('\n'.join(src_dict))
    with open('./Dataset/raw/training_target.txt', 'a') as f:
        f.write('\n'.join(trg_dict))

    return


if __name__ == "__main__":
    # Parameter checking 
    if len(sys.argv) < 2:
        print("Usage: python preprocess.py [bilingual-dictionary-file(s)]")
        sys.exit(0)
    
    preprocessing(sys.argv[1:])
