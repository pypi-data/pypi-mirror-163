import re

CONSONANT_RE = re.compile("[BCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz]")

VOWEL_RE = re.compile("[aeiouAEIOU]")

MEDIEVAL_MAP = {
    'a': '𝖆',
    'b': '𝖇',
    'c': '𝖈',
    'd': '𝖉',
    'e': '𝖊',
    'f': '𝖋',
    'g': '𝖌',
    'h': '𝖍',
    'i': '𝖎',
    'j': '𝖏',
    'k': '𝖐',
    'l': '𝖑',
    'm': '𝖒',
    'n': '𝖓',
    'o': '𝖔',
    'p': '𝖕',
    'q': '𝖖',
    'r': '𝖗',
    's': '𝖘',
    't': '𝖙',
    'u': '𝖚',
    'v': '𝖛',
    'w': '𝖜',
    'x': '𝖝',
    'y': '𝖞',
    'z': '𝖟',
    'A': '𝕬',
    'B': '𝕭',
    'C': '𝕮',
    'D': '𝕯',
    'E': '𝕰',
    'F': '𝕱',
    'G': '𝕲',
    'H': '𝕳',
    'I': '𝕴',
    'J': '𝕵',
    'K': '𝕶',
    'L': '𝕷',
    'M': '𝕸',
    'N': '𝕹',
    'O': '𝕺',
    'P': '𝕻',
    'Q': '𝕼',
    'R': '𝕽',
    'S': '𝕾',
    'T': '𝕿',
    'U': '𝖀',
    'V': '𝖁',
    'W': '𝖂',
    'X': '𝖃',
    'Y': '𝖄',
    'Z': '𝖅'
}

UPSIDE_DOWN_MAP = {
    'a': '\u0250',
    'b': '\u0071',
    'c': '\u0254',
    'd': '\u0070',
    'e': '\u01DD',
    'f': '\u025F',
    'g': '\u0253',
    'h': '\u0265',
    'i': '\u1D09',
    'j': '\u027e',
    'k': '\u029E',
    'l': '\u006C',
    'm': '\u026F',
    'n': '\u0075',
    'o': '\u006F',
    'p': '\u0064',
    'q': '\u0062',
    'r': '\u0279',
    's': '\u0073',
    't': '\u0287',
    'u': '\u006E',
    'v': '\u028C',
    'w': '\u028D',
    'x': '\u0078',
    'y': '\u028E',
    'z': '\u007A',
    'A': '\u2200',
    'B': '\u15FA',
    'C': '\u0186',
    'D': '\u15E1',
    'E': '\u018E',
    'F': '\u2132',
    'G': '\u2141',
    'H': '\u0048',
    'I': '\u0049',
    'J': '\u017F',
    'K': '\uA4D8',
    'L': '\u2142',
    'M': '\u0057',
    'N': '\u004E',
    'O': '\u004F',
    'P': '\u0500',
    'Q': '\u10E2',
    'R': '\u1D1A',
    'S': '\u0053',
    'T': '\uA7B1',
    'U': '\u0548',
    'V': '\u039B',
    'W': '\u004D',
    'X': '\u0058',
    'Y': '\u2144',
    'Z': '\u005A'
}

BUBBLE_MAP = {
    'A': '\u24B6',
    'B': '\u24B7',
    'C': '\u24B8',
    'D': '\u24B9',
    'E': '\u24BA',
    'F': '\u24BB',
    'G': '\u24BC',
    'H': '\u24BD',
    'I': '\u24BE',
    'J': '\u24BF',
    'K': '\u24C0',
    'L': '\u24C1',
    'M': '\u24C2',
    'N': '\u24C3',
    'O': '\u24C4',
    'P': '\u24C5',
    'Q': '\u24C6',
    'R': '\u24C7',
    'S': '\u24C8',
    'T': '\u24C9',
    'U': '\u24CA',
    'V': '\u24CB',
    'W': '\u24CC',
    'X': '\u24CD',
    'Y': '\u24CE',
    'Z': '\u24CF',
    'a': '\u24D0',
    'b': '\u24D1',
    'c': '\u24D2',
    'd': '\u24D3',
    'e': '\u24D4',
    'f': '\u24D5',
    'g': '\u24D6',
    'h': '\u24D7',
    'i': '\u24D8',
    'j': '\u24D9',
    'k': '\u24DA',
    'l': '\u24DB',
    'm': '\u24DC',
    'n': '\u24DD',
    'o': '\u24DE',
    'p': '\u24DF',
    'q': '\u24E0',
    'r': '\u24E1',
    's': '\u24E2',
    't': '\u24E3',
    'u': '\u24E4',
    'v': '\u24E5',
    'w': '\u24E6',
    'x': '\u24E7',
    'y': '\u24E8',
    'z': '\u24E9',
    '0': '\u24EA',
    '1': '\u2460',
    '2': '\u2461',
    '3': '\u2462',
    '4': '\u2463',
    '5': '\u2464',
    '6': '\u2465',
    '7': '\u2466',
    '8': '\u2467',
    '9': '\u2468'
}

