from robot.api.deco import keyword, library
from robot.api import logger
from motlayer import *


@library
class MotTest(object):
    def __init__(self):
        self.mot = 0
        self.testSts = 'OFF'

    def initMot(self, name):
        self.mot = Mot(name)
        sleep(1)

    @keyword
    def initEOP(self):
        self.initMot('EOP')

    @keyword
    def Cycle(self, counter):
        for i in range(counter):
            self.mot.wholeCycle()

    @keyword
    def testBrkandDutyConflict(self):
        self.mot.setPwrMode(PWR_BRK)
        self.mot.setVoltage(200)
        self.Cycle(20)
        if (self.mot.motSpd > 300):
            raise Exception('Motor false Started!')

    @keyword
    def testDutyandBrkConflict(self):
        self.mot.setPwrMode(PWR_ON)
        self.mot.setVoltage(200)
        self.Cycle(1)
        self.mot.setPwrMode(PWR_BRK)

        self.Cycle(20)
        if (self.mot.motSpd > 300):
            raise Exception('Motor false Started!')

    @keyword
    def testHiZandDutyConflict(self):
        self.mot.setPwrMode(PWR_HIZ)
        self.mot.setVoltage(200)

        self.Cycle(20)
        if (self.mot.motSpd > 300):
            raise Exception('Motor false Started!')

    @keyword
    def testDutyandHiZConflict(self):
        self.mot.setPwrMode(PWR_ON)
        self.mot.setVoltage(200)
        self.Cycle(1)
        self.mot.setPwrMode(PWR_HIZ)

        self.Cycle(20)
        if (self.mot.motSpd > 300):
            raise Exception('Motor false Started!')

    @keyword
    def testOnandDutyConflict(self):
        self.mot.setPwrMode(PWR_ON)
        self.mot.setVoltage(200)

        self.Cycle(20)
        if (self.mot.motSpd < 300):
            raise Exception('Motor not Started!')

    @keyword
    def testDutyandOnConflict(self):
        self.mot.setVoltage(200)
        self.mot.setPwrMode(PWR_ON)
        self.Cycle(20)
        if (self.mot.motSpd < 300):
            raise Exception('Motor not Started!')

    @keyword
    def testOntoHiz(self):
        self.mot.setVoltage(200)
        self.mot.setPwrMode(PWR_ON)
        self.Cycle(1)
        self.mot.setPwrMode(PWR_HIZ)
        self.Cycle(10)
        if (self.mot.motSpd > 300):
            raise Exception('Motor not Stop!')

    @keyword
    def testOntoBrk(self):
        self.mot.setVoltage(200)
        self.mot.setPwrMode(PWR_ON)
        self.Cycle(1)
        self.mot.setPwrMode(PWR_BRK)
        self.Cycle(10)
        if (self.mot.motSpd > 300):
            raise Exception('Motor not Stop!')

    @keyword
    def testBrktoOn(self):
        self.mot.setPwrMode(PWR_BRK)
        self.Cycle(5)
        self.mot.setVoltage(200)
        self.mot.setPwrMode(PWR_ON)
        self.Cycle(10)
        if (self.mot.motSpd < 300):
            raise Exception('Motor not Start!')
    @keyword
    def testBrktoHiz(self):
        self.mot.setPwrMode(PWR_BRK)
        self.Cycle(5)
        self.mot.setPwrMode(PWR_HIZ)
        self.Cycle(10)
        if (self.mot.motSpd > 300):
            raise Exception('Motor not Stop!')
    @keyword
    def testHiztoBrk(self):
        self.mot.setPwrMode(PWR_BRK)
        self.Cycle(5)
        self.mot.setPwrMode(PWR_HIZ)
        self.Cycle(10)
        if (self.mot.motSpd > 300):
            raise Exception('Motor not Stop!')