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
import sys, getopt, os.path


def help():
   print('checkOpenPMD_h5.py -i <fileName> [-v]')
   sys.exit()


def parseCmd(argv):
   fileName = ''
   verbose = False
   try:
      opts, args = getopt.getopt(argv,"hvi:",["file="])
   except getopt.GetoptError:
      print('test.py -i <fileName>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         help()
      elif opt in ("-v", "--verbose"):
         verbose = True
      elif opt in ("-i", "--file"):
         fileName = arg
   if not os.path.isfile(fileName):
      help()
   return(fileName, verbose)


def openFile(fileName):
   if h5.is_hdf5(fileName):
      f = h5.File(fileName, "r")
      return(f)
   else:
      help()


def getAttr(f, name):
   if name in f.attrs.keys():
       return(True, f.attrs[name])
   else:
       return(False, None)


def testAttr(f, v, request, name):
   """ todo: add format and type checks! """
   valid, value = getAttr(f, name)
   if valid:
     if v:
        print("Attibute " + name + " (" + request + ") exists! Value = " + str(value))
     return(np.array([0, 0]))
   else:
     if request == "required":
         print("Error: Attibute " + name + " (" + request + ") does NOT exist!")
         return(np.array([1, 0]))
     if request == "recommended":
         print("Warning: Attibute " + name + " (" + request + ") does NOT exist!")
         return(np.array([0, 1]))
     if request == "optional":
         if v:
            print("Info: Attibute " + name + " (" + request + ") does NOT exist!")
         return(np.array([0, 0]))


def testRootAttr(f, v):
   """ todo: add format and type checks! """
   err = 0
   warn = 0
   # required
   err, warn = [err, warn] + testAttr(f, v, "required", "version")
   err, warn = [err, warn] + testAttr(f, v, "required", "basePath")
   err, warn = [err, warn] + testAttr(f, v, "required", "fieldsPath")
   err, warn = [err, warn] + testAttr(f, v, "required", "particlesPath")

   err, warn = [err, warn] + testAttr(f, v, "required", "iterationEncoding")
   err, warn = [err, warn] + testAttr(f, v, "required", "iterationFormat")
   err, warn = [err, warn] + testAttr(f, v, "required", "time")
   err, warn = [err, warn] + testAttr(f, v, "required", "timeStep")
   err, warn = [err, warn] + testAttr(f, v, "required", "timeUnitSI")

   # recommended
   err, warn = [err, warn] + testAttr(f, v, "recommended", "author")
   err, warn = [err, warn] + testAttr(f, v, "recommended", "software")
   err, warn = [err, warn] + testAttr(f, v, "recommended", "softwareVersion")
   err, warn = [err, warn] + testAttr(f, v, "recommended", "date")

   # optional
   err, warn = [err, warn] + testAttr(f, v, "optional", "comment")

   return np.array([err, warn])


if __name__ == "__main__":
   fileName, verbose = parseCmd(sys.argv[1:])
   f = openFile(fileName)

   # root attributes at "/"
   err, warn = np.array([0, 0])
   err, warn = [err, warn] + testRootAttr(f, verbose)

   # field checks

   # particle checks

   # results
   print("Result: " + str(err) + " Errors and " + str(warn) + " Warnings.")
