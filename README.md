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

openPMD provides naming and attribute conventions that allow for the exchange
of **particle and mesh-based data** from scientific simulations and experiments.
The primary goal is to define

  - a minimal set/kernel of meta information

that allows to share and exchange data to achieve

  - portability between various applications and differing algorithms
  - a unified open-access description for scientific data (publishing and archiving)
  - a unified description for post-processing, visualization, and analysis.

openPMD suits for **any kind of hierarchical, self-describing** data format,
such as, but not limited to

  - [ADIOS1 (BP3)](https://www.olcf.ornl.gov/center-projects/adios/)
  - [ADIOS2 (BP4)](https://github.com/ornladios/ADIOS2)
  - [HDF5](http://hdfgroup.org/HDF5/)
  - [JSON](https://en.wikipedia.org/wiki/JSON)
  - [XML](https://en.wikipedia.org/wiki/XML).


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
and auxiliary software, if not stated otherwise, under the **ISC license**.

For more details, see the [contributions](CONTRIBUTING.md) page.
