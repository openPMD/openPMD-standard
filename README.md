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

Open, hierarchical, machine-independent, self-describing (binary) data formats
are available for a while now. Nevertheless, without a certain agreement for
a domain of applications, standard tasks like automated data processing and
import/export do not come for free.

This standard tries to bridge the gap between the common "blob of data"
and the *algorithms*, *methods* and/or *schemes* that created these.


Users or "Why should I care?"
-----------------------------

If output from programs, devices (such as cameras), simulations or
post-processed data-sets contain a minimal set of meta information as provided
by **openPMD**, you can exchange data between those with minimal effort and you
use the same tools for visualization.

Furthermore, since **openPMD is not a file format** but just an object-oriented
**markup** and **meta data naming convention** you can still use the large
variety of tools that come with the *intrinsic data format* that you chose
to use (e.g., HDF5 or ADIOS BP). Of course you are completely free to use your
favorite software (open source or proprietary) to create or process your files.

If the software you are using is not yet able to read/write the information
needed to fulfill the openPMD standard, please talk to your software developers
and point them to these documents: further adoptions of the current standard
and contributions for the design of upcoming versions are very welcome!


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
  - status:
    - 1.3.0+: full API available to fulfill the standard (read+write)
    - 2.0.0+ (upcoming): high-level interface for openPMD objects (base standard)

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

### Additional Tools

We provide and collect further tools, software modules and plugins for popular
frameworks in our GitHub organization:
  https://github.com/openPMD

Please check the individual repositories and feel free to contribute.
