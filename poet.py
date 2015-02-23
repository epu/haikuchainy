import random
import re
from unidecode import unidecode
from nltk.corpus import cmudict

# compile the regexes we'll use to try to count syllables
VOWELS = u"aeiou"
STRIP_RE = re.compile(r'(?:[^l%sy]es?|ed)$' % VOWELS)
Y_RE = re.compile(r'^y')
VOWELS_RE = re.compile(r'[%sy]{1,2}' % VOWELS)


class Poet():

    words = None
    cmu_dict = None
    path = None
    corpus = None

    def __init__(self, corpus):

        self.corpus = corpus

    def read_text(self):
        words = []
        with open(self.corpus) as f:
            for w in f.read().split():
                w.strip()
                if w and w.upper() != w:
                    words.append(w)
        self.words = {}
        for i, word in enumerate(words):
            try:
                first, second, third = words[i], words[i + 1], words[i + 2]
            except IndexError:
                break
            key = (first, second)
            if key not in self.words:
                self.words[key] = []
            self.words[key].append(third)
        return self.words

    def line(self):
        li = [key for key in self.words.keys() if key[0][0].isupper()]
        key = random.choice(li)

        li = []
        first, second = key
        li.append(first)
        li.append(second)
        while True:
            try:
                third = random.choice(self.words[key])
            except KeyError:
                break
            li.append(third)
            if third[-1] in ',.?!':
                break
            # else
            key = (second, third)
            first, second = key
        return ' '.join(li)

    def syllables(self, word):
        """
        Count the number of syllables in a word, using the counts in the cmudict corpus if possible.
        """

        # the cmu corpus contains syllable counts
        if not self.cmu_dict:
            self.cmu_dict = cmudict.dict()

        word = word.lower()

        # transliterate unicode strings into 7-bit ascii
        if type(word) is unicode:
            word = unidecode(word)

        # cf: http://stackoverflow.com/a/4103234
        if word in self.cmu_dict:
            return [len(list(y for y in x if y[-1].isdigit())) for x in self.cmu_dict[word]][0]

        # If the word is not in the cmu corpus, do our best to count syllables:

        # 1. remove suffixes  of l, y, and vowels followed by an e, es, or ed
        word = STRIP_RE.sub('', word)

        # 2. remove leading Ys
        word = Y_RE.sub('', word)

        # 3. count the remaining occurances of either 1 or 2 vowels
        c = len(VOWELS_RE.findall(word))

        # time for Jell-O(tm).
        return c

    def free_verse(self, limit=140):
        lines = []
        while True:
            lines.append(self.line())
            while len("\n".join(lines)) > limit:
                lines = lines[1:]
            if len(lines) < 3:
                continue
            if len("\n".join(lines)) > limit - 20 < limit:
                break
        lines[-1] = re.sub(r'[;,]$', '.', lines[-1])
        return lines

    def haiku(self, limit=140):

        lines = []
        while len(lines) != 3:
            l = self.line()
            l = re.sub(r'\W$', '', l)
            count = sum([self.syllables(re.sub(r'\W', '', w)) for w in l.split()])
            needed = 5 if len(lines) in (0, 2) else 7
            if count == needed:
                lines.append(l)
            if len("\n".join(lines)) > limit:
                lines = []
        return lines

    def compose(self, form, limit=140):
        """
        Compose a poem in 140 characters or less
        """

        try:
            form = getattr(self, form)
        except:
            raise Exception("This poet cannot compose %ss." % form)

        if not self.words:
            self.read_text()

        poem = ''
        while poem == '':
            poem = "\n".join(form(limit=limit))
            if len(poem) > limit:
                poem = ''
        return poem
