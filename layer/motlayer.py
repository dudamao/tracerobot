from robot.api.deco import keyword, library
from robot.api import logger
from iolayer import Trace_IO
from time import sleep
import configparser


# Marco

PWR_NONE = 0
PWR_ON = 170
PWR_HIZ = 15
PWR_BRK = 240
PWR_OFF = 255


class Translate(object):
    def __init__(self):
        self.d = dict()
        self.ini = configparser.ConfigParser()
        self.ini.read('./layer/config.ini')
        self.d['EOP'] = self.ini['motor']['EOP']
        self.d['SEL'] = self.ini['motor']['SEL']
        self.d['CA'] = self.ini['motor']['CA']
        self.d['SHF'] = self.ini['motor']['SHF']

        self.d['getpwrmode'] = self.ini['read']['getpwrmode']
        self.d['getvoltage'] = self.ini['read']['getvoltage']
        self.d['getspeed'] = self.ini['read']['getspeed']
        self.d['getcurrent'] = self.ini['read']['getspeed']
        self.d['getposition'] = self.ini['read']['getcurrent']
        self.d['setpwrmode'] = self.ini['write']['setpwrmode']
        self.d['setvoltage'] = self.ini['write']['setvoltage']


    def getIdx(self, name):
        return self.d[name]

    def getVar(self,idx,para):
        return self.d[para]+ '[' +str(idx) + ']'

    def getMotVar(self,motname,para):
        return self.getVar(self.d[motname],para)

@library
class Mot(object):
    def __init__(self, name):
        self.translayer = Translate()
        self.io = Trace_IO()
        self.io.traceInit()
        self.io.resetProgram()
        self.io.runProgram()
        self.motName = name
        self.cycleCounter = 0
        self.motIdx = self.translayer.getIdx(self.motName)
        self.motMode = 0
        self.motVol = 0
        self.motSpd = 0
        self.motCurr = 0
        self.motPos = 0
        self.setMode = 0
        self.setVol = 0


    def getVar(self,var):
        return self.translayer.getMotVar(self.motName,var)

    def down(self,para,value):
        var = self.getVar(para)
        self.io.addWriteSymbol(var,value)

    def up(self, para):
        var = self.getVar(para)
        self.io.addReadSymbol(var)

    def setPwrMode(self,mode):
        self.down('setpwrmode',mode)

    def setVoltage(self,vol):
        self.down('setvoltage',vol)

    def readStatus(self):
        for val in ['getpwrmode','getvoltage','getspeed' ,'getcurrent','getposition','setpwrmode','setvoltage']:
            self.up(val)

    def preCycle(self):
        self.readStatus()
        vlist = self.io.rdAll()
        self.motMode = vlist[0].value
        self.motVol =  vlist[1].value
        self.motSpd =  vlist[2].value
        self.motCurr = vlist[3].value
        self.motPos =  vlist[4].value
        self.setMode = vlist[5].value
        self.setVol =  vlist[6].value

    def postCycle(self):
        self.io.wrAll()

    def wholeCycle(self):
        self.cycleCounter += 1
        self.preCycle()
        self.postCycle()
        print('cycle %d is end' % (self.cycleCounter))
        sleep(0.05)

