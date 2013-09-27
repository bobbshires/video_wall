#!/usr/bin/env python

import datetime
import os
import sys

##-------------------------------##
DEBUG = True
CLOSED_MONDAYS = True
SLEEP = False
##-------------------------------##

# Command line constants

if SLEEP:
    cmd_str_ON  = 'pmset schedule wake \"'
    cmd_str_OFF = 'pmset schedule sleep \"'
else:
    cmd_str_ON  = 'pmset schedule poweron \"'
    cmd_str_OFF = 'pmset schedule shutdown \"'


current_date  = datetime.datetime.today()
#current_date  = datetime.date(2013,12,15)
day_increment = datetime.timedelta(days=1)

## Holidays
## We observes three holidays: Thanksgiving day, Christmas Eve (Dec 24) and Christmas Day (Dec 25)
#
# Determine the date of Thanksgiving
first_day_in_november = datetime.date(current_date.year, 11, 1).isoweekday()
if first_day_in_november <= 4:
    thanksgiving = datetime.date(current_date.year, 11, 26 - first_day_in_november)
else:
    thanksgiving = datetime.date(current_date.year, 11, 33 - first_day_in_november)

# and the other two holidays we observe, xmas eve and xmas day
xmas_eve = datetime.date(current_date.year, 12, 24)
xmas_day = datetime.date(current_date.year, 12, 25)
## End holidays

def process_day(my_date):

    day_of_week = my_date.weekday()     # 0==Monday, 6==Sunday

    commandline_ON  = ''
    commandline_OFF = ''

    if ((my_date == thanksgiving) or (my_date == xmas_eve) or (my_date == xmas_day)):
        if DEBUG:
            print my_date, 'is a Holiday!'
        process_day(my_date + day_increment)

    elif day_of_week == 6:        # Sunday
        if DEBUG:
            print '\n', my_date, 'is weekday()', day_of_week, '... a Sunday. We open at 11:30, close at 17:00.'
        commandline_ON  = cmd_str_ON  + my_date.strftime('%m/%d/%Y') + ' 11:30:00\"'
        commandline_OFF = cmd_str_OFF + my_date.strftime('%m/%d/%Y') + ' 17:10:00\"'

    elif day_of_week == 0 and CLOSED_MONDAYS:
        if DEBUG:
            print my_date, 'is a Monday and we\'re closed!'
        process_day(my_date + day_increment)

    else:
        if DEBUG:
            print '\n', my_date, 'is weekday()', day_of_week, '... a normal day. We open at 09:30, close at 17:00.'
        commandline_ON  = cmd_str_ON  + my_date.strftime('%m/%d/%Y') + ' 09:30:00\"'
        commandline_OFF = cmd_str_OFF + my_date.strftime('%m/%d/%Y') + ' 17:10:00\"'

    if DEBUG:
        print commandline_ON
        print commandline_OFF
    else:
        os.system(commandline_ON)
        os.system(commandline_OFF)


process_day(current_date + day_increment)
