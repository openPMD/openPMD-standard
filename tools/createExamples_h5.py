#!/usr/bin/env python
#
# Copyright (c) 2015, Axel Huebl
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

import h5py as h5
import numpy as np
import sys
import datetime
from dateutil.tz import tzlocal


def openFile(fileName):
   f = h5.File(fileName, "w")
   return f


def writeRootAttr(f):
   # required
   f.attrs["version"] = "1.0.0"
   f.attrs["basePath"] = "/data/%T/"
   f.attrs["fieldsPath"] = "fields/"
   f.attrs["particlesPath"] = "particles/"

   f.attrs["iterationEncoding"] = "fileBased"
   f.attrs["iterationFormat"] = f.attrs["basePath"]
   f.attrs["time"] = 0.0
   f.attrs["timeStep"] = 0.0
   f.attrs["timeUnitSI"] = 1.0e-9 # 1ns

   # recommended
   f.attrs["author"] = "Axel Huebl <a.huebl@hzdr.de>"
   f.attrs["software"] = "OpenPMD Example Script"
   #f.attrs["softwareVersion"] = "1.0.0"
   f.attrs["date"] = datetime.datetime.now(tzlocal()).strftime('%Y-%m-%d %H:%M:%S %z')

   # optional
   f.attrs["comment"] = "This is a dummy file for test purposes."


def addEDPICAttrFields(f, fieldName):
   f[fieldName].attrs["fieldSolver"] = "Yee"
   f[fieldName].attrs["fieldSolverOrder"] = 2.0
   #f[fieldName].attrs["fieldSolverParameters"] = ""
   f[fieldName].attrs["fieldSmoothing"] = "none"
   #f[fieldName].attrs["fieldSmoothingParameters"] = "period=10;numPasses=4;compensator=true"
   f[fieldName].attrs["currentSmoothing"] = "none"
   #f[fieldName].attrs["currentSmoothingParameters"] = "period=1;numPasses=2;compensator=false"
   f[fieldName].attrs["chargeCorrection"] = "none"
   #f[fieldName].attrs["chargeCorrectionParameters"] = "period=100"

   return

def writeFields(f):
   fullFieldsPath = f.attrs["basePath"] + f.attrs["fieldsPath"]

   # scalar field
   f.create_dataset(fullFieldsPath + "rho", (32,64), dtype='f4')
   f[fullFieldsPath + "rho"].attrs["unitSI"] = 1.0
   f[fullFieldsPath + "rho"].attrs["unitDimension"] = \
      np.array([-3.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0 ])
      #           L    M    T    J  theta  N    J
      # C / m^3 = A * s / m^3
      #  -> M^-3 * T * J
   f[fullFieldsPath + "rho"].attrs["geometry"] = "cartesian"
   f[fullFieldsPath + "rho"].attrs["gridSpacing"] = np.array([1.0, 1.0])
   f[fullFieldsPath + "rho"].attrs["gridGlobalOffset"] = np.array([0.0, 0.0])
   f[fullFieldsPath + "rho"].attrs["gridUnitSI"] = 1.0
   f[fullFieldsPath + "rho"].attrs["dataOrder"] = "C"
   f[fullFieldsPath + "rho"].attrs["position"] = np.array([0.0, 0.0])
   addEDPICAttrFields(f, fullFieldsPath + "rho")

   # vector field
   f.create_dataset(fullFieldsPath + "E/x", (32,64), dtype='f4')
   f.create_dataset(fullFieldsPath + "E/y", (32,64), dtype='f4')
   f.create_dataset(fullFieldsPath + "E/z", (32,64), dtype='f4')
   f[fullFieldsPath + "E"].attrs["unitSI"] = 1.0
   f[fullFieldsPath + "E"].attrs["unitDimension"] = \
      np.array([1.0, 1.0, -3.0, -1.0, 0.0, 0.0, 0.0 ])
      #          L    M     T     J  theta  N    J
      # V / m = kg * m / (A * s^3)
      #      -> L * M * T^-3 * J^-1
   f[fullFieldsPath + "E"].attrs["geometry"] = "cartesian"
   f[fullFieldsPath + "E"].attrs["gridSpacing"] = np.array([1.0, 1.0])
   f[fullFieldsPath + "E"].attrs["gridGlobalOffset"] = np.array([0.0, 0.0])
   f[fullFieldsPath + "E"].attrs["gridUnitSI"] = 1.0
   f[fullFieldsPath + "E"].attrs["dataOrder"] = "C"
   f[fullFieldsPath + "E/x"].attrs["position"] = np.array([0.0, 0.5])
   f[fullFieldsPath + "E/y"].attrs["position"] = np.array([0.5, 0.0])
   f[fullFieldsPath + "E/z"].attrs["position"] = np.array([0.0, 0.0])
   addEDPICAttrFields(f, fullFieldsPath + "E")

   return


