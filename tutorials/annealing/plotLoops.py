# /opt/local/bin/python3.14 plotLoops.py
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
sys.path.append("../../build/tools/pyMoDELib")
import pyMoDELib
sys.path.append("../../python/")
from modlibUtils import *

fig, axs = plt.subplots(1,1)


simulationDir=os.path.abspath(".")
materialFile=getStringInFile('inputFiles/polycrystal.txt','materialFile')
#b_SI=getValueInFile('inputFiles/'+materialFile,'b_SI')
#cs_SI=getValueInFile('inputFiles/'+materialFile,'cs_SI')

F,Flabels=readFfile(simulationDir+'/F')
ddBase=pyMoDELib.DislocationDynamicsBase(simulationDir)
b_SI=ddBase.poly.b_SI
cs_SI=ddBase.poly.cs_SI
configIO=pyMoDELib.DDconfigIO(simulationDir+'/evl')
defectiveCrystal=pyMoDELib.DefectiveCrystal(ddBase)
dislocationNetwork=defectiveCrystal.dislocationNetwork()
runIDs=getFarray(F,Flabels,'runID')
times=getFarray(F,Flabels,'time [b/cs]')
loopRaii=[]
loopTimes=[]
for k in range(0,len(runIDs)):
    runID=int(runIDs[k])
    time=times[k]
#    print(runID)
    configIO.read(runID)
    defectiveCrystal.initializeConfiguration(configIO)
    for loopID in dislocationNetwork.loops():
        loop=dislocationNetwork.loops().getRef(loopID)
        loopRaii.append(np.sqrt(loop.slippedArea()/np.pi)*b_SI*1.0e9)
        loopTimes.append(time*b_SI/cs_SI/3600) # time in hours
#        loopRunIDs.append(runID)

axs.scatter(loopTimes,loopRaii,0.1,color='k')
axs.set_xlabel('time [hours]')
axs.set_ylabel('average loop radii [nm]')
#fig.show()
fig.savefig("loopRadii.pdf", bbox_inches='tight', format='pdf')
