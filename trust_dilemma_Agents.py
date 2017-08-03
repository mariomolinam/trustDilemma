import string, random, itertools
import numpy as np
from scipy import stats

class Agent(object):
    """
        This class creates agents with certain profile characteristics
        Characteristics:
            - trustThreshold is given, homogeneuous, and set to 0.05 arbitrarily. This parameter can be adapted.
            - a shareable subset of items
            - a unique subset of items
            - agent ID

            - among others (needs completion)
    """
    # global parameter to count number of agents in the model. This parameter is dynamically
    # updated every time an agent is created.
    TotalNumberOfAgents = 0

    def __init__(self, trustThreshold, MaxNumberOfAgents, alpha):
        self.__trustThreshold = (1.0/(MaxNumberOfAgents-1)) * trustThreshold
        self.__shareableItems = random.sample(set(list(string.ascii_uppercase)[:4]), 2)
        self.__uniqueItems =  random.sample(set(list(string.ascii_uppercase)[4:]), 1)

        # agents ids starting at 0
        self.__agentId = Agent.TotalNumberOfAgents
        Agent.TotalNumberOfAgents += 1

        self.__firstInteraction = True
        self.__attractiveness = False
        self.alphaParameter = alpha
        self.__probabilityOfInteraction = None

        # stable variables
        self.selectedTargetAgent = None
        self.shareableItem = None
        self.newItem = None

        # vectors
        self.__memoryInteraction = np.zeros((MaxNumberOfAgents,1))
        self.__memoryAttractiveness = np.ones((MaxNumberOfAgents,1))
        self.__probabilityOfInteraction = np.zeros((MaxNumberOfAgents,1))
        self.__recordMemory = np.zeros((MaxNumberOfAgents,1))

        # reset TotalNumberOfAgents variable after exhausting the number of agents needed
        if Agent.TotalNumberOfAgents > MaxNumberOfAgents:
            self.__agentId = 0
            Agent.TotalNumberOfAgents = 1

    def myID(self):
        return self.__agentId

    def totalAgents(self):
        return Agent.TotalNumberOfAgents

    def initialProbabilityOfInteraction(self):
        p_initial = 1.0 / (self.totalAgents() - 1)
        self.__probabilityOfInteraction[:] = p_initial
        #self.__probabilityOfInteraction = np.copy(p_initial)
        agentID = self.myID()

        # put a zero in your position
        self.__probabilityOfInteraction[agentID] = 0

        return self.__probabilityOfInteraction

    def followingProbabilityOfInteraction(self):

        # get target agent with whom probability of interaction is updated
        target_Agent = self.getSelectedTargetAgent()
        nonzeroIndex = int(self.__memoryInteraction[target_Agent])
        print 'nonzeroIndex', nonzeroIndex

        # if nonzeroIndex is NOT zero, then previous interactions have ocurred
        if nonzeroIndex > 0 and self.__probabilityOfInteraction[target_Agent] < self.__trustThreshold:
            # get DELTA parameter:
            # a weight for interaction with agent j relative to all other interactions

            howmany_nonzero = np.count_nonzero(self.__memoryInteraction)
            print 'Before constructing delta...'
            print 'Numerator:', str(nonzeroIndex + 1)
            print 'Denominator:'
            print '     sum memoryInteraction:', str(self.__memoryInteraction.sum())
            print '     integer added:', str(howmany_nonzero)
            delta = ( nonzeroIndex + 1) / ( self.__memoryInteraction.sum() + howmany_nonzero )
            print 'Delta:'
            print delta

            # get GAMMA parameter
            print 'memoryAttractiveness:', self.__memoryAttractiveness
            gamma = self.__memoryAttractiveness[target_Agent]
            if gamma < 0:
                gamma = 0
                self.__memoryAttractiveness[target_Agent] = 0

            print 'Gamma:', gamma

            if delta < 1:
                self.__probabilityOfInteraction[target_Agent] = self.__probabilityOfInteraction[target_Agent] * (delta + 1) * gamma
            else:
                self.__probabilityOfInteraction[target_Agent] = self.__probabilityOfInteraction[target_Agent] * (delta) * gamma

            print 'Printing the sum value:', self.__probabilityOfInteraction.sum()
            print 'Printing New probabilities normalized'
            print self.__probabilityOfInteraction / self.__probabilityOfInteraction.sum()

            self.__probabilityOfInteraction = self.__probabilityOfInteraction / self.__probabilityOfInteraction.sum()

        return self.__probabilityOfInteraction

    def selectTargetAgent(self):
        # get a list of values with all agent Ids
        totalAgents = range(self.totalAgents())

        # but remove yourself from this list by finding your position in the list and removing yourself
        own_position = totalAgents.index(self.__agentId)
        remove_yourself = totalAgents.pop(own_position)

        possibleAgents = totalAgents
        print 'Focal Agent', self.myID()
        if self.__firstInteraction:
            initialProbabilities = self.initialProbabilityOfInteraction()
            initialProbabilities = np.delete(initialProbabilities, self.myID())

            targetAgent = np.random.choice(possibleAgents, 1, p=initialProbabilities.flatten())
            # update first Interaction interruptor
            self.__firstInteraction = False
        else:
            print 'Entering else statement...'

            followingProbabilities = self.followingProbabilityOfInteraction()
            #print followingProbabilities
            followingProbabilities = np.delete(followingProbabilities, self.myID())
            print "Probabilities after deleting itself:"
            print followingProbabilities

            targetAgent = np.random.choice(possibleAgents, 1, p=followingProbabilities.flatten())

        print 'Target agent:', targetAgent[0]

        # update stable varialble so we can access this selected partner without running the function all over again.
        self.selectedTargetAgent = targetAgent[0]

        return self.selectedTargetAgent

    def shareInformation(self):
        # take into account trust threshold to share information
        target_Agent= self.getSelectedTargetAgent()
        probabilityForTargetID = self.__probabilityOfInteraction[target_Agent]

        if probabilityForTargetID < self.__trustThreshold:
            # only share items from shareable set
            setToShare = self.__shareableItems
            item = random.sample(setToShare, 1)
            self.shareableItem = item
        else:
            #open unique set to share new information
            setToShare = self.__shareableItems + self.__uniqueItems
            item = random.sample(setToShare, 1)
            self.shareableItem = item

        return None

    def storeNewInformation(self, item):
        self.newItem = item
        shareableItems = ['A', 'B', 'C', 'D']
        if self.newItem not in shareableItems:
            if self.newItem not in self.__uniqueItems:
                self.__uniqueItems.append(self.newItem)


    def updateMemoryAttractiveness(self, value):
        # call updateAttractiveness function
        self.__attractiveness = value

        # update attractiveness for nominated target agent
        targetID = self.getSelectedTargetAgent()


        # update attractiveness vector for target agent
        if self.__attractiveness:
            if self.__probabilityOfInteraction[targetID] < self.__trustThreshold:
                self.__memoryAttractiveness[targetID] += self.alphaParameter
            self.__attractiveness = False
        else:
            self.__memoryAttractiveness[targetID] -= self.alphaParameter


    def updateMemoryInteraction(self, targetID):
        if not self.__recordMemory:
            if self.__probabilityOfInteraction[targetID] < self.__trustThreshold:
                self.__memoryInteraction[targetID] += 1
            self.__recordMemory = True

    def updateMemoryNeighbors(self, targetID):
        if self.__probabilityOfInteraction[targetID] < self.__trustThreshold:
            self.__memoryAttractiveness[targetID] += self.alphaParameter/2


    def updateRecordMemory(self):
        self.__recordMemory = False

    #############################################################
    # Functions that get values from agents

    def getCommonNeighbors(self, target):
        # The arguemtn target excludes agent in current interaction.
        # get neighbors with probability of interaction higher than the modal agent in that current agent's vector.
        p_mode = stats.mode(self.__probabilityOfInteraction)[0]
        p_vector = self.__probabilityOfInteraction

        # neighbors is vector with values for agents selected
        neighbors = np.where(p_vector > p_mode )[0]

        # remove current agent from probability vector
        neighbors = neighbors[neighbors!=target]

        return neighbors

    def getSelectedTargetAgent(self):
        return self.selectedTargetAgent

    def getSelectedInformationItem(self):
        return self.shareableItem

    def getAttractiveness(self):
        return self.__attractiveness

    def getMemoryInteraction(self):
        return self.__memoryInteraction

    def getMemoryAttractiveness(self):
        return self.__memoryAttractiveness

    def getProbabilityOfInteraction(self):
        return self.__probabilityOfInteraction

    def getNewInformationStore(self):
        return self.__uniqueItems

    def getClassItem(self, item):
        message = None
        if item in self.__shareableItems:
            message = 'shareable'
        elif item in self.__uniqueItems:
            message = 'unique'
        return message