MORSE_MAP = {
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',
    'a': '.-',
    'b': '-...',
    'c': '-.-.',
    'd': '-..',
    'e': '.',
    'f': '..-.',
    'g': '--.',
    'h': '....',
    'i': '..',
    'j': '.---',
    'k': '-.-',
    'l': '.-..',
    'm': '--',
    'n': '-.',
    'o': '---',
    'p': '.--.',
    'q': '--.-',
    'r': '.-.',
    's': '...',
    't': '-',
    'u': '..-',
    'v': '...-',
    'w': '.--',
    'x': '-..-',
    'y': '-.--',
    'z': '--..',
    '0': '-----',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    '!': '-.-.--',
    '?': '..--..',
    '-': '-....-',
    '.': '.-.-.-',
    ',': '--..--',
    '@': '.--.-.',
    '=': '-...-',
    '(': '-.--.',
    ')': '-.--.-',
    '+': '.-.-.',
    '&': '.-...',
    '\'': '.----.',
    '"': '.-..-.',
    ';': '-.-.-.',
    ':': '---...',
    '$': '...-..-',
    '_': '..--.-',
    ' ': '/'
}

# TODO: https://www.unicode.org/charts/PDF/UFF00.pdf
FULLWIDTH_MAP = {
    "!": "\uFF01",
    "\"": "\uFF02",
    "A": "\uFF21",
    "B": "\uFF22",
    "C": "\uFF23",
    "D": "\uFF24",
    "E": "\uFF25",
    "F": "\uFF26",
    "G": "\uFF27",
    "H": "\uFF28",
    "I": "\uFF29",
    "J": "\uFF2A",
    "K": "\uFF2B",
    "L": "\uFF2C",
    "M": "\uFF2D",
    "N": "\uFF2E",
    "O": "\uFF2F",
    "P": "\uFF30",
    "Q": "\uFF31",
    "R": "\uFF32",
    "S": "\uFF33",
    "T": "\uFF34",
    "U": "\uFF35",
    "V": "\uFF36",
    "W": "\uFF37",
    "X": "\uFF38",
    "Y": "\uFF39",
    "Z": "\uFF3A",
    "a": "\uFF41",
    "b": "\uFF42",
    "c": "\uFF43",
    "d": "\uFF44",
    "e": "\uFF45",
    "f": "\uFF46",
    "g": "\uFF47",
    "h": "\uFF48",
    "i": "\uFF49",
    "j": "\uFF4A",
    "k": "\uFF4B",
    "l": "\uFF4C",
    "m": "\uFF4D",
    "n": "\uFF4E",
    "o": "\uFF4F",
    "p": "\uFF50",
    "q": "\uFF51",
    "r": "\uFF52",
    "s": "\uFF53",
    "t": "\uFF54",
    "u": "\uFF55",
    "v": "\uFF56",
    "w": "\uFF57",
    "x": "\uFF58",
    "y": "\uFF59",
    "z": "\uFF5A"
}

SMALLCAPS_MAP = {
    "a": "ᴀ",
    "b": "ʙ",
    "c": "ᴄ",
    "d": "ᴅ",
    "e": "ᴇ",
    "f": "ꜰ",
    "g": "ɢ",
    "h": "ʜ",
    "i": "ɪ",
    "j": "ᴊ",
    "k": "ᴋ",
    "l": "ʟ",
    "m": "ᴍ",
    "n": "ɴ",
    "o": "ᴏ",
    "p": "ᴘ",
    "q": "ǫ",
    "r": "ʀ",
    "s": "ꜱ",
    "t": "ᴛ",
    "u": "ᴜ",
    "v": "ᴠ",
    "w": "ᴡ",
    "x": "x",
    "y": "ʏ",
    "z": "ᴢ"
}

