#Diagnostic Tools - 1
def draw():
    return test.reshape(slen,slen)
def draw2():
    return np.array(np.arange(0,size)).reshape(slen,slen)
def draw3(mat):
    m = np.matrix(mat.reshape(slen,slen))
    plt.imshow(np.flipud(m),interpolation='nearest',cmap='hot')
    plt.show()
def sumch():
    mat = np.matrix(rhog.reshape(slen,slen))
    return np.sum(mat[1:(slen-1),1:(slen-1)])
def drawtrons():
    #plt.plot(posx,posy,marker='.',linewidth = 0,ms=50,alpha=-0.9)
    plt.plot(posx,posy,marker='x',linewidth = 0)    
    plt.xlim(0,blen)
    plt.ylim(0,blen)
    plt.show()       
def chgcons():
    print(np.sum(rhog[1:(slen-1),1:(slen-1)]))