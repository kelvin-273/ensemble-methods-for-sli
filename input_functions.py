"""functions to be used in the file_to_vector module"""

def file_to_list(file_name):
    """file_name -> list of lines"""
    with open(file_name, 'r') as transcript:
        raw_text = []
        for i in transcript:
            if i[0] == '\t':
                raw_text[-1] += i.replace('\t', ' ').replace('\n', '')
            else:
                raw_text.append(i.replace('\n', ''))
        return raw_text

def split_meta_data(raw_text):
    """list of lines -> tuple of meta_data and convo_data"""
    meta_data = []
    convo_data = []
    for i in raw_text:
        if i[0] == '@':
            meta_data.append(i[1:])
        else:
            convo_data.append(i)

    return meta_data, convo_data

def line_cluster(convo_data):
    """convo_data -> list of line clusters"""
    result = []
    line_dict = {}
    storing = False
    # build a set of dictionaries
    for i in convo_data:
        if i[0] == '*':
            if storing:
                result.append(line_dict)
            else:
                storing = True
            line_dict = {}
            i = i.split(':\t')
            line_dict['ID'] = i[0]
            line_dict['sentence'] = i[1]
        elif i[0] == '%':
            i = i.split(':\t')
            line_dict[i[0]] = i[1]
    result.append(line_dict)
    return result

def vect_append(dictionary, value, key):
    """function docstring"""
    if key.__class__.__name__ in ('list', 'tuple'):
        assert len(key) == len(value)
        for i in range(len(key)):
            if value[i].__class__.__name__ in ('list', 'tuple'):
                for j in range(len(value[i])):
                    assert value[i][j].__class__.__name__ in ('int', 'float', 'bool')
                    dictionary[key[i] + str(j)] = value[i][j]
            elif value[i].__class__.__name__ == "dict":
                for j in value[i]:
                    dictionary[key[i] + str(j)] = value[i][j]
            else:
                assert value[i].__class__.__name__ in ('int', 'float', 'bool')
                dictionary[key[i]] = value[i]

    elif key.__class__.__name__ == 'str':
        if value.__class__.__name__ in ('list', 'tuple'):
            for i in range(len(value)):
                dictionary[key + str(i)] = value[i]
        else:
            assert value.__class__.__name__ in ('int', 'float', 'bool')
            dictionary[key] = value

def npos(tup):
    return list(map(_npos_aux, tup))

def _npos_aux(tup):
    assert tup.__class__.__name__ == 'tuple'
    return tup[1]

def nword(tup):
    return list(map(_nword_aux, tup))

def _nword_aux(tup):
    assert tup.__class__.__name__ == 'tuple'
    return tup[0]

def syllables(word):
    """
    counts the number of syllables
    scraped from StackOverflow
    """
    count = 0
    vowels = 'aeiouy'
    word = word.lower().strip(".:;?!")
    if word[0] in vowels:
        count +=1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count+=1
    if count == 0:
        count +=1
    # print(word, count)
    return count

if __name__ == '__main__':
    d = {}
    try:
        vect_append(d, [['adsf', 'asdff'], [4, 6, 7], 3], ["Words", "Num", "Number"])
    except Exception as e:
        print("Eish")

    print(d)
