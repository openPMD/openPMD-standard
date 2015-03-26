#!/usr/bin/env python
#
# Copyright (c) 2015, Axel Huebl, Remi Lehe
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
    """ Print usage information for this file """
    print('This is the openPMD file check for HDF5 files.\n')
    print('Check for format version: %s\n' % formatVersion)
    print('Usage:\n  checkOpenPMD_h5.py -i <fileName> [-v] [--EDPIC]')
    sys.exit()


def parse_cmd(argv):
    """ Parse the command line arguments """
    file_name = ''
    verbose = False
    extension_pic = False
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
            extension_pic = True
        elif opt in ("-i", "--file"):
            file_name = arg
    if not os.path.isfile(file_name):
        help()
    return(file_name, verbose, extension_pic)


def open_file(fileName):
    if h5.is_hdf5(file_name):
        f = h5.File(file_name, "r")
        return(f)
    else:
        help()


def get_attr(f, name):
    """
    Try to access the path `name` in the file `f`
    Return the corresponding attribute if it is present
    """
    if name in f.attrs.keys():
        return(True, f.attrs[name])
    else:
        return(False, None)


def test_attr(f, v, request, name):
    """
    Checks whether an attribute is present.
    Returns an error if the attribute if absent and requested
    Returns a warning if the attribute if absent and recommanded

    Parameters
    ----------
    f : an h5py.File object
        The HDF5 file in which to find the attribute

    v : bool
        Verbose option

    request : string
        Either "required", "recommended" or "optional

    name : string
        The path to the attribute within the HDF5 file

    Returns
    -------
    An array with 2 elements :
    - The first element is 1 if an error occured, and 0 otherwise
    - The second element is 0 if a warning arised, and 0 otherwise
    """
    valid, value = get_attr(f, name)
    if valid:
        if v:
            print("Attribute %s (%s) exists in `%s`! Value = %s" \
            %(name, request, str(f.name), str(value)) )
        result_array = np.array([0,0])
    else:
        if request == "required":
            print("Error: Attribute %s (%s) does NOT exist in `%s`!" \
            %(name, request, str(f.name)) )
            result_array = np.array([1, 0])
        elif request == "recommended":
            print("Warning: Attribute %s (%s) does NOT exist in `%s`!" \
            %(name, request, str(f.name)) )
            result_array = np.array([0, 1])
        elif request == "optional":
            if v:
                print("Info: Attribute %s (%s) does NOT exist in `%s`!"  \
            %(name, request, str(f.name)) )
            result_array = np.array([0, 0])
        else :
            raise ValueError("Unrecognized string for `request` : %s" %request)

    return(result_array)

def check_root_attr(f, v, pic):
    """
    Scan the root of the file and make sure that the attributes are present

    Parameters
    ----------
    f : an h5py.File object
        The HDF5 file in which to find the attribute

    v : bool
        Verbose option

    pic : bool
        Whether to check for the ED-PIC extension attributes

    Returns
    -------
    An array with 2 elements :
    - The first element is the number of errors encountered
    - The second element is the number of warnings encountered
    """
    err = 0
    warn = 0

    # STANDARD.md
    #   required
    err, warn = [err, warn] + test_attr(f, v, "required", "version")
    err, warn = [err, warn] + test_attr(f, v, "required", "basePath")
    err, warn = [err, warn] + test_attr(f, v, "required", "fieldsPath")
    err, warn = [err, warn] + test_attr(f, v, "required", "particlesPath")
    err, warn = [err, warn] + test_attr(f, v, "required", "iterationEncoding")
    err, warn = [err, warn] + test_attr(f, v, "required", "iterationFormat")

    #   recommended
    err, warn = [err, warn] + test_attr(f, v, "recommended", "author")
    err, warn = [err, warn] + test_attr(f, v, "recommended", "software")
    err, warn = [err, warn] + test_attr(f, v, "recommended", "softwareVersion")
    err, warn = [err, warn] + test_attr(f, v, "recommended", "date")

    #   optional
    err, warn = [err, warn] + test_attr(f, v, "optional", "comment")

    # Extension: ED-PIC
    #   no addition requirements for "/" defined
    return np.array([err, warn])

