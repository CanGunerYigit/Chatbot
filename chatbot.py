from cleverbotfree import Cleverbot 
from googletrans import Translator
from gtts import gTTS #uygun ses formatına dönüştürecek
import random #random mp3 formatında kayıt oluşturacak
import os #ses kayıtlarını oluşturmaya ve silmeye yarar
from playsound import playsound #seslendirme
import speech_recognition as sr
import tkinter as tk
from PIL import Image,ImageTk
from itertools import count
import threading

translator = Translator()            #Translator objesinden referans alan değişken oluştur
rec=sr.Recognizer()         #sr ı referans alacak değişken oluştur
stopgif= True




class ImageLabel(tk.Label):
   def load(self,im):
      if isinstance(im,str):
         im=Image.open(im)
      self.loc=0
      self.frames=[]
      self.runtimes=0
      try:
         for i in count(1):
            self.frames.append(ImageTk.PhotoImage(im.copy()))
            im.seek(i)
      except EOFError:
         pass
      try:
         self.delay = im.info["duration"]
      except:
         self.delay = 100
      if len(self.frames)==1:
         self.config(image=self.frames[0])
      else:
         self.next_frame()
   def unload(self):
      self.config(image="")
      self.frames=None
   def next_frame(self):
      if self.frames:
         if stopgif == False:
            self.loc +=1
         else:
            self.loc = 1
         self.loc %= len(self.frames)
         self.config(image=self.frames[self.loc])
         self.after(self.delay,self.next_frame)




def record():      #konuşmamızı kayıt alacak olan fonksyion
   with sr.Microphone() as source:  #mikrofonu kaynak olarak kullansın
      voice_rec=""
      audio=rec.listen(source,5,5) #mikrofonu dinlesin 5 saniye boyunca konuşmazsa kapansın, 5 saniyede konuşma uzunluğu olsun
      try:
         voice_rec=rec.recognize_google(audio,language="tr-TR") #seslendirmemizi türkçe yapsın
      except sr.UnknownValueError: #gelen veriyi yakalayamadığında
         speak("anlayamadım")
      except sr.Recognizer: #program beklenmedik bir hata aldığında
         speak("sistem hata aldı")
      return voice_rec #hatasızsa almış olduğu voice_rec değişkenini dönsün


def speak(text): #gönderdiğimiz texti sese çevirecek bir fonksiyon 
   global stopgif
   stopgif=False
  
   tts=gTTS(text,lang="tr") #texti türkçe seslendirecek bir atama
   rand=random.randint(1,10000) #kaydedilecek mp3 seslendirmesine random isim atama
   file="audio"+str(rand)+".mp3" #ismi audio ile başlayan random isim verip sonuna .mp3 uzantısını ekleyen file oluşturma
   tts.save(file) #ses dosyasını alıp projeye kaydeder
   playsound(file) #oluşturulan file ı seslendir
   os.remove(file) #kullanıldıktan sonra otomatik sil
   stopgif=True
   

def translate_text(who,text,lang):             #translate etmek üzere bir fonksiyon oluştur
   text_translated= translator.translate(text,dest=lang) #translate edip text_translated değişkenine atadı
   print(who,"(",lang,"):",text_translated.text)
   return text_translated.text   #translate edilmiş halini yakalayalım

@Cleverbot.connect                             #cleverbota erişim
def chat(bot,user_konus,bot_konus):          #chat diye bir fonksiyon tanımlandı
    while True:                                #konuşurken sonsuz döngü için
      user_input=record()           #öncelikle konuşmayı bizim başlatmamız gerekiyor
      print(user_konus,user_input)  #hangi dilde ne konuştuk terminale bassın
      user_input_en =translate_text(user_konus,user_input,"en") #girdiğimiz türkçe metni ingilizceye çevirecek
      if user_input == "quit":                 #sonsuz while döngüsünden çıkmak için
         break
      reply = bot.single_exchange(user_input_en)   #botun bize cevap vermesi için reply diye bir değişkende tutacağız
      print(bot_konus,reply)                 #vermiş olduğu cevabı terminal ekranına yazdır
      bot_reply_tr =translate_text(bot_konus,reply,"tr") #botun cevabını türkçeye çevirecek 
      speak(bot_reply_tr) #türkçe seslendirmeyi dinlemek için
      
    bot.close()


    
def display_gif():
   print("gif calisti")
   root = tk.Tk()
   lbl = ImageLabel(root)
   lbl.pack()
   lbl.load("bot.gif")
   root.mainloop()

def run_bot():
   print("bot calisti")
   chat("User: ","Bot: ")

t1 = threading.Thread(target=display_gif)
t1.start()
t2 = threading.Thread(target=run_bot)
t2.start()




