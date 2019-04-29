from collections import defaultdict
import string

JUNK_WORDS = ['S', 'SBAR', 'SBARQ', 'SINV', 'SQ', 'ADJP', 'ADVP', 'CONJP', 'FRAG', 'INTJ', 'LST', 'NAC', 'NP', 'NX', 
              'PP', 'PRN', 'PRT', 'QP', 'RRC', 'UCP', 'VP', 'WHADJP', 'WHAVP', 'WHNP', 'WHPP', 'X', 'CC', 'CD', 'DT', 
              'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS',  'PDT', 'POS', 'PRP', 
              'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 
              'WP', 'WP$', 'WRB', 'ADV', 'NOM', 'DTV', 'LGS', 'PRD', 'PUT', 'SBJ', 'TPC', 'VOC', 'BNF', 'DIR', 'EXT', 
              'LOC', 'MNR', 'PRP', 'TMP', 'CLR', 'CLF', 'HLN', 'TTL', 'LRB', 'RRB', 'LSB', 'RSB', 'NONE', 
              'ROOT']


def findAlignment(target_txt, source_align_idx, source_txt, target_align_idx):
    '''
        Given a pair of sentences along with the word alignment 
        this code returns the union of the word alignment matrix 
    '''
    word_alignment = defaultdict(lambda: defaultdict(int))
    word_index_target = defaultdict(lambda: -1)
    word_index_source = defaultdict(lambda: -1)

    source_txt = source_txt.translate(str.maketrans("", "", string.punctuation))
    source_txt  = source_txt.strip().split()
    for i in range(len(source_txt)):
        if source_txt[i] in JUNK_WORDS:
            source_txt[i] = ''
        #source_txt[i] = source_txt[i].translate(str.maketrans("", "", string.punctuation))
    
    target_txt = target_txt.translate(str.maketrans("", "", string.punctuation))
    target_txt = target_txt.strip().split()
    for i in range(len(target_txt)):
        if target_txt[i] in JUNK_WORDS:
            target_txt[i] = ''
        #target_txt[i] = target_txt[i].translate(str.maketrans("", "", string.punctuation))
    
    
    target_align_idx = target_align_idx.strip().split(" })")
    target_align_idx = target_align_idx[1:]
    t_idx = 0
    for key in target_align_idx:
        word_idx = key.split('({')
        if (len(word_idx) > 1) and (word_idx[1] != ''):
            target_word = word_idx[0].strip()
            target_word = target_word.translate(str.maketrans("", "", string.punctuation))
            indices = word_idx[1].split()
            for s_idx in indices:
                s_idx = int(s_idx)
                word_alignment[s_idx - 1][t_idx] = 1
        t_idx += 1
    
    source_align_idx = source_align_idx.strip().split(" })")
    source_align_idx = source_align_idx[1:]
    s_idx = 0
    for key in source_align_idx:
        word_idx = key.split('({')
        if (len(word_idx) > 1) and (word_idx[1] != ''):
            source_word = word_idx[0].strip()
            source_word = source_word.translate(str.maketrans("", "", string.punctuation))
            indices = word_idx[1].split()
            for t_idx in indices:
                t_idx = int(t_idx)
                word_alignment[s_idx][t_idx - 1] = 1
        s_idx +=1
    
    return word_alignment, source_txt, target_txt
