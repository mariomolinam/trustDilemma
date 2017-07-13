import trust_dilemma
import numpy as np

# Master Code
trustThresholdParameters = [0.9, 1.1, 10, 25]
#file_names = ['trustThreshold-0.9.txt']#, 'trustThreshold-2.5.txt', 'trustThreshold-4.txt', 'trustThreshold-6.txt', 'trustThreshold-8.txt', 'trustThreshold-16.txt']
#file_names_weights = ['networkWeights-0.9.txt'], 'networkWeights-2.5.txt', 'networkWeights-4.txt', 'networkWeights-6.txt', 'networkWeights-8.txt', 'networkWeights-16.txt']

for value in range(len(trustThresholdParameters)):
    numberOfIterationsAgents = 10
    store_Results = {}
    for agent in range(numberOfIterationsAgents):
        createAgents = trust_dilemma.createAgents(trustThreshold = trustThresholdParameters[value], MaxNumberOfAgents = 50)
        agents_list = createAgents['agents_list']
        totalInformationAvailable = len(createAgents['totalInformationAvailable']) + 4
        numberOfIterationsTime = 2
        # pairs change every time
        globalInformationSystem = []
        cumulativeInformationFlow = []
        p = 0
        for t in range(numberOfIterationsTime):
            globalInformationExchanged = trust_dilemma.runTrustDilemma(agents_list = agents_list, totalInformationAvailable = totalInformationAvailable, t=t)
            print '#################'
            print globalInformationExchanged
            print '#################'
            # get how much new information was exchanged at one particular time
            for i in globalInformationExchanged:
                if i not in globalInformationSystem:
                    globalInformationSystem.append(i)
            # calculate proportion of new information flowing in the system (relative to all info available)
            p = len(globalInformationSystem) / float(totalInformationAvailable)
            if agent == 0:
                store_Results[t] = [p]
            else:
                store_Results[t][agent-1]
                store_Results[t].append(p)
    file_name = 'trustThreshold-' + str(trustThresholdParameters[value]) + '.txt'
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
        for a in range(len(createAgents['agents_list'])):
            getWeights = createAgents['agents_list'][a].getProbabilityOfInteraction()
            if a == 0:
                matrix = getWeights
            else:
                matrix = np.append(matrix, getWeights, axis=1)
        # save network weights
        file_network = 'networkWeights-' + str(trustThresholdParameters[value]) + '.txt'
        np.savetxt(file_network, matrix)
