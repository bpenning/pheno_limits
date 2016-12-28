#!/usr/bin/env python
"""
run exactly the same way as './plotContour.py' but gives only list of values needed for fancy limit plotter
"""
import ROOT as r
import sys
import math as m
import numpy as np
from array import array
import random
from array import array

from scipy import interpolate
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.colors as mcol



def makePlot():


  for k in range(len(sys.argv)-1):
    infile = open(sys.argv[k+1],"r")
    filestoread=infile.readlines()
    yvalues=[]

    #get from info file all yvalued (first column) and sort
    for i in range(len(filestoread)):
      thisline=filestoread[i].split()
      yvalues.append([float(thisline[0]),thisline[1]])
    yvalues.sort(key=lambda x: float(x[0]))

    #loop over y values getting tfiles and extracting x values and limits
    medianvalues=[]  #these are the median expectd mu values
    xbins=[]
    ybins=[]
    
    values = np.empty(shape=[0,3])
    
    for i in range(len(yvalues)):
     # ybincenters.append(float(yvalues[i][0]))  #store yvalue in ybincenter
      tf = r.TFile(yvalues[i][1]) #get the root files with x values per y value
      tree = tf.Get('limit') #get limit branch
      xvalues=[]  #will contain six values, observed (5) plus 5 expected (median (2) and +/- 1/2 sigma (0,1,3,4)), then repeating the pattern
      for j in range(tree.GetEntries()):
        tree.GetEntry(j)  
        #this is awkard but best I could come up with without being mega error prone because of the way combine stores values
        if ((j-2)%6==0):
#          print str(j)+': '+str(yvalues[i][0])+'\t'+str(tree.mh)+'\t'+str(tree.limit) #in principle we have here all values
          print '['+str(yvalues[i][0])+', '+str(tree.mh)+', '+str(tree.limit)+'],' #in principle we have here all values
          xbins.append(tree.mh)
          ybins.append(yvalues[i][0])
          medianvalues.append(tree.limit)
          values = np.append(values, [[tree.mh, yvalues[i][0], tree.limit]], axis=0)

    values.view('i8,i8,i8').sort(order=['f2'], axis=0)  #sort according to last column (f0, f1, f2 etc)
    #now we have all values in some sort of sensible numpy array
#    print values

    stops = [0.0000, 0.1250, 0.2500, 0.3750, 0.5000, 0.6250, 0.7500, 0.8750, 1.0000]
    red   = [0.2082, 0.0592, 0.0780, 0.0232, 0.1802, 0.5301, 0.8186, 0.9956, 0.9764]
    green = [0.1664, 0.3599, 0.5041, 0.6419, 0.7178, 0.7492, 0.7328, 0.7862, 0.9832]
    blue  = [0.5293, 0.8684, 0.8385, 0.7914, 0.6425, 0.4662, 0.3499, 0.1968, 0.0539]

    ered = []
    egreen = []
    eblue = []
    for i, stop in enumerate(stops):
      if i is 0:
        ered.append( (stop, 0., red[i]) )
        egreen.append( (stop, 0., green[i]) )
        eblue.append( (stop, 0., blue[i]) )
      elif i is len(stops)-1:
        ered.append( (stop, red[i], 1.) )
        egreen.append( (stop, green[i], 1.) )
        eblue.append( (stop, blue[i], 1.) )
      else:
        ered.append( (stop, red[i], red[i]) )
        egreen.append( (stop, green[i], green[i]) )
        eblue.append( (stop, blue[i], blue[i]) )
      cdict = {'red': ered, 'green': egreen, 'blue': eblue}
      
      bird = mcol.LinearSegmentedColormap('bird', cdict)

      exp=values
#      xi, yi, zi = interp2(exp, 'cubic')
#      plt.contour(xi, yi, zi, [1.0], colors='k')
#      plt.contourf(xi, yi, zi, 200, cmap=bird)
#      plt.colorbar()


#      plt.title('ms_50, cubic interpolation')
#      plt.show()

#      xi, yi, zi = interp2(exp, 'linear')
#      plt.contour(xi, yi, zi, [1.0], colors='k')
#      plt.contourf(xi, yi, zi, 200, cmap=bird)
#      plt.colorbar()

#      plt.title('ms_50, linear interpolation')
#      plt.show()


      
def interp(data, method='linear'):
      x = data[:,0]
      y = data[:,1]
      z = data[:,2]
      
      xi = np.linspace(x.min(), x.max(), 1000)
      yi = np.linspace(y.min(), y.max(), 1000)
      zi = mlab.griddata(x, y, z, xi, yi, interp=method)
      
      return xi, yi, zi

def interp2(data, method='linear'):
      x = data[:,0]
      y = data[:,1]
      z = data[:,2]
      
      xi = np.linspace(x.min(), x.max(), 1000)
      yi = np.linspace(y.min(), y.max(), 1000)
      xi, yi = np.meshgrid(xi,yi)
      zi = interpolate.griddata((x, y), z, (xi, yi), method=method)

      return xi, yi, zi


def interp3(data, method='linear'):
      x = data[:,0]
      y = data[:,1]
      z = data[:,2]

      xi = np.linspace(x.min(), x.max(), 1000)
      yi = np.linspace(y.min(), y.max(), 1000)
      xi, yi = np.meshgrid(xi,yi)
      zi = interpolate.LinearNDInterpolator(x, y, z, method=method)(xi, yi)
      
      return xi, yi, zi
                                
makePlot()

 

