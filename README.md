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

The content of this standard is provided under the **CC0 license** and
auxiliary software under the **ISC license**.

For more details, see the [contributions](CONTRIBUTING.md) page.


Partners and Subscribers
------------------------

The following projects participated and/or implemented the
**openPMD** standard to describe their data:

- [PIConGPU](http://picongpu.hzdr.de) (HZDR, Germany)
  - domain: electro-dynamic particle-in-cell code
  - link to open source implementation

- [Warp](http://warp.lbl.gov) (LBL, United States)
  - domain: electro-dynamic/static particle-in-cell code
  - link to open source implementation
