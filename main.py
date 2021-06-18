from layer.motlayer import *


if __name__ == '__main__':
    list = []
    EOP = mot('EOP')
    while (True):
        EOP.setPwrMode(PWR_BRK)
        EOP.setVoltage(200)
        EOP.wholeCycle()
