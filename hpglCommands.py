import serial
import time
import sys

class plotter():

    # The page limits of the plotter

    p1x = 250
    p1y = 279
    p2x = 10250
    p2y = 7479

    terminationCharacter = chr(3)

    def __init__(self, comPort: str, baud: int, timeout: int):
        
        try:
            self.plotterObject = serial.Serial(comPort, baud, timeout = timeout, dsrdtr=True)
            self.plotterObject.write(hpgl.DF().encode())
            self.plotterObject.write(hpgl.IN().encode())

        except Exception as e:
            print('Problem connecting to the plotter!')
            print(e)

    def generateCommandString(commandList:list, startingPen=1):
        '''
        Turn a list of command strings into somethig that can be send to the plotter.
        '''
        resultString = 'IN;'

        if startingPen != None:
            resultString += 'SP' + str(startingPen) + ';'

        for item in commandList:
            resultString += item

        resultString += 'PU;SP0;'

        return resultString

    def serialSend(self, listOfCommands, prefixCommands=['IN;'], suffixCommands=['PU;', 'SP0;'], penSelect=1, checkDelay=0.1, slowInit=True):
        '''
        listOfCommands: A list of small commands to send to the plotter.

        CAUTION! If you send commands that are too large, the plotter buffer might
        overflow. Some tell you that happened, others just do stupid stuff! 

        This is a manual RTS/CTS mechanism to take the place of the one pySerial 
        should have implemented when someone menitioned it didnt work in 2016.

        Thanks to Amulek1416 for the solution.
        https://github.com/pyserial/pyserial/issues/89
        '''

        # Add the pen select command to the prefix command list.
        prefixCommands.append('SP' + str(penSelect) + ';')

        # Add prefex commands to the beginning of the command list.
        # Added in reverse order so 'IN' ends up in the front.

        if slowInit:
            for pre in prefixCommands:
                    
                self.plotterObject.setRTS(True)

                # Check the clear to send (CTS) line and if it is in the 
                # False state, wait
                while not self.plotterObject.getCTS():
                    pass

                self.plotterObject.write(pre.encode())
                time.sleep(1)
                self.plotterObject.setRTS(False)

        elif not slowInit:
            for pre in prefixCommands[::-1]:
                listOfCommands.insert(0, pre)

        # Appending the suffix commands to the command list.
        for suf in suffixCommands:
            listOfCommands.append(suf)

        # Iterate through the list of commands, sending each to the
        # plotter over the serial port while checking and pausing if
        # the plotter HW handshaking indicates a full buffer. 
        for command in listOfCommands:

            #Set the request to send (RTS) line 'True''.
            self.plotterObject.setRTS(True)

            # Check the clear to send (CTS) line and if it is in the 
            # False state, wait
            while not self.plotterObject.getCTS():
                pass

            self.plotterObject.write(command.encode())
            time.sleep(checkDelay)
            self.plotterObject.setRTS(False)

    def commandDownsizer_inkscape(command, splitAll=True):

        returnList = []

        if splitAll:
            commandInstruction = command[0:2]
            coordinates = command.strip(commandInstruction).strip(';').split(',')
            coordinatePairs = zip(coordinates[0::2], coordinates[1::2])

            for pair in coordinatePairs:
                returnList.append(commandInstruction + pair[0] + ',' + pair[1] + ';')
            
            return(returnList)

        elif not splitAll:
            raise NotImplementedError('This feature is not implemented yet! Sorry!')



class hpgl():

    def IN():
        '''
        Sets some values in the plotter to their default state.
        '''
        return 'IN;'

    def DF():
        '''
        Sets all parameters in the plotter to their default state.
        '''
        return 'DF;'

    def SP(pen):
        '''
        SP - Select Pen
        Selects the pen for the plotter to use

        pen: integer, 0-8
        0 value puts all the pens away.
        '''
        return('SP' + str(pen) + ';')

    def PU(points=[], setCoordMode = 'keep'):
        '''
        PU - Pen Up
        If no point tuples in list, pen lifts in current position

        points: list of coordinate tuples. [(X,Y)]
        Ex: [(3000, 5000), (500, 1500)]

        setCoordMode: Change coordinate mode
            Options:
                - 'abs': Absolute Mode
                - 'rel': Relitive Mode
                - 'keep': Maintain current mode
        '''
        # Return single PU command string
        if len(points) == 0:
            return('PU;')

        returnString = ''

        if setCoordMode == 'abs':
            returnString += 'PA;'

        elif setCoordMode == 'rel':
            returnString += 'PR;'
        
        # Parse the coordinate list into a string for the plotter
        returnString += 'PU '
        for point in points:
            returnString += str(point[0]) + ',' + str(point[1]) + ' '

        returnString += ';'

        return returnString

    def PD(points = [], setCoordMode = 'keep'):
        '''
        PD - Pen Down
        If no point tuples in list, pen drops in current position

        points: list of coordinate tuples. [(X,Y)]
        Ex: [(3000, 5000), (500, 1500)]

        setCoordMode: Change coordinate mode
            Options:
                - 'abs': Absolute Mode
                - 'rel': Relitive Mode
                - 'keep': Maintain current mode
        '''
        # Return single PU command string
        if len(points) == 0:
            return('PD;')

        returnString = ''

        if setCoordMode == 'abs':
            returnString += 'PA;'

        elif setCoordMode == 'rel':
            returnString += 'PR;'

        # Parse the coordinate list into a string for the plotter
        returnString += 'PD '
        for point in points:
            returnString += str(point[0]) + ',' + str(point[1]) + ' '

        returnString += ';'
        
        return returnString

    def LT(lineType=''):
        '''
        LT - Line Type
        Sets the line type for the subsequent plotted lines
        Remains for any lines plotted after the execution,
        unless IN issued or plotter reset/rebooted.

        lineType: integer(0 to 6) or empty string
            Options:
                - '': (empty string) Sets line type to solid (default)
                - 0: Dots only at the points plotted
                - 1: Dotted line between points
                - 2: Short dashed line
                - 3: Long dashed line
                - 4: Long dash, dot line
                - 5: Long dash, short dash line
                - 6: Long dash, double short dash line
        '''
        return 'LT' + str(lineType) + ';'

    def LB(labelString, lineEndChar='', termChar=chr(3)):
        '''
        LB - Label
        Creates a text label at the current pen location

        labelString: string, text for the label.

        lineEndChar: string, character to end the line with.
            Options:
                - 'LF': Line feed (chr(10))
                - 'CR': Carriage return (chr(13))
                - 'ETX': End-of-text (chr(3), default LB term char)
                - 'SO': Shift out (chr(14))
                - 'SI': Shift in (chr(15))

        termChar: The character used to terminate the plotted 
                    characters.
                    TODO add a tieback to check against current
                    termination character in plotter class.

        '''
        lineEndChars = {
            'LF': chr(10),
            'CR': chr(13),
            'ETX': chr(3),
            'SO': chr(14),
            'SI': chr(15),
            '':''
            }


        return 'LB' + labelString + lineEndChars[lineEndChar] + termChar

    def PA(pointsList):
        '''
        PA - Plot Relative
        Essentially the same as PU/PD
        Set the plotter to plot absolute coordinates.
        This setting will be assumed for all plotted coordinates
        until the plotter is sent a command stating otherwise (See PA)
        '''

        returnString = ''

        # Catch to not allow 0 len lists to be passed
        if len(pointsList) == 0:
            raise("List must not be 0 length")

        # Parse the coordinate list into a string for the plotter
        returnString += 'PA '
        for point in pointsList:
            returnString += str(point[0]) + ',' + str(point[1]) + ' '

        returnString += ';'
        
        return returnString

    def PR(points):
        '''
        PR - Plot Relative
        Essentially the same as PU/PD
        Set the plotter to plot relative coordinates.
        This setting will be assumed for all plotted coordinates
        until the plotter is sent a command stating otherwise (See PA)
        '''

        returnString = ''

        # Catch to not allow 0 len lists to be passed
        if len(points) == 0:
            raise("List must not be 0 length")

        # Parse the coordinate list into a string for the plotter
        returnString += 'PR '
        for point in points:
            returnString += str(point[0]) + ',' + str(point[1]) + ' '

        returnString += ';'
        
        return returnString

    def SM():
        '''
        SM - Symbol Mode
        '''
        print("placeholder!")

    def DT():
        '''
        DT - Define label Terminator
        '''
        print("placeholder!")

    def CP():
        '''
        CP - Charater Plot cell
        Inserts a character plot cell, used for indentation and extra spacing.
        '''

    def SI():
        '''
        SI - Absolute Label Character Size
        '''

    def SR():
        '''
        SR - Relative Label Character Size
        '''

    def DI():
        '''
        DI - Absolute Label Direction
        '''

    def DR():
        '''
        DR - Relative Label Direction
        '''

    def SL():
        '''
        SL - Label Character Slant
        '''

    def CS():
        '''
        CS - Set Standard Label Character Set
        '''

    def CA():
        '''
        CA - Set Alternate Label Character Set
        '''

    def SS():
        '''
        SS - Select Standard label character set
        '''

    def SA():
        '''
        SA - Select Alternate label character set
        '''
    def UC():
        '''
        UC - User defined character
        '''
    
    
class geometry():

    def line():
        print("placeholder!")

    def symbolPointLine():
        print("placeholder!")

    def textChart():
        '''
        Create a series of labels that render like a list
        '''
        print('placeholder')
        

        
        

