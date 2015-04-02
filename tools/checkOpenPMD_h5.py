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
import string
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

def test_key(f, v, request, name):
    """
    Checks whether a key is present.
    Returns an error if the key if absent and requested
    Returns a warning if the key if absent and recommanded

    Parameters
    ----------
    f : an h5py.File, h5py.Group or h5py.DataSet object
        The object in which to find the key
        
    v : bool
        Verbose option

    request : string
        Either "required", "recommended" or "optional

    name : string
        The name of the key within this File, Group or DataSet
    
    Returns
    -------
    An array with 2 elements :
    - The first element is 1 if an error occured, and 0 otherwise
    - The second element is 0 if a warning arised, and 0 otherwise
    """
    valid = (name in f.keys())
    if valid:
        if v:
            print("Key %s (%s) exists in `%s`!" %(name, request, str(f.name) ) )
        result_array = np.array([0,0])
    else:
        if request == "required":
            print("Error: Key %s (%s) does NOT exist in `%s`!" \
            %(name, request, str(f.name)) )
            result_array = np.array([1, 0])
        elif request == "recommended":
            print("Warning: Key %s (%s) does NOT exist in `%s`!" \
            %(name, request, str(f.name)) )
            result_array = np.array([0, 1])
        elif request == "optional":
            if v:
                print("Info: Key %s (%s) does NOT exist in `%s`!"  \
            %(name, request, str(f.name)) )
            result_array = np.array([0, 0])
        else :
            raise ValueError("Unrecognized string for `request` : %s" %request)

    return(result_array)
        
def test_attr(f, v, request, name):
    """
    Checks whether an attribute is present.
    Returns an error if the attribute if absent and requested
    Returns a warning if the attribute if absent and recommanded

    Parameters
    ----------
    f : an h5py.File, h5py.Group or h5py.DataSet object
        The object in which to find the key
        
    v : bool
        Verbose option

    request : string
        Either "required", "recommended" or "optional

    name : string
        The name of the attribute within this File, Group or DataSet
    
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
    Scan the root of the file and make sure that all the attributes are present

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
    result_array = np.array([0,0])
    
    # STANDARD.md
    #   required
    result_array += test_attr(f, v, "required", "version")
    result_array += test_attr(f, v, "required", "basePath")
    result_array += test_attr(f, v, "required", "meshesPath")
    result_array += test_attr(f, v, "required", "particlesPath")
    result_array += test_attr(f, v, "required", "iterationEncoding")
    result_array += test_attr(f, v, "required", "iterationFormat")

    #   recommended
    result_array += test_attr(f, v, "recommended", "author")
    result_array += test_attr(f, v, "recommended", "software")
    result_array += test_attr(f, v, "recommended", "softwareVersion")
    result_array += test_attr(f, v, "recommended", "date")

    #   optional
    result_array += test_attr(f, v, "optional", "comment")

    # Extension: ED-PIC
    #   no addition requirements for "/" defined
    return(result_array)


def check_iterations(f, v, pic) :
    """
    Scan all the iterations present in the file, checking both
    the meshes and the particles

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

    # Find all the iterations
    format_error = False
    try :
        list_iterations = f['/data/'].keys()
    except KeyError, TypeError :
        format_error = True
    else :
        # Check that these iterations are indeed encoded as integers
        for iteration in list_iterations :
            for character in iteration : # go through the string
                if not (character in string.digits) :
                    format_error = True                    
    # Detect any error and interrupt execution if one is found
    if format_error == True :
        print("Error : it seems that the path of the data within the HDF5 file"
              "is not of the form '/data/%T/', where %T corresponds to an "
              "actual integer.")
        return(np.array([1, 0]))
    else :
        print("Found %d iteration(s)" % len(list_iterations) )

    # Initialize the result array
    # First element : number of errors
    # Second element : number of warnings
    result_array = np.array([ 0, 0]) 
        
    # Loop over the iterations and check the meshes and the particles 
    for iteration in list_iterations :
        result_array += check_meshes(f, iteration, v, pic)
        result_array += check_particles(f, iteration, v, pic)

    return(result_array)
    
def check_meshes(f, iteration, v, pic):
    """
    Scan all the meshes corresponding to one iteration

    Parameters
    ----------
    f : an h5py.File object
        The HDF5 file in which to find the attribute

    iteration : string representing an integer
        The iteration at which to scan the meshes
        
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

    # Find the path to the data
    base_path = "/data/%s/" % iteration
    valid, meshes_path = get_attr(f, "meshesPath")
    if os.path.join( base_path, meshes_path) != ( base_path + meshes_path ):
        print("Error: `basePath`+`meshesPath` seems to be malformed "
            "(is `basePath` absolute and ends on a `/` ?)")
        return( np.array([1, 0]) )
    else:
        full_meshes_path = base_path + meshes_path
        # Find all the meshes
        list_meshes = f[full_meshes_path].keys()
    print( "Iteration %s : found %d meshes"
        %( iteration, len(list_meshes) ) )

    # Check for the attributes of the STANDARD.md
    for field_name in list_meshes :
        field = f[full_meshes_path + field_name]
        
        # General attributes of the record
        result_array += test_attr(field, v, "required", "unitSI")
        result_array += test_attr(field, v, "required", "unitDimension")
        result_array += test_attr(field, v, "required", "geometry")
        result_array += test_attr(field, v, "optional",
                                      "geometryParameters")
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
                result_array += test_attr(component, v, "required",
                                              "position")

    # Check for the attributes of the PIC extension,
    # if asked to do so by the user 
    if pic:
        
        # Check the attributes associated with the field solver
        result_array += test_attr( f[full_meshes_path], v, "required",
                    "fieldSolver" )
        valid, field_solver = get_attr(field, "fieldSolver")
        if (valid == True) and (field_solver != "none") :
            result_array += test_attr( f[full_meshes_path], v, "required",
                    "fieldSolverOrder")
            result_array += test_attr( f[full_meshes_path], v, "required",
                    "fieldSolverParameters")
            
        # Check the attributes associated with the current smoothing
        result_array += test_attr( f[full_meshes_path], v, "required",
                                    "currentSmoothing")
        valid, current_smoothing = get_attr(field, "currentSmoothing")
        if (valid == True) and (current_smoothing != "none") :
            result_array += test_attr(f[full_meshes_path], v, "required",
                                        "currentSmoothingParameters")
    
        # Check the attributes associated with the charge conservation
        result_array += test_attr(f[full_meshes_path], v, "required",
                                    "chargeCorrection")
        valid, charge_correction = get_attr(field, "chargeCorrection")
        if valid == True and charge_correction != "none":
            result_array += test_attr(f[full_meshes_path], v, "required",
                                      "chargeCorrectionParameters")
		
        # Check for the attributes of each record
        for field_name in list_meshes :
            field = f[full_meshes_path + field_name]
            result_array + test_attr(field, v, "required", "fieldSmoothing")
            valid, field_smoothing = get_attr(field, "fieldSmoothing")
            if field_smoothing != "none":
                result_array += test_attr(field,v, "required",
                                            "fieldSmoothingParameters")
    return(result_array)


def check_particles(f, iteration, v, pic) :
    """
    Scan all the particle data corresponding to one iteration

    Parameters
    ----------
    f : an h5py.File object
        The HDF5 file in which to find the attribute

    iteration : string representing an integer
        The iteration at which to scan the particle data
        
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

    # Find the path to the data
    base_path = "/data/%s/" % iteration
    valid, particles_path = get_attr(f, "particlesPath")
    if os.path.join( base_path, particles_path) !=  \
        ( base_path + particles_path ) :
        print("Error: `basePath`+`meshesPath` seems to be malformed "
            "(is `basePath` absolute and ends on a `/` ?)")
        return( np.array([1, 0]) )
    else:
        full_particle_path = base_path + particles_path
        # Find all the particle species
        list_species = f[full_particle_path].keys()
    print( "Iteration %s : found %d particle species"
        %( iteration, len(list_species) ) )

    # Go through all the particle species
    for species_name in list_species :
        species = f[full_particle_path + species_name]
        
        # Check that the position and momenta of the particles are present
        result_array += test_key( species, v, "required", "position" )
        result_array += test_key( species, v, "required", "momentum" )

        # Check the records required by the PIC extension
        if pic :
            result_array += test_key( species, v, "required", "charge" )
            result_array += test_key( species, v, "required", "mass" )
            result_array += test_key( species, v, "required", "weighting" )
            result_array += test_key( species, v, "recommended", "longName" )
            result_array += test_key( species, v, "recommended",
                                      "globalCellId" )
            result_array += test_key( species, v, "optional", "particlePatches" )
            result_array += test_key( species, v, "optional", "boundElectrons" )
            result_array += test_key( species, v, "optional", "protonNumber" )
            result_array += test_key( species, v, "optional", "neutronNumber" )

        # Check the attributes associated with the PIC extension
        if pic :
            result_array += test_attr(species, v, "required",
                                      "particleShape")
            result_array += test_attr(species, v, "required",
                                      "currentDeposition")
            result_array += test_attr(species, v, "required",
                                      "particlePush")
            result_array += test_attr(species, v, "required",
                                      "particleInterpolation")
            result_array += test_attr(species, v, "required",
                                      "particleSmoothing")
            valid, particle_smoothing = get_attr(species, "particleSmoothing")
            if valid == True and particle_smoothing != "none":            
                result_array += test_attr(species, v, "required",
                                    "particleSmoothingParameters")

        # Check each record of the particle
        for record in species.keys() :
            if record != "particlePatches" :
                result_array += test_attr(species[record], v,
                                          "required", "unitSI")
                result_array += test_attr(species[record], v,
                                          "required", "unitDimension")
 
            
    return(result_array)

    
if __name__ == "__main__":
    file_name, verbose, extension_pic = parse_cmd(sys.argv[1:])
    f = open_file(file_name)

    # root attributes at "/"
    result_array = np.array([0, 0])
    result_array += check_root_attr(f, verbose, extension_pic)

    # Go through all the iterations, checking both the particles
    # and the meshes
    result_array += check_iterations(f, verbose, extension_pic)

    # results
    print("Result: %d Errors and %d Warnings."
          %( result_array[0], result_array[1]))
