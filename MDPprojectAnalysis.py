import MDP as MDP
import TDlambda as TD
import MonteCarlo as MC
import random as rand
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def episodeComp(mdp, initial, stepSize, method):
    if method == MC.MonteCarlo:
        nameMethod = 'Monte Carlo'
    else:
        nameMethod = 'TD(0)'
    true = [1/6, 2/6, 3/6, 4/6, 5/6]
    estimates = []
    numEpisodes = [0,10,100,1000]
    letters = ['A', 'B', 'C', 'D', 'E']
    for i in numEpisodes:
        estimates.append(method(mdp, initial, i, stepSize))
    black_patch = mpatches.Patch(color='black', label = 'True values')
    blue_patch = mpatches.Patch(color='blue', label = 'Value estimates after 0 episodes')
    red_patch = mpatches.Patch(color='red', label = 'Value estimates after 10 episodes')
    green_patch = mpatches.Patch(color='green', label = 'Value estimates after 100 episodes')
    cyan_patch = mpatches.Patch(color='cyan', label = 'Value estimates after 1000 episodes')
    plt.plot(letters, true, 'ko-', 
             letters, estimates[0], 'bo-',
             letters, estimates[1], 'ro-',
             letters, estimates[2], 'go-',
             letters, estimates[3], 'co-')
    plt.ylabel('Estimated Value')
    plt.xlabel('State')
    plt.legend(handles=[black_patch, blue_patch, red_patch, green_patch, cyan_patch])
    plt.title('Analysis of Number of Episodes for ' + nameMethod)
    plt.show()
    
def stepSizeComp(mdp, initial, numEpisodes, method):
    true = [1/6, 2/6, 3/6, 4/6, 5/6]
    estimates = []
    stepSizes = [.1,.05, .025, .001]
    letters = ['A', 'B', 'C', 'D', 'E']
    for i in stepSizes:
        estimates.append(method(mdp, initial, numEpisodes, i))
    black_patch = mpatches.Patch(color='black', label = 'True values')
    blue_patch = mpatches.Patch(color='blue', label = 'Step size .1')
    red_patch = mpatches.Patch(color='red', label = 'Step size .05')
    green_patch = mpatches.Patch(color='green', label = 'Step size .025')
    cyan_patch = mpatches.Patch(color='cyan', label = 'Step size .001')
    plt.plot(letters, true, 'ko-', 
             letters, estimates[0], 'bo-',
             letters, estimates[1], 'ro-',
             letters, estimates[2], 'go-',
             letters, estimates[3], 'co-')
    plt.ylabel('Estimated Value')
    plt.xlabel('State')
    plt.legend(handles=[black_patch, blue_patch, red_patch, green_patch, cyan_patch])
    plt.title('Analysis of Step Size for TD(0), '+ str(numEpisodes)+' Episodes')
    plt.show()
          
def main():
    mdp = MDP.ex6dot2
    initial = MDP.initialize(mdp)
    stepSizeComp(mdp, initial, 100, TD.TD0)
    #episodeComp(mdp, initial, .1, TD.TD0)
    #MC.MonteCarlo(mdp, initial, 500, .5)
main()
