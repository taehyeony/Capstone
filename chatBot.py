import re
import nltk
import speech_recognition as sr
from nltk.corpus import wordnet
from gtts import gTTS
import playsound as ps
import os


nltk.download('wordnet')
nltk.download('omw-1.4')

#stt
def stt():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("질문을 하세요.")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='ko-KR')
        except:
            print('음성 인식에 실패하였습니다.')
            return 0
    return text

#tts
def tts(text):
    tts = gTTS(
        text=text,
        lang='ko', slow=False
    )
    tts.save('ex_ko.mp3')
    
    ps.playsound('ex_ko.mp3')
    
    os.remove('ex_ko.mp3')

#키워드 동의어
list_words = ['hello','timings'] #키워드
list_syn = {} #동의어(유사어)를 저장할 dictionary - 사용자가 입력할 가능성이 있는 단어
for word in list_words:
    sysnonyms = [] # 동의어 임시 저장
    for syn in wordnet.synsets(word):
        for lem in syn.lemmas(): #.lemmas는 syn이 Synset('***.?.00')형식으로 되어있는데 이를 Lemma class로 변환
            lem_name = re.sub('[^a-zA-Z0-9 \n\.]',' ',lem.name()) #동의어 문자열에서 특수문자 제거
            sysnonyms.append(lem_name)
    list_syn[word]=set(sysnonyms)#중복된 값 제거

keywords = {} #Intent 목록
keywords_dict = {}#Intent를 |로 구분해 저장

#chatBot
