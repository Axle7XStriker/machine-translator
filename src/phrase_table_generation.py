from collections import defaultdict
import sys

def calculateProbability(translation_file, language_model_file, output_file_name):
    '''
        Combine the translationProbability obtained from the word alignments and 
        the unigram probability obtained from the language model for the source language 
        to compute the final score 
    '''
    lang_model_prob = {}
    inp_file = open(language_model_file, 'r')
    for line in inp_file:
        line = line.strip().split('\t')
        if len(line) == 2:
            lang_model_prob[line[1]] = float(line[0]) * -1
    inp_file.close()

    data=[]
    inp_file = open(translation_file, 'r')
    for line in inp_file:
        words = line.strip().split('\t')
        sourceWords = words[1].split(' ')
        prob = float(words[2])
        lang_prob = 1
        flag = 0
        for src_word in sourceWords:
            if src_word in lang_model_prob:
                flag = 1
                lang_prob *= lang_model_prob[src_word]
        if flag:
            lang_prob = lang_prob * -1
            prob += lang_prob
        data.append(words[0] + '\t' + words[1] + '\t' + str(prob))
    inp_file.close()

    out_file = open(output_file_name, 'w')
    out_file.write('\n'.join(data))
    out_file.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 finalScore.py <translationProbabilityTargetGivenSource.txt> <trainSource.lm> <finalTranslationProbabilityTargetGivenSource.txt>")
        sys.exit(0)

    calculateProbability(sys.argv[1], sys.argv[2], sys.argv[3])
