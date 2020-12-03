from MDP import MDP
import random as rand
        
def TD0(mdp, vals, numEpisodes, stepSize):
    for episode in range(numEpisodes):
        mdp.total = [0,0]
        mdp.state = rand.randint(1,mdp.params[0]-1)
        mdp.terminated = False
        while mdp.terminated == False:
            state = mdp.state
            direction = rand.randint(0,1)
            mdp.move(direction)
            stepChange = stepSize*(mdp.total[1]+mdp.params[2]*vals[mdp.state]-vals[state])
            vals[state] += stepChange
    mdp.total = [0,0]
    vals = vals[1:-1]
    return vals
    
