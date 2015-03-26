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

formatVersion="1.0.0"


def help():
    print('This is the openPMD file check for HDF5 files.\n')
    print('Check for format version: %s\n' % formatVersion)
    print('Usage:\n  checkOpenPMD_h5.py -i <fileName> [-v] [--EDPIC]')
    sys.exit()


def parseCmd(argv):
    fileName = ''
    verbose = False
    extensionPIC = False
    try:
        opts, args = getopt.getopt(argv,"hvi:e",["file=","EDPIC"])
    except getopt.GetoptError:
        print('test.py -i <fileName>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            help()
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("--EDPIC"):
            extensionPIC = True
        elif opt in ("-i", "--file"):
            fileName = arg
    if not os.path.isfile(fileName):
        help()
    return(fileName, verbose, extensionPIC)


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
            print("Attibute " + name + " (" + request + ") exists in `" + \
                  str(f.name) + "`! Value = " + str(value))
        return(np.array([0, 0]))
    else:
        if request == "required":
            print("Error: Attibute " + name + " (" + request + ") does NOT exist in `" + \
                  str(f.name) + "`!")
            return(np.array([1, 0]))
        if request == "recommended":
            print("Warning: Attibute " + name + " (" + request + ") does NOT exist in `" + \
                  str(f.name) + "`!")
            return(np.array([0, 1]))
        if request == "optional":
            if v:
                print("Info: Attibute " + name + " (" + request + ") does NOT exist in `" + \
                      str(f.name) + "`!")
            return(np.array([0, 0]))


def checkRootAttr(f, v, pic):
    """ todo: add format and type checks! """
    err = 0
    warn = 0
    # STANDARD.md
    #   required
    err, warn = [err, warn] + testAttr(f, v, "required", "version")
    err, warn = [err, warn] + testAttr(f, v, "required", "basePath")
    err, warn = [err, warn] + testAttr(f, v, "required", "fieldsPath")
    err, warn = [err, warn] + testAttr(f, v, "required", "particlesPath")

    err, warn = [err, warn] + testAttr(f, v, "required", "iterationEncoding")
    err, warn = [err, warn] + testAttr(f, v, "required", "iterationFormat")

    #   recommended
    err, warn = [err, warn] + testAttr(f, v, "recommended", "author")
    err, warn = [err, warn] + testAttr(f, v, "recommended", "software")
    err, warn = [err, warn] + testAttr(f, v, "recommended", "softwareVersion")
    err, warn = [err, warn] + testAttr(f, v, "recommended", "date")

    #   optional
    err, warn = [err, warn] + testAttr(f, v, "optional", "comment")

    # Extension: ED-PIC
    #   no addition requirements for "/" defined

    return np.array([err, warn])


def checkFields(f, v, pic):
    """ Check if fields are stored in the right place and follow the standard
    """
    err = 0
    warn = 0
    # find fields
    valid, basePath = getAttr(f, "basePath")
    valid, fieldsPath = getAttr(f, "fieldsPath")
    if os.path.join( basePath, fieldsPath) != ( basePath + fieldsPath ):
        print("Error: `basePath`+`fieldsPath` seems to be malformed "
              "(is `basePath` absolute and ends on a `/` ?)")
        np.array([1, 0])
    else:
        fullFieldsPath = basePath + fieldsPath

    if v:
        print("Found %d fields" % len(f[fullFieldsPath].keys()))

    # check for required attributes of the STANDARD.md
    for fieldName in f[fullFieldsPath].keys():
        field = f[fullFieldsPath + fieldName]
        # general attributes
        err, warn = [err, warn] + testAttr(field, v, "required", "unitSI")
        err, warn = [err, warn] + testAttr(field, v, "required", "unitDimension")
        err, warn = [err, warn] + testAttr(field, v, "required", "geometry")
        err, warn = [err, warn] + testAttr(field, v, "optional", "geometryParameters")
        err, warn = [err, warn] + testAttr(field, v, "required", "gridSpacing")
        err, warn = [err, warn] + testAttr(field, v, "required", "gridGlobalOffset")
        err, warn = [err, warn] + testAttr(field, v, "required", "gridUnitSI")
        err, warn = [err, warn] + testAttr(field, v, "required", "dataOrder")

        # data set attributes
        isScalar = type(field) is h5.Dataset
        if isScalar:
            err, warn = [err, warn] + testAttr(field, v, "required", "position")
        else:
            for componentName in field:
                component = field[componentName]
                err, warn = [err, warn] + testAttr(component, v, "required", "position")

    if not pic:
        return np.array([err, warn])

    # check for attributes of the ED-PIC extension
    #   for the fieldsPath
    err, warn = [err, warn] + testAttr(f[fullFieldsPath], v, "required", "fieldSolver")
    if err == 0:
        valid, fieldSolver = getAttr(field, "fieldSolver")
        if fieldSolver != "none":
            err, warn = [err, warn] + testAttr(f[fullFieldsPath], v, "required", "fieldSolverOrder")
            err, warn = [err, warn] + testAttr(f[fullFieldsPath], v, "required", "fieldSolverParameters")
    err, warn = [err, warn] + testAttr(f[fullFieldsPath], v, "required", "currentSmoothing")
    if err == 0:
        valid, currentSmoothing = getAttr(field, "currentSmoothing")
        if currentSmoothing != "none":
            err, warn = [err, warn] + testAttr(f[fullFieldsPath], v, "required", "currentSmoothingParameters")
    err, warn = [err, warn] + testAttr(f[fullFieldsPath], v, "required", "chargeCorrection")
    if err == 0:
        valid, chargeCorrection = getAttr(field, "chargeCorrection")
        if currentSmoothing != "none":
            err, warn = [err, warn] + testAttr(f[fullFieldsPath], v, "required", "chargeCorrectionParameters")

    #   for each `fieldName`
    for fieldName in f[fullFieldsPath].keys():
        field = f[fullFieldsPath + fieldName]
        # general attributes
        err, warn = [err, warn] + testAttr(field, v, "required", "fieldSmoothing")
        if err == 0:
            valid, fieldSmoothing = getAttr(field, "fieldSmoothing")
            if fieldSmoothing != "none":
                err, warn = [err, warn] + \
                            testAttr(field, v, "required", "fieldSmoothingParameters")

    return np.array([err, warn])


if __name__ == "__main__":
    fileName, verbose, extensionPIC = parseCmd(sys.argv[1:])
    f = openFile(fileName)

    # root attributes at "/"
    err, warn = np.array([0, 0])
    err, warn = [err, warn] + checkRootAttr(f, verbose, extensionPIC)

    # field checks
    if err == 0:
        err, warn = [err, warn] + checkFields(f, verbose, extensionPIC)

    # particle checks

    # results
    print("Result: " + str(err) + " Errors and " + str(warn) + " Warnings.")
