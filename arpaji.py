#!/usr/bin/python
import logging
import argparse
from enum import Enum
# Overengineered romaji to ARPAbet approximator
# 2. The "su" in "desu" should be silent.

parser = argparse.ArgumentParser()
parser.add_argument("text",help="romaji to translate")
args = parser.parse_args()
text = args.text

class TokenType(Enum):
    JI = 1 
    PUNC = 2 
    SEP = 3
TOKENS = (
    ("shi", "SH IY0"),
    ("chi", "CH IY0"),
    ("tsu", "Z UW0"),
    ("dzu", "Z UW0"),
    ("dzi", "JH IY0"),

    ("kya", "K Y AA0"),
    ("gya", "G Y AA0"),
    ("sha", "SH AA0"),
    ("cha", "CH AA0"),
    ("nya", "N Y AA0"),
    ("hya", "HH Y AA0"),
    ("bya", "B Y AA0"),
    ("mya", "M Y AA0"),
    ("pya", "P Y AA0"),
    ("rya", "L Y AA0"),

    ("kyu", "K Y UW0"),
    ("gyu", "G Y UW0"),
    ("shu", "SH UW0"),
    ("chu", "CH UW0"),
    ("nyu", "N Y UW0"),
    ("hyu", "HH Y UW0"),
    ("byu", "B Y UW0"),
    ("myu", "M Y UW0"),
    ("pyu", "P Y UW0"),
    ("ryu", "L Y UW0"),

    ("kyo", "K Y OW0"),
    ("gyo", "G Y OW0"),
    ("sho", "SH OW0"),
    ("cho", "CH OW0"),
    ("nyo", "N Y OW0"),
    ("hyo", "HH Y OW0"),
    ("byo", "B Y OW0"),
    ("myo", "M Y OW0"),
    ("pyo", "P Y OW0"),
    ("ryo", "L Y OW0"),

    ("ka", "K AA0"),
    ("ki", "K IY0"),
    ("ku", "K UW0"),
    ("ke", "K EH0 EH0"),
    ("ko", "K AO0 OW0"),

    ("ga", "G AA0"),
    ("gi", "G IY0"),
    ("gu", "G UW0"),
    ("ge", "G EH0 EH0"),
    ("go", "G AO0 OW0"),

    ("ba", "B AA0"),
    ("bi", "B IY0"),
    ("bu", "B UW0"),
    ("be", "B EH0"),
    ("bo", "B AO0 OW0"),

    ("pa", "P AA0"),
    ("pi", "P IY0"),
    ("pu", "P UW0"),
    ("pe", "P EH0 EH0"),
    ("po", "P AO0 OW0"),

    ("za", "Z AA0"),
    ("zu", "Z UW0"),
    ("ze", "Z EH0"),
    ("zo", "Z AO0 OW0"),

    ("ja", "JH AA0"),
    ("ji", "JH IY0"),
    ("ju", "JH UW0"),
    ("jo", "JH AO0 OW0"),

    ("sa", "S AA0"),
    ("su", "S UW0"),
    ("se", "S EH0"),
    ("so", "S AO0 OW0"),

    ("ta", "T AA0"),
    ("te", "T EH0 EH0"),
    ("ti", "T IY0"),
    ("to", "T AO0 OW0"),

    ("da", "D AA0"),
    ("di", "D IY0"),
    ("de", "D EH0 EH0"),
    ("do", "D AO0 OW0"),

    ("na", "N AA0"),
    ("ni", "N IY0"),
    ("nu", "N UW0"),
    ("ne", "N EH0 EH0"),
    ("no", "N AO0 OW0"),

    ("ha", "HH AA0"),
    ("hi", "HH IY0"),
    ("fu", "F UW0"),
    ("he", "HH EH0 EH0"),
    ("ho", "HH AO0 OW0"),

    ("ma", "M AA0"),
    ("mi", "M IY0"),
    ("mu", "M UW0"),
    ("me", "M EH0 EH0"),
    ("mo", "M AO0 OW0"),

    ("ya", "Y AA0"),
    ("yu", "Y UW0"),
    ("yo", "Y AO0 OW0"),

    ("ra", "L AA0"),
    ("ri", "L IY0"),
    ("ru", "L UW0"),
    ("re", "L EH0 EH0"),
    ("ro", "L AO0 OW0"),

    ("wa", "W AA0"),
    ("wo", "AO0 OW0"),

    ("a", "AA0"),
    ("i", "IY0"),
    ("u", "UW0"),
    ("e", "EH0 EH0"),
    ("o", "AO0 OW0"),
    ("n", "N"),
)
SMALL_TSU = "stckgbp"
MAX_TOKEN_SIZE = 3
token_list = []

# Example input: "chikadzukanakya... teme wo buchinomesenaindena."

def ji():
    ret = False

    # small tsu is not interpreted b/c ARPAbet has no way to encode
    # pauses/glottal stops
    if text[:2] and (text[:2][0] in SMALL_TSU) and (text[:2][1] in SMALL_TSU):
        nextsym(1)

    for tok in TOKENS:
        if (text.startswith(tok[0])):
            token_list.append((TokenType.JI, tok[1]))
            nextsym(len(tok[0]))
            ret = True
            break
    return ret

def nextsym(c):
    global text
    text = text[c:]

def punctuation():
    ret = False
    # Oi Josuke!
    # I erased a string with ZA HANDO!
    # Now, according to Python, it's a substring of every string!
    # Isn't that whacky, Josuke?
    while text[:1] and (text[:1] in ".,?!-"):
        token_list.append((TokenType.PUNC, text[:1]))
        ret = True
        nextsym(1)
    return ret

def whitespace():
    ret = False
    while text[:1] and (text[:1].isspace()):
        ret = True
        nextsym(1)
    if ret:
        token_list.append((TokenType.SEP, " "))
    return ret

def word():
    cont = False
    while ji():
        cont = True
        pass
    if punctuation():
        cont = True
    elif whitespace():
        cont = True
        token_list.append((TokenType.SEP, ""))
    return cont
    
def parse():
    while word():
        pass

def next_token():
    global token_list
    token_list = token_list[1:]

def gen():
    output = ""

    # Are we in a word?
    word = False

    while len(token_list):
        if token_list[0][0] == TokenType.JI:
            if word == False: output += "{"
            word = True
            output += token_list[0][1]
            output += " "
        else:
            if word == True: output += "}"
            word = False
            output += token_list[0][1]
        next_token()
    if word: output += "}"
    return output

parse()
print(gen())
