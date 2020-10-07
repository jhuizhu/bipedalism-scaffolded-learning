#!/usr/bin/env python
#Warning - this reads whole file into RAM for speed and creates a list with every robot ever - don't do it with a small RAM!
import matplotlib.pyplot as plt
import math
import sys
import time
import os
import re
import ast
import numpy as np
from scipy.signal import savgol_filter
import pandas as pd
def chunks(l, n):
  for i in xrange(0, len(l), n):
    yield l[i:i+n]

matchBraces = re.compile('^{.*}$')
number = re.compile('.*\(\d*\)')
bigList = []
fitness = open(sys.argv[1], 'r')
fitnessLines = fitness.readlines()
num_lines = len(fitnessLines)
#generationMatch = number.match(fitnessLines[1])
#print 'match', generationMatch
#match = int(generationMatch.group())
#print 'No of gens', match
i = 0
while i < num_lines:
  line = fitnessLines[i]
  if line == 'Fitness:\n':
    #print 'Found fitness'
    i += 1
    if (i > num_lines):
      # print 'EOF'
      break
    fitnessVal = float(fitnessLines[i])
    #print 'Fitness:', fitnessVal
    while True:
      i += 1
      if (i > num_lines):
        # print 'EOF'
        break
      newLine = fitnessLines[i]
      if newLine == 'Fitness:\n' or newLine == '*** Robot ID: ***\n':
        # print 'Broken file at line', i
        i -= 1
        break

      else:
        #print 'Test line:', newLine
        match = matchBraces.match(newLine)
        #print 'Passed'
        if match:
          match = match.group()
          bigList.append([fitnessVal, ast.literal_eval(match)])
          i += 1
          break
  i += 1

s = 11
fitness.close()
fitnessLines = None

bigList = list(chunks(bigList, 16))
k2List = []
for key in bigList[0][0][1]:
  for i in bigList:
    gen = [el[1][key] for el in i]
    k2List.append(sum(gen)/float(len(gen)))
  #plt.rc('text', usetex=True)
  # plt.rc('font', family='serif')
  if key == 'halfBodyX':
    global df
    df = pd.DataFrame(k2List)
    plt.plot(df[0], 'lightblue', df[0].rolling(10).mean(), 'dodgerblue')
    # k2List = savgol_filter(k2List,11,4)
    # plt.plot(k2List, 'b')
    plt.xlim((0, 4001))    
    plt.ylim((0, 0.9))    
    my_x_ticks = np.arange(0, 4001, 500)
    my_y_ticks = np.arange(0, 0.91, 0.1)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)

    # plt.yticks(fontsize=s)
    plt.ylabel('Body length (m)')
    plt.xlabel('Generations (-)')
    #plt.show()
    plt.grid(alpha=0.6)
    # plt.savefig('/home/lima/Desktop/Case/figs/para/length/bodyLength.pdf', bbox_inches='tight')
    plt.clf()
    # plt.close()
    # k2List = []
  elif key == 'femurLength':
    df1 = pd.DataFrame(k2List)
    plt.plot(df1[0], 'lightblue', df1[0].rolling(10).mean(), 'dodgerblue')
    # k2List_av = savgol_filter(k2List,11,4)
    # plt.plot(k2List_av)
    plt.xlim((0, 4001))    
    # plt.ylim((0.29, 0.66))  
    plt.ylim((0.29, 0.91))    
      
    my_x_ticks = np.arange(0, 4001, 500)
    my_y_ticks = np.arange(0.35, 0.86, 0.1)

    # my_y_ticks = np.arange(0.3, 0.65, 0.05)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)
    plt.ylabel('Femur length (m)')
    plt.xlabel('Generations (-)')
    #plt.show()
    plt.grid(alpha=0.6)
    # plt.savefig('/home/lima/Desktop/Case/figs/para/length/' + key + '.pdf', bbox_inches='tight')
    plt.clf()
    # plt.close()
    # k2List = []
  elif key == 'tibiaLength':
    df2 = pd.DataFrame(k2List)
    plt.plot(df2[0], 'lightblue', df2[0].rolling(10).mean(), 'dodgerblue')
    # k2List_av = savgol_filter(k2List, 11, 4)
    # plt.plot(k2List_av)
    plt.xlim((0, 4001))    
    plt.ylim((0.29, 0.91))    
    
    my_x_ticks = np.arange(0, 4001, 500)
    my_y_ticks = np.arange(0.35, 0.86, 0.1)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)
    plt.ylabel('Tibia length (m)')
    plt.xlabel('Generations (-)')
    #plt.show()
    plt.grid(alpha=0.6)
    # plt.savefig('/home/lima/Desktop/Case/figs/para/length/' + key + '.pdf', bbox_inches='tight')
    plt.clf()
    # plt.close()
    # k2List = []
  else:
    plt.plot(k2List)
    plt.xlim((0, 4001))    
    #plt.ylim((0, 19))    
    my_x_ticks = np.arange(0, 4001, 500)
    #my_y_ticks = np.arange(0, 19, 2)
    plt.xticks(my_x_ticks, fontsize=s)
    plt.yticks(fontsize=s)
    plt.ylabel(key + ' (m)', fontsize=s)
    plt.xlabel('Generations (-)', fontsize=s)
    #plt.show()
    # plt.savefig('/home/lima/Desktop/Case/figs/para/psa_1/' + key + '.pdf', bbox_inches='tight')
    plt.clf()
    plt.close()
    k2List = []
fig = plt.figure(figsize=(6,5))
ax = fig.add_subplot(111)


ax.plot(df1[0], 'lightsalmon')
type2 = ax.plot(df1[0].rolling(10).mean(), 'orangered')

ax.plot(df2[0], 'lightgreen')
type3 = ax.plot(df2[0].rolling(10).mean(), 'seagreen')

ax.plot(df[0], 'lightblue')
type1 = ax.plot(df[0].rolling(10).mean(), 'dodgerblue')
# ax.legend(loc='lower right')

# ax.legend([type1, type2, type3], ('Body length', 'Femur length', 'Tibia length'), loc='lower right')

import matplotlib.lines as mlines
blue_line = mlines.Line2D([], [], color='dodgerblue', label='Body length')
red_line = mlines.Line2D([], [], color='orangered', label='Femur length')
green_line = mlines.Line2D([], [], color='seagreen', label='Tibia length')


plt.legend(handles=[green_line, red_line, blue_line], loc=0)
# k2List = savgol_filter(k2List,11,4)
# ax.plot(k2List, 'b')
ax.set_xlim((0, 4001))    
ax.set_ylim((0, 0.9))    
my_x_ticks = np.arange(0, 4001, 500)
my_y_ticks = np.arange(0, 0.91, 0.1)
ax.set_xticks(my_x_ticks)
ax.set_yticks(my_y_ticks)

s = 12
plt.xticks(fontsize=s)
plt.yticks(fontsize=s)
# ax.yticks(fontsize=s)
ax.set_ylabel('Body parameters (m)', fontsize=s)
ax.set_xlabel('Generations (-)', fontsize=s)
#ax.show()
plt.grid(alpha=0.6)
# plt.rc('font', family='serif', size=20)
plt.savefig('/home/lima/Desktop/Case/image/length.pdf', bbox_inches='tight')
#fig = plt.figure()
#ax = fig.add_subplot(111)

#k2List = [[]]*64
#for i in bigList:
  #for j in range(len(i)):
    #k2List[j].append(i[j][1]['tibiaLength'])

#for i in range(1):
  #ax.plot(k2List[i])

plt.show()
