import MDP as MDP
import random as rand

#sets up MC algorithm
#inputs: mdp from mdp class, initial value function, number of episodes to include, step stepSize
#note: initial value function gets redefined and stepSize never gets used, but it was convenient to have TD(0) and MC have the same inputs
#output: value function for states 1-5

def MonteCarlo(mdp, vals, numEpisodes, stepSize):
    for i in range(len(vals)):
        vals[i] = [0]
    for episode in range(numEpisodes):
        vals2update = []
        mdp.state = rand.randint(1,mdp.params[0]-2)
        mdp.total = [0,0]
        mdp.terminated = False
        while mdp.terminated == False:
            state = mdp.state
            vals2update.append(state)
            direction = rand.randint(0,1)
            mdp.move(direction)
        for j in range(len(vals2update)):
            s = vals2update[j]
            vals[s].append(mdp.total[0])
    for i in range(len(vals)):
        numVals = len(vals[i])
        if numVals != 0:
            vals[i] = sum(vals[i])/numVals
    vals = vals[1:-1]
    print(vals)
    return vals

#same as above but saves estimate after every episode
def MonteCarloevery(mdp, vals, numEpisodes, stepSize):
    allVals = []
    for i in range(len(vals)):
        vals[i] = [0]
    for episode in range(numEpisodes):
        newVals = []
        vals2update = []
        mdp.state = rand.randint(1,mdp.params[0]-2)
        mdp.total = [0,0]
        mdp.terminated = False
        while mdp.terminated == False:
            state = mdp.state
            vals2update.append(state)
            direction = rand.randint(0,1)
            mdp.move(direction)
        for j in range(len(vals2update)):
            s = vals2update[j]
            vals[s].append(mdp.total[0])
        for i in range(len(vals)):
            numVals = len(vals[i])
            if numVals != 0:
                newVals.append(sum(vals[i])/numVals)
        newVals = newVals[1:-1]
        allVals.append(newVals)
    return allVals
