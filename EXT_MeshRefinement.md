Conventions for Mesh Refinement
===============================

openPMD extension name: `MeshRefinement`

Introduction
------------

This extension defines naming conventions to identify refined meshes.

Mesh Records
------------

Mesh refinement levels of a mesh record describe a higher resolution subselection of a mesh record.

### Additional Naming Conventions or Each Mesh `Record`

The coarsest level of a record is implicitly assigned the level `0` of a simulation.
The record names of finer levels are suffixed with `_lvl<N>` where `<N>` is the integer of the refined level.

A patch of a refinemnet level shall be a spatially hyperrectangular subselection of the previous level.
Multiple patches might exist in a refined level.

If the implemented file format supports sparse data sets, i.e. through efficient chunking of patches, the refined level must over the previous level in extend and store multiple patches through its chunking mechanism.

File formats that do not support efficient storage a sparesly populated refinement level can store continguous patches on the same level with an additional suffix `_<P>` where `<P>` is the number of the (hyperrectangular) patch in the refinement level.

### Additional Attributes

A mesh record describing a refined level shall add the following attribute:

  - `refinementRatio`
    - type: 1-dimensional array containing N *(int)*
            elements, where N is the number of dimensions in the mesh
    - description: the refinement ratio compared to the prior level
    - advice to implementors: the order of the N values must be identical to the axes in `axisLabels`
