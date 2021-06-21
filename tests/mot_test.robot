*** Settings ***
Library           OperatingSystem
Library           testlayer.MotTest

*** Test Cases ***

EOP Test1-1 - setBrk and setDuty
    initEOP
    testBrkandDutyConflict

EOP Test1-2 - setDuty and setBrk
    initEOP
    testBrkandDutyConflict

EOP Test2-1 - setHiz and setDuty
    initEOP
    testHiZandDutyConflict

EOP Test2-2 - setDuty and setHiz
    initEOP
    testDutyandHiZConflict

EOP Test3-1 - setOn and setDuty
    initEOP
    testOnandDutyConflict

EOP Test3-2 - setDuty and setOn
    initEOP
    testDutyandOnConflict

EOP Teardown
    initEOP


*** Keywords ***
