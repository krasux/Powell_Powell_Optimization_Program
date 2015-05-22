from powell import *

def powellConstr(F, x0, constrains=[], deltas=[], thetas=[], cMin=0.01, iterations=100, m2=10, m1=0.25):

    print("Number of constraints:", len(constrains))

    c = 0.01

    locThetas = []
    locDeltas = []

    for theta in thetas:
        locThetas.append(theta)

    for delta in deltas:
        locDeltas.append(delta)

    print("Deltas:", deltas)
    print("Thetas:", thetas)

    def H(sum):
        if sum > 0:
            return 1
        if sum <= 0:
            return 0


    for j in range(iterations):    # Allow for 100 cycles as default:
        print("_"*80)
        print("Step: ", j)
        print("Deltas:", locDeltas)
        def sumOfConstr(x):
            value = 0
            for i in range(len(constrains)):
                value += locDeltas[i]*(constrains[i](x)+locThetas[i])**2*H(constrains[i](x)+locThetas[i])
            return value

        def f(x):
            return F(x) + sumOfConstr(x)    # F in direction of v

        # 2 Dokonaj minimalizacji funkcji oraz uzyskany pkt ekstremalny podstaw w miejsce x0, a ponadto c w miejsce c0
        x0, nIter, success = powell(f, x0)
        print("x0 w trakcie:", x0)
        c0 = c

        # 3 Oblicz w punkcie ekstremalnym wartoœæ ograniczeñ gi(x) dla i=1,...,m oraz now¹ wartoœæ c w myœl zasady
        constrViolation = []
        for i in range(len(constrains)):
            temp = constrains[i](x0) + locThetas[i]
            if temp > 0:
                print("Violation of constraint", i)
                constrViolation.append(abs(constrains[i](x0)))
        # Nale¿y siê upewniæ, ¿e jest ograniczenie, ktore nie zostalo spelnione
        if len(constrViolation) > 0:
            c = max(constrViolation)
        print("The largest violation of constraints:", c)

        # 4 zbadaj czy zosta³o spe³nione kryterium na "minimum" tzn. czy c<cMin.
        if c < cMin:
            print('zostalo spelnione kryterium na "minimum" tzn. czy c<cMi')
            print(f(x0))
            print ("Xmin:", x0)
            return x0
        # Jeœli tak to zakoñcz dzia³anie procedury, natomiast jeœli nie to kolejne kroki.

        modifiedIndexes = []
        for i in range(len(deltas)):
            if (abs((constrains[i](x0)) > m1*c0) and (constrains[i](x0) + locThetas[i] > 0)):
                modifiedIndexes.append(i)

        for i in modifiedIndexes:
            locDeltas[i] *= m2
            locThetas[i] /= m2

