import MDP as MDP
import TDlambda as TD
import MonteCarlo as MC
import random as rand
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

'''
This file contains the functions that compute mean squared error and generate the graphs.
'''

def compareMCwithTD(mdp, initial, episodes, runs):
    true = [1/6, 2/6, 3/6, 4/6, 5/6]
    MCerrors = [[0,0,0,0,0] for i in range(episodes)]
    xVals = [i+1 for i in range(episodes)]
    stepSize = 0
    for i in range(runs):
        MCvals = MC.MonteCarloevery(mdp, initial.copy(), episodes, stepSize)
        for j in range(episodes):
            for k in range(len(MCvals[0])):
                MCerrors[j][k] += ((MCvals[j][k]-true[k])**2)
    MCerrs = []
    for i in range(episodes):
        totalOfMCErrs = 0
        for state in range(len(MCvals[0])):
            totalOfMCErrs += np.sqrt(MCerrors[i][state]/runs)
        MCerrs.append(totalOfMCErrs/len(MCvals[0]))
    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set1')
    color = 0
    plt.plot(xVals, MCerrs, '-', label = 'MC error', color=palette(color))
    
    for stepSize in [.1, .05]:
        color += 1
        TDerrors = [[0,0,0,0,0] for i in range(episodes)]
        for i in range(runs):
            TDvals = TD.TD0every(mdp, initial.copy(), episodes, stepSize)
            for j in range(episodes):
                for k in range(len(MCvals[0])):
                    TDerrors[j][k] += ((TDvals[j][k]-true[k])**2)
        TDerrs = []
        for i in range(episodes):
            totalOfTDErrs = 0
            for state in range(len(MCvals[0])):
                totalOfTDErrs += np.sqrt(TDerrors[i][state]/runs)
            TDerrs.append(totalOfTDErrs/len(TDvals[0]))
        plt.plot(xVals, TDerrs, '-', label = 'TD(0) error, step size = '+str(stepSize), color=palette(color))
    plt.ylabel('Root Mean-squared Error ')
    plt.xlabel('Number of Episodes')
    plt.ylim(.025,.1)
    plt.legend()
    plt.title('Comparison of Error with MC vs TD(0)')
    plt.show()
    

def episodeComp(mdp, initial, episodes, stepSize, method, runs):
    if method == MC.MonteCarloevery:
        nameMethod = 'Monte Carlo'
    else:
        nameMethod = 'TD(0)'
    true = [1/6, 2/6, 3/6, 4/6, 5/6]
    errors = [[0,0,0,0,0] for i in range(episodes)]
    xVals = [i+1 for i in range(episodes)]
    for i in range(runs):
        vals = method(mdp, initial.copy(), episodes, stepSize)
        for j in range(episodes):
            for k in range(len(vals[0])):
                errors[j][k] += ((vals[j][k]-true[k])**2)
    errs = []
    for i in range(episodes):
        totalOfErrs = 0
        for state in range(len(vals[0])):
            totalOfErrs += np.sqrt(errors[i][state]/runs)
        errs.append(totalOfErrs/len(vals[0]))
    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set1')
    color = 0
    plt.plot(xVals, errs, '-', color=palette(color))
    plt.ylabel('Root Mean-squared Error ')
    plt.xlabel('Number of Episodes')
    plt.title('Effect of Increasing Number of Episodes on Error of '+nameMethod)
    plt.show()
    
def stepSizeComp(mdp, initial, method):
    true = [1/6, 2/6, 3/6, 4/6, 5/6]
    runs = 100
    stepSizes = np.arange(.005, .2, 0.005).tolist()
    numEpisodes = [25, 50, 100, 250, 500, 1000]
        
    xVals = stepSizes
    
    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set1')
    color = 0
    
    for e in numEpisodes:
        errors = [[0,0,0,0,0] for i in range(len(stepSizes))]
        color += 1
        label0 = str(e) + ' episodes'
        for i in range(runs):
            for j in range(len(stepSizes)):
                vals = method(mdp, initial, e, stepSizes[j])
                for k in range(5):
                    errors[j][k] += ((vals[k]-true[k])**2)
        errs = []
        for i in range(len(stepSizes)):
            totalOfErrs = 0
            for state in range(5):
                totalOfErrs += np.sqrt(errors[i][state]/runs)
            errs.append(totalOfErrs/5)
            
        plt.plot(xVals, errs, '-', label = label0, color=palette(color))
    plt.ylabel('Root Mean-squared Error ')
    plt.xlabel('Step Size')
    plt.title('Analysis of Step Size for TD(0)')
    plt.legend()
    plt.show()
    
def numEpisodesVsStepSize(mdp, initial):
    episodes = 1000
    stepSizes = np.arange(.05, .2, 0.005).tolist()

    true = [1/6, 2/6, 3/6, 4/6, 5/6]
    runs = 100
        
    xVals = stepSizes
    epps = []
    
    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set1')
    color = 0
    
    for stepSize in stepSizes:
        minError = 1
        optimalEpisode = 1
        color += 1
        TDerrors = [[0,0,0,0,0] for i in range(episodes)]
        for i in range(runs):
            TDvals = TD.TD0every(mdp, initial.copy(), episodes, stepSize)
            for j in range(episodes):
                for k in range(len(TDvals[0])):
                    TDerrors[j][k] += ((TDvals[j][k]-true[k])**2)
        for i in range(episodes):
            totalOfTDErrs = 0
            for state in range(len(TDvals[0])):
                totalOfTDErrs += np.sqrt(TDerrors[i][state]/runs)
            if totalOfTDErrs/len(TDvals[0]) < minError:
                minError = totalOfTDErrs/len(TDvals[0])
                optimalEpisode = i
        epps.append(optimalEpisode)
        
    plt.plot(xVals, epps, '-', color=palette(color))
    plt.ylabel('Number of Episodes to Minimize Error')
    plt.xlabel('Step Size')
    plt.title('Step Size vs Number of Episodes, TD(0)')
    plt.show()
    
def minErrorVsStepSize(mdp, initial):
    episodes = 1000
    stepSizes = np.arange(.05, .2, 0.005).tolist()

    true = [1/6, 2/6, 3/6, 4/6, 5/6]
    runs = 100
        
    xVals = stepSizes
    minErrs = []
    
    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set1')
    color = 0
    
    for stepSize in stepSizes:
        minError = 1
        optimalEpisode = 1
        color += 1
        TDerrors = [[0,0,0,0,0] for i in range(episodes)]
        for i in range(runs):
            TDvals = TD.TD0every(mdp, initial.copy(), episodes, stepSize)
            for j in range(episodes):
                for k in range(len(TDvals[0])):
                    TDerrors[j][k] += ((TDvals[j][k]-true[k])**2)
        for i in range(episodes):
            totalOfTDErrs = 0
            for state in range(len(TDvals[0])):
                totalOfTDErrs += np.sqrt(TDerrors[i][state]/runs)
            if totalOfTDErrs/len(TDvals[0]) < minError:
                minError = totalOfTDErrs/len(TDvals[0])
                optimalEpisode = i
        minErrs.append(minError)
        
    plt.plot(xVals, minErrs, '-', color=palette(color))
    plt.ylabel('Minimal Error')
    plt.xlabel('Step Size')
    plt.title('Step Size vs Minimal Error, TD(0)')
    plt.show()
          
def main():
    mdp = MDP.ex6dot2
    initial = MDP.initialize(mdp)
    minErrorVsStepSize(mdp, initial)
    #stepSizeComp(mdp, initial, TD.TD0)
    #episodeComp(mdp, initial, 150, .1, MC.MonteCarloevery, 100)
    #compareMCwithTD(mdp, initial.copy(), 350, 100)
main()