SCRIPT_MAP = {
    "A": "𝓐",
    "B": "𝓑",
    "C": "𝓒",
    "D": "𝓓",
    "E": "𝓔",
    "F": "𝓕",
    "G": "𝓖",
    "H": "𝓗",
    "I": "𝓘",
    "J": "𝓙",
    "K": "𝓚",
    "L": "𝓛",
    "M": "𝓜",
    "N": "𝓝",
    "O": "𝓞",
    "P": "𝓟",
    "Q": "𝓠",
    "R": "𝓡",
    "S": "𝓢",
    "T": "𝓣",
    "U": "𝓤",
    "V": "𝓥",
    "W": "𝓦",
    "X": "𝓧",
    "Y": "𝓨",
    "Z": "𝓩",
    "a": "𝓪",
    "b": "𝓫",
    "c": "𝓬",
    "d": "𝓭",
    "e": "𝓮",
    "f": "𝓯",
    "g": "𝓰",
    "h": "𝓱",
    "i": "𝓲",
    "j": "𝓳",
    "k": "𝓴",
    "l": "𝓵",
    "m": "𝓶",
    "n": "𝓷",
    "o": "𝓸",
    "p": "𝓹",
    "q": "𝓺",
    "r": "𝓻",
    "s": "𝓼",
    "t": "𝓽",
    "u": "𝓾",
    "v": "𝓿",
    "w": "𝔀",
    "x": "𝔁",
    "y": "𝔂",
    "z": "𝔃"
}

BLACKBOARD_BOLD_MAP = {
    "A": "𝔸",
    "B": "𝔹",
    "C": "ℂ",
    "D": "𝔻",
    "E": "𝔼",
    "F": "𝔽",
    "G": "𝔾",
    "H": "ℍ",
    "I": "𝕀",
    "J": "𝕁",
    "K": "𝕂",
    "L": "𝕃",
    "M": "𝕄",
    "N": "ℕ",
    "O": "𝕆",
    "P": "ℙ",
    "Q": "ℚ",
    "R": "ℝ",
    "S": "𝕊",
    "T": "𝕋",
    "U": "𝕌",
    "V": "𝕍",
    "W": "𝕎",
    "X": "𝕏",
    "Y": "𝕐",
    "Z": "ℤ",
    "a": "𝕒",
    "b": "𝕓",
    "c": "𝕔",
    "d": "𝕕",
    "e": "𝕖",
    "f": "𝕗",
    "g": "𝕘",
    "h": "𝕙",
    "i": "𝕚",
    "j": "𝕛",
    "k": "𝕜",
    "l": "𝕝",
    "m": "𝕞",
    "n": "𝕟",
    "o": "𝕠",
    "p": "𝕡",
    "q": "𝕢",
    "r": "𝕣",
    "s": "𝕤",
    "t": "𝕥",
    "u": "𝕦",
    "v": "𝕧",
    "w": "𝕨",
    "x": "𝕩",
    "y": "𝕪",
    "z": "𝕫",
    "0": "𝟘",
    "1": "𝟙",
    "2": "𝟚",
    "3": "𝟛",
    "4": "𝟜",
    "5": "𝟝",
    "6": "𝟞",
    "7": "𝟟",
    "8": "𝟠",
    "9": "𝟡"
}

MONOSPACE_MAP = {
    "A": "\U0001D670",
    "B": "\U0001D671",
    "C": "\U0001D672",
    "D": "\U0001D673",
    "E": "\U0001D674",
    "F": "\U0001D675",
    "G": "\U0001D676",
    "H": "\U0001D677",
    "I": "\U0001D678",
    "J": "\U0001D679",
    "K": "\U0001D67a",
    "L": "\U0001D67b",
    "M": "\U0001D67c",
    "N": "\U0001D67d",
    "O": "\U0001D67e",
    "P": "\U0001D67f",
    "Q": "\U0001D680",
    "R": "\U0001D681",
    "S": "\U0001D682",
    "T": "\U0001D683",
    "U": "\U0001D684",
    "V": "\U0001D685",
    "W": "\U0001D686",
    "X": "\U0001D687",
    "Y": "\U0001D688",
    "Z": "\U0001D689",
    "a": "\U0001D68a",
    "b": "\U0001D68b",
    "c": "\U0001D68c",
    "d": "\U0001D68d",
    "e": "\U0001D68e",
    "f": "\U0001D68f",
    "g": "\U0001D690",
    "h": "\U0001D691",
    "i": "\U0001D692",
    "j": "\U0001D693",
    "k": "\U0001D694",
    "l": "\U0001D695",
    "m": "\U0001D696",
    "n": "\U0001D697",
    "o": "\U0001D698",
    "p": "\U0001D699",
    "q": "\U0001D69a",
    "r": "\U0001D69b",
    "s": "\U0001D69c",
    "t": "\U0001D69d",
    "u": "\U0001D69e",
    "v": "\U0001D69f",
    "w": "\U0001D6a0",
    "x": "\U0001D6a1",
    "y": "\U0001D6a2",
    "z": "\U0001D6a3",
    "0": "\U0001D7f6",
    "1": "\U0001D7f7",
    "2": "\U0001D7f8",
    "3": "\U0001D7f9",
    "4": "\U0001D7fa",
    "5": "\U0001D7fb",
    "6": "\U0001D7fc",
    "7": "\U0001D7fd",
    "8": "\U0001D7fe",
    "9": "\U0001D7ff"
}