def check_fields(f, v, pic):
    """
    Scan all the fields in the file and checks the attributes are present

    Parameters
    ----------
    f : an h5py.File object
        The HDF5 file in which to find the attribute

    v : bool
        Verbose option

    pic : bool
        Whether to check for the ED-PIC extension attributes

    Returns
    -------
    An array with 2 elements :
    - The first element is the number of errors encountered
    - The second element is the number of warnings encountered
    """
    # Initialize the result array
    # First element : number of errors
    # Second element : number of warnings
    result_array = np.array([ 0, 0])

    # Find all the fields
    valid, base_path = get_attr(f, "basePath")
    valid, fields_path = get_attr(f, "fieldsPath")
    if os.path.join( base_path, fields_path) != ( base_path + fields_path ):
        print("Error: `basePath`+`fieldsPath` seems to be malformed "
              "(is `basePath` absolute and ends on a `/` ?)")
        return( np.array([1, 0]) )
    else:
        full_fields_path = base_path + fields_path
        # Find all the fields (avoid simple attributes)
        list_fields = f[full_fields_path].keys()
    if v:
        print("Found %d fields" % len(f[full_fields_path].keys()))

    # Check for the attributes of the STANDARD.md
    for field_name in list_fields :
        field = f[full_fields_path + field_name]

        # General attributes of the record
        result_array += test_attr(field, v, "required", "unitSI")
        result_array += test_attr(field, v, "required", "unitDimension")
        result_array += test_attr(field, v, "required", "geometry")
        result_array += test_attr(field, v, "optional", "geometryParameters")
        result_array += test_attr(field, v, "required", "gridSpacing")
        result_array += test_attr(field, v, "required", "gridGlobalOffset")
        result_array += test_attr(field, v, "required", "gridUnitSI")
        result_array += test_attr(field, v, "required", "dataOrder")

        # Attributes of data set
        if type(field) is h5.Dataset :   # If the record is a scalar field
            result_array += test_attr(field, v, "required", "position")
        else:                            # If the record is a vector field
            # Loop over the components
            for component_name in field:
                component = field[component_name]
                result_array += test_attr(component, v, "required", "position")

    # Check for the attributes of the PIC extension, if asked to do so by the user
    if pic:

        # Check the attributes associated with the field solver
        result_array += test_attr( f[full_fields_path], v, "required",
                                    "fieldSolver" )
        valid, field_solver = get_attr(field, "fieldSolver")
        if (valid == True) and (field_solver != "none") :
            result_array += test_attr( f[full_fields_path], v, "required",
                                       "fieldSolverOrder")
            result_array += test_attr( f[full_fields_path], v, "required",
                                       "fieldSolverParameters")

        # Check the attributes associated with the current smoothing
        result_array += test_attr( f[full_fields_path], v, "required",
                                   "currentSmoothing")
        valid, current_smoothing = get_attr(field, "currentSmoothing")
        if (valid == True) and (current_smoothing != "none") :
            result_array += test_attr(f[full_fields_path], v, "required",
                                      "currentSmoothingParameters")

        # Check the attributes associated with the charge conservation
        result_array += test_attr(f[full_fields_path], v, "required",
                                  "chargeCorrection")
        valid, charge_correction = get_attr(field, "chargeCorrection")
        if valid == True and charge_correction != "none":
            result_array += test_attr(f[full_fields_path], v, "required",
                                      "chargeCorrectionParameters")

        # Check for the attributes of each record
        for field_name in list_fields :
            field = f[full_fields_path + field_name]
            result_array + test_attr(field, v, "required", "fieldSmoothing")
            valid, field_smoothing = get_attr(field, "fieldSmoothing")
            if field_smoothing != "none":
                result_array += test_attr(field,v, "required",
                                          "fieldSmoothingParameters")
    return(result_array)


if __name__ == "__main__":
    file_name, verbose, extension_pic = parse_cmd(sys.argv[1:])
    f = open_file(file_name)

    # root attributes at "/"
    result_array = np.array([0, 0])
    result_array += check_root_attr(f, verbose, extension_pic)

    # field checks
    if result_array[0] == 0:
        result_array += check_fields(f, verbose, extension_pic)

    # particle checks

    # results
    print("Result: %d Errors and %d Warnings."
          %( result_array[0], result_array[1]))
