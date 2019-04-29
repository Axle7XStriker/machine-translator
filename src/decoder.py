import sys
from collections import defaultdict
import operator
import string

JUNK_WORDS = ['S', 'SBAR', 'SBARQ', 'SINV', 'SQ', 'ADJP', 'ADVP', 'CONJP', 'FRAG', 'INTJ', 'LST', 'NAC', 'NP', 'NX', 
              'PP', 'PRN', 'PRT', 'QP', 'RRC', 'UCP', 'VP', 'WHADJP', 'WHAVP', 'WHNP', 'WHPP', 'X', 'CC', 'CD', 'DT', 
              'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS',  'PDT', 'POS', 'PRP', 
              'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 
              'WP', 'WP$', 'WRB', 'ADV', 'NOM', 'DTV', 'LGS', 'PRD', 'PUT', 'SBJ', 'TPC', 'VOC', 'BNF', 'DIR', 'EXT', 
              'LOC', 'MNR', 'PRP', 'TMP', 'CLR', 'CLF', 'HLN', 'TTL', 'LRB', 'RRB', 'LSB', 'RSB', 'NONE', 
              'ROOT']


def findBestTranslation(final_translation_probability, input_file):
    '''
        Gives the translation for a given input file sentence-by-sentence based on hypothesis recombiniation 
    '''
    trans_prob = defaultdict(dict)
    inp_file = open(final_translation_probability, 'r')
    for line in inp_file:
        line = line.strip().split('\t')
        line[0] = line[0].translate(str.maketrans("", "", string.punctuation))
        line[1] = line[1].translate(str.maketrans("", "", string.punctuation))
        trans_prob[line[0]][line[1]] = float(line[2])
    inp_file.close()
    
    
    data = []
    src_file = open(input_file + '.in', 'r')
    inp_file = open(input_file, 'r')
    for line in inp_file:
        translation_score = defaultdict(int)
        translation_sentence = defaultdict(list)
        line = line.translate(str.maketrans("", "", string.punctuation))
        words = line.strip().split(' ')
        for i in range(len(words)):
            if words[i] in JUNK_WORDS:
                words[i] = ''
            #words[i] = words[i].translate(str.maketrans("", "", string.punctuation))
        count = 1
        for i in range(len(words)):
            translation = ""
            for j in range(len(words) - count + 1):
                phrase = words[j:(j + count)]
                phrase = ' '.join(phrase)
                #print(phrase)
                if phrase in trans_prob:
                    translationPhrase = max(trans_prob[phrase].items(), key = operator.itemgetter(1))[0]
                    translation_score[count] += trans_prob[phrase][translationPhrase]
                    translation += translationPhrase + ' '
            if translation != '':
                translation_sentence[count].append(translation)
            count += 1
        print(translation_sentence)
        index = max(translation_score.items(), key = operator.itemgetter(1))[0]
        finalTranslation = ' '.join(translation_sentence[index])
        data.append(src_file.readline() + ' -> ' + finalTranslation)
    inp_file.close()

    out_file = open('translations.txt', 'w')
    out_file.write('\n'.join(data))
    out_file.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 finalScore.py <finalTranslationProbability.txt> <inputFile.txt>")
        sys.exit(0)

    findBestTranslation(sys.argv[1], sys.argv[2])