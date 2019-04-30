import sys
from collections import defaultdict, namedtuple
import operator
import string
import copy

JUNK_WORDS = ['S', 'SBAR', 'SBARQ', 'SINV', 'SQ', 'ADJP', 'ADVP', 'CONJP', 'FRAG', 'INTJ', 'LST', 'NAC', 'NP', 'NX', 
              'PP', 'PRN', 'PRT', 'QP', 'RRC', 'UCP', 'VP', 'WHADJP', 'WHAVP', 'WHNP', 'WHPP', 'X', 'CC', 'CD', 'DT', 
              'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS',  'PDT', 'POS', 'PRP', 
              'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 
              'WP', 'WP$', 'WRB', 'ADV', 'NOM', 'DTV', 'LGS', 'PRD', 'PUT', 'SBJ', 'TPC', 'VOC', 'BNF', 'DIR', 'EXT', 
              'LOC', 'MNR', 'PRP', 'TMP', 'CLR', 'CLF', 'HLN', 'TTL', 'LRB', 'RRB', 'LSB', 'RSB', 'NONE', 
              'ROOT']


def getTranslations(hypo, src_words, trans_prob):
    '''
        Get all possible translations of a source phrase 
    '''
    translations = []
    src_words_len = len(src_words)
    for src_start in range(src_words_len):
        for src_end in range(src_start + 1, src_words_len + 1):
            unmarked = True
            for i in range(src_start, src_end):
                if hypo.marked[i] == 1:
                    unmarked = False
                    break
            if unmarked:
                src_phrase = ' '.join(src_words[src_start:src_end])
                if src_phrase in trans_prob:
                    trg_phrases = dict(sorted(trans_prob[src_phrase].items(), key = operator.itemgetter(1), reverse = True)[0:3])
                    for p in trg_phrases:
                        translations.append(({'sent': p, 'logprob': trg_phrases[p]}, (src_start, src_end)))
    #print(translations, end="\n\n")
    
    return translations


def hypoToPhrases(hypo):
    '''
        Convert a hypothesis to list of phrases 
    '''
    phrases = []
    def getPhrases(hypo, phrase_list):
        if hypo.predecessor == None:
            return 
        else :
            phrase_list.insert(0, (hypo.trg_phrase, hypo.src_phrase, hypo.end_idx))
            getPhrases(hypo.predecessor, phrase_list)
    getPhrases(hypo, phrases)
    phrases.sort(key = lambda p: p[2])

    return phrases


def stackDecode(src_words, trans_prob):
    '''
        Decode a sentence using a stack decoder 
    '''
    MAX_STACK_SIZE = 100
    
    Hypo = namedtuple('Hypothesis', ['logprob', 'marked', 'predecessor', 'trg_phrase', 'src_phrase', 'end_idx'])
    marked = [0 for i in src_words]
    init_hypo = Hypo(0.0, marked, None, None, None, 0)

    stacks = [{} for i in src_words] + [{}]
    stacks[0][''] = init_hypo
    for i, stack in enumerate(stacks[:-1]):
        if len(stack) > MAX_STACK_SIZE:
            max_logprob_hypo = max(stack.items(), key = lambda h: h[1].logprob)[1]
            threshold = 1.3 * max_logprob_hypo.logprob
            pruned_stack = sorted(filter(lambda h: h[1].logprob >= threshold, stack.items()), key = lambda h: -h[1].logprob)[:MAX_STACK_SIZE]
        else :
            pruned_stack = stack.items()
        
        for key, hypo in pruned_stack:
            translations = getTranslations(hypo, src_words, trans_prob)
            for (phrase, idxs) in translations:
                start_idx = idxs[0]
                end_idx = idxs[1]
                logprob = hypo.logprob + phrase['logprob']

                marked = copy.deepcopy(hypo.marked)
                for i in range(start_idx, end_idx):
                    marked[i] = 1
                num_marked = 0
                for x in marked: 
                    num_marked += 1 if x == 1 else 0
                tmark = tuple(marked)

                new_hypo = Hypo(logprob, marked, hypo, phrase, ' '.join(src_words[start_idx:end_idx]), end_idx)
                if (tmark not in stacks[num_marked]) or (stacks[num_marked][tmark].logprob < logprob):
                    stacks[num_marked][tmark] = new_hypo
    i = 0
    while i < len(stacks):
        if stacks[-(i + 1)]:
            final_translation_hypo = max(stacks[-(i + 1)].items(), key = lambda h: h[1].logprob)[1]
            break
        i += 1

    return hypoToPhrases(final_translation_hypo)


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
        
        ret = stackDecode(words, trans_prob)
        res = ''
        for x in ret:
            res += x[0]['sent'] + ' '
        print(res)

        #count = 1
        #for i in range(len(words)):
        #    translation = ""
        #    for j in range(len(words) - count + 1):
        #        phrase = words[j:(j + count)]
        #        phrase = ' '.join(phrase)
        #        if phrase in trans_prob:
        #            translationPhrase = max(trans_prob[phrase].items(), key = operator.itemgetter(1))[0]
        #            translation_score[count] *= trans_prob[phrase][translationPhrase]*count
        #            translation += translationPhrase + ' '
        #    if translation != '':
        #        translation_sentence[count].append(translation)
        #    count += 1
        #print(translation_sentence)
        #index = max(translation_score.items(), key = operator.itemgetter(1))[0]
        #final_translation = ' '.join(translation_sentence[index])
        
        data.append(src_file.readline() + ' -> ' + res)
    inp_file.close()

    out_file = open('translations.txt', 'w')
    out_file.write('\n'.join(data))
    out_file.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 finalScore.py <finalTranslationProbability.txt> <inputFile.txt>")
        sys.exit(0)

    findBestTranslation(sys.argv[1], sys.argv[2])