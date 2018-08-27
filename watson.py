#!/usr/bin/python
import re
import sys
import math
import pytz
import calendar_helper_functions as icalhelper
import glob
import datetime
import argparse
import os
import json
import timechart
from entry import Entry



# Whole new THING

def propagate_dates(entries):
    current_date=None
    for entry in entries:
        if entry.date!=None:
            current_date=entry.date
        entry.date=current_date


def propagate_endings(entries,max_minutes):
    laststart=None
    for entry in reversed(entries):
        if entry.end==None:
            entry.end=laststart
            if entry.get_duration()>max_minutes:
                entry.end=None
        laststart=entry.start

def total_duration(entries,matchtext=""):
    running_total=0
    for entry in entries:
        if matchtext in entry.title:
            running_total+=entry.get_duration()
    return running_total



#Todo:
# (C) log file to atoms should take content rather than a filename

__TIME_FORMAT = "%d/%m/%y %H:%M"

max_dist_between_logs = 15  # in minutes TODO these should be arguments for different types of input.
min_session_size = 15  # in minutes

def setup_argument_list():
    "creates and parses the argument list for Watson"
    parser = argparse.ArgumentParser( description="manages Watson")
    parser.add_argument('-d', nargs="?" , help="Show only tasks that are at least this many days old")
    parser.set_defaults(verbatim=False)
    return parser.parse_args()


def output_sessions_as_account(sessions):
        total_time = sum([entry.length()
                          for entry in sessions], datetime.timedelta())
        projects = {}
        for session in sessions:
            if session.project in projects:
               projects[session.project]+=session.length()
            else:
               projects[session.project]=session.length()

        for key, value in sorted(projects.iteritems(), key=lambda (k,v): (v,k)):
            print "%s: %s" % (value, key)


        print "Total project time".ljust(45)+str(total_time)
        return total_time


def days_old(session):
        delta = datetime.datetime.now() - session.start.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
	return delta.days

def report_on_day(file):
    print file
    entries=[]
    content=icalhelper.get_content('testinputs/entrytest.txt')
    for line in content:
        entries.append(Entry(line))
    propagate_dates(entries)
    propagate_endings(entries,15)
    print "Date: {}".format(entries[0].date)
    print "Ordered list of topics"





########## Input ##########

def full_detect(config_file='/config.json'):

    print "Watson v2.0"
    print "------------------------------"
    cwd=os.path.dirname(os.path.abspath(__file__))
    config = json.loads(open(cwd+config_file).read())
    for file in glob.glob(config["journals"]+"/*.md"):
        report_on_day(file)


