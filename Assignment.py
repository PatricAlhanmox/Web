from socket import *
import threading
import time
import datetime as dt
import sys

class Peer():
    def __init__(self, Type, _id, succssor1, succssor2, time):
        self._id = succssor[0]
        self.succssor1 = succssor[1]
        self.succssor2 = succssor[2]
        self.Type = Type
        self.time = int(time)
        self.files = [] 
        self.PORT = int(self._id) + 10000        
        self.HOST = '127.0.0.1'
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.s.bind((self.HOST,self.PORT))


    def udpAsClient(self, succssor):
        try:
            while True:
                time.sleep(self.time)
                address1 = ('127.0.0.1', self.succssor1 + 10000)
                address2 = ('127.0.0.1', self.succssor2 + 10000)
                message = str(self._id) + ',' + '1' + ',' + '1'
                message = message.encode(encoding='utf-8', errors='ignore')
                self.s.sendto(message, address1)
                self.s.sendto(message, address2)
                break
            print('A request has sent to peer',self.succssor1,'and',self.succssor2)
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            pass         
        
    
    def udpAsServer(self, succssor):
        address = ('127.0.0.1',self.PORT)
        try:
            while True:
                data, addr = self.s.recvfrom(2048)
                data = data.decode(encoding='utf-8', errors = 'ignore')
                udpStore = [0,0]
                udpStore = data.split(',')
                print('A request is received from peers', udpStore[0])
                message = str(self._id) + ',' + '2' + ',' + '2'+ udpStore[2]
                message = message.encode(encoding='utf-8', errors='ignore')
                address = ('127.0.0.1', int(udpStore[0]) + 10000)
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            pass   
            
    def TCPReceving(self):
        sock = socket(AF_INET, SOCK_STREAM)    
        sock.bind(('127.0.0.1', self.PORT))
        sock.listen(5)
        print('Server Joining...')  
        while True:
            c, ad = sock.accept()
            Data = c.recv(2048)
            Data = tcp_data.decode()
            rec = []  
            rec = Data.split(',')
            message = rec[0] + ',' + str(self.succssor1) + ',' + str(self.succssor2)
            Sending(Data, int(rec[2]))
            print('My first succssor is now peer ', str(self.succssor1))
            print('My second succssor is now peer ', str(self.succssor2))
            c.cloes()
        sock.close()
    
    def Sending(self, message, destination):
        tcp = socket(AF_INET, SOCK_STREAM)
        tcp.connect((self.HOST, self.PORT))
        message = message.encode(encoding='utf-8', errors='ignore')
        tcp.send(message)
        tcp.close()
    
succssor = [int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])]
peer = Peer(sys.argv[1], succssor[0], succssor[1], succssor[2], sys.argv[5])
if sys.argv[1] == 'init':
    print('Start peer' + sys.argv[6] +' at Port', str(peer.PORT))
    print('Peer',sys.argv[6],' can find first successor on port', str(int(succssor[1])+1000), 'second successor on port', str(int(succssor[2])+1000))    
elif sys.argv[1] == 'Ping':
    threading.Thread(target=peer.udpAsClient(succssor), args=()).start()
    threading.Thread(target=peer.udpAsServer(succssor), args=()).start()
elif sys.argv[1] == 'Joining':
    threading.Thread(target=peer.TCPReceving(), args=()).start() 
