import os
import time

commandList1 = [
    'python3 hpglPlotter.py -f designFiles/cardDesigns/snowflake/hpgl/SnowflakeBodyText.hpgl -p 1',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/snowflake/hpgl/SnowflakeDimensionMarkers.hpgl -p 1',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/snowflake/hpgl/SnowflakeFlakesLayer1.hpgl -p 6',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/snowflake/hpgl/SnowflakeFlakesLayer2.hpgl -p 5',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/snowflake/hpgl/SnowflakeTitle2.hpgl -p 6',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/snowflake/hpgl/SnowflakeFlakesLayer3.hpgl -p 4',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/snowflake/hpgl/SnowflakeSignature.hpgl -p 4',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/snowflake/hpgl/SnowflakeTitle1.hpgl -p 4'
]

commandList2 = [
    'python3 hpglPlotter.py -f designFiles/cardDesigns/snowflake/hpgl/distributionFlakesDimensioning.hpgl -p 1',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/snowflake/hpgl/distributionFlakes_layer1.hpgl -p 6',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/snowflake/hpgl/distributionFlakes_layer2.hpgl -p 5',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/snowflake/hpgl/distributionFlakes_layer3.hpgl -p 4',
]

commandList3 = [
    'python3 hpglPlotter.py -f designFiles/cardDesigns/geometryCards/allFoxes/allFoxes_layer1.hpgl -p 1',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/geometryCards/allFoxes/allFoxes_markers.hpgl -p 1',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/geometryCards/allFoxes/allFoxes_layer2.hpgl -p 2',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/geometryCards/allFoxes/allFoxes_layer3.hpgl -p 3',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/geometryCards/allFoxes/allFoxes_layer4.hpgl -p 5',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/geometryCards/allFoxes/allFoxes_layer5.hpgl -p 6',
]

commandList4=[
    'python3 hpglPlotter.py -f designFiles/cardDesigns/geometryCards/allPens/allPens_layer1.hpgl -p 1',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/geometryCards/allPens/allPens_layer2.hpgl -p 2',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/geometryCards/allPens/allPens_layer3.hpgl -p 3',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/geometryCards/allPens/allPens_layer4.hpgl -p 4',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/geometryCards/allPens/allPens_layer5.hpgl -p 5',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/geometryCards/allPens/allPens_layer6.hpgl -p 6',
    'python3 hpglPlotter.py -f designFiles/cardDesigns/geometryCards/allPens/allPens_markers.hpgl -p 1',
]

for command in commandList1:

    print('Command: ', command)
    os.system(command)
    time.sleep(5)
