## module powell
''' xMin,nCyc = powell(F,x,h=0.1,tol=1.0e-6)
    Powell's method of minimizing user-supplied function F(x).
    x    = starting point
    h   = initial search increment used in 'bracket'
    xMin = mimimum point
    nCyc = number of cycles
'''
import numpy as np
from goldSearch import *
import math

def powell(F, x, bracketStep=0.001, goldenSearchWindow=0.001,
           epsilon=1.0e-6, iterations=100, bracketing=True, epsilonGoldenSearch=1.0e-6):

    def f(s):
        return F(x + s*v)    # F in direction of v

    n = len(x)                     # Number of design variables
    df = np.zeros(n)               # Decreases of F stored here
    u = np.identity(n)             # Vectors v stored here by rows
    for j in range(iterations):    # Allow for 100 cycles as default:
        xOld = x.copy()            # Save starting point
        fOld = F(xOld)
      # First n line searches record decreases of F
        for i in range(n):
            #print(i)
            v = u[i]
            if bracketing:   # Check if bracketing is selected
                a, b, isGood = bracket(f, 0.0, bracketStep)
            else:
                a = -goldenSearchWindow
                b = goldenSearchWindow
            if not isGood:
                return x, j+1, False, abs(F(x)-fOld), math.sqrt(np.dot(x-xOld, x-xOld)/n)
            s, fMin = search(f, a, b, tol=epsilonGoldenSearch)
            df[i] = fOld - fMin
            fOld = fMin
            x = x + s*v
      # Last line search in the cycle    
        v = x - xOld
        if bracketing:   # Check if bracketing is selected
            a, b, isGood = bracket(f, 0.0, bracketStep)
        else:
            a = -goldenSearchWindow
            b = goldenSearchWindow
        s, fLast = search(f, a, b, tol=epsilonGoldenSearch)
        x = x + s*v

      # Check for convergence
        if abs(F(x)-fOld) < epsilon:
            result = [float(i) for i in x]
            return result, j+1, True, abs(F(x)-fOld), math.sqrt(np.dot(x-xOld, x-xOld)/n)

        if math.sqrt(np.dot(x-xOld, x-xOld)/n) < epsilon:
            result = [float(i) for i in x]
            return result, j+1, True, abs(F(x)-fOld), math.sqrt(np.dot(x-xOld, x-xOld)/n)


      # Identify biggest decrease & update search directions
        iMax = np.argmax(df)
        for i in range(iMax, n-1):
            u[i] = u[i+1]
        u[n-1] = v

    return x, j+1, False, abs(F(x)-fOld), math.sqrt(np.dot(x-xOld, x-xOld)/n)
