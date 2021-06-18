from robot.api.deco import keyword, library
from robot.api import logger
from iolayer import Trace_IO
from time import sleep


# Marco

PWR_NONE = 0
PWR_ON = 170
PWR_HIZ = 15
PWR_BRK = 240
PWR_OFF = 255


class translate(object):
    def __init__(self):
        self.d = dict()

        self.d['EOP'] = 0
        self.d['SEL'] = 1
        self.d['CA'] = 2
        self.d['SHF'] = 3

        self.d['getpwrmode'] = 'EcMotShr_xGetPwrMod'
        self.d['getvoltage'] = 'EcMotShr_rGetVoltAct'
        self.d['getspeed'] = 'EcMotShr_nGetAvgSpd'
        self.d['getcurrent'] = 'EcMotShr_iGetAvgCur'
        self.d['getposition'] = 'EcMotShr_stGetHallPos'

        self.d['setpwrmode'] = 'EcMotShr_xSetPwrMod_C'
        self.d['setvoltage'] = 'EcMotShr_uSetUTgt_C'


    def getIdx(self, name):
        return self.d[name]

    def getVar(self,idx,para):
        return self.d[para]+ '[' +str(idx) + ']'

    def getMotVar(self,motname,para):
        return self.getVar(self.d[motname],para)

@library
class mot(object):
    def __init__(self, name):
        self.translayer = translate()
        self.io = Trace_IO()
        self.io.traceInit()
        self.motName = name
        self.cycleCounter = 0
        self.motIdx = self.translayer.getIdx(self.motName)


    def getVar(self,var):
        return self.translayer.getMotVar(self.motName,var)

    def down(self,para,value):
        var = self.getVar(para)
        self.io.addWriteSymbol(var,value)

    def setPwrMode(self,mode):
        self.down('setpwrmode',mode)

    def setVoltage(self,vol):
        self.down('setvoltage',vol)

    def preCycle(self):
        self.io.rdAll()


    def postCycle(self):
        self.io.wrAll()

    def wholeCycle(self):
        self.cycleCounter += 1
        self.preCycle()
        self.postCycle()
        print('cycle %d is end' % (self.cycleCounter))
        sleep(0.05)

