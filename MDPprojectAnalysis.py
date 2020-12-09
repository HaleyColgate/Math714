import MDP as MDP
import TDlambda as TD
import MonteCarlo as MC
import random as rand
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

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
    

def episodeComp(mdp, initial, stepSize, method):
    if method == MC.MonteCarlo:
        nameMethod = 'Monte Carlo'
    else:
        nameMethod = 'TD(0)'
    true = [1/6, 2/6, 3/6, 4/6, 5/6]
    estimates = []
    numEpisodes = [10, 25, 50,75]
    letters = ['A', 'B', 'C', 'D', 'E']
    for i in numEpisodes:
        estimates.append(method(mdp, initial, i, stepSize))

    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set1')
    color = 0
    plt.plot(letters, true, 'k-', label = 'True values', linewidth = 4)
    for x in numEpisodes:
        label0 = str(x) + ' episodes'
        plt.plot(letters, estimates[color], 'o-', label = label0, color=palette(color), linewidth=1)
        color += 1
    plt.ylabel('Estimated Value')
    plt.xlabel('State')
    plt.legend()
    plt.title('Analysis of Number of Episodes for ' + nameMethod)
    plt.show()
    
def stepSizeComp(mdp, initial, method):
    true = [1/6, 2/6, 3/6, 4/6, 5/6]
    estimates = []
    runs = 100
    stepSizes = np.arange(.005, .2, 0.005).tolist()
    letters = ['A', 'B', 'C', 'D', 'E']
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
          
def main():
    mdp = MDP.ex6dot2
    initial = MDP.initialize(mdp)
    #stepSizeComp(mdp, initial, TD.TD0)
    #episodeComp(mdp, initial, .1, TD.TD0)
    compareMCwithTD(mdp, initial.copy(), 350, 100)
main()
