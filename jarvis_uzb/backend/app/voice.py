import speech_recognition as sr
import sys

def listen():
    r = sr.Recognizer()
    # Mikrofonni sozlash
    with sr.Microphone() as source:
        # Shovqinni kamaytirish
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            # Ovozni yozib olish (5 soniya limit)
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            
            # Google Speech Recognition orqali matnga o'girish (O'zbek tili)
            text = r.recognize_google(audio, language="uz-UZ")
            
            # Natijani stdout ga chiqarish (bu C++ ga boradi)
            print(text)
            
        except sr.WaitTimeoutError:
            pass # Hech narsa deyilmasa tinchgina chiqish
        except sr.UnknownValueError:
            pass # Tushunarsiz ovoz
        except Exception as e:
            pass # Boshqa xatolar

if __name__ == "__main__":
    listen()