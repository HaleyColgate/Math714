import random as rand

class MDP:

    def __init__(self, numStates, rewards, checkF, leftTrans, rightTrans, leftReward, rightReward, gamma=1, solution = None):
        #inputs: 
            #numStates - number of states
            #rewards - tuple of possible rewards
            #target - when total >= target MDP episode will terminate
            #leftTrans/rightTrans - tuple of numStates tuples with numStates entries, cumulative transition probabilities when actor goes left/right
            #leftReward/rightReward - tuple of numStates tuples with an entry for each possible reward, cumulative reward probabilities when actor goes left/right
            #gamma - positive discount factor <1
        self.state = rand.randint(1,numStates-2) 
        self.params = (numStates, rewards, gamma)
        self.total = [0, 0] #[total reward, latest reward]
        self.left = [leftTrans,leftReward]
        self.right = [rightTrans,rightReward]
        self.check = checkF
        self.terminated = False

    def move(self, direction):
        #updates state and adds reward, updates termination status
        #direction can be ('left' or 0) or ('right' or 1)
        if direction == 'left' or direction == 0:
            transitionProbs = self.left[0][self.state]
            rewardProbs = self.left[1][self.state]
        elif direction == 'right' or direction == 1:
            transitionProbs = self.right[0][self.state]
            rewardProbs = self.right[1][self.state]
        transitionRandom = rand.random()
        rewardRandom = rand.random()
        for i in range(self.params[0]):
            if transitionProbs[i] > transitionRandom:
                self.state = i
                break
        for j in range(len(self.params[1])):
            if rewardProbs[j] >= rewardRandom:
                self.total[0] += self.params[1][j]
                self.total[1] = self.params[1][j]
                break
        self.updateTermination()
        #print(self.state)
        
    def updateTermination(self):
        #updates termination status based on check function
        if self.check(self) == True:
            self.terminated = True
            #print('Ended Episode')
