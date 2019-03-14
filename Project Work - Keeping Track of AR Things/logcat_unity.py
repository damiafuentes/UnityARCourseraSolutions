#!/usr/bin/python
#
# Usage:
# adb logcat -v time | python logcat_unity.py
# 
# To add adb to the directory:
# export PATH=$PATH:~/Library/Android/sdk/platform-tools/

import sys
import re

IGNORED_LINES=["(Filename:"]
LOG_TAG="Unity"
REGEX_LINE = "([0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]) ([DIWEF])\/"+LOG_TAG+"\s*\((\s*[0-9]*)\):(.*)"

RED="\033[1;31m"
YELLOW="\033[1;33m"
NO_COLOR="\033[0m"

def colorize(color, text):
	return color + text + NO_COLOR

def isDebugOrInfo(log_level):
	log_level = log_level.rstrip()
	return log_level=="I" or log_level=="D"

def isException(log_message):
	containsException = (log_message.find("Error") != -1) or (log_message.find("Exception") != -1)
	return containsException or log_message.strip().startswith("at ")

def isIgnored(log_message):
	for ignored in IGNORED_LINES:
		if ignored in log_message:
			return True
	return False


while True:
	line = sys.stdin.readline().rstrip()
	match = re.search(REGEX_LINE, line)

	if not match:
		continue

	time = match.group(1)
	log_level = match.group(2).strip()
	process_id = match.group(3)
	log_message = match.group(4)

	if not log_message:
		continue

	if isIgnored(log_message):
		continue

	output = time + " " + log_level + " " + log_message
	if isException(log_message):
		print colorize(RED, output)		
	elif not isDebugOrInfo(log_level):
		print colorize(YELLOW, output)
	else:
		print output