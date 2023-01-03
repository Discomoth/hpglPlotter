from hpglCommands import plotter, hpgl
import sys
import argparse

'''
A function to handle the plotting of an Inkscape generated HPGL file.
Using the hpglCommands.py script it chops the hpgl file up into pieces
small enough for HP plotters to handle, whule implementing a simple
RTS/CTS flow control system. 

Parameters such as the ctsdelay may need to be adjusted for different
systems. Buffer overflows can result from using the same parameters 
between a usbTTY device and a normal tty/tyyS device. Increase to 
reduce buffer overflow problems on start of plot. 

'''

argParser = argparse.ArgumentParser()

argParser.add_argument(
    '-f',
    '--file',
    type=str,
    required=True)

argParser.add_argument(
    '-p',
    '--pen',
    type=int,
    default=1,
    required=False)

argParser.add_argument(
    '-P',
    '--plotter',
    default='/dev/ttyUSB0',
    type=str,
    required=False)

argParser.add_argument(
    '-b',
    '--baud',
    default=9600,
    type=int,
    required=False)
    
argParser.add_argument(
    '-t',
    '--timeout',
    default=1,
    type=int,
    required=False)

argParser.add_argument(
    '-c',
    '--ctsdelay',
    default=0.015,
    type=int,
    required=False)
    
argParser.add_argument(
    '-d', 
    '--dryrun',
    type=bool,
    default=False,
    required=False)

try:
    args = argParser.parse_args()
except:
    quit()

with open(args.file) as file:
    fileInformation = file.readlines()

splitList = fileInformation[0].split(';')

commandList = [x + ';' for x in splitList]

finalList = []

for command in commandList:
    commandList = plotter.commandDownsizer_inkscape(command)
    if len(commandList) == 0:
        continue
    else:
        finalList.extend(commandList)

if not args.dryrun:

    plt = plotter(
        comPort=args.plotter,
        baud=args.baud,
        timeout=args.timeout)

    plt.serialSend(
        finalList,
        penSelect=args.pen,
        checkDelay=args.ctsdelay,
        prefixCommands=['IN;', 'VS15;', 'AS2;', 'FS2;'])
elif args.dryrun:
    sizeList = []
    for command in finalList:
        sizeList.append(len(command.encode('utf-8')))

    print('Max bytestring size: ', max(sizeList), ' bytes')
    print('Min bytestring size: ', min(sizeList), ' bytes')
    print('Number of commands: ', len(sizeList), ' commands')
