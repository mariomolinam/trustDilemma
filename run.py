import trust_dilemma
import numpy as np

# Master Code. This makes the process run
alpha_paramater = [0.05, 0.2]
trustThresholdParameters = [0.9, 1.1, 10, 25]

for alpha in range(len(alpha_paramater)):
    for value in range(len(trustThresholdParameters)):
        numberOfIterationsAgents = 150
        store_Results = {}
        for agent in range(numberOfIterationsAgents):
            createAgents = trust_dilemma.createAgents(trustThreshold = trustThresholdParameters[value], MaxNumberOfAgents = 50, alpha = alpha_paramater[alpha])
            agents_list = createAgents['agents_list']
            InformationAvailable = set(createAgents['totalInformationAvailable'])   # unique information available
            totalInformationAvailable = len(InformationAvailable) + 4
            numberOfIterationsTime = 400
            # pairs change every time
            globalInformationSystem = set()
            p = 0
            for t in range(numberOfIterationsTime):
                print 'BEFORE Trust Dilemma'
                print '     agents_list', agents_list
                globalInformationExchanged = trust_dilemma.runTrustDilemma(agents_list = agents_list, totalInformationAvailable = totalInformationAvailable, t=t)
                print 'AFTER Trust Dilemma'
                print '#################'
                print 'Global Information Exchanged:', globalInformationExchanged
                print '#################'
                print ' '
                # get how much new information was exchanged at one particular time
                globalInformationSystem = globalInformationSystem.union(globalInformationExchanged)
                print '#################'
                print 'Global Information System:', globalInformationSystem
                print '#################'
                # for i in globalInformationExchanged:
                #     if i not in globalInformationSystem:
                #         globalInformationSystem.append(i)
                # calculate proportion of new information flowing in the system (relative to all info available)
                p = len(globalInformationSystem) / float(totalInformationAvailable)
                if agent == 0:
                    store_Results[t] = [p]
                else:
                    store_Results[t][agent-1]
                    store_Results[t].append(p)
        file_name = 'trustThreshold-' + str(trustThresholdParameters[value]) + '-alpha-' + str(alpha_paramater[alpha]) + '.txt'
        with open(file_name, 'w') as f:
            iterations = ''
            for i in range(1, numberOfIterationsAgents + 1):
                iterations += 'iter' + str(i) + '\t'
            headline = 'time' + '\t' + iterations + '\n'
            f.write(headline)
            for key, values in store_Results.items():
                time = str(key)
                for item in values:
                    iterations = ''
                    for val in values:
                        piece = str(val) + '\t'
                        iterations += piece
                    print iterations
                line = time + '\t' + iterations + '\n'
                f.write(line)
        f.close()
        #create weights matrix
        if agent == numberOfIterationsAgents - 1:
            agentInfo = []
            for a in range(len(createAgents['agents_list'])):
                getWeights = createAgents['agents_list'][a].getProbabilityOfInteraction()
                uniqueInfo = len(createAgents['agents_list'][a].getNewInformationStore()) # number of unique items of information
                agentInfo.append(uniqueInfo)
                if a == 0:
                    matrix = getWeights
                else:
                    matrix = np.append(matrix, getWeights, axis=1)
            # append uniqueInfo
            rows = len(agentInfo)
            agentInfo = np.asarray(agentInfo).reshape(rows,1)

            matrix = np.append(matrix, agentInfo, axis=1)
            # save network weights
            file_network = 'networkWeights-' + str(trustThresholdParameters[value]) + '.txt'
            np.savetxt(file_network, matrix)
