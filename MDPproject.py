from MDP import MDP
import random as rand
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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
    vals = vals[1:-1]
    return vals, episodes, steps
    
def episodeComp(mdp, initial, stepSize):
    true = [1/6, 2/6, 3/6, 4/6, 5/6]
    estimates = []
    numEpisodes = [0,1,10,100]
    letters = ['A', 'B', 'C', 'D', 'E']
    for i in numEpisodes:
        estimates.append(TD0(mdp, initial, i, stepSize)[0])
    black_patch = mpatches.Patch(color='black', label = 'True values')
    blue_patch = mpatches.Patch(color='blue', label = 'Value estimates after 0 episodes')
    red_patch = mpatches.Patch(color='red', label = 'Value estimates after 1 episodes')
    green_patch = mpatches.Patch(color='green', label = 'Value estimates after 10 episodes')
    cyan_patch = mpatches.Patch(color='cyan', label = 'Value estimates after 100 episodes')
    plt.plot(letters, true, 'ko-', 
             letters, estimates[0], 'bo-',
             letters, estimates[1], 'ro-',
             letters, estimates[2], 'go-',
             letters, estimates[3], 'co-')
    plt.ylabel('Estimated Value')
    plt.xlabel('State')
    plt.legend(handles=[black_patch, blue_patch, red_patch, green_patch, cyan_patch])
    plt.title('Analysis of Number of Episodes for TD(0)')
    plt.show()
          
def main():
    mdp = ex6dot2
    initial = initialize(mdp)
    episodeComp(mdp, initial[0].copy(), .1)
    #print(initial)
    #for i in range(100):
    #    initial = initialize(mdp)
    #    value = [TD0(mdp, initial[0].copy(), 100, .05)]
    
main()
