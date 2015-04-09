The openPMD Standard
======================


TL;DR
-----

[Technical files](STANDARD.md) of the **openPMD** standard.


Introduction
------------

The **openPMD** standard, short for
  *open standard for particle-mesh data files*
is **not a file format** per se.
It is a standard for **meta data and naming schemes**.

openPMD provides naming and attribute conventions that allow to exchange
**particle and mesh based data** from scientific simulations and experiments.
The primary goals are to define

  - a minimal set/kernel of meta information

that allows to share and exchange data to achieve

  - portability between various applications and differing algorithms
  - a unified open-access description for scientific data (publishing and archiving)
  - a unified description for post-processing, visualization and analysis.

openPMD suits for **any kind of hierarchical, self-describing** data format,
such as, but not limited to

  - [ADIOS BP](https://www.olcf.ornl.gov/center-projects/adios/)
  - [HDF5](http://hdfgroup.org/HDF5/)
  - [SDF](http://ccpforge.cse.rl.ac.uk/gf/project/epoch/)
  - [VTK-XML](http://www.vtk.org/VTK/img/file-formats.pdf)
  - [netCDF](http://www.unidata.ucar.edu/software/netcdf/).


Motivation
----------

Open, hierarchical, machine-independent, self-describing binary data formats
are available for a while now. Nevertheless, without a certain agreement for
a domain of applications standard tasks like automated data processing and
import/export do not come for free.

This standard tries to bridge the gap between the common "blob of data"
and the *algorithms*, *methods* and/or *schemes* that created these.


License
-------

The content of this standard is provided under the
[**CC-BY 4.0 license**](http://creativecommons.org/licenses/by/4.0/)
(see [list of authors](AUTHORS.md))
and auxiliary software under the **ISC license**.

For more details, see the [contributions](CONTRIBUTING.md) page.


Projects and Libraries
----------------------

The following list of projects uses the
**openPMD** standard to describe their data.

### Libraries

- [libSplash](https://github.com/ComputationalRadiationPhysics/libSplash) (TU Dresden/HZDR, Germany)
  - domain: high-level C++ HDF5 library for mesh and particle records
  - [repository](https://github.com/ComputationalRadiationPhysics/libSplash) (LGPLv3+)
  - status: upcoming version 1.3 will automatically write valid openPMD files (base standard)

### Scientific Simulations

- [PIConGPU](http://picongpu.hzdr.de) (HZDR, Germany)
  - domain: electro-dynamic particle-in-cell code
  - [repository](https://github.com/ComputationalRadiationPhysics/picongpu) (GPLv3+/LGPLv3+)
  - status: currently implementing (base standard + ED-PIC)

- [Warp](http://warp.lbl.gov) (LBNL & LLNL, United States)
  - domain: electro-dynamic/static particle-in-cell code
  - [repository](https://bitbucket.org/berkeleylab/warp) (BSD-3-Clause-LBNL)
  - status: currently implementing (base standard + ED-PIC)

### Data Processing and Visualization

- [pyDive](https://github.com/ComputationalRadiationPhysics/pyDive) (HZDR, Germany)
  - domain: parallel numpy for ipython notebook
  - [repository](https://github.com/ComputationalRadiationPhysics/pyDive) (GPLv3+/LGPLv3+)
  - status: currently implementing reader and writer (base standard + ED-PIC)

- [postpic](https://github.com/skuschel/postpic) (U Jena, Germany)
  - domain: serial post-processing tool for particle-in-cell codes
  - [repository](https://github.com/skuschel/postpic) (GPLv3+)
  - status: currently implementing (reader for base standard + ED-PIC)
