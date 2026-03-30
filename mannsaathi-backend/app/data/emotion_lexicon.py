"""
Comprehensive Multilingual Emotion Lexicon for Indian Languages
Supports: Hindi, English, Hinglish, Tamil, Telugu, Bengali, Marathi, Gujarati
"""

# Hindi Emotion Keywords (Devanagari)
HINDI_EMOTIONS = {
    'sadness': {
        'udaas': 0.8, 'dard': 0.9, 'dukhi': 0.85, 'takleef': 0.8,
        'gham': 0.85, 'mayus': 0.75, 'nirash': 0.8, 'akela': 0.7,
        'tanha': 0.75, 'bebas': 0.8, 'kamzor': 0.6, 'thaka': 0.5,
        'khoya': 0.7, 'pareshan': 0.65, 'chinta': 0.6, 'khatam': 0.9,
        'jeene': 0.85, 'marne': 0.9, 'suicide': 0.95, 'aatmahatya': 0.95
    },
    'fear': {
        'dar': 0.85, 'dara': 0.8, 'gabrahat': 0.75, 'chinta': 0.7,
        'fikar': 0.7, 'ghabra': 0.8, 'khatra': 0.85, 'bhay': 0.8,
        'atank': 0.9, 'bechaini': 0.75, 'ghabrahat': 0.8, 'shak': 0.6,
        'ankush': 0.7, 'control': 0.65, 'pagal': 0.7, 'paagal': 0.7
    },
    'anger': {
        'gussa': 0.9, 'naraz': 0.8, 'naraaz': 0.8, 'krodh': 0.85,
        'chidd': 0.75, 'irritate': 0.7, 'bhadaas': 0.8, 'shikayat': 0.6,
        'shikwa': 0.65, 'nafrat': 0.85, 'ghrina': 0.8, 'takraar': 0.7,
        'jhagda': 0.75, 'larai': 0.8, 'gusse': 0.85
    },
    'joy': {
        'khush': 0.9, 'anand': 0.85, 'maza': 0.8, 'masti': 0.75,
        'hansi': 0.8, 'muskurahat': 0.85, 'khushi': 0.9, 'jashn': 0.8,
        'umang': 0.75, 'utsah': 0.8, 'prasannata': 0.85, 'sukoon': 0.7,
        'chain': 0.75, 'santosh': 0.8, 'dhanyavad': 0.7, 'shukriya': 0.7
    },
    'surprise': {
        'hairan': 0.85, 'achanak': 0.7, 'shocking': 0.8, 'wow': 0.75,
        'wah': 0.7, 'kamaal': 0.75, 'zabardast': 0.7, 'ashcharya': 0.8,
        'achraj': 0.75, 'heran': 0.8, 'herani': 0.8
    },
    'neutral': {
        'theek': 0.5, 'normal': 0.5, 'bas': 0.4, 'chalo': 0.4,
        'hmm': 0.3, 'acha': 0.4, 'thik': 0.5, 'sahi': 0.4
    }
}

# Hinglish (Roman Script Hindi) Emotion Keywords
HINGLISH_EMOTIONS = {
    'sadness': {
        'udaas': 0.8, 'dard': 0.9, 'dukhi': 0.85, 'takleef': 0.8,
        'gham': 0.85, 'mayus': 0.75, 'nirash': 0.8, 'akela': 0.7,
        'tanha': 0.75, 'bebas': 0.8, 'kamzor': 0.6, 'thaka': 0.5,
        'khoya': 0.7, 'pareshan': 0.65, 'chinta': 0.6, 'khatam': 0.9,
        'jeena': 0.85, 'marne': 0.9, 'marjaana': 0.95, 'jeenanahi': 0.95,
        'khatamkarna': 0.95, 'khatam': 0.9, 'khatamkar': 0.95,
        'sabkhatam': 0.95, 'khatamhai': 0.9, 'khatamkardu': 0.95,
        'worthless': 0.85, 'useless': 0.8, 'bekar': 0.75, 'bekaar': 0.75,
        'thakgaya': 0.8, 'thakgayahu': 0.85, 'bore': 0.6, 'boring': 0.5,
        'hopeless': 0.85, 'nirasha': 0.8, 'disappointed': 0.75,
        'cry': 0.8, 'rota': 0.85, 'rona': 0.8, 'roysa': 0.85,
        'suicide': 0.95, 'aatmahatya': 0.95, 'khudkushi': 0.95,
        'depressed': 0.9, 'depression': 0.9, 'tension': 0.7,
        'stress': 0.75, 'stressed': 0.8, 'anxiety': 0.8, 'anxious': 0.8,
        'worried': 0.75, 'worry': 0.7, 'tensed': 0.75, 'tense': 0.7,
        'lonely': 0.8, 'alone': 0.75, 'akela': 0.8, 'akelapan': 0.85,
        'empty': 0.75, 'khaali': 0.7, 'meaningless': 0.8, 'bekaar': 0.75,
        'hurt': 0.8, 'dard': 0.85, 'pain': 0.8, 'sad': 0.85, 'upset': 0.75,
        'broken': 0.85, 'toota': 0.8, 'tootagaya': 0.85, 'gaya': 0.7,
        'lost': 0.75, 'confused': 0.65, 'mushkil': 0.7, 'difficult': 0.65,
        'problem': 0.6, 'problems': 0.65, 'mushkilein': 0.75,
        'pareshani': 0.7, 'pareshaniya': 0.75, 'suffering': 0.85,
        'suffer': 0.8, 'struggling': 0.8, 'struggle': 0.75, 'mushkilse': 0.75
    },
    'fear': {
        'dar': 0.85, 'dara': 0.8, 'gabrahat': 0.75, 'chinta': 0.7,
        'fikar': 0.7, 'ghabra': 0.8, 'khatra': 0.85, 'bhay': 0.8,
        'atank': 0.9, 'bechaini': 0.75, 'ghabrahat': 0.8, 'shak': 0.6,
        'ankush': 0.7, 'control': 0.65, 'pagal': 0.7, 'paagal': 0.7,
        'scared': 0.85, 'afraid': 0.8, 'fear': 0.85, 'worried': 0.75,
        'nervous': 0.75, 'tensed': 0.75, 'panic': 0.85, 'darlagta': 0.85,
        'darr': 0.85, 'phobia': 0.8, 'phobic': 0.75, 'haunted': 0.8,
        'nightmare': 0.8, 'bad dream': 0.75, 'uncertain': 0.7,
        'insecure': 0.75, 'unsafe': 0.8, 'danger': 0.85, 'khatra': 0.85,
        'risk': 0.7, 'pareshan': 0.7, 'bechain': 0.75, 'restless': 0.7,
        'ghabrahat': 0.8, 'anxiety': 0.85, 'anxious': 0.85, 'tension': 0.75
    },
    'anger': {
        'gussa': 0.9, 'naraz': 0.8, 'naraaz': 0.8, 'krodh': 0.85,
        'chidd': 0.75, 'irritate': 0.7, 'bhadaas': 0.8, 'shikayat': 0.6,
        'shikwa': 0.65, 'nafrat': 0.85, 'ghrina': 0.8, 'takraar': 0.7,
        'jhagda': 0.75, 'larai': 0.8, 'gusse': 0.85, 'angry': 0.9,
        'mad': 0.85, 'frustrated': 0.8, 'frustration': 0.8, 'irritated': 0.75,
        'annoyed': 0.75, 'furious': 0.9, 'rage': 0.9, 'hate': 0.85,
        'gussemein': 0.85, 'gussemain': 0.85, 'gussema': 0.85,
        'chiddgaya': 0.8, 'chiddi': 0.75, 'irritating': 0.75,
        'bhadaasnikaalna': 0.85, 'bhadaasnikal': 0.8, 'shikayatkarna': 0.7,
        'complain': 0.6, 'shikwa': 0.65, 'nafratkarta': 0.85,
        'hatekarta': 0.8, 'larai': 0.8, 'jhagada': 0.75, 'fight': 0.75,
        'argument': 0.7, 'disagree': 0.6, 'unfair': 0.7, 'unjust': 0.75,
        'cheated': 0.8, 'betrayed': 0.85, 'dhoka': 0.85, 'dhokha': 0.85,
        'bewafa': 0.8, 'bewafai': 0.85
    },
    'joy': {
        'khush': 0.9, 'anand': 0.85, 'maza': 0.8, 'masti': 0.75,
        'hansi': 0.8, 'muskurahat': 0.85, 'khushi': 0.9, 'jashn': 0.8,
        'umang': 0.75, 'utsah': 0.8, 'prasannata': 0.85, 'sukoon': 0.7,
        'chain': 0.75, 'santosh': 0.8, 'dhanyavad': 0.7, 'shukriya': 0.7,
        'happy': 0.9, 'joy': 0.9, 'excited': 0.85, 'excitement': 0.8,
        'glad': 0.8, 'pleased': 0.8, 'delighted': 0.85, 'thrilled': 0.85,
        'blessed': 0.85, 'grateful': 0.8, 'thankful': 0.8, 'proud': 0.8,
        'confident': 0.75, 'hopeful': 0.8, 'optimistic': 0.75,
        'khushhu': 0.9, 'khushhun': 0.9, 'khushhai': 0.85, 'mazaa': 0.8,
        'mazaaraha': 0.85, 'hasi': 0.8, 'hasraha': 0.85, 'muskurahat': 0.85,
        'smile': 0.8, 'laugh': 0.85, 'laughing': 0.85, 'enjoy': 0.8,
        'enjoying': 0.85, 'enjoykiya': 0.8, 'celebrate': 0.8,
        'celebration': 0.8, 'party': 0.75, 'fun': 0.8, 'masti': 0.75,
        'dhamaal': 0.8, 'jhakaas': 0.8, 'jhakas': 0.8, 'badhiya': 0.75,
        'badiya': 0.75, 'awesome': 0.8, 'amazing': 0.8, 'great': 0.8,
        'wonderful': 0.85, 'fantastic': 0.85, 'excellent': 0.8,
        'perfect': 0.8, 'best': 0.8, 'love': 0.85, 'loving': 0.85,
        'pyaar': 0.85, 'pyar': 0.85, 'mohabbat': 0.85, 'ishq': 0.8
    },
    'surprise': {
        'hairan': 0.85, 'achanak': 0.7, 'shocking': 0.8, 'wow': 0.75,
        'wah': 0.7, 'kamaal': 0.75, 'zabardast': 0.7, 'ashcharya': 0.8,
        'achraj': 0.75, 'heran': 0.8, 'herani': 0.8, 'surprised': 0.85,
        'shocked': 0.85, 'amazed': 0.8, 'astonished': 0.85, 'unexpected': 0.75,
        'sudden': 0.7, 'unbelievable': 0.85, 'incredible': 0.8,
        'hairaan': 0.85, 'hairaankar': 0.85, 'shock': 0.8, 'shocking': 0.8,
        'wow': 0.75, 'wah': 0.7, 'kya': 0.7, 'kyabaat': 0.75, 'kyabaathai': 0.75,
        'omg': 0.8, 'ohmygod': 0.75, 'hanji': 0.6, 'sachmein': 0.75,
        'sach': 0.7, 'really': 0.7, 'seriously': 0.75, 'cantbelieve': 0.8,
        'yakin': 0.7, 'yakinnahi': 0.75
    },
    'neutral': {
        'theek': 0.5, 'normal': 0.5, 'bas': 0.4, 'chalo': 0.4,
        'hmm': 0.3, 'acha': 0.4, 'thik': 0.5, 'sahi': 0.4,
        'okay': 0.5, 'ok': 0.5, 'fine': 0.5, 'alright': 0.5,
        'theekhai': 0.5, 'theekh': 0.5, 'chaltha': 0.45, 'chalta': 0.45,
        'hota': 0.4, 'hotaai': 0.4, 'dekhte': 0.4, 'dekhenge': 0.45,
        'sochte': 0.4, 'sochunga': 0.45, 'patanahi': 0.4, 'shayad': 0.4,
        'maybe': 0.4, 'perhaps': 0.4, 'notsure': 0.4, 'confused': 0.45
    }
}

# Tamil Emotion Keywords
TAMIL_EMOTIONS = {
    'sadness': {
        'sogam': 0.85, 'vedhanai': 0.8, 'thuyaram': 0.85, 'kavalai': 0.75,
        'kastam': 0.8, 'thunbam': 0.85, 'murai': 0.7, 'thevai': 0.6,
        'thaniyai': 0.75, 'veruppu': 0.7, 'maranam': 0.9, 'saaganum': 0.95
    },
    'fear': {
        'bayam': 0.85, 'accham': 0.8, 'viyapu': 0.75, 'kavalai': 0.7,
        'sankadam': 0.8, 'pagal': 0.7, 'control': 0.65
    },
    'anger': {
        'kopathu': 0.9, 'seruppu': 0.85, 'kovanam': 0.8, 'veri': 0.75,
        'saththam': 0.7, 'paga': 0.85, 'sandai': 0.75
    },
    'joy': {
        'santhosam': 0.9, 'maga': 0.85, 'aanandham': 0.85, 'sirippu': 0.8,
        'magizhchi': 0.85, 'nandri': 0.7, 'sugam': 0.75
    },
    'surprise': {
        'atcharam': 0.85, 'maru': 0.7, 'ascharyam': 0.8, 'visithiram': 0.75
    },
    'neutral': {
        'sari': 0.5, 'normal': 0.5, 'apdi': 0.4, 'seri': 0.45
    }
}

# Telugu Emotion Keywords
TELUGU_EMOTIONS = {
    'sadness': {
        'bada': 0.85, 'vedana': 0.8, 'dukkham': 0.85, 'kastam': 0.8,
        'tondara': 0.75, 'badha': 0.85, 'edupu': 0.8, 'okkariga': 0.75,
        'chavali': 0.95, 'chanipovali': 0.95
    },
    'fear': {
        'bayam': 0.85, 'bhayam': 0.85, 'andhola': 0.75, 'chinta': 0.7,
        'pagal': 0.7, 'control': 0.65
    },
    'anger': {
        'kopam': 0.9, 'krodham': 0.85, 'tittu': 0.75, 'vemati': 0.8,
        'dwesham': 0.85, 'godava': 0.75
    },
    'joy': {
        'santosham': 0.9, 'anandham': 0.85, 'maza': 0.8, 'navvu': 0.8,
        'dhanyavadamulu': 0.7, 'sukham': 0.75
    },
    'surprise': {
        'ascharyam': 0.85, 'acharya': 0.8, 'adbhutam': 0.8, 'vismayam': 0.75
    },
    'neutral': {
        'bagundi': 0.5, 'normal': 0.5, 'parledu': 0.45, 'sare': 0.5
    }
}

# Bengali Emotion Keywords
BENGALI_EMOTIONS = {
    'sadness': {
        'dukkhito': 0.85, 'koshto': 0.8, 'bedona': 0.85, 'chinta': 0.7,
        'bhoy': 0.75, 'akla': 0.75, 'shesh': 0.9, 'morte': 0.95, 'attyahotta': 0.95
    },
    'fear': {
        'bhoy': 0.85, 'chinta': 0.75, 'shongshoy': 0.8, 'pagol': 0.7,
        'control': 0.65
    },
    'anger': {
        'rosh': 0.9, 'krodh': 0.85, 'oggyan': 0.75, 'ghrina': 0.8,
        'jhogra': 0.75, 'lorai': 0.8
    },
    'joy': {
        'anondo': 0.9, 'khushi': 0.9, 'moja': 0.8, 'hashi': 0.8,
        'dhonnobad': 0.7, 'shanti': 0.75
    },
    'surprise': {
        'obak': 0.85, 'hottash': 0.75, 'ashchorjo': 0.8, 'bisshoy': 0.75
    },
    'neutral': {
        'bhalo': 0.5, 'normal': 0.5, 'thik': 0.5, 'ache': 0.4
    }
}

# Marathi Emotion Keywords
MARATHI_EMOTIONS = {
    'sadness': {
        'dukhi': 0.85, 'vedana': 0.8, 'dukh': 0.85, 'chinta': 0.7,
        'akela': 0.75, 'thaklelo': 0.8, 'samapta': 0.9, 'marayche': 0.95,
        'aatmaghat': 0.95
    },
    'fear': {
        'bhiti': 0.85, 'ghabrahat': 0.8, 'chinta': 0.75, 'pagal': 0.7,
        'control': 0.65
    },
    'anger': {
        'rag': 0.9, 'krodh': 0.85, 'chid': 0.75, 'dwesh': 0.85,
        'bhadas': 0.8, 'bhanda': 0.75
    },
    'joy': {
        'anand': 0.9, 'khushi': 0.9, 'maza': 0.8, 'hasha': 0.8,
        'dhanyawad': 0.7, 'sukha': 0.75
    },
    'surprise': {
        'aashcharya': 0.85, 'ghabra': 0.75, 'vismay': 0.8, 'achraj': 0.75
    },
    'neutral': {
        'thik': 0.5, 'normal': 0.5, 'bas': 0.4, 'chala': 0.45
    }
}

# Gujarati Emotion Keywords
GUJARATI_EMOTIONS = {
    'sadness': {
        'udas': 0.85, 'dard': 0.9, 'dukh': 0.85, 'chinta': 0.7,
        'eklo': 0.75, 'thaki gayo': 0.8, 'khatam': 0.9, 'marvu': 0.95,
        'aatmahatya': 0.95
    },
    'fear': {
        'bhay': 0.85, 'ghabrahat': 0.8, 'chinta': 0.75, 'pagal': 0.7,
        'control': 0.65
    },
    'anger': {
        'gussa': 0.9, 'krodh': 0.85, 'chid': 0.75, 'ghrina': 0.8,
        'jhagda': 0.75
    },
    'joy': {
        'khushi': 0.9, 'anand': 0.85, 'maza': 0.8, 'hashi': 0.8,
        'aabhar': 0.7, 'shanti': 0.75
    },
    'surprise': {
        'ashcharya': 0.85, 'hairan': 0.8, 'vismay': 0.8, 'achraj': 0.75
    },
    'neutral': {
        'saru': 0.5, 'normal': 0.5, 'bas': 0.4, 'chalo': 0.45
    }
}

# English Emotion Keywords (Supplementary)
ENGLISH_EMOTIONS = {
    'sadness': {
        'sad': 0.85, 'depressed': 0.9, 'depression': 0.9, 'unhappy': 0.8,
        'miserable': 0.9, 'hopeless': 0.85, 'worthless': 0.85, 'empty': 0.75,
        'lonely': 0.8, 'alone': 0.75, 'crying': 0.85, 'cry': 0.8, 'tears': 0.8,
        'hurt': 0.8, 'pain': 0.8, 'heartbroken': 0.9, 'broken': 0.85,
        'suicide': 0.95, 'suicidal': 0.95, 'kill': 0.9, 'die': 0.9, 'death': 0.9,
        'end': 0.8, 'over': 0.75, 'finished': 0.75, 'done': 0.7,
        'tired': 0.7, 'exhausted': 0.75, 'drained': 0.75, 'burnout': 0.8,
        'stressed': 0.8, 'anxious': 0.8, 'worried': 0.75, 'nervous': 0.75,
        'scared': 0.8, 'afraid': 0.75, 'fear': 0.8, 'panic': 0.85,
        'overwhelmed': 0.8, 'lost': 0.75, 'confused': 0.65, 'stuck': 0.7
    },
    'fear': {
        'scared': 0.85, 'afraid': 0.8, 'fear': 0.85, 'fearful': 0.8,
        'terrified': 0.9, 'horrified': 0.9, 'panic': 0.85, 'anxiety': 0.85,
        'anxious': 0.85, 'worried': 0.75, 'worry': 0.7, 'nervous': 0.75,
        'tensed': 0.75, 'tense': 0.7, 'stressed': 0.75, 'pressure': 0.7,
        'overwhelmed': 0.75, 'insecure': 0.75, 'unsafe': 0.8, 'danger': 0.85,
        'threat': 0.8, 'risk': 0.7, 'uncertain': 0.7, 'doubt': 0.65,
        'suspicious': 0.7, 'paranoid': 0.8, 'phobia': 0.8, 'nightmare': 0.8,
        'haunted': 0.8, 'trauma': 0.85, 'ptsd': 0.85
    },
    'anger': {
        'angry': 0.9, 'mad': 0.85, 'furious': 0.9, 'rage': 0.9, 'hate': 0.85,
        'frustrated': 0.8, 'frustration': 0.8, 'irritated': 0.75, 'annoyed': 0.75,
        'pissed': 0.85, 'annoying': 0.75, 'irritating': 0.75, 'fed up': 0.8,
        'sick of': 0.8, 'tired of': 0.75, 'resent': 0.8, 'bitter': 0.75,
        'jealous': 0.7, 'envy': 0.7, 'betrayed': 0.85, 'cheated': 0.8,
        'lied': 0.75, 'disappointed': 0.75, 'unfair': 0.7, 'injustice': 0.75
    },
    'joy': {
        'happy': 0.9, 'joy': 0.9, 'joyful': 0.9, 'glad': 0.8, 'pleased': 0.8,
        'delighted': 0.85, 'thrilled': 0.85, 'excited': 0.85, 'excitement': 0.8,
        'ecstatic': 0.9, 'elated': 0.85, 'blessed': 0.85, 'grateful': 0.8,
        'thankful': 0.8, 'proud': 0.8, 'confident': 0.75, 'hopeful': 0.8,
        'optimistic': 0.75, 'love': 0.85, 'loving': 0.85, 'loved': 0.85,
        'peaceful': 0.75, 'calm': 0.7, 'relaxed': 0.75, 'content': 0.75,
        'satisfied': 0.75, 'fulfilled': 0.8, 'amazing': 0.8, 'awesome': 0.8,
        'great': 0.8, 'wonderful': 0.85, 'fantastic': 0.85, 'excellent': 0.8,
        'perfect': 0.8, 'best': 0.8, 'beautiful': 0.8, 'enjoy': 0.8, 'fun': 0.8
    },
    'surprise': {
        'surprised': 0.85, 'shocked': 0.85, 'amazed': 0.8, 'astonished': 0.85,
        'stunned': 0.85, 'speechless': 0.8, 'wow': 0.75, 'omg': 0.8,
        'unbelievable': 0.85, 'incredible': 0.8, 'unexpected': 0.75,
        'sudden': 0.7, 'weird': 0.65, 'strange': 0.65, 'odd': 0.6
    },
    'neutral': {
        'okay': 0.5, 'ok': 0.5, 'fine': 0.5, 'alright': 0.5, 'normal': 0.5,
        'average': 0.5, 'medium': 0.5, 'moderate': 0.5, 'so-so': 0.45,
        'meh': 0.4, 'whatever': 0.4, 'not sure': 0.4, 'maybe': 0.4,
        'perhaps': 0.4, 'confused': 0.45, 'thinking': 0.45
    }
}

# Crisis Keywords for All Languages
CRISIS_KEYWORDS = {
    'suicide': [
        # English
        'suicide', 'suicidal', 'kill myself', 'end my life', 'want to die',
        'better off dead', 'not worth living', 'end it all', 'take my life',
        'self harm', 'self-harm', 'cutting', 'overdose', 'jump off',
        'hang myself', 'shoot myself', 'slit', 'wrists', 'pills',
        # Hinglish
        'aatma hatya', 'aatmahatya', 'khudkushi', 'khud khushi',
        'mar jaana', 'marjaana', 'mar jana', 'marjana', 'jeena nahi',
        'jeenanahi', 'jeena mushkil', 'sab khatam', 'sabkhatam',
        'khatam karna', 'khatamkarna', 'khatam kar', 'khatamkar',
        'khatam kardu', 'khatamkardu', 'khatam hai', 'khatamhai',
        'zindagi khatam', 'zindagikhatam', 'life khatam', 'lifekhatam',
        'marne ka', 'marneka', 'marna hai', 'marnahai', 'mar jau',
        'marjau', 'mar jaun', 'marjaun', 'khatam karu', 'khatamkaru',
        # Hindi (Devanagari)
        'आत्महत्या', 'खुदकुशी', 'मर जाना', 'जीना नहीं', 'सब खतम',
        'खत्म करना', 'खत्म कर दूं', 'जिंदगी खत्म', 'मरने का',
        # Tamil
        'saaganum', 'saagalam', 'uyirai mutru', 'sethidalam',
        # Telugu
        'chavali', 'chanipovali', 'pranalani', 'chetabadi',
        # Bengali
        'attyahotta', 'attyahotya', 'morte chai', 'jibon shesh',
        # Marathi
        'aatmaghat', 'aatmaghatna', 'marayche ahe', 'jivan samapt',
        # Gujarati
        'aatmahatya', 'marvu chhe', 'jivan khatam', 'khudkushi'
    ],
    'self_harm': [
        # English
        'self harm', 'self-harm', 'cutting', 'cutter', 'blade', 'razor',
        'hurt myself', 'hurt me', 'pain makes me feel', 'burn myself',
        'scratch', 'pinch', 'hit myself', 'punish myself',
        # Hinglish
        'apnu nuksan', 'apne aap ko hurt', 'khud ko dard', 'blade se',
        'chaku se', 'kaatna', 'khud ko kaat', 'zakhm', 'chot',
        # Hindi
        'आत्महानि', 'खुद को चोट', 'चाकू से', 'ब्लेड से'
    ],
    'hopelessness': [
        # English
        'no hope', 'hopeless', 'no point', 'no reason', 'give up',
        'cant go on', 'cannot go on', 'nothing matters', 'nobody cares',
        'everyone hates me', 'alone forever', 'never get better',
        # Hinglish
        'koi ummeed nahi', 'ummeed nahi', 'koi fayda nahi', 'fayda nahi',
        'chhod do', 'haar maan li', 'sab bekar', 'koi nahi poochta',
        'koi nahi samajhta', 'kabhi nahi sudhrega', 'kabhi theek nahi hoga',
        # Hindi
        'कोई उम्मीद नहीं', 'हार मान ली', 'सब बेकार', 'कोई नहीं समझता'
    ]
}

# Indian Cultural Context Keywords
CULTURAL_CONTEXT = {
    'family_pressure': [
        'family', 'parents', 'papa', 'mummy', 'maa', 'baap', 'gharwalon',
        'gharwale', 'rishtedaar', 'relatives', 'samaj', 'society',
        'log kya kahenge', 'logkyakahenge', 'izzat', 'sharm', 'sharam',
        'family izzat', 'ghar ki izzat', 'baap ka sapna', 'parents expectation',
        'force', 'force kar rahe', 'zabardasti', 'majboor', 'majburi',
        'compromise', 'compromise karna', 'adjust', 'adjust karna'
    ],
    'academic_stress': [
        'jee', 'neet', 'exam', 'exams', 'board', 'boards', 'result', 'results',
        'marks', 'percentage', 'rank', 'competition', 'competitive',
        'padhai', 'studies', 'study', 'fail', 'failure', 'pass', 'top',
        'first division', 'distinction', 'career', 'future', 'job', 'placement',
        'pressure', 'tension', 'stress', 'anxiety', 'depression', 'suicide',
        'coaching', 'tuition', 'tution', 'classes', 'institute'
    ],
    'relationship_issues': [
        'boyfriend', 'girlfriend', 'bf', 'gf', 'love', 'pyaar', 'pyar',
        'mohabbat', 'ishq', 'breakup', 'break up', 'break-up', 'chhoda',
        'chhod diya', 'dhoka', 'dhokha', 'bewafa', 'bewafai', 'cheat',
        'cheating', 'trust', 'vishwas', 'relationship', 'rishta',
        'marriage', 'shaadi', 'engaged', 'engagement', 'arranged marriage',
        'love marriage', 'caste', 'religion', 'intercaste', 'inter-caste',
        'interfaith', 'family反对', 'parents against', 'maana nahi'
    ],
    'financial_stress': [
        'paise', 'money', 'financial', 'karza', 'loan', 'debt', 'emi',
        'expenses', 'kharcha', 'gharcha', 'mehangai', 'inflation',
        'job loss', 'naukri', 'naukri nahi', 'unemployed', 'berozgar',
        'business loss', 'loss hua', 'nuksan', 'garibi', 'poor',
        'struggle', 'sangharsh', 'mehnat', 'hard work'
    ],
    'social_stigma': [
        'stigma', 'sharm', 'sharam', 'shame', 'guilty', 'guilty feel',
        'blame', 'blamed', 'taana', 'taane', 'criticism', 'criticize',
        'judge', 'judging', 'society', 'samaj', 'community', 'caste',
        'religion', 'minority', 'discrimination', 'discriminate',
        'mental health', 'depression', 'anxiety', 'pagal', 'paagal',
        'psychiatrist', 'therapy', 'counseling', 'doctor', 'dawai',
        'medicine', 'pills', 'log kya kahenge', 'what will people say'
    ]
}

# Combine all lexicons
ALL_EMOTION_LEXICONS = {
    'hindi': HINDI_EMOTIONS,
    'hinglish': HINGLISH_EMOTIONS,
    'tamil': TAMIL_EMOTIONS,
    'telugu': TELUGU_EMOTIONS,
    'bengali': BENGALI_EMOTIONS,
    'marathi': MARATHI_EMOTIONS,
    'gujarati': GUJARATI_EMOTIONS,
    'english': ENGLISH_EMOTIONS
}

# Emotion intensity modifiers
INTENSITY_MODIFIERS = {
    'increase': {
        'bahut': 1.3, 'bohot': 1.3, 'bahuth': 1.3, 'bhot': 1.3,
        'very': 1.3, 'extremely': 1.4, 'too': 1.2, 'so': 1.2,
        'really': 1.2, 'quite': 1.15, 'totally': 1.25, 'completely': 1.3,
        'absolutely': 1.35, 'highly': 1.25, 'intensely': 1.35,
        'jyada': 1.25, 'zyada': 1.25, 'bohat': 1.3, 'kaafi': 1.2,
        'kafi': 1.2, 'bahut zyada': 1.4, 'bohot jyada': 1.4
    },
    'decrease': {
        'thoda': 0.7, 'thora': 0.7, 'thodi': 0.7, 'thori': 0.7,
        'little': 0.7, 'slightly': 0.75, 'somewhat': 0.8,
        'a bit': 0.75, 'kind of': 0.8, 'sort of': 0.8,
        'kam': 0.7, 'kaam': 0.7, 'kum': 0.7, 'thora bahut': 0.75
    },
    'negation': {
        'nahi': -1, 'nahin': -1, 'nai': -1, 'na': -1,
        'not': -1, 'no': -1, 'never': -1.2, 'dont': -1, 'dont': -1,
        'wont': -1, 'cant': -1, 'cannot': -1, 'kuch nahi': -1.1
    }
}

# Negation scope markers
NEGATION_MARKERS = [
    'nahi', 'nahin', 'nai', 'na', 'not', 'no', 'never', 'dont', 'dont',
    'wont', 'cant', 'cannot', 'nothing', 'nobody', 'nowhere', 'neither',
    'nor', 'kuch nahi', 'koi nahi', 'kabhi nahi'
]
