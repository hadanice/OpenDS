import numpy as np

class CSCMatrix:
    def __init__(self, nzval, rowind, colptr):
        self.nzval=list(nzval)
        self.rowind=list(rowind)
        self.colptr=list(colptr)

def x2ax_csc(x,A):
    result=np.zeros_like(x)
    val=A.nzval
    index=A.rowind
    ptr=A.colptr
    track=0
    for i in range(len(val)):
        while i>=ptr[track]:
            track+=1
        result[index[i]]+=val[i]*x[ptr[track]]
    return result

def x2atx_csc(x,A):
    result=np.zeros_like(x)
    val=A.nzval
    index=A.rowind
    ptr=A.colptr
    track=0
    for i in range(len(val)):
        while i>=ptr[track]:
            track+=1
        result[ptr[track]]+=val[i]*x[index[i]]
    return result