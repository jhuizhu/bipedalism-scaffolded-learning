#!/usr/bin/env python
import math
import operator
import copy
import subprocess
import os
import sys
import signal
from time import strftime, sleep
import cPickle as pickle
import random
from numpy.random import binomial, normal

continuing = False
currentTime = strftime('%m_%d_%H_%M_%S')

if len(sys.argv) > 3:
  partFile = sys.argv[3]
  currentTime = partFile[5:-4]
  continuing = True

with open(sys.argv[1], 'w') as trackerFile:
  trackerFile.write(currentTime + '\n')
threads = int(sys.argv[2])

print 'No of threads =', threads

if continuing:
  print partFile
  fitnessOutput = open ('fitnessOutput-' + currentTime, 'a')
  summarisedOutput = open ('summarisedOutput-' + currentTime, 'a')
else:
  fitnessOutput = open ('fitnessOutput-' + currentTime, 'w')
  summarisedOutput = open ('summarisedOutput-' + currentTime, 'w')

maxGens = 4000
fitnessOutput.write ('Max generations: ' + str(maxGens) + '\n')
fitnessOutput.write ('Filename: ' + sys.argv[0] + '\n')
fitnessOutput.write ('Changeset: ' + os.popen('hg log | head -n1').read())
genSize = 16
fitnessOutput.write ('Generation Size: ' + str(genSize) + '\n')
mutationOffspring = 10
fitnessOutput.write ('Mutation offspring: ' + str(mutationOffspring) + '\n')
fittestThresh = 16
if (fittestThresh % 2 != 0):
  print 'Fittest thresh should be a multiple of 2'
  sys.exit(-1)
fitnessOutput.write ('Fittest thresh: ' + str(fittestThresh) + '\n\n')
timeout = '25'
sigFigs = 3

binaryLoc = '../simbody/twoLegVar/build/walker.o'
visBinaryLoc = '../simbody/twoLegVar/build/walkerVis.o'

defaultParams = {'ankleMass': 0.1, 'kneeMass': 0.7, 'halfFootBodyX': 0.22018185203456214, 'stableTolerance': 0.23297511065336013, 'hipMass': 0.1, 'stepK': 206.62152951267495, 'standOffset': 0.014009581796928235, 'bodyStraightL': 103.77362891303223, 'bodyStraightK': 300, 'stepOffset': -0.00213586038101777, 'femurLength': 0.5301194705959408, 'lambda1': 756.2758489218877, 'tibiaLength': 0.6845846448329076, 'k1': 1572.4184169068672, 'halfFootBodyY': 0.05, 'halfBodyX': 0.8822120184545844, 'halfBodyY': 0.1353015130243578, 'halfFootBodyZ': 0.06957592968690621, 'k2': 6980.007289620993, 'halfBodyZ': 0.329704208858325, 'lambda2': 1930.5445286783713}


fitnessOutput.write ('Default parameters: \n' + str(defaultParams) + '\n\n')
paramSize = len(defaultParams)

parameterDic = {
'halfBodyX':      {'position': 0,  'mutationProb': 0.9, 'standardDev': abs(defaultParams['halfBodyX'])         /3.,'floor': 0.05, 'ceil': 0.9},
'halfBodyY':      {'position': 1,  'mutationProb': 0.9, 'standardDev': abs(defaultParams['halfBodyY'])         /3.,'floor': 0.05, 'ceil': 0.3},
'halfBodyZ':      {'position': 2,  'mutationProb': 0.9, 'standardDev': abs(defaultParams['halfBodyZ'])         /3.,'floor': 0.25, 'ceil': 0.4},
'halfFootBodyX':  {'position': 3,  'mutationProb': 0.9, 'standardDev': abs(defaultParams['halfFootBodyX'])     /3.,'floor': 0.05, 'ceil': 0.4},
'halfFootBodyY':  {'position': 4,  'mutationProb': 0.9, 'standardDev': abs(defaultParams['halfFootBodyY'])     /3.,'floor': 0.05, 'ceil': 0.4},
'halfFootBodyZ':  {'position': 5,  'mutationProb': 0.9, 'standardDev': abs(defaultParams['halfFootBodyZ'])     /3.,'floor': 0.05, 'ceil': 0.23},
'k1':             {'position': 6,  'mutationProb': 0.9, 'standardDev': abs(defaultParams['k1'])                /5.,'floor': 0, 'ceil': 20000},
'k2':             {'position': 7,  'mutationProb': 0.9, 'standardDev': abs(defaultParams['k2'])                /5.,'floor': 3000, 'ceil': 24000},
'lambda1':        {'position': 8,  'mutationProb': 0.9, 'standardDev': abs(defaultParams['lambda1'])           /5.,'floor': 0, 'ceil': 2000},
'lambda2':        {'position': 9,  'mutationProb': 0.9, 'standardDev': abs(defaultParams['lambda2'])           /5.,'floor': 0, 'ceil': 2000},
'bodyStraightK':  {'position': 10, 'mutationProb': 0.9, 'standardDev': abs(defaultParams['bodyStraightK'])     /5.,'floor': 0, 'ceil': 300},
'bodyStraightL':  {'position': 11, 'mutationProb': 0.9, 'standardDev': abs(defaultParams['bodyStraightL'])    /11.,'floor': 0, 'ceil': 300},
'kneeMass':       {'position': 12, 'mutationProb': 0,   'standardDev': abs(defaultParams['kneeMass'])          /5.,'floor': 0.9, 'ceil': 1},
'ankleMass':      {'position': 13, 'mutationProb': 0,   'standardDev': abs(defaultParams['ankleMass'])         /5.,'floor': 0.9, 'ceil': 1},
'hipMass':        {'position': 14, 'mutationProb': 0,   'standardDev': abs(defaultParams['hipMass'])           /5.,'floor': 0.9, 'ceil': 1},
'stepK':          {'position': 15, 'mutationProb': 0.9, 'standardDev': abs(defaultParams['stepK'])             /5.,'floor': 0, 'ceil': 800},
'stableTolerance':{'position': 16, 'mutationProb': 0.9, 'standardDev': abs(defaultParams['stableTolerance'])   /5.,'floor': 0, 'ceil': 0.25},
'tibiaLength':    {'position': 17, 'mutationProb': 0.9, 'standardDev': abs(defaultParams['tibiaLength'])       /5.,'floor': 0.1, 'ceil': 1.9},
'femurLength':    {'position': 18, 'mutationProb': 0.9, 'standardDev': abs(defaultParams['femurLength'])       /5.,'floor': 0.1, 'ceil': 1.9},
'standOffset':    {'position': 19, 'mutationProb': 0.9, 'standardDev': abs(defaultParams['standOffset'])       /5.,'floor': -0.2, 'ceil': 0.35},
'stepOffset':     {'position': 20, 'mutationProb': 0.9, 'standardDev': abs(defaultParams['stepOffset'])        /5.,'floor': -1., 'ceil': 0.3},
}
hashTable = set()

fitnessOutput.write ('Parameter Dictionary : \n' + str(parameterDic) + '\n\n')

def saturate(lower, upper, inp):
  if (inp > upper):
    inp = upper
  elif (inp < lower):
    inp = lower
  return inp

def roundToN(x, n):
  return 0 if (x == 0) else round(x, -int(math.floor(math.log10(abs(x)))) + (n - 1))

class Robot():
  def __init__(self, params, parents):
    self.params = params
    self.args = [None]*paramSize
    self.fitness = 0
    self.stdout = ''
    self.error = ''
    self.parents = parents
    for key in self.params:
      self.args[parameterDic[key]['position']] = self.params[key]

    global hashTable
    hashTable.add(hash(tuple([roundToN(i, sigFigs) for i in self.args])))

  def setId(self, generation, number):
    self.robotId = str(generation) + '_' + str(number)

  def duplicate(self, other):
    return (self.args == other.args)

  def simulate(self):
    self.simulation = (
    subprocess.Popen(['timeout', timeout, binaryLoc] + [str(i) for i in self.args], stdout=subprocess.PIPE, stderr=subprocess.PIPE))

  def descrip(self):
    argsToPrint = ' ' + ' '.join([str(i) for i in self.args]) + '\n'

    return ('\n*** Robot ID: ***\n' + self.robotId + '\nFitness:\n' + 
        str(self.fitness) + '\nParent(s)\nParent 1: ' + self.parents + '\nOutput:\n' + self.stdout + '\nError:\n' + self.error + 
  '\n' + str(self.params) + '\nCommand:\n' + visBinaryLoc + argsToPrint + binaryLoc + argsToPrint)

  def mutate(self):
    return Robot(self.mutateParams(self.params), str(self.robotId))

  def mutateParams(self, inputParams):
    while True:
      newParams = copy.deepcopy(inputParams)
      for key in defaultParams:
        if (binomial (1, parameterDic[key]['mutationProb'])):
          newParams[key] = saturate(parameterDic[key]['floor'], parameterDic[key]['ceil'], normal(newParams[key], parameterDic[key]['standardDev']))
###Simulted annealing
      #global currentGen
      if (currentGen>=0 and currentGen<499):
        newParams['halfBodyX'] = saturate(parameterDic['halfBodyX']['floor'], parameterDic['halfBodyX']['ceil'], normal(newParams['halfBodyX'], parameterDic['halfBodyX']['standardDev']))
            # print 'X1: ' + str(newParams['halfBodyX'])
      elif (currentGen>=499 and currentGen<999):
        newParams['halfBodyX'] = saturate(parameterDic['halfBodyX']['floor'], parameterDic['halfBodyX']['ceil']-0.2, normal(newParams['halfBodyX'], parameterDic['halfBodyX']['standardDev']))
        # print 'X2: ' + str(newParams['halfBodyX'])
      elif (currentGen>=999 and currentGen<1499):
        newParams['halfBodyX'] = saturate(parameterDic['halfBodyX']['floor'], parameterDic['halfBodyX']['ceil']-0.4, normal(newParams['halfBodyX'], parameterDic['halfBodyX']['standardDev']))
        # print 'X3: ' + str(newParams['halfBodyX'])
      elif (currentGen>=1499 and currentGen<1999):
        newParams['halfBodyX'] = saturate(parameterDic['halfBodyX']['floor'], parameterDic['halfBodyX']['ceil']-0.6, normal(newParams['halfBodyX'], parameterDic['halfBodyX']['standardDev']))
        # print 'X4: ' + str(newParams['halfBodyX'])
      else:
        newParams['halfBodyX'] = saturate(parameterDic['halfBodyX']['floor'], parameterDic['halfBodyX']['ceil']-0.8, normal(newParams['halfBodyX'], parameterDic['halfBodyX']['standardDev']))
        # print 'para: ' + key + '>>>'+ str(newParams[key])      
      # print 'halfBodyX: ' + str(newParams['halfBodyX'])      
###

      newArgs = [None]*paramSize
      for key in newParams:
        newArgs[parameterDic[key]['position']] = roundToN(newParams[key], sigFigs)
        # print 'pass2'
      global hashtable
      if (hash(tuple(newArgs)) not in hashTable):
        break
      else:
        print 'Duplicate!'

    return newParams

  def combine(self, mate):
    parentArgs = str(self.robotId) + '\nParent 2: ' + str(mate.robotId)
    newParams = copy.deepcopy(self.params)
    for key in self.params:
      newParams[key] = (self.params[key] + mate.params[key])/2.

    return Robot(self.mutateParams(newParams), parentArgs)

def main_function():
  currentGen = 0
  global currentGen
  global hashTable
  if continuing:
    with open(partFile, 'rb') as input:
      robots = pickle.load(input)
      hashTable = pickle.load(input)
      currentGen = pickle.load(input)
    print 'Robots:', len(robots)
    robots.sort(key=operator.attrgetter('fitness'), reverse=True)
    for i in range(len(robots)):
      print robots[i].fitness
      robots[i] = Robot(robots[i].params, '')

    robots.sort(key=operator.attrgetter('fitness'), reverse=True)
    if genSize > len(robots):
      for i in range(genSize - len(robots)):
        robots.append(robots[i].mutate())
    else:
      robots = robots[:genSize]    
    print 'Robots:', len(robots)

  else:
    defaultRobot = Robot(defaultParams, '')
    defaultRobot.setId(0, 0)
    robots = [defaultRobot]
    for i in range(genSize - 1):
      robots.append(defaultRobot.mutate())

  fittest = []

  def sigHandler(signal, frame):
    with open('dump-' + currentTime + '.pkl', 'wb') as output:
      pickle.dump (fittest, output, pickle.HIGHEST_PROTOCOL)
      pickle.dump (hashTable, output, pickle.HIGHEST_PROTOCOL)
      pickle.dump (currentGen, output, pickle.HIGHEST_PROTOCOL)

    with open(sys.argv[1], 'a') as trackerFile:
      trackerFile.write('Killed\n')

    summarisedOutput.write(str([[i.params, i.fitness] for i in fittest])) 
    fitnessOutput.flush()
    summarisedOutput.flush()
    os.system('sync')
    fitnessOutput.close()
    summarisedOutput.close()
    for i in range(len(robots)):
      try:
        print robots[i].simulation.pid
        robots[i].simulation.terminate()
        robots[i].simulation.wait()
      except:
        print 'This robot', i, 'never had a simulation'

    sys.exit(0)

  signal.signal(signal.SIGXCPU, sigHandler)
  signal.signal(signal.SIGINT, sigHandler)
  signal.signal(signal.SIGTERM, sigHandler)

  while currentGen < maxGens:
    for k in range(genSize / threads):
      for l in range(threads):
        robots[threads*k+l].setId(currentGen, threads*k+l)
        robots[threads*k+l].simulate()

      for l in range(threads):
        robots[threads*k+l].returnCode = robots[threads*k+l].simulation.wait()

        output = robots[threads*k+l].simulation.communicate()
        robots[threads*k+l].stdout = output[0]
        if robots[threads*k+l].returnCode == 124:
          robots[threads*k+l].fitness = -124 #signals timeout
          print 'Generation ' + str(currentGen) + ' Robot ' + str(threads*k+l) + ' timed out'
          robots[threads*k+l].error += 'Timeout\n'
        elif robots[threads*k+l].returnCode != 0:
          robots[threads*k+l].fitness = -1
        else:
          robots[threads*k+l].fitness = float(output[0])

        print 'Robot', threads*k+l, 'fitness =', robots[threads*k+l].fitness

        robots[threads*k+l].error += output[1]

    fitnessOutput.write ('****** Generation no. ' + str(currentGen) + ' ******' )
    for aRobot in robots:
      fitnessOutput.write(str(aRobot.descrip()))

    print 'Generation: ' + str(currentGen)
    currentGenFitnesses = [n.fitness for n in robots]
    print currentGenFitnesses
    summarisedOutput.write('Generation: ' + str(currentGen) + '\n')
    summarisedOutput.write('Current Fitness:\n')
    summarisedOutput.write(str(currentGenFitnesses) + '\n\n')
    fittest += robots
    fittest.sort(key=operator.attrgetter('fitness'), reverse=True)
    fittest = fittest[:fittestThresh]

    print 'Fittest'
    overallFittest = [n.fitness for n in fittest]
    print overallFittest
    summarisedOutput.write('All time fittest:\n')
    summarisedOutput.write(str(overallFittest) + '\n\n')
    robots = []
    for j in range(mutationOffspring):
      if (j % len(fittest) == 0):
        parentTracker = range (len(fittest))
        random.shuffle(parentTracker)
      robots.append(fittest[parentTracker.pop()].mutate())

    for j in range(genSize - mutationOffspring): # combined robots
      if (j % (len(fittest)/2) == 0):
        parentTracker = range (len(fittest))
        random.shuffle(parentTracker)
      robots.append(fittest[parentTracker.pop()].combine(fittest[parentTracker.pop()]))

    fitnessOutput.flush()
    summarisedOutput.flush()
    os.system('sync')
    currentGen += 1

  summarisedOutput.write(str([[i.params, i.fitness] for i in fittest])) 
  doneMsg = 'Done at ' + strftime('%m_%d_%H_%M_%S') + '\n'
  summarisedOutput.write(doneMsg)
  print doneMsg

  fitnessOutput.close()
  summarisedOutput.close()

  with open(sys.argv[1], 'a') as trackerFile:
    trackerFile.write('Done\n')

if __name__ == '__main__':
  main_function()