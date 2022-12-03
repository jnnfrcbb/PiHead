
STEP_COUNT = 10

def getGraph(GRP_CUT,GRP_PROP):    
    tempGraph = []
    NEW_STEP=GRP_CUT[0]/(STEP_COUNT*GRP_PROP[0])
    for g in GRP_CUT:
        grpIndex = GRP_CUT.index(g)
        grpStep = (STEP_COUNT*GRP_PROP[grpIndex])    
        stepCount = 0
        while NEW_STEP < g:
            tempGraph.append(NEW_STEP)
            print(NEW_STEP)
            if grpIndex > 1:
                NEXT_VAL = NEW_STEP+((GRP_CUT[grpIndex]-GRP_CUT[grpIndex-1])/grpStep)                
            else:
                NEXT_VAL = NEW_STEP+(GRP_CUT[grpIndex]/grpStep)
            if stepCount <= grpStep:
                NEW_STEP = NEXT_VAL
                stepCount+=1            
        if grpIndex == len(GRP_CUT)-1:
            NEW_STEP = GRP_CUT[grpIndex]
            tempGraph.append(NEW_STEP)
            print(NEW_STEP)
    return tempGraph

#lux graph values
#0-1        3   20%
#2-50       2   20%
#51-200     3   30%
#201-400    2   20%

#set upper boundaries for groups
LUX_CUT = [1,50,200,400]

#set % of step count in each group
LUX_PROP = [0.3, 0.2, 0.3, 0.2]

#get lux graph for group values
LUX_LEVEL = getGraph(LUX_CUT,LUX_PROP)

#display brightness graph values
#0-9        1
#10-89      4
#90-179     3
#180-255    3

#set upper boundaries for groups
DISP_CUT = [10,75,180,255]          #adjust these numbers up or down to raise or lower brightness for each group

#set % of step count in each group
DISP_PROP = [0.3, 0.3, 0.2, 0.2]    #distribute towards top to raise brightness, towards bottom to lower brightness

#get lux graph for group values
DISP_BRIGHTNESS = getGraph(DISP_CUT,DISP_PROP)