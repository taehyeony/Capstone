import re
import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')
nltk.download('omw-1.4')
# wordnet은 단어들 간의 의미론적인 관계를 정의한 어휘 데이터베이스이다. 
# 이후 wordnet 을 활용하여 Intent 로 정의해 놓은 키워드들의 동의어들을 추출한 이후,
# 해당 동의어들을 value로 하는 a dictionary of synonyms 를 생성할 것이다.
# 이를 통해 직접 사용자가 사용할 가능성이 있는 단어들을 사전에 정의할 필요없이, 동의어 확장이 가능하다.

# 키워드 목록 작성 및 동의어 획득
list_words = ['hello','timings'] #키워드
list_syn = {} #동의어(유사어)를 저장할 dictionary - 사용자가 입력할 가능성이 있는 단어
for word in list_words:
    sysnonyms = []#동의어 임시 저장
    for syn in wordnet.synsets(word):
        for lem in syn.lemmas(): #.lemmas는 syn이 Synset('***.?.00')형식으로 되어있는데 이를 Lemma class로 변환
            lem_name = re.sub('[^a-zA-Z0-9 \n\.]',' ',lem.name()) #동의어 문자열에서 특수문자 제거
            sysnonyms.append(lem_name)
    list_syn[word]=set(sysnonyms)#중복된 값 제거
    
# Keyword List 는 챗봇이 사용자의 입력을 받은 이후 탐색할 대상이다.
# 많은 Keyword 를 추가할 수록, 사용자의 입력에 대해 적절한 응답을 수행할 가능성이 많아지기 때문에, 결과적으로 챗봇이 성능이 올라갈 것이다.
# 앞에서 말했듯이, wordnet 을 사용하여 Intent 의 동의어들을 dictionary 구조에 저장할 것이다.
# 소스코드에서 list_syn 이 저장될 변수이다.

#Intent(의도) 목록 작성
keywords = {}
keywords_dict = {}

# Defining a new key in the keywords dictionary
keywords['greet'] = []
# Populating the values in the keywords dictionary with synonyms of keywords
# formatted with RegEx metacharacters
for synonym in list(list_syn['hello']):
    keywords['greet'].append('.*\\b' + synonym + '\\b.*')

# Defining a new key in the keywords dictionary
keywords['timings'] = []
for synonym in list(list_syn['timings']):
    keywords['timings'].append('.*\\b' + synonym + '\\b.*')

for intent, keys in keywords.items():
    # Joining the values in the keywords dictionary with the OR(|) operator updating
    # them in keywords_dict dictionary
    keywords_dict[intent]=re.compile('|'.join(keys))
    
#앞서 지정한 list_syn(키워드의 동의어 집합 리스트)을 Intent 와 매칭 시키는 dictionary 를 생성해야 한다.
# list_syn 은 사용자가 입력할 가능성이 있는 키워드를 정의해놓은 데이터라면,
# keywords_dict 는 해당 키워드들이 실제 Intent 와 매칭될 수 있도록 정의하는 자료구조이다.