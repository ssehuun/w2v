#-*- coding:utf-8 -*-

#startTimeStr : '2008-08-10'
#endTimeStr : '2008-09-10'
#Iteration Range : 'D' = day, 'H' = hour

#USAGE 1 : getTimeList('2008-08-01', '2008-08-10', 'H')
#USAGE 2 : getTimeList('2008-08-01', '2008-08-10', 'D')

#RESULT 1 : '2008-08-01 00:00:00', '2008-08-01 01:00:00' ...
#           '2008-08-10 22:00:00', '2008-08-10 23:00:00'
#RESULT 2 : '2008-08-01 00:00:00', '2008-08-02 00:00:00' ...
#           '2008-08-09 00:00:00', '2008-08-10 00:00:00'
from time import *

def getTimeList(startTimeStr, endTimeStr, rangeType):
    #init vars
    startTime = ''
    endTime = ''
    startTimeDigit = 0
    endTimeDigit = 0
    addRange = 0
    
    timeList = []
    
    #set rangeTime
    if rangeType == 'H':
        addRange = 60 * 60
    elif rangeType == 'D':
        addRange = 60 * 60 * 24
    else:
        return []

    #set startTime, endTime
    startTime = strptime(startTimeStr, '%Y-%m-%d')
    startTimeDigit = mktime(startTime)
    endTime = strptime(endTimeStr + " 23:59:59", '%Y-%m-%d %H:%M:%S')
    endTimeDigit = mktime(endTime)

    if startTimeDigit >= endTimeDigit:
        timeList.append(strftime('%Y-%m-%d %H:%M:%S', localtime(startTimeDigit)))
        return timeList

    #set time list
    while True:
        if startTimeDigit > endTimeDigit:
            break;
        timeList.append(strftime('%Y-%m-%d %H:%M:%S', localtime(startTimeDigit)))
        startTimeDigit += addRange
    
    return timeList

def getTimeTuple(startTimeStr, endTimeStr, rangeType):
    #init vars
    startTime = ''
    endTime = ''
    startTimeDigit = 0
    endTimeDigit = 0
    addRange = 0

    timeList = []
    timeTuple = ()
     
    #set rangeTime
    if rangeType == 'H':
        addRange = 60 * 60
    elif rangeType == 'D':
        addRange = 60 * 60 * 24
    else:
        return ()

    #set startTime, endTime
    startTime = strptime(startTimeStr, '%Y-%m-%d')
    startTimeDigit = mktime(startTime)
    endTime = strptime(endTimeStr + " 23:59:59", '%Y-%m-%d %H:%M:%S')
    endTimeDigit = mktime(endTime)

    if startTimeDigit >= endTimeDigit:
        timeList.append(localtime(startTimeDigit))
        return timeTuple

    #set time tuple
    while True:
        if startTimeDigit > endTimeDigit:
            break;
        timeList.append(localtime(startTimeDigit))
        #print localtime(startTimeDigit)
        startTimeDigit += addRange

    timeTuple = tuple(timeList)
    return timeTuple
