import re
import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')
nltk.download('omw-1.4')
# wordnet은 단어들 간의 의미론적인 관계를 정의한 어휘 데이터베이스이다. 
# 이후 wordnet 을 활용하여 Intent 로 정의해 놓은 키워드들의 동의어들을 추출한 이후,
# 해당 동의어들을 value로 하는 a dictionary of synonyms 를 생성할 것이다.
# 이를 통해 직접 사용자가 사용할 가능성이 있는 단어들을 사전에 정의할 필요없이, 동의어 확장이 가능하다.

# 키워드 목록 작성
list_words = ['hello','timings'] #키워드
list_syn = {} #동의어(유사어)를 저장할 dictionary
for word in list_words:
    sysnonyms = []#동의어 임시 저장
    for syn in wordnet.synsets(word):
        for lem in syn.lemmas(): #.lemmas는 syn이 Synset('***.?.00')형식으로 되어있는데 이를 Lemma class로 변환
            lem_name = re.sub('[^a-zA-Z0-9 \n\.]',' ',lem.name()) #동의어 문자열에서 특수문자 제거
            sysnonyms.append(lem_name)
    list_syn[word]=set(sysnonyms)#중복된 값 제거