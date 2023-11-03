class RecieveEvent(type):

    def onRecieved(self, message:str) -> None:
        raise NotImplementedError()