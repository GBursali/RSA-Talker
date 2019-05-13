#!/usr/bin/python3
#-*-coding:utf8-*-
from Crypto.PublicKey import RSA # Şifre çözme
import socket # LAN üzerinden iletişim
import threading # Aynı anda hem mesaj okuyup hem yazabilmek
import os # Ekran temizlemek
class Kullanıcı:
  def __init__(self, isim):
    #Sabitler
    self.isim = isim
    self._PORT = 1423
    self.SET = "ISO-8859-1"
    self.TR="UTF-8"
    self.get_key(isim)
    if self.key is None:
      print("Sertifikan bulunmamakta. Lütfen önce bir sertifika edin.")
    self.bağlantıyı_ayarla()  
    self.send_pubkey()
    self.log = [isim]
    self.crypter = None
    os.system('cls' if os.name == 'nt' else 'clear')

  def get_key(self,isim = None):
    sertifika = isim
    try:
      with open(isim, "r") as sertifika:
        self.key = RSA.importKey(sertifika.read())
    except FileNotFoundError:
      print("Sertifikan yokmuş. Neyseki, şimdilik senin için geçici olarak oluşturuyoruz {}".format(isim))
      with open(isim, "wb") as sertifika:# Şimdilik yeni sertifika oluşturuyor
        anahtar = RSA.generate(1024)
        sertifika.write(anahtar.exportKey())
        self.key = anahtar
      
  def encode(self,text):
    try:
      return text.encode(self.TR)
    except UnicodeEncodeError:
      return text.encode(self.SET)

  def decode(self, text):
    try:
      return text.decode(self.TR)
    except UnicodeDecodeError:
      return text.decode(self.SET)

  def send_pubkey(self):
    seed =self.encode(self.isim + ':') + self.key.publickey().exportKey()
    self._bağlantı.send(seed)
    print("Public key gönderildi.")

  def bağlantıyı_ayarla(self):
    self._bağlantı = socket.socket()  
    self._bağlantı.connect(('', self._PORT))# LAN ile yapacaksak buraya serve ip girmemiz gerekiyor.

  def send(self, düz_metin):
    if düz_metin.rfind(':') == -1:
      düz_metin = '{}:{}'.format(self.isim,düz_metin) 
    şifreli_metin = self.encode(düz_metin)
    self.log.append(düz_metin)
    self.yaz()
    self._bağlantı.send(şifreli_metin)

  def listen(self):
    _BUFFER = 16384 
    while True:
      data = self._bağlantı.recv(_BUFFER)
      if data == b'':
        continue
      düz_metin = self.deşifrele(data)
      self.log.append(düz_metin)
      self.yaz()

  def yaz(self):
    os.system('cls' if os.name == 'nt' else 'clear')
    for metin in self.log:
      print(metin)      

  def deşifrele(self, şifreli_metin):
    veri = self.key.decrypt(şifreli_metin)
    return self.decode(veri)

pawn = Kullanıcı(input('Adınız:'))
threading.Thread(target=pawn.listen).start()
while True:
  pawn.send(input())
