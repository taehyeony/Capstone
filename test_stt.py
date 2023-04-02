#stt(speech to text)
import speech_recognition as sr
r = sr.Recognizer()

with sr.Microphone() as source:
    print("마이크로 말해보세요.")
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language='ko-KR') 
        print(text)
    except:
        print('음성 인식에 실패하였습니다.')