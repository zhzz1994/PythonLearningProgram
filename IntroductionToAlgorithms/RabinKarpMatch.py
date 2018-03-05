import random

def RKmatch(str,partternstr):
    parttern = 0
    for item in partternstr:
        parttern = item + parttern * 10
    parttern = parttern % 99
    strpt = 0
    for index in range(0,len(partternstr)):
        strpt = str[index] + strpt * 10
    strpt = strpt % 99
    start = 0
    for substr in range(0,len(str) - len(partternstr)):
        if strpt == parttern:
            match = True
            for index in range(0, len(partternstr)):
                if partternstr[index] != str[start + index]:
                    match = False
            if match:
                print(start)
                return start
            else:
                strpt = (((strpt - (str[start] * (10**(len(partternstr) - 1)))) * 10 ) + str[len(partternstr) + start]) % 99
                start = start + 1
        else:
            strpt = (((strpt - (str[start] * (10**(len(partternstr) - 1)))) * 10 ) + str[len(partternstr) + start])  % 99
            start = start + 1
    print('no str match the pattern')

def AutomationMatch(partternstr,str):
    statePosible = []
    partternstr = list(partternstr)
    str = list(str)
    compare = partternstr.copy()
    statePosible.append(0)
    start = 0
    for index in range(1,len(partternstr)):
        if compare[index] == partternstr[start]:
            start = start + 1
            statePosible.append(start)
        else:
            start = 0
            statePosible.append(start)
    state = 0
    for position in range(0,len(str)):
        while str[position] != partternstr[state] and state != 0:
            state = statePosible[state]
        if str[position] == partternstr[state]:
            state = state + 1
        if state == len(partternstr):
            return position - len(partternstr) + 1
    print('no str match the pattern')







# s = AutomationMatch('ababaca','sgshjklssssdfgeqwsxdfrtasdhghgfhgdgfdgfababcashjababacaksljs')
# print(s)

    # inputAtoms = list(set(partternstr))
    # stateArrays.append(inputAtoms)
    # state = 0
    # for item in partternstr:
    #     stateArray = []
    #     for inputAtom in inputAtoms:
    #         if item == inputAtom:
    #             theState = state + 1
    #             stateArray.append(theState)
    #         else:

def RKtest():
    str = []
    for i in range(0,100):
        str.append(random.randint(0,9))
    print(str)
    partternstr = [4,3]
    RKmatch(str,partternstr)

def AMtest():
    rg = 'asdf'
    str = []
    for i in range(0, 1000):
        str.append(rg[random.randint(0, 3)])
    print(str)
    partternstr = 'asff'
    print(AutomationMatch(partternstr, str))

AMtest()