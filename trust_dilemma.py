import trust_dilemma_Agents as agents
import time, string

def createAgents(trustThreshold, MaxNumberOfAgents):
    # First, we need to create the Agents. Create N=100 agents and have them in a list
    agents_list = []
    totalInformationAvailable = []
    for i in range(MaxNumberOfAgents):
        agent = agents.Agent(trustThreshold=trustThreshold, MaxNumberOfAgents=MaxNumberOfAgents)
        items = agent.getNewInformationStore()
        totalInformationAvailable.append(items[0])
        agents_list.append(agent)

    output = { 'agents_list': agents_list, 'totalInformationAvailable': totalInformationAvailable}

    return output


def runTrustDilemma(agents_list, totalInformationAvailable, t=0):

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
    pairs = {}
    paired_agents = []      # keep track of agents who were paired
    for focal_agent in agents_list:
        # This is the target Agent selected by focal Agent in the loop
        focal_targetAgent = focal_agent.getSelectedTargetAgent()
        focalID = focal_agent.myID()
        # print 'Focal ID:', focalID
        # Then see if someone else selected focal Agent
        for target_agent in agents_list:
            # get target agent ID
            targetID = target_agent.myID()
            if targetID == focalID:
                # print 'We are the same Agent...'
                pass
            else:
                target_targetAgent = target_agent.getSelectedTargetAgent()
                if (targetID == focal_targetAgent) and (target_targetAgent == focalID):
                    print 'We have a pair!'
                    print 'Agent:', focalID, 'and', targetID
                    pairs[target_agent.myID()] = focal_agent # keep track of agents paired
                    # update Interaction Memory
                    focal_agent.updateMemoryInteraction(targetID)
                    target_agent.updateMemoryInteraction(focalID)
                    # This list avoids double counting
                    paired_agents.append(focal_agent.myID())
                    paired_agents.append(target_agent.myID())
                    break
                #else:
                    #print 'No pair found'
    print 'end loop'
    # if we have more than
    # if len(pairs) > 0:
    #     if len(pairs.keys())/2 > pairs.values()[0].totalAgents():
    #         print 'We have a problem!!!'
    #         break

    #########################################
    # THIRD, SEARCH FOR INFORMATION ITEMS AGENTS SHARE.
    # BUT ONLY IF THERE ARE PAIRS
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
