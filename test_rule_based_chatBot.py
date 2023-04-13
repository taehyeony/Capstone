import re
import nltk
from nltk.corpus import wordnet

nltk.download("wordnet")
nltk.download("omw-1.4")
# wordnet은 단어들 간의 의미론적인 관계를 정의한 어휘 데이터베이스이다.
# 이후 wordnet 을 활용하여 Intent 로 정의해 놓은 키워드들의 동의어들을 추출한 이후,
# 해당 동의어들을 value로 하는 a dictionary of synonyms 를 생성할 것이다.
# 이를 통해 직접 사용자가 사용할 가능성이 있는 단어들을 사전에 정의할 필요없이, 동의어 확장이 가능하다.

# 키워드 목록 작성 및 동의어 획득
list_words = ["안녕", "timings"]  # 키워드
list_syn = {}  # 동의어(유사어)를 저장할 dictionary - 사용자가 입력할 가능성이 있는 단어
for word in list_words:
    sysnonyms = []  # 동의어 임시 저장
    for syn in wordnet.synsets(word):
        for (lem) in (syn.lemmas()):  # .lemmas는 syn이 Synset('***.?.00')형식으로 되어있는데 이를 Lemma class로 변환
            lem_name = re.sub("[^a-zA-Z0-9 \n\.]", " ",
                              lem.name())  # 동의어 문자열에서 특수문자 제거
            sysnonyms.append(lem_name)
    list_syn[word] = set(sysnonyms)  # 중복된 값 제거

# Keyword List 는 챗봇이 사용자의 입력을 받은 이후 탐색할 대상이다.
# 많은 Keyword 를 추가할 수록, 사용자의 입력에 대해 적절한 응답을 수행할 가능성이 많아지기 때문에, 결과적으로 챗봇이 성능이 올라갈 것이다.
# 앞에서 말했듯이, wordnet 을 사용하여 Intent 의 동의어들을 dictionary 구조에 저장할 것이다.
# 소스코드에서 list_syn 이 저장될 변수이다.

# Intent(의도) 목록 작성
# 예를 들어 hello와 유사한 단어가 입력되면 안녕이라는 intent를 가짐
keywords = {}  # Intent 목록
keywords_dict = {}  # Intent를 |로 구분해 저장

# 키워드 사전에서 새 키 정의
keywords["안녕"] = []
# 키워드 동의어로 키워드 사전 값 채우기
# 정규식에 맞춰 formatting
for synonym in list(list_syn["안녕"]):  # Intent에 맞는 동의어를 keyword dictionary에 저장
    keywords["안녕"].append(synonym)

keywords["timings"] = []
for synonym in list(list_syn["timings"]):
    keywords["timings"].append(synonym)

for intent, keys in keywords.items():
    # Join 연산으로 키워드를 |로 결합
    # keywords_dict dictionary에 저장
    keywords_dict[intent] = "|".join(keys)

# 앞서 지정한 list_syn(키워드의 동의어 집합 리스트)을 Intent 와 매칭 시키는 dictionary 를 생성해야 한다.
# list_syn 은 사용자가 입력할 가능성이 있는 키워드를 정의해놓은 데이터라면,
# keywords_dict 는 해당 키워드들이 실제 Intent 와 매칭될 수 있도록 정의하는 자료구조이다.

# Intent : responses - 의도 : 반응
responses = {
    "안녕": "안녕하세요",
    "timings": "We are open from 9AM to 5PM, Monday to Friday. We are closed \
        on weekends and public holidays",
    "fallback": "다시 한번 말씀해 주시겠어요?",
}

# 의도와 일치하는 응답 생성
# 챗봇 실행
while True:
    print("How may I help you?")
    # 사용자 입력을 받아 모든 문자를 소문자로 변환
    # 1. User Input
    user_input = input().lower()
    # 챗봇 종료 조건 정의
    if user_input == "quit":
        print("Thank you for visiting.")
        break
    matched_intent = None
    for intent, pattern in keywords_dict.items():
        # 정규식 검색 기능을 사용하여 사용자 입력에서 키워드 찾기
        if re.search(pattern, user_input):
            # 키워드가 일치하면 keywords_dict에서 해당 의도를 선택
            matched_intent = intent
    # 맞는 의도가 없으면 fallback을 기본으로 선택
    key = "fallback"
    if matched_intent in responses:
        key = matched_intent
    # 챗봇이 선택한 intent와 일치하는 응답 출력
    print(responses[key])
