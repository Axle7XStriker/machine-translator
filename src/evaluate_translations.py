'''this method takes as input the translation, actual input and the real output and gives a precision and recall value for each sentence'''

import sys
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu

def calculatePrecision(translated, actual):
    '''
        Computes precision 
    '''
    print(translated, actual)
    count = 0
    for word in translated:
        if word in actual:
            count += 1
    
    return (float(count) / len(translated))

def calculateRecall(translated, actual):
    '''
        Computes recall 
    '''
    count = 0
    for word in actual:
        if word in translated:
            count += 1
    
    return (float(count) / len(actual))


def sentenceBleuScore(translated, actual):
    '''
        Computes sentence BLEU Score 
    '''
    references = [actual]
    candidate = translated

    return sentence_bleu(references, candidate)


def corpusBleuScore(translated, actual):
    '''
        Computes corpus BLEU Score 
    '''
    references = [actual]
    candidate = translated
    
    return corpus_bleu(references, candidate)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 errorAnalysis.py <reference-corpus> <candidate-corpus>")
        sys.exit(0)

    data = []
    data.append("Precision\t\t\t\tRecall\t\t\t\tSentence BLEU Score")
    ref_corp = open(sys.argv[1], 'r')
    cand_corp = open(sys.argv[2], 'r')
    for ref_line, cand_line in zip(ref_corp, cand_corp):
        translated = cand_line.strip().split(' ')
        actual = ref_line.strip().split(' ')
        precision = calculatePrecision(translated, actual)
        recall = calculateRecall(translated,actual)
        sent_bleu_score = sentenceBleuScore(translated, actual)
        data.append(str(precision) + '\t\t' + str(recall) + '\t\t' + str(sent_bleu_score))
    ref_corp.close()
    cand_corp.close()

    out_file = open('evaluation.txt', 'w')
    out_file.write('\n'.join(data))
    out_file.write('\n')
    out_file.close()
