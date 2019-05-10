#!/usr/bin/python3
import socket
import threading
from Crypto.PublicKey import RSA
class Server:
  def __init__(self):
    self.PORT = 1423
    self.PUBLIC_TEXT = "Baglandi."
    self.CODING = "ISO-8859-1"
    self.TEXTCODE = "UTF-8"
    self.sock = socket.socket()
    self.sock.bind(('', self.PORT))
    self.sock.listen()
    self.clients = []
    threading.Thread(target=self.invite).start()
  
  def start_listen(self,client):
    while True:
        data = self.listen(client.socket)
        if data == '':
          continue
        
        ad = data.split(':')[0]
        veri = ''.join(data.split(':')[1:]).encode(self.CODING)
        try:
          outer_key = RSA.importKey(veri)
          print("Public Key Alındı...")
          client.set_key(outer_key,ad)
        except:
          self.send(veri,client,ad)
          
  def encode(self, text):
    try:
      return text.encode(self.TEXTCODE)
    except UnicodeEncodeError:
      return text.encode(self.CODING)
  
  def send(self,data,client,target=None):
    sender = self.find_sender(target)
    veri = sender.key.encrypt(self.encode(client.name)+ b'->' + data, b'')[0]
    for user in self.clients:
      if user.name == client.name:
        continue
      user.send(veri)

  def find_sender(self,name):
    for client in self.clients:
      if client.name == name:
        return client

  def invite(self):
    while True:
      conn,add = self.sock.accept()
      client = Client(conn,add)
      self.clients.append(client)
      print("Kullanıcı katıldı.")
      threading.Thread(target=self.start_listen, args=(client,)).start()
  
  def listen(self,connection):
    data = connection.recv(16384).decode(self.CODING)
    return data

class Client:
  def __init__(self,connection,address):
    self.socket = connection
    self.key = None
    self.name = None
    self.address = address

  def set_key(self,key,ad):
    if self.key != None:
      return 
    self.key = key
    self.name = ad

  def send(self,data):
    self.socket.send(data)

server = Server()
