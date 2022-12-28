import os
import time

commandList1 = [
    'python3 hpglPlotter.py -f designFiles/5x7images/1/5x7_Layer1.hpgl -P 1',
    'python3 hpglPlotter.py -f designFiles/5x7images/1/5x7_Layer2.hpgl -P 2',
    'python3 hpglPlotter.py -f designFiles/5x7images/1/5x7_Layer3.hpgl -P 3',
    'python3 hpglPlotter.py -f designFiles/5x7images/1/5x7_Layer4.hpgl -P 4',
    'python3 hpglPlotter.py -f designFiles/5x7images/1/5x7_Layer5.hpgl -P 5',
    'python3 hpglPlotter.py -f designFiles/5x7images/1/5x7_Layer6.hpgl -P 6',
    'python3 hpglPlotter.py -f designFiles/5x7images/1/5x7_markers.hpgl -P 1',
]

commandList2 = [
    'python3 hpglPlotter.py -f designFiles/5x7images/2/5x7_layer1.hpgl -p 6',
    'python3 hpglPlotter.py -f designFiles/5x7images/2/5x7_layer2.hpgl -p 5',
    'python3 hpglPlotter.py -f designFiles/5x7images/2/5x7_layer3.hpgl -p 4',
    'python3 hpglPlotter.py -f designFiles/5x7images/2/5x7_markers.hpgl -p 1',
]

for command in commandList2:

    print('Command: ', command)
    os.system(command)
    time.sleep(5)
