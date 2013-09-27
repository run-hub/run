import ipclight
from lib31.python import cachedproperty
from .unpacker import Unpacker

class Decoder:
    
    #Public
       
    #TODO: add protocol return
    #TODO: add error handling/convertion       
    def decode(self, text_message):
        transport_message = self._transport_decoder.decode(text_message)
        message = self._transport_unpacker.unpack(transport_message)
        return message

    #Protected

    @cachedproperty
    def _transport_decoder(self):
        return ipclight.Decoder()
    
    @cachedproperty
    def _transport_unpacker(self):
        return Unpacker()    

    
class DecodeError(Exception): pass      