*** Settings ***
Library           OperatingSystem
Library           iolayer.Trace_IO

*** Variables ***


*** Test Cases ***
Init TCP Connection
    traceInit

Print Lib Layer Status
    printCPU



*** Keywords ***