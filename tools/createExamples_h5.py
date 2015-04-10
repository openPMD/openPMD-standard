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
import sys
import datetime
from dateutil.tz import tzlocal

def get_basePath(f, iteration):
    """
    Get the basePath for a certain iteration

    Parameter
    ---------
    f : an h5py.File object
        The file in which to write the data
    iteration : an iteration number

    Returns
    -------
    A string with a in-file path.
    """
    return f.attrs["basePath"].replace("%T", str(iteration))


def setup_root_attr(f):
    """
    Write the root metadata for this file

    Parameter
    ---------
    f : an h5py.File object
        The file in which to write the data
    """

    # Required attributes
    f.attrs["openPMD"] = "1.0.0"
    f.attrs["basePath"] = "/data/%T/"
    f.attrs["meshesPath"] = "meshes/"
    f.attrs["particlesPath"] = "particles/"
    f.attrs["iterationEncoding"] = "fileBased"
    f.attrs["iterationFormat"] = "/data/%T/"

    # Recommended attributes
    f.attrs["author"] = "Axel Huebl <a.huebl@hzdr.de>"
    f.attrs["software"] = "OpenPMD Example Script"
    f.attrs["softwareVersion"] = "1.0.0"
    f.attrs["date"] = datetime.datetime.now(tzlocal()).strftime('%Y-%m-%d %H:%M:%S %z')

    # Optional
    f.attrs["comment"] = "This is a dummy file for test purposes."


def write_rho_cylindrical(meshes, mode0, mode1):
    """
    Write the metadata and the data associated with the scalar field rho,
    using the cylindrical representation (with azimuthal decomposition going up to m=1)

    Parameters
    ----------
    meshes : an h5py.Group object
             Group of the meshes in basePath + meshesPath

    mode0 : a 2darray of reals
        The values of rho in the azimuthal mode 0, on the r-z grid
        (The first axis corresponds to r, and the second axis corresponds to z)

    mode1 : a 2darray of complexs
        The values of rho in the azimuthal mode 1, on the r-z grid
        (The first axis corresponds to r, and the second axis corresponds to z)
    """
    # Path to the rho meshes, within the h5py file
    full_rho_path = "rho"
    meshes.create_dataset( full_rho_path, (3, mode0.shape[0], mode0.shape[1]), \
                           dtype='f4')
    rho = meshes[full_rho_path]
    rho.attrs["comment"] = "Density of electrons in azimuthal decomposition"

    # Create the dataset (cylindrical representation with azimuthal modes up to m=1)
    # The first axis has size 2m+1
    rho.attrs["geometry"] = "cylindrical"
    rho.attrs["geometryParameters"] = "m=1; imag=+"

    # Add information on the units of the data
    rho.attrs["unitSI"] = np.float64(1.0)
    rho.attrs["unitDimension"] = \
       np.array([-3.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0 ], dtype="float64")
       #           L    M    T    J  theta  N    J
       # rho is in Coulomb per meter cube : C / m^3 = A * s / m^3 -> M^-3 * T * J

    # Add time information
    rho.attrs["time"] = 0.  # Time is expressed in nanoseconds here
    rho.attrs["timeUnitSI"] = np.float64(1.e-9)  # Conversion from nanoseconds to seconds

    # Add information on the r-z grid
    rho.attrs["gridSpacing"] = np.array([1.0, 1.0], dtype="float32")  # dr, dz
    rho.attrs["gridGlobalOffset"] = np.array([0.0, 0.0], dtype="float32") # rmin, zmin
    rho.attrs["position"] = np.array([0.0, 0.0], dtype="float32")
    rho.attrs["gridUnitSI"] = np.float64(1.0)
    rho.attrs["dataOrder"] = "C"

    # Add specific information for PIC simulations
    add_EDPIC_attr_meshes(rho)

    # Fill the array with the field data
    if mode0.shape != mode1.shape :
        raise ValueError("`mode0` and `mode1` should have the same shape")
    rho[0,:,:] = mode0[:,:] # Store the mode 0 first
    rho[1,:,:] = mode1[:,:].real # Then store the real part of mode 1
    rho[2,:,:] = mode1[:,:].imag # Then store the imaginary part of mode 1


def write_e_2d_cartesian(meshes, data_ex, data_ey, data_ez ):
    """
    Write the metadata and the data associated with the vector field E,
    using a 2d Cartesian representation

    Parameters
    ----------
    meshes : an h5py.Group object
             Group of the meshes in basePath + meshesPath

    data_ex, data_ey, data_ez : 2darray of reals
        The values of the components ex, ey, ez on the 2d x-y grid
        (The first axis corresponds to x, and the second axis corresponds to y)
    """
    # Path to the E field, within the h5py file
    full_e_path_name = "E"
    meshes.create_group(full_e_path_name)
    E = meshes[full_e_path_name]

    # Create the dataset (2d cartesian grid)
    E.attrs["componentOrder"] = "x;y;z"
    E.create_dataset("x", data_ex.shape, dtype='f4')
    E.create_dataset("y", data_ey.shape, dtype='f4')
    E.create_dataset("z", data_ez.shape, dtype='f4')

    # Write the common metadata for the group
    E.attrs["geometry"] = "cartesian"
    E.attrs["gridSpacing"] = np.array([1.0, 1.0], dtype="float32")       # dx, dy
    E.attrs["gridGlobalOffset"] = np.array([0.0, 0.0], dtype="float32")  # xmin, ymin
    E.attrs["gridUnitSI"] = np.float64(1.0)
    E.attrs["dataOrder"] = "C"
    E.attrs["unitSI"] = np.float64(1.0e9) # convert normalized simulation units to SI
    E.attrs["unitDimension"] = \
       np.array([1.0, 1.0, -3.0, -1.0, 0.0, 0.0, 0.0 ], dtype="float64")
       #          L    M     T     J  theta  N    J
       # E is in volts per meters : V / m = kg * m / (A * s^3) -> L * M * T^-3 * J^-1

    # Add specific information for PIC simulations at the group level
    add_EDPIC_attr_meshes(E)

    # Add time information
    E.attrs["time"] = 0.  # Time is expressed in nanoseconds here
    E.attrs["timeUnitSI"] = np.float64(1.e-9)  # Conversion from nanoseconds to seconds

    # Write attribute that is specific to each dataset: staggered position within a cell
    E["x"].attrs["position"] = np.array([0.0, 0.5], dtype="float32")
    E["y"].attrs["position"] = np.array([0.5, 0.0], dtype="float32")
    E["z"].attrs["position"] = np.array([0.0, 0.0], dtype="float32")

    # Fill the array with the field data
    E["x"][:,:] =  data_ex[:,:]
    E["y"][:,:] =  data_ey[:,:]
    E["z"][:,:] =  data_ez[:,:]


def add_EDPIC_attr_meshes(field):
    """
    Write the metadata which is specific to PIC algorithm
    for a given field

    Parameters
    ----------
    field : an h5py.Group or h5py.Dataset object
            The record of the field (Group for vector mesh
            and Dataset for scalar meshes)

    """
    field.attrs["fieldSmoothing"] = "none"
    # field.attrs["fieldSmoothingParameters"] = \
    #     "period=10;numPasses=4;compensator=true"


def add_EDPIC_attr_particles(particle):
    """
    Write the metadata which is specific to the PIC algorithm
    for a given species.

    Parameters
    ----------
    particle : an h5py.Group object
               The group of the particle that gets additional attributes.

    """
    particle.attrs["particleShape"] = 3.0
    particle.attrs["currentDeposition"] = "Esirkepov"
    # particle.attrs["currentDepositionParameters"] = ""
    particle.attrs["particlePush"] = "Boris"
    particle.attrs["particleInterpolation"] = "Trilinear"
    particle.attrs["particleSmoothing"] = "none"
    # particle.attrs["particleSmoothingParameters"] = \
    #     "period=1;numPasses=2;compensator=false"


def write_meshes(f, iteration):
    full_meshes_path = get_basePath(f, iteration) + f.attrs["meshesPath"]
    f.create_group(full_meshes_path)
    meshes = f[full_meshes_path]

    # Extension: Additional attributes for ED-PIC
    meshes.attrs["fieldSolver"] = "Yee"
    meshes.attrs["fieldSolverOrder"] = 2.0
    # meshes.attrs["fieldSolverParameters"] = ""
    meshes.attrs["currentSmoothing"] = "none"
    # meshes.attrs["currentSmoothingParameters"] = \
    #     "period=1;numPasses=2;compensator=false"
    meshes.attrs["chargeCorrection"] = "none"
    # meshes.attrs["chargeCorrectionParameters"] = "period=100"

    # (Here the data is randomly generated, but in an actual simulation, this would
    # be replaced by the simulation data.)

    # - Write rho
    # Mode 0 : real values, mode 1 : complex values
    data_rho0 = np.random.rand(32,64)
    data_rho1 = np.random.rand(32,64) + 1.j*np.random.rand(32,64)
    write_rho_cylindrical(meshes, data_rho0, data_rho1)

    # - Write E
    data_ex = np.random.rand(32,64)
    data_ey = np.random.rand(32,64)
    data_ez = np.random.rand(32,64)
    write_e_2d_cartesian( meshes, data_ex, data_ey, data_ez )

def write_particles(f, iteration):
    fullParticlesPath = get_basePath(f, iteration) + f.attrs["particlesPath"]
    f.create_group(fullParticlesPath + "electrons")
    electrons = f[fullParticlesPath + "electrons"]

    globalNumParticles = 128 # example number of all particles

    electrons.attrs["comment"] = "My first electron species"

    # Extension: ED-PIC Attributes
    #   required
    add_EDPIC_attr_particles(electrons)
    #   recommended
    # currently none

    # constant scalar particle records (that could also be variable records)
    electrons.create_group("charge")
    charge = electrons["charge"]
    charge.attrs["value"] = -1.0;
    charge.attrs["unitSI"] = np.float64(1.60217657e-19);
    charge.attrs["unitDimension"] = \
       np.array([0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0 ], dtype="float64")
       #          L    M    T    J  theta  N    J
       # C = A * s
    electrons.create_group("mass")
    mass = electrons["mass"]
    mass.attrs["value"] = 1.0;
    mass.attrs["unitSI"] = np.float64(9.10938291e-31);
    mass.attrs["unitDimension"] = \
       np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], dtype="float64")
       #          L    M    T    J  theta  N    J

    # scalar particle records (non-const/individual per particle)
    electrons.create_dataset("weighting", (globalNumParticles,), dtype='f4')
    weighting = electrons["weighting"]
    weighting.attrs["unitSI"] = np.float64(1.0);
    weighting.attrs["unitDimension"] = \
       np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], dtype="float64") # plain floating point number

    # vector particle records (non-const/individual per particle)
    electrons.create_group("position")
    position = electrons["position"]
    position.attrs["componentOrder"] = "x;y;z"
    position.create_dataset("x", (globalNumParticles,), dtype='f4')
    position.create_dataset("y", (globalNumParticles,), dtype='f4')
    position.create_dataset("z", (globalNumParticles,), dtype='f4')
    position.attrs["unitSI"] = np.float64(1.e-9);
    position.attrs["unitDimension"] = \
       np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ], dtype="float64")
       #          L    M     T    J  theta  N    J
       # Dimension of Length per component

    electrons.create_group("momentum")
    momentum = electrons["momentum"]
    momentum.attrs["componentOrder"] = "x;y;z"
    momentum.create_dataset("x", (globalNumParticles,), dtype='f4')
    momentum.create_dataset("y", (globalNumParticles,), dtype='f4')
    momentum.create_dataset("z", (globalNumParticles,), dtype='f4')
    momentum.attrs["unitSI"] = np.float64(1.60217657e-19);
    momentum.attrs["unitDimension"] = \
       np.array([1.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0 ], dtype="float64")
       #          L    M     T    J  theta  N    J
       # Dimension of Length * Mass / Time

    # Record `particlePatches`
    #   recommended
    mpi_size = 4  # "emulate" example MPI run with 4 ranks
    data_size = 2 + 2 * len(position.keys())  # 2 + 2 * Dimensionality of position record
    grid_layout = np.array( [512, 128, 1] ) # global grid in cells
    electrons.create_dataset("particlePatches", (data_size*mpi_size,), dtype='f64')
    particlePatches = electrons["particlePatches"]

    for rank in np.arange(mpi_size): # each MPI rank would write it's part independently
        particlePatches[rank*data_size + 0] = globalNumParticles / mpi_size
        particlePatches[rank*data_size + 1] = rank
        # example: 1D domain decompositon along the first axis
        particlePatches[rank*data_size + 2] = rank * grid_layout[0] / mpi_size # 1st dimension spatial offset
        particlePatches[rank*data_size + 3] = 0 # 2nd dimension spatial offset
        particlePatches[rank*data_size + 4] = 0 # 3rd dimension spatial offset
        particlePatches[rank*data_size + 5] = grid_layout[0] / mpi_size # 1st dimension spatial extend
        particlePatches[rank*data_size + 6] = 0 # 2nd dimension spatial extend
        particlePatches[rank*data_size + 7] = 0 # 3rd dimension spatial extend



if __name__ == "__main__":

    # Open an exemple file
    f = h5.File("example.h5", "w")

    # Setup the root attributes for iteration 0
    setup_root_attr(f)

    # Write the field records
    write_meshes(f, iteration=0)

    # Write the particle records
    write_particles(f, iteration=0)

    # Close the file
    f.close()
    print("File example.h5 created!")
