'''
Created on Nov 26, 2014

@author: Mrinal
'''
import operator
from  collections import defaultdict
argmax = lambda x : max(x.iteritems(),key=operator.itemgetter(1))[0]

def predict(instance,weights,labels):
    scores = defaultdict(int);
    for feat,count in instance.iteritems():
        for label in labels:
            scores[label] = scores.get(label,0) + weights.get((label,feat),0)*count
              
    return argmax(scores),scores

all_labels = ['spam','ham']
def evalClassifier(weights,outfilename,testfile=devkey):
    err = 0    
    tp = fp = tn = fn = p = n = precision = recall = acc = 0 
    with open(outfilename,'w') as outfile:
        for i,(counts,label) in enumerate(dataIterator(testfile)): #iterate through eval set
            maxscore = predict(counts,weights,all_labels)[0]
            print >>outfile, maxscore #print prediction to file
            if label == 'spam':
                p += 1
            else:
                n += 1
                
            if maxscore == 'spam' and label == 'spam':
                tp += 1
            elif maxscore == 'spam' and label == 'ham':
                fp += 1
                err += 1
            elif maxscore == 'ham' and label == 'ham':
                tn += 1
            else:
                fn += 1
                err += 1
                #print 'Line : ',counts               
        precision = tp / float(tp + fp)
        recall = tp / float(tp + fn)
        acc = (tp + tn) / float (p + n)
        print tp,fp,tn,fn,p,n,err
        print 'precision : ',precision,'Recall: ',recall,'acc : ',acc
    print err
    
def oneItPerceptron(data_generator,weights,labels):
    tr_err = 0    
    for i,(counts,label) in enumerate(data_generator):
        maxScore, _ = predict(counts,weights,labels);
        if maxScore != label:
            for word,count in counts.iteritems():
                weights[(label,word)] = weights.get((label,word),0) + count
                weights[(maxScore,word)] = weights.get((maxScore,word),0) - count
                
            tr_err += 1
                
    return weights, tr_err, i

# this code trains the perceptron for N iterations on the supplied training data
def trainPerceptron(N_its,inst_generator=all_tr_insts,labels=all_labels):
    tr_acc = [None]*N_its #holder for training accuracy
    weights = defaultdict(float) 
    for i in xrange(N_its):
        createKfold(i)
        docsToBOWs(trainkey)
        docsToBOWs(devkey)
        inst_generator, dev_insts = allinsts()
        weights,tr_err,tr_tot = oneItPerceptron(inst_generator,weights,labels) #call your function for a single iteration
        evalClassifier(weights,'perc.txt') #evaluate on dev data
        tr_acc[i] = 1. - tr_err/float(tr_tot) #compute training accuracy from output
    return weights, tr_acc

