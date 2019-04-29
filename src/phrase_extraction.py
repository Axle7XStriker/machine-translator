import sys
from alignment import findAlignment


def checkConsistency(src_start, src_end, trg_start, trg_end, word_alignment, source, target):
    '''
        Check whether the phrase is consistent or not 
    '''
    flag =1
    
    list_source = []
    list_target = []

    for i in range(len(source)):
        if (i >= src_start) and (i <= src_end):
            list_source.append(i)

    for i in range(len(target)):
        if (i >= trg_start )and (i <= trg_end):
            list_target.append(i)

    for trg in list_target:
        for src in range(len(source)):
            if word_alignment[src][trg] == 1:
                if (src >= src_start) and (src <= src_end):
                    continue
                else:
                    flag = 0

    for src in list_source:
        for trg in range(len(target)):
            if word_alignment[src][trg]==1:
                if (trg >= trg_start) and (trg <= trg_end):
                    continue
                else:
                    flag = 0

    return flag


def findPhrase(src_start, src_end, trg_start, trg_end, source, target):
    '''
        Given the starting and ending points, return the phrase 
        corresponding to both the source and the target language 
    '''
    #print(src_start, src_end, trg_start, trg_end)
    #print(source)
    #print(target)
    
    phrase_src = []
    for i in range(src_start, src_end + 1):
        phrase_src.append(source[i])
    
    phrase_trg = []
    for i in range(trg_start, trg_end + 1):
        phrase_trg.append(target[i])

    return [' '.join(phrase_src), ' '.join(phrase_trg)]

def extract(src_start, src_end, trg_start, trg_end, word_alignment, source, target):
    '''
        Extract and return consistent phrases 
    '''
    if trg_end == -1:
        return None
    else:
        flag = checkConsistency(src_start, src_end, trg_start, trg_end, word_alignment, source, target)
        if flag:
            return findPhrase(src_start, src_end, trg_start, trg_end, source, target)
        else:
            return None

def extractPhrases(source_target, target_source):
    '''
        Extract consistent phrases from the bi-lingual sentences 
    '''
    data = []
    src_align_file = open(source_target, 'r')
    trg_align_file = open(target_source, 'r')
    count = 0
    while True:
        count += 1
        #print(count)
        
        line = src_align_file.readline()
        if line == "":
            break
        target_txt = src_align_file.readline()
        source_align_idx = src_align_file.readline()
        #print("Target Text:", target_txt.rstrip('\n'))
        line = trg_align_file.readline()
        source_txt = trg_align_file.readline()
        target_align_idx = trg_align_file.readline()
        #print("Source Text:", source_txt.rstrip('\n'))

        word_alignment, source, target = findAlignment(target_txt, source_align_idx, source_txt, target_align_idx)
        print("Source Text:", source)
        print("Target Text:", target)
        print("Word Alignment:", word_alignment, end = "\n\n")

        src_len = len(source)
        trg_len = len(target)
        
        phrases = []
        for src_start in range(src_len):
            for src_end in range(src_start,(src_len)):
                trg_start = trg_len
                trg_end = -1
                for i in word_alignment:
                    if i <= src_end and i >= src_start:
                        for j in word_alignment[i]:
                            trg_start = min(j, trg_start)
                            trg_end = max(j, trg_end)
                if ((src_end - src_start) <= 5) or ((trg_end - trg_start) <= 5) :
                    phrases.append([src_start, src_end, trg_start, trg_end])
        #print(phrases)
        for key in phrases:
            src_start = key[0]
            src_end = key[1]
            trg_start = key [2]
            trg_end = key[3]
            phrase = extract (src_start, src_end, trg_start, trg_end, word_alignment, source, target)
            if phrase is not None:
                #print(phrase)
                data.append(phrase[0] + '\t' + phrase[1])
    src_align_file.close()
    trg_align_file.close()

    phrase_file = open('phrases.txt','w')
    phrase_file.write('\n'.join(data))
    phrase_file.close()


if __name__ == "__main__":
    if len(sys.argv)!=3:
        print("Usage: python phraseExtraction.py <source-target_alignment> <target-source_alignment>")
        sys.exit(0)

    extractPhrases(sys.argv[1], sys.argv[2])
