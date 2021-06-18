import lauterbach.trace32.rcl as t32
from queue import Queue
from robot.api.deco import keyword, library
from robot.api import logger


class Var(object):
    def __init__(self, name, *initvalue):
        self.name = ''
        self.value = 0
        self.name = name
        if (len(initvalue) != 0):
            self.value = initvalue[0]

    def setvalue(self, value):
        self.value = value


class VarQueue(object):
    def __init__(self, queue_name):
        self.name = queue_name
        self.state = 'Init'
        self.q = Queue()

    def checkQueue(self):
        if (self.q.empty() == False):
            self.state = 'NotEmpty'
        else:
            self.state = 'Empty'
        return self.state

    def getStatus(self):
        return self.state

    def addSignal(self, var):
        if (type(var) is Var):
            self.q.put(var)
            ret = True
        else:
            ret = False
        self.checkQueue()

    def flushQ(self):
        self.q = Queue()
        self.checkQueue()

    def getSignal(self):
        self.checkQueue()
        if (self.state == 'NotEmpty'):
            tempvar = self.q.get()
        else:
            tempvar = False
        return tempvar


@library
class Trace_IO(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.1'

    def __init__(self):
        self.readQ = VarQueue('readQ')
        self.writeQ = VarQueue('writeQ')
        self.dbg = 0xFF

    @keyword
    def traceInit(self):
        try:
            self.dbg  = t32.connect()
        except:
            print('Init Failed, please check connection')
        else:
            print('Init Successful!')

    def retStatus(self):
        return loggger.info(dbg.VERSION)

    def rd(self, name):
        variable = self.dbg.variable.read(name)
        return variable.value

    def wr(self, name, value):
        self.dbg.variable.write(name, value)

    @keyword
    def addReadSymbol(self, name):
        var = Var(name)
        self.readQ.addSignal(var)

    @keyword
    def addWriteSymbol(self, name, value):
        var = Var(name, value)
        self.writeQ.addSignal(var)

    @keyword
    def wrAll(self):
        while (self.writeQ.checkQueue() == 'NotEmpty'):
            symbol = self.writeQ.getSignal()
            self.wr(symbol.name, symbol.value)

    @keyword
    def rdAll(self):
        symbol_list = []
        symbol = Var('NoName')
        while (self.readQ.checkQueue() == 'NotEmpty'):
            symbol = self.readQ.getSignal()
            symbol.value = self.rd(symbol.name)
            symbol_list.append(symbol)
        return symbol_list

    @keyword
    def printCPU(self):
        cpu = self.dbg.fnc('CPU()')
        print('TRACE32 is connecting to ' + cpu)
