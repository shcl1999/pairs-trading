import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def subfindOptimalZValue(threshold, zData):
    chance = 0
    startHigh = False
    startLow = False
    for i in range(len(zData.values)):
        if startHigh == True:
            if (zData.values[i] < -threshold):
                chance += 1 
                startHigh = False
        elif startLow == True:
            if (zData.values[i] > threshold):
                chance += 1 
                startLow = False
        else:
            if (zData.values[i] > threshold):
                startHigh = True
            if (zData.values[i] < -threshold):
                startLow = True
    return (chance * (2* threshold))

def findOptimalZValue(zData, title, start, end, step):
    testThresholds = np.arange(start, end, step)
    profits = []
    for tT in testThresholds:
        profits.append(subfindOptimalZValue(tT, zData))
        #print(f'Threshold value :{tT}, profit : {subfindOptimalZValue(tT, zData)}')
        
    profits_df = pd.DataFrame()
    profits_df['profits'] = profits
    profits_df['z'] = testThresholds
    
    plt.title(f'Optimal Z-threshold of {title}')
    plt.xlabel('z-threshold value')
    plt.ylabel('Expected profit')
    plt.plot(profits_df['z'], profits_df['profits'])
    
    bestZ = round((profits_df[profits_df['profits'] == profits_df['profits'].max()]['z'].values)[0], 4)
    bestProfit = round((profits_df[profits_df['profits'] == profits_df['profits'].max()]['profits'].values)[0], 4)
    
    plt.plot(bestZ, bestProfit, 'r*')
    plt.text(bestZ, bestProfit, '({}, {})'.format(bestZ, bestProfit))