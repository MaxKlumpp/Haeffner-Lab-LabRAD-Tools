'''
### BEGIN NODE INFO
[info]
name = Pulser_729
version = 1.0
description =
instancename = Pulser_729

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 20
### END NODE INFO
'''
from labrad.server import LabradServer, setting
from twisted.internet.defer import Deferred, DeferredLock, inlineCallbacks, returnValue
from twisted.internet.threads import deferToThread
from twisted.internet import reactor
from api import api
from labrad.types import Error

class Pulser_729(LabradServer):
    
    name = 'pulser_729'
    
    @inlineCallbacks    
    def initServer(self):
        self.api  = api()
        self.inCommunication = DeferredLock()
        yield self.initializeBoard()
    
    @inlineCallbacks
    def initializeBoard(self):
        connected = self.api.connectOKBoard()
        while not connected:
            print 'not connected, waiting for 10 seconds to try again'
            yield self.wait(10.0)
            connected = self.api.connectOKBoard()
    
    @setting(0, 'Reset DDS', returns = '')
    def resetDDS(self , c):
        """
        Reset the ram position to 0
        """
        self.check_control(c)
        yield self.inCommunication.acquire()
        yield deferToThread(self.api.resetAllDDS)
        self.inCommunication.release()
        
    @setting(1, "Program DDS", program = '*(is)', returns = '')
    def programDDS(self, c, program):
        """
        Programs the DDS, the input is a tuple of channel numbers and buf objects for the channels
        """
        self.check_control(c)
        print program
        yield self.inCommunication.acquire()
        yield deferToThread(self._programDDSSequence, program)
        self.inCommunication.release()
    
    @setting(2, "Reinitialize DDS", returns = '')
    def reinitializeDDS(self, c):
        """
        Reprograms the DDS chip to its initial state
        """
        yield self.inCommunication.acquire()
        yield deferToThread(self.api.initializeDDS)
        self.inCommunication.release()
    
    def _programDDSSequence(self, program):
        '''takes the parsed dds sequence and programs the board with it'''
        for chan, buf in program:
            self.api.setDDSchannel(chan)
            self.api.programDDS(buf)
        self.api.resetAllDDS()
    
    def wait(self, seconds, result=None):
        """Returns a deferred that will be fired later"""
        d = Deferred()
        reactor.callLater(seconds, d.callback, result)
        return d
        
if __name__ == "__main__":
    from labrad import util
    util.runServer( Pulser_729() )