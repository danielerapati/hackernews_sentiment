import requests
import json
import string
from contractions import contractions

positive_url = 'http://www.unc.edu/~ncaren/haphazard/positive.txt'
negative_url = 'http://www.unc.edu/~ncaren/haphazard/negative.txt'

positive = set(requests.get(positive_url).text.split())

negative = set(requests.get(negative_url).text.split())

exclude = set(map(unicode,string.punctuation))
def remove_punct(s):
    return ''.join(ch for ch in s if ch not in exclude)

def replace_contr(words):
    for word in words:
        if word in contractions:
            words.remove(word)
            words.extend(contractions.get(word).split())
        return words

def sentiment(text):
    if not text: return 0
    words = text.lower().split()
    words = replace_contr(words)
    words = map(remove_punct, words)
    return sum((word in positive)-(word in negative) for word in words)/float(len(words))


def score(n):
    if n > 0.5: return "++"
    elif n >= 0.1: return "+"
    elif n < -0.5: return "--"
    elif n<= -0.1: return "-"
    else: return '0'

print
for i in range(100000,1500000):
    url = 'https://hacker-news.firebaseio.com/v0/item/'+str(i)+'.json'
    r = requests.get(url)
    data = json.loads(r.text)
    txt = data.get('text',data.get('title'))
    s = score(sentiment(txt))
    if s != '0':
        print txt
        print s


