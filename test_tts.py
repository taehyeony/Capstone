from gtts import gTTS
import playsound as ps
import os

tts = gTTS(
    text='안녕하세요',
    lang='ko', slow=False
)
tts.save('ex_ko.mp3')
# 음원 재생
ps.playsound('ex_ko.mp3')
# 재생한 음원 삭제
os.remove('ex_ko.mp3')
