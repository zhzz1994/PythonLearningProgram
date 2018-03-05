import numpy as np

X = np.array([[0,0,1],
              [0,1,1],
              [1,0,1],
              [1,1,1]])
y = np.array([[0,1,1,0]]).T

np.random.seed(1)
syn0 = 2*np.random.random((3,5))-1
syn1 = 2*np.random.random((5,1))-1

def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))

for iter in range(60000):
    Inp = X
    Outpin = nonlin(np.dot(Inp,syn0))
    Outp = nonlin(np.dot(Outpin, syn1))
    Outp_error = y - Outp
    if(iter%10000)==0:
        print('error:'+str(np.mean(np.abs(Outp_error))))
    Outp_delta = Outp_error*nonlin(Outp,True)
    Outpin_error = Outp_delta.dot(syn1.T)
    Outpin_delta = Outpin_error*nonlin(Outpin,True)
    syn1 += np.dot(Outpin.T,Outp_delta)
    syn0 += np.dot(Inp.T,Outpin_delta)


print('output after training')
print(Outp)