def addEDPICAttrParticles(f, particleName):
   f[particleName].attrs["particleShape"] = 3.0
   f[particleName].attrs["currentDeposition"] = "Esirkepov"
   #f[particleName].attrs["currentDepositionParameters"] = ""
   f[particleName].attrs["particlePush"] = "Boris"
   f[particleName].attrs["particleInterpolation"] = "Trilinear"
   f[particleName].attrs["particleSmoothing"] = "none"
   #f[particleName].attrs["particleSmoothingParameters"] = "period=1;numPasses=2;compensator=false"

   return

def writeParticles(f):
   fullParticlesPath = f.attrs["basePath"] + f.attrs["particlesPath"]

   # constant scalar particle attributes (that could also be variable data sets)
   f.create_group(fullParticlesPath + "electrons/charge")
   f[fullParticlesPath + "electrons/charge"].attrs["value"] = -1.0;
   f[fullParticlesPath + "electrons/charge"].attrs["unitSI"] = 1.60217657e-19;
   f[fullParticlesPath + "electrons/charge"].attrs["unitDimension"] = \
      np.array([0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0 ])
      #          L    M    T    J  theta  N    J
      # C = A * s
   f.create_group(fullParticlesPath + "electrons/mass")
   f[fullParticlesPath + "electrons/mass"].attrs["value"] = 1.0;
   f[fullParticlesPath + "electrons/mass"].attrs["unitSI"] = 9.10938291e-31;
   f[fullParticlesPath + "electrons/mass"].attrs["unitDimension"] = \
      np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0 ])
      #          L    M    T    J  theta  N    J

   f[fullParticlesPath + "electrons"].attrs["longName"] = "My first electron species"
   addEDPICAttrParticles(f, fullParticlesPath + "electrons")

   # scalar particle attribute (non-const/individual per particle)
   f.create_dataset(fullParticlesPath + "electrons/weighting", (128,), dtype='f4')
   f[fullParticlesPath + "electrons/weighting"].attrs["unitSI"] = 1.0;
   f[fullParticlesPath + "electrons/weighting"].attrs["unitDimension"] = \
      np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]) # plain floating point number

   # vector particle attribute (non-const/individual per particle)
   f.create_dataset(fullParticlesPath + "electrons/position/x", (128,), dtype='f4')
   f.create_dataset(fullParticlesPath + "electrons/position/y", (128,), dtype='f4')
   f.create_dataset(fullParticlesPath + "electrons/position/z", (128,), dtype='f4')
   f[fullParticlesPath + "electrons/position"].attrs["unitSI"] = 1.e-9;
   f[fullParticlesPath + "electrons/position"].attrs["unitDimension"] = \
      np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ])
      #          L    M     T    J  theta  N    J
      # Dimension of Length per component

   f.create_dataset(fullParticlesPath + "electrons/momentum/x", (128,), dtype='f4')
   f.create_dataset(fullParticlesPath + "electrons/momentum/y", (128,), dtype='f4')
   f.create_dataset(fullParticlesPath + "electrons/momentum/z", (128,), dtype='f4')
   f[fullParticlesPath + "electrons/momentum"].attrs["unitSI"] = 1.60217657e-19;
   f[fullParticlesPath + "electrons/momentum"].attrs["unitDimension"] = \
      np.array([1.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0 ])
      #          L    M     T    J  theta  N    J
      # Dimension of Length * Mass / Time

   return


if __name__ == "__main__":
   f = openFile("example.h5")
   writeRootAttr(f)
   writeFields(f)
   writeParticles(f)
   f.close()
   print "file example.h5 created!"
