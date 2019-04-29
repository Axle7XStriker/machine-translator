import sys
import random
import string
from collections import defaultdict

def preprocessing(train_size, source_file, target_file):
    '''
        Splits the bi-text corpus into training and testing set 
        according to given number of sentences. 
    '''
    train_indices = [0 for i in range(2000000)]
    test_indices = [0 for i in range(2000000)]
    for i in random.sample(range(45642), int(train_size * 45641)):
        train_indices[i] = 1
    for i in random.sample(range(45642), 100):
        test_indices[i] = 1
    training_source = []
    training_target = []
    testing_source = []
    testing_target = []

    # Read from source language corpus
    with open(source_file, 'r') as  inp:
        for index,line in enumerate(inp):
            if len(line) > 0:
                line = line.strip()
                if train_indices[index] == 1:
                    training_source.append(line.lower())
                if test_indices[index] == 1:
                    testing_source.append(line.lower())
    training_source.append("")
    testing_source.append("")
    
    #Read from target language corpus
    with open(target_file, 'r') as  inp:
        for index,line in enumerate(inp):
            if len(line) > 0:
                line = line.strip()
                if train_indices[index] == 1:
                    training_target.append(line)
                if test_indices[index] == 1:
                    testing_target.append(line)
    training_target.append("")
    testing_target.append("")

    
    # Write into training file for source data
    with open('./Dataset/raw/training_source.txt','w') as f:
        f.write('\n'.join(training_source))
    
    # Write into training file for target data
    with open('./Dataset/raw/training_target.txt','w') as f:
        f.write('\n'.join(training_target))

     # Write into testing file for source data
    testing_source = testing_source[:5]
    with open('./Dataset/raw/testing_source.txt','w') as f:
        f.write('\n'.join(testing_source))

    # Write into testing file for target data
    testing_target = testing_target[:5]
    with open('./Dataset/raw/testing_target.txt','w') as f:
        f.write('\n'.join(testing_target))

    return


if __name__ == "__main__":
    # Parameter checking 
    if len(sys.argv) != 4:
        print("Usage: python preprocess.py <file_source> <file_target> <train-size>")
        sys.exit(0)
    
    train_size = float(sys.argv[3])
    preprocessing(train_size, sys.argv[1], sys.argv[2])
