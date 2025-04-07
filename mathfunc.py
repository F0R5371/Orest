import math
import re
import collections

def cosine_sim(str1, str2):

    # Find every character of the phrases and count the occurances
    WORD = re.compile(r"\w")

    words = WORD.findall(str1)
    vec1 = collections.Counter(words)
                
    words1 = WORD.findall(str2)
    vec2 = collections.Counter(words1)

    # & bitwise operator, used here to line up the keys together
    # Takes which ever keys are in similarity to each other
    intersect = set(vec1.keys()) & set(vec2.keys())

    # Multiplies each matching values to each other in both vectors and adds them up
    num = sum([vec1[x] * vec2[x] for x in intersect])
    
    # Squares every value in each counter obj and then multiples the square root of both of them
    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])

    denom = math.sqrt(sum1) * math.sqrt(sum2)

    if not denom:
        return 0
    else:
        return float(num) / denom