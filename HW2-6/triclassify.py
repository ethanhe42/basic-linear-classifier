import sys
import numpy as np
import numpy.linalg as alg
D=False

with open(sys.argv[1]) as f:
    s=f.readline().strip().split()
    dim=s[0]
    label=[]
    nlabel=len(s)-1
    if nlabel!=3:
        print "error:this is a boring triclassifer, only allow 3 classes"
        quit()
    for i in s[1:]:
        label.append(float(i))
    data=[]
    for line in f.readlines():
        data.append([float(i) for i in line.split()])
    ndata=len(data)

data=np.array(data)
centroids=[]
begin=0
for i in label:
    centroids.append(np.mean(data[begin:begin+i-1],0))
    begin+=i
if D:
    print np.shape(centroids)

def segment(dataset,w=None,b=None):
    prediction=dict()
    if w is None:
        train=True
        w=dict()
        b=dict()
    else:
        train=False
    for i in range(len(centroids)-1):
        for j in range(i+1,len(centroids)):
            if train:
                w[i,j]=centroids[i]-centroids[j]
                b[i,j]=w[i,j].dot((centroids[i]+centroids[j])/2.0).T
            if D:
                #print dataset.dot(w[i,j])
                pass
            y=dataset.dot(w[i,j].T)-b[i,j]
            prediction[i,j]=y>=0 # prefer higher alphabet 
    if train:
        return prediction,w,b
    return prediction

p,w,b=segment(data)
def eval(predict,label_bound,n,verbose=True):
    classes=dict()
    #A vs B
    classes[0]= predict[0,1]
    classes[1]=~predict[0,1]
    #A vs C
    classes[2]=~predict[0,2] & classes[0]
    classes[0]= predict[0,2] & classes[0]
    #B cs C
    classes[2]=(~predict[1,2] & classes[1])| classes[2]
    classes[1]=  predict[1,2] & classes[1]
    
    rate=dict()
    names=['True positive rate',
            'False positive rate',
            'Accuracy',
            'Error rate',
            'Precision']
    for i in names:
        rate[i]=[]

    low=0
    for pos,i in zip(label_bound,range(nlabel)):
        positions=np.argwhere(classes[i])
        high=low+pos
        neg=n-pos
        if D:
            print neg
        TP=sum((positions>=low) & (positions<high))
        FN=pos-TP
        FP=sum((positions<low)|(positions >=high))
        TN=neg-FP
        rate['True positive rate'].append(float(TP)/pos)
        #rate['FNR',i]=1-rate['True positive rate',i]
        rate['False positive rate'].append(float(FP)/neg)
        #rate['TNR',i]=1-rate['FPR',i]
        rate['Accuracy'].append(float(TP+TN)/n)
        rate['Error rate'].append(1-rate['Accuracy'][i])
        rate['Precision'].append(float(float(TP)/(TP+FP)))
        low=high
    if verbose:
        for i in names:
            print i,'=',sum(rate[i])/3.0
    return rate
    
rate=eval(p,label,ndata,False)
if D:
    print rate
# testing
with open(sys.argv[2]) as f:
    s=f.readline().strip().split()
    tdim=s[0]
    tlabel=[]
    for i in s[1:]:
        tlabel.append(float(i))
    tdata=[]
    for line in f.readlines():
        tdata.append([float(i) for i in line.split()])
tdata=np.array(tdata)
ntdata=len(tdata)
ty=dict()
tp=segment(tdata,w,b)
trate=eval(tp,tlabel,ntdata)
if D:
    print trate
