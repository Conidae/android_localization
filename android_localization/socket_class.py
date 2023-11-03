import socket
class SympleServer:
    def __init__(self,host:str,port:int):
        print('server start')
        self.__socket = None
        self.socket_listener:SympleServer = None
        self.__buffer = 1024
        self.entry = (host,port)
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        try:
            self.__socket.shutDown(socket.SHUT_RDWR)
            self.socket.close()
        except:
            pass

    def accept(self):
        #create socket
        self.__socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)

        self.__socket.settimeout(60)
        self.__socket.bind(self.entry)
        self.__socket.listen(1)
        
        print("Server started :", self.entry)
        while True:
            conn, _ = self.__socket.accept()
            print('accepted!')
            while True:
                try:
                    message_recv = conn.recv(self.__buffer).decode('utf-8')
                    if message_recv == '':
                        break
                    if 'quit' in message_recv:
                        return
                    self.onRecieved(message_recv)
                except ConnectionResetError:
                    break
                except BrokenPipeError:
                    break

    def onRecieved(self, message:str) -> None:
        if self.socket_listener != None:
            self.socket_listener.onRecieved(message=message)
        raise NotImplementedError()