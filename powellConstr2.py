from powell import *
from copy import deepcopy
def powellConstr(F, x0in, constrains=[], deltas=[], thetas=[], cMin=0.01, iterations=100, m2=10, m1=0.25,
                 bracketStep=0.001, goldenSearchWindow=0.001, epsilon=1.0e-6, bracketing=True, epsilonGoldenSearch=1.0e-6):
    x0 = deepcopy(x0in)
    x0list = []
    locThetas = []
    locDeltas = []
    c0 = 1e6

    for theta in thetas:
        locThetas.append(theta)

    for delta in deltas:
        locDeltas.append(delta)

    def H(sum):
        if sum > 0:
            return 1
        if sum <= 0:
            return 0

    #--------------------------------------------------------------------------------#
    # TUTAJ BEZ OGRANICZEN POLICZY
    if len(constrains) == 0:
        #print("Nie ma ograniczen!")
        x0, nIter, success, stopValue, stopNorm = powell(F, x0, epsilon=epsilon, iterations=iterations, bracketing=bracketing,
                                      bracketStep=bracketStep, goldenSearchWindow=goldenSearchWindow,
                                      epsilonGoldenSearch=epsilonGoldenSearch)
        #print("Pkt minimum:", x0)
        #print("F(x):", F(x0))
        x0list.append(x0)
        return True, x0list, stopValue, stopNorm,  nIter

    #--------------------------------------------------------------------------------#
    # WPROWADZANIE OGRANICZEN
    c = 0.01
    sixStep = False

    for k in range(iterations):    # Allow for 100 cycles as default:
        #print("_"*80)
        #print("Step: ", k)
        #print("Deltas:", locDeltas)
        #print("Thetas:", locThetas)
        #print("X0:", x0)
        def sumOfConstr(x):
            value = 0
            for i in range(len(constrains)):
                value += locDeltas[i]*(constrains[i](x)+locThetas[i])**2*H(constrains[i](x)+locThetas[i])
            return value

        def f(x):
            return F(x) + sumOfConstr(x)    # F in direction of v

        # 2 Dokonaj minimalizacji funkcji oraz uzyskany pkt ekstremalny podstaw w miejsce x0, a ponadto c w miejsce c0
        x0, nIter, success, stopValue, stopNorm = powell(f, x0, epsilon=epsilon, iterations=iterations, bracketing=bracketing,
                                      bracketStep=bracketStep, goldenSearchWindow=goldenSearchWindow,
                                      epsilonGoldenSearch=epsilonGoldenSearch)
        x0list.append(x0)
        # print("x0 w trakcie:", x0)
        c0 = c

        # 3 Oblicz w punkcie ekstremalnym wartoœæ ograniczeñ gi(x) dla i=1,...,m oraz now¹ wartoœæ c w myœl zasady
        constrViolation = []
        for i in range(len(constrains)):
            temp = constrains[i](x0) + locThetas[i]
            if temp > 0:
                #print("Violation of constraint", i)
                constrViolation.append(abs(constrains[i](x0)))
        # Nale¿y siê upewniæ, ¿e jest ograniczenie, ktore nie zostalo spelnione
        if len(constrViolation) > 0:
            c = max(constrViolation)
        #print("The largest violation of constraints:", c)

        # 4 zbadaj czy zosta³o spe³nione kryterium na "minimum" tzn. czy c<cMin.
        if c < cMin:
            #print('zostalo spelnione kryterium na "minimum" tzn. czy c<cMi')
            #print(f(x0))
            #print ("Xmin:", x0)
            return True, x0list, stopValue, stopNorm,  nIter
        # Jeœli tak to zakoñcz dzia³anie procedury, natomiast jeœli nie to kolejne kroki.

        # 5 Zbadaj czy po minimalizacji (krok 2) nastapilo zmniejszenie naruszenia ograniczen,
        # tzn. czy c<c0. Jesli tak, to przejdz do wykonania kroku (8),
        if c < c0:
            # Tutaj jest robiony krok 8
            # 8 Jesli k=0 lub w poprzedniej iteracji byl krok 6 to
            if k == 0 or sixStep:
                # To jest krok 8a, zmien wartosci theta w mysl zasady:
                for i in range(len(locThetas)):
                    locThetas[i] = min(constrains[i](x0) + locThetas[i], 0)
                sixStep = False  # nie bylo 6 kroku w tej iteracji
                continue
            else:
                # Krok 8b
                if c <= m1*c0:
                    # Wykonaj krok 8a, zmien wartosci theta w mysl zasady:
                    for i in range(len(locThetas)):
                        locThetas[i] = min(constrains[i](x0) + locThetas[i], 0)
                else:
                    # Wykonaj krok 6:
                    sixStep = True
                    modifiedIndexes = []
                    for i in range(len(locDeltas)):
                        if (abs((constrains[i](x0)) > m1*c0) and (constrains[i](x0) + locThetas[i] > 0)):
                            modifiedIndexes.append(i)
                    for i in modifiedIndexes:
                        locDeltas[i] *= m2
                        locThetas[i] /= m2
                    continue
        # Natomiast w przecinwym razie podstaw na miejsce c jego wartosc przed minimalizacja, tzn c=c0
        else:
            c = c0

        # 6 Zmien wartosc parametriw delta i theta wedlug reguly: delta = m2*delta, theta = theta/m2
        modifiedIndexes = []
        for i in range(len(locDeltas)):
            if (abs((constrains[i](x0)) > m1*c0) and (constrains[i](x0) + locThetas[i] > 0)):
                modifiedIndexes.append(i)

        for i in modifiedIndexes:
            locDeltas[i] *= m2
            locThetas[i] /= m2
    return True, x0list, stopValue, stopNorm,  nIter