import trust_dilemma_Agents as agents
import time, string, random
import numpy as np


def createAgents(trustThreshold, MaxNumberOfAgents, alpha):
    # First, we need to create the Agents. Create N=100 agents and have them in a list
    agents_list = []
    totalInformationAvailable = []
    for i in range(MaxNumberOfAgents):
        agent = agents.Agent(trustThreshold=trustThreshold, MaxNumberOfAgents=MaxNumberOfAgents, alpha=alpha)
        items = agent.getNewInformationStore()
        totalInformationAvailable.append(items[0])
        agents_list.append(agent)

    output = { 'agents_list': agents_list, 'totalInformationAvailable': totalInformationAvailable}

    return output


def runTrustDilemma(agents_list, totalInformationAvailable, t):

    # store new information flow at every iteration
    globalInformationExchanged = []

    #########################################
    # FIRST, AGENTS SELECT PARTNERS
    for focal_agent in agents_list:
        if t > 0:
            print 'memory Interaction'
            print focal_agent.getMemoryInteraction()
        # make sure that self.__recordMemory is False, so we allow for memory interaction to increase
        focal_agent.updateRecordMemory()
        # select Target agent
        focal_targetAgent = focal_agent.selectTargetAgent()
        # print 'Focal:', focal_agent.myID()
        # print 'Target:', focal_targetAgent
    #########################################
    # SECOND, SEARCH FOR AGENTS WHO SELECTED EACH OTHER
    # agents_provisional to be removed from list while looping
    agents_provisional = agents_list[:]
    # keep track of agents who were paired
    pairs = {}
    paired_agents = []
    for focal_agent in agents_provisional[:]:
        # This is the target Agent selected by focal Agent in the loop
        focal_targetAgent = focal_agent.getSelectedTargetAgent()
        focalID = focal_agent.myID()
        # Then see if someone else selected focal Agent
        for target_agent in agents_provisional:
            # get target agent ID
            targetID = target_agent.myID()
            print 'Focal ID:', focalID, 'and Target ID:', targetID
            if targetID == focalID:
                # print 'We are the same Agent...'
                pass
            else:
                target_targetAgent = target_agent.getSelectedTargetAgent()
                if (targetID == focal_targetAgent) and (target_targetAgent == focalID):
                    print '     We have a pair!'
                    print '     Agent:', focalID, 'and', targetID
                    # keep track of agents paired
                    pairs[target_agent.myID()] = focal_agent
                    pairs[focalID] = target_agent

                    # update Interaction Memory
                    focal_agent.updateMemoryInteraction(targetID)
                    target_agent.updateMemoryInteraction(focalID)

                    # This list avoids double counting
                    paired_agents.append(focal_agent.myID())
                    paired_agents.append(target_agent.myID())

                    # Check if we have a likelable agents in common. If so, update its tie by half of alpha
                    focal_neighbors = focal_agent.getCommonNeighbors(targetID)
                    print 'Focal Neighbors:', focal_neighbors
                    target_neighbors = target_agent.getCommonNeighbors(focalID)
                    print 'Target Neighbors:', target_neighbors

                    commonNeighbors = np.intersect1d(focal_neighbors, target_neighbors)

                    if commonNeighbors.shape[0] != 0:
                        focal_agent.updateMemoryNeighbors(targetID)
                        target_agent.updateMemoryNeighbors(focalID)
                    break
        # Remove agents as we are done searching their neighbors.
        # Notice that that we start the loop with agents_list[:]. This is needed for the update and removal of an agent to happen while we are looping over items.
        # We then get the index of agent and remove from list.
        index = agents_provisional.index(focal_agent)
        removed = agents_provisional.pop(index)
                #else:
                    #print 'No pair found'
    print 'end loop'
    print ' '
    # if we have more than
    # if len(pairs) > 0:
    #     if len(pairs.keys())/2 > pairs.values()[0].totalAgents():
    #         print 'We have a problem!!!'
    #         break

    #########################################
    # THIRD, SEARCH FOR INFORMATION ITEMS AGENTS SHARE.
    # BUT ONLY IF THERE ARE PAIRS
    print 'Pairs list:', paired_agents
    print ' '
    print 'Pairs dict:', pairs

    if len(pairs) > 0:
        pairs_exchanged = []
        for item in pairs:
            # we are getting the Agent instance!
            focal_agent = pairs[item]
            focalID = focal_agent.myID()
            target_agent = pairs[focalID]
            targetID = target_agent.myID()
            # exchange INFO only if agents haven't exchanged already
            if (focalID not in pairs_exchanged) and (targetID not in pairs_exchanged):
                # make agents select an item to share and save item into a variable
                focal_agent.shareInformation()
                focal_agent_ITEM = focal_agent.getSelectedInformationItem()[0]
                target_agent.shareInformation()
                target_agent_ITEM = target_agent.getSelectedInformationItem()[0]
                # Incorporate information
                focal_agent.storeNewInformation(target_agent_ITEM)
                target_agent.storeNewInformation(focal_agent_ITEM)
                # keep track of new information exchanged in the system
                if target_agent_ITEM not in globalInformationExchanged:
                    globalInformationExchanged.append(target_agent_ITEM)
                if focal_agent_ITEM not in globalInformationExchanged:
                    globalInformationExchanged.append(focal_agent_ITEM)
                print 'Focal:', focal_agent_ITEM, 'and Target:', target_agent_ITEM
                # check whether ITEMS are the same
                focal_agent_classOfItem = focal_agent.getClassItem(focal_agent_ITEM)
                target_agent_classOfItem = target_agent.getClassItem(target_agent_ITEM)
                if focal_agent_ITEM == target_agent_ITEM:
                    focal_agent.updateMemoryAttractiveness(True)
                    target_agent.updateMemoryAttractiveness(True)
                elif (focal_agent_classOfItem == 'unique') or (target_agent_classOfItem == 'unique'):
                    focal_agent.updateMemoryAttractiveness(True)
                    target_agent.updateMemoryAttractiveness(True)
                elif focal_agent_ITEM != target_agent_ITEM:
                    focal_agent.updateMemoryAttractiveness(False)
                    target_agent.updateMemoryAttractiveness(False)
                # flag focal and target agent as already used
                pairs_exchanged.append(focalID)
                pairs_exchanged.append(targetID)

    print '#####################################################################'
    print ' '

    return globalInformationExchanged
