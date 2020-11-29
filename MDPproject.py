from MDP import MDP
import random as rand

def endpointCheck(mdp):
    return mdp.state == 0 or mdp.state == 6
        

####INITIALIZE MDP FROM SUTTON AND BARTO
ex6dot2 = MDP(numStates = 7, 
            rewards = (0,1), 
            checkF = endpointCheck, 
            leftTrans = ((1,0,0,0,0,0,0), (.5,.5,1,0,0,0,0), (0,.5,.5,1,1,1,1), (0,0,.5,.5,1,1,1), (0,0,0,.5,.5,1,1), (0,0,0,0,.5,.5,1), (0,0,0,0,0,0,1)),
            rightTrans = ((1,1,1,1,1,1,1), (.5,.5,1,1,1,1,1,1), (0,.5,.5,1,1,1,1), (0,0,.5,.5,1,1,1), (0,0,0,.5,.5,1,1), (0,0,0,0,.5,.5,1), (0,0,0,0,0,0,1)),
            leftReward = ((1,1),(1,1),(1,1),(1,1),(1,1),(1,1),(1,1)), 
            rightReward = ((1,1), (1,1), (1,1), (1,1), (1,1), (0,1),(1,1)),
            gamma = 1
            )

######TD(0)
def initialize(mdp):
    vals = []
    policy = {}
    vals.append(0)
    for s in range(1,mdp.params[0]-1):
        vals.append(0.5)
        policy[s] = rand.randint(0,1)
    vals.append(0)
    return [vals, policy]
        
def TD0(mdp, vals, numEpisodes, stepSize):
    episodes = 0
    steps = 0
    while episodes < numEpisodes:
        episodes += 1
        episodeSteps = 0
        mdp.state = rand.randint(1,mdp.params[0]-1)
        mdp.terminated = False
        while mdp.terminated == False:
            steps += 1
            episodeSteps += 1
            state = mdp.state
            direction = rand.randint(0,1)
            mdp.move(direction)
            stepChange = stepSize*(mdp.total[1]+mdp.params[2]*vals[mdp.state]-vals[state])
            vals[state] += stepChange
    mdp.total = [0,0]
    return vals, episodes, steps
    
            
def main():
    mdp = ex6dot2
    #initial = initialize(mdp)
    #print(initial)
    for i in range(100):
        initial = initialize(mdp)
        value = [TD0(mdp, initial[0].copy(), 100, .05)]
        print(value)
    
main()
