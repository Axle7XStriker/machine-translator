import string
import sys

def createInput(input_file,output_file):
    '''
        Generates the language model input 
    '''
    data = []
    inp_file = open(input_file, 'r')
    for line in inp_file:
        words = line.strip().split()
        for i in range(len(words)):
            words[i] = words[i].translate(str.maketrans("", "", string.punctuation))
        line = ' '.join(words)
        data.append(line)
    inp_file.close()

    out_file = open(output_file, 'w')
    out_file.write('\n'.join(data))
    out_file.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 languageModelInput.py <trainSource.txt> <trainS.txt>")
        sys.exit(0)

    createInput(sys.argv[1], sys.argv[2])
