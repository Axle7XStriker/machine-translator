'''after obtaining the consistent phrases from the phrase extraction algorithm we next move to find the translationProbability
this is done by calculating the relative occurrences of the target phrase for a given source phrase for both directions'''
'''it takes as input the phrases.txt file and returns the translationProbability in the file named 
translationProbabilityGermanGivenEnglish.txt and translationProbabilityEnglishGivenGerman.txt'''

from collections import defaultdict
import sys
import math


def findTranslationProbability(phrases_file):
    '''
        Calculate the relative occurrences of the target phrase 
        for a given source phrase for both the directions 
    '''
    count_src = defaultdict(lambda: defaultdict(int))
    sum_count_trg = defaultdict(int)
    count_trg = defaultdict(lambda: defaultdict(int))
    sum_count_src = defaultdict(int)

    inp_file = open (phrases_file, 'r')
    for line in inp_file:
        phrases = line.strip().split('\t')
        if len(phrases) == 2:
            count_src[phrases[0]][phrases[1]] += 1
            sum_count_trg[phrases[0]] += 1
            count_trg[phrases[1]][phrases[0]] += 1
            sum_count_src[phrases[1]] += 1
    inp_file.close

    data = []
    for src in count_src:
        for trg in count_src[src]:
            translation_probability = math.log(float(count_src[src][trg]) / sum_count_trg[src])
            data.append(trg + '\t' + src + '\t' + str(translation_probability))

    out_file = open('translationProbabilityTargetGivenSource.txt', 'w')
    out_file.write('\n'.join(data))
    out_file.close()

    data=[]
    for trg in count_trg:
        for src in count_trg[trg]:
            translation_probability = math.log(float(count_trg[trg][src]) / sum_count_src[trg])
            data.append(src + '\t' + trg + '\t' + str(translation_probability))

    out_file = open('translationProbabilitySourceGivenTarget.txt', 'w')
    out_file.write('\n'.join(data))
    out_file.close()


if __name__ == "__main__":
    if len(sys.argv)!=2:
        print("Usage: python3 findTranslationProbability.py <phrases-file>")
        sys.exit(0)
    
    findTranslationProbability(sys.argv[1])