COMBINING_MARKS = [
    '\u0300',  # ̀ 	768 	Combining Grave Accent
    '\u0301',  # ́ 	769 	Combining Acute Accent
    '\u0302',  # ̂ 	770 	Combining Circumflex Accent
    '\u0303',  # ̃ 	771 	Combining Tilde
    '\u0304',  # ̄ 	772 	Combining Macron
    '\u0305',  # ̅ 	773 	Combining Overline
    '\u0306',  # ̆ 	774 	Combining Breve
    '\u0307',  # ̇ 	775 	Combining Dot Above
    '\u0308',  # ̈ 	776 	Combining Diaeresis
    '\u0309',  # ̉ 	777 	Combining Hook Above
    '\u030A',  # ̊ 	778 	Combining Ring Above
    '\u030B',  # ̋ 	779 	Combining Double Acute Accent
    '\u030C',  # ̌ 	780 	Combining Caron
    '\u030D',  # ̍ 	781 	Combining Vertical Line Above
    '\u030E',  # ̎ 	782 	Combining Double Vertical Line Above
    '\u030F',  # ̏ 	783 	Combining Double Grave Accent
    '\u0310',  # ̐ 	784 	Combining Candrabindu
    '\u0311',  # ̑ 	785 	Combining Inverted Breve
    '\u0312',  # ̒ 	786 	Combining Turned Comma Above
    '\u0313',  # ̓ 	787 	Combining Comma Above
    '\u0314',  # ̔ 	788 	Combining Reversed Comma Above
    '\u0315',  # ̕ 	789 	Combining Comma Above Right
    '\u0316',  # ̖ 	790 	Combining Grave Accent Below
    '\u0317',  # ̗ 	791 	Combining Acute Accent Below
    '\u0318',  # ̘ 	792 	Combining Left Tack Below
    '\u0319',  # ̙ 	793 	Combining Right Tack Below
    '\u031A',  # ̚ 	794 	Combining Left Angle Above
    '\u031B',  # ̛ 	795 	Combining Horn
    '\u031C',  # ̜ 	796 	Combining Left Half Ring Below
    '\u031D',  # ̝ 	797 	Combining Up Tack Below
    '\u031E',  # ̞ 	798 	Combining Down Tack Below
    '\u031F',  # ̟ 	799 	Combining Plus Sign Below
    '\u0320',  # ̠ 	800 	Combining Minus Sign Below
    '\u0321',  # ̡ 	801 	Combining Palatalized Hook Below
    '\u0322',  # ̢ 	802 	Combining Retroflex Hook Below
    '\u0323',  # ̣ 	803 	Combining Dot Below
    '\u0324',  # ̤ 	804 	Combining Diaeresis Below
    '\u0325',  # ̥ 	805 	Combining Ring Below
    '\u0326',  # ̦ 	806 	Combining Comma Below
    '\u0327',  # ̧ 	807 	Combining Cedilla
    '\u0328',  # ̨ 	808 	Combining Ogonek
    '\u0329',  # ̩ 	809 	Combining Vertical Line Below
    '\u032A',  # ̪ 	810 	Combining Bridge Below
    '\u032B',  # ̫ 	811 	Combining Inverted Double Arch Below
    '\u032C',  # ̬ 	812 	Combining Caron Below
    '\u032D',  # ̭ 	813 	Combining Circumflex Accent Below
    '\u032E',  # ̮ 	814 	Combining Breve Below
    '\u032F',  # ̯ 	815 	Combining Inverted Breve Below
    '\u0330',  # ̰ 	816 	Combining Tilde Below
    '\u0331',  # ̱ 	817 	Combining Macron Below
    '\u0332',  # ̲ 	818 	Combining Low Line
    '\u0333',  # ̳ 	819 	Combining Double Low Line
    '\u0334',  # ̴ 	820 	Combining Tilde Overlay
    '\u0335',  # ̵ 	821 	Combining Short Stroke Overlay
    '\u0336',  # ̶ 	822 	Combining Long Stroke Overlay
    '\u0337',  # ̷ 	823 	Combining Short Solidus Overlay
    '\u0338',  # ̸ 	824 	Combining Long Solidus Overlay
    '\u0339',  # ̹ 	825 	Combining Right Half Ring Below
    '\u033A',  # ̺ 	826 	Combining Inverted Bridge Below
    '\u033B',  # ̻ 	827 	Combining Square Below
    '\u033C',  # ̼ 	828 	Combining Seagull Below
    '\u033D',  # ̽ 	829 	Combining X Above
    '\u033E',  # ̾ 	830 	Combining Vertical Tilde
    '\u033F',  # ̿ 	831 	Combining Double Overline
    '\u0340',  # ̀ 	832 	Combining Grave Tone Mark
    '\u0341',  # ́ 	833 	Combining Acute Tone Mark
    '\u0342',  # ͂ 	834 	Combining Greek Perispomeni
    '\u0343',  # ̓ 	835 	Combining Greek Koronis
    '\u0344',  # ̈́ 	836 	Combining Greek Dialytika Tonos
    '\u0345',  # ͅ 	837 	Combining Greek Ypogegrammeni
    '\u0346',  # ͆ 	838 	Combining Bridge Above
    '\u0347',  # ͇ 	839 	Combining Equals Sign Below
    '\u0348',  # ͈ 	840 	Combining Double Vertical Line Below
    '\u0349',  # ͉ 	841 	Combining Left Angle Below
    '\u034A',  # ͊ 	842 	Combining Not Tilde Above
    '\u034B',  # ͋ 	843 	Combining Homothetic Above
    '\u034C',  # ͌ 	844 	Combining Almost Equal To Above
    '\u034D',  # ͍ 	845 	Combining Left Right Arrow Below
    '\u034E',  # ͎ 	846 	Combining Upwards Arrow Below
    '\u034F',  # ͏ 	847 	Combining Grapheme Joiner
    '\u0350',  # ͐ 	848 	Combining Right Arrowhead Above
    '\u0351',  # ͑ 	849 	Combining Left Half Ring Above
    '\u0352',  # ͒ 	850 	Combining Fermata
    '\u0353',  # ͓ 	851 	Combining X Below
    '\u0354',  # ͔ 	852 	Combining Left Arrowhead Below
    '\u0355',  # ͕ 	853 	Combining Right Arrowhead Below
    '\u0356',  # ͖ 	854 	Combining Right Arrowhead And Up Arrowhead Below
    '\u0357',  # ͗ 	855 	Combining Right Half Ring Above
    '\u0358',  # ͘ 	856 	Combining Dot Above Right
    '\u0359',  # ͙ 	857 	Combining Asterisk Below
    '\u035A',  # ͚ 	858 	Combining Double Ring Below
    '\u035B',  # ͛ 	859 	Combining Zigzag Above
    '\u035C',  # ͜ 	860 	Combining Double Breve Below
    '\u035D',  # ͝ 	861 	Combining Double Breve
    '\u035E',  # ͞ 	862 	Combining Double Macron
    '\u035F',  # ͟ 	863 	Combining Double Macron Below
    '\u0360',  # ͠ 	864 	Combining Double Tilde
    '\u0361',  # ͡ 	865 	Combining Double Inverted Breve
    '\u0362',  # ͢ 	866 	Combining Double Rightwards Arrow Below
    '\u0363',  # ͣ 	867 	Combining Latin Small Letter A
    '\u0364',  # ͤ 	868 	Combining Latin Small Letter E
    '\u0365',  # ͥ 	869 	Combining Latin Small Letter I
    '\u0366',  # ͦ 	870 	Combining Latin Small Letter O
    '\u0367',  # ͧ 	871 	Combining Latin Small Letter U
    '\u0368',  # ͨ 	872 	Combining Latin Small Letter C
    '\u0369',  # ͩ 	873 	Combining Latin Small Letter D
    '\u036A',  # ͪ 	874 	Combining Latin Small Letter H
    '\u036B',  # ͫ 	875 	Combining Latin Small Letter M
    '\u036C',  # ͬ 	876 	Combining Latin Small Letter R
    '\u036D',  # ͭ 	877 	Combining Latin Small Letter T
    '\u036E',  # ͮ 	878 	Combining Latin Small Letter V
    '\u036F',  # ͯ 	879 	Combining Latin Small Letter X
]

LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
