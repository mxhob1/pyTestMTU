#!/usr/local/bin/python3

## imports
import argparse
import subprocess
import re

## global variables
ping = "/sbin/ping"

## parse cli args
parser = argparse.ArgumentParser(description='Find the max MTU of a connection')
parser.add_argument("ip", help="target ip")
parser.add_argument("mtu", help="target mtu")
args = parser.parse_args()

def isAlive(ip):
	## check if host is alive
	subp = subprocess.Popen(
			[ping, "-D", "-c 1", "-v", ip],
			stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = subp.communicate()

	if "100.0% packet loss" in str(output): 
		return False
	else:	
		return True

## welcome and check ip
print("pyTestMTU")
print()
print("IP: " + args.ip)
if args.mtu.isdigit():
	print("MTU: " + args.mtu)
else:
	print("MTU: Maximum")
print()
if isAlive(args.ip): 
	print("Host is alive.")
else:
	print("Host is down.")
	quit()

def checkMTU(ip, mtu):
	## ping host with sized packet
	subp = subprocess.Popen(
		[ping, "-D", "-c 1", "-v", "-s " + str(mtu), ip],
		stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = subp.communicate()

	if "Message too long" in str(error):
		return False
	else:
		return True

## determine test type
if args.mtu.isdigit():
	args.mtu = int(args.mtu)
	## ensure mtu size is within spec
	if 1 <= args.mtu <= 9000:
		if checkMTU(args.ip, args.mtu):
			print("MTU testing passed.")
		else:
			print("MTU testing failed.")
elif args.mtu == 'max':
	args.mtu = 1
	while True:
		if checkMTU(args.ip, args.mtu):
			print("Testing MTU " + str(args.mtu), end='\r')
			args.mtu = args.mtu + 1
		else:
			print("Maximum MTU: " + str(args.mtu + 27))
			break
else:
	print("Invalid MTU Specified.")