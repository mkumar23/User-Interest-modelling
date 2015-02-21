from classifier import *

testingTweetsWithIDs = np.loadtxt("sample.txt", comments='\\<>=#', delimiter="\t", unpack=False, dtype ='string' )

results = getPredictions (testingTweetsWithIDs)

for result in results:
    print result
    
