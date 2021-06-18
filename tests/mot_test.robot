*** Settings ***
Library           OperatingSystem
Library           motlayer.mot

*** Variables ***
${Var}          VHAL


*** Test Cases ***
Init TCP Connection
    traceInit

Print Lib Layer Status
    printCPU



*** Keywords ***