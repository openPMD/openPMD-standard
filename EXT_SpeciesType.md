Convention for Specifying Particle Species 
==========================================

openPMD extension name: `SpeciesType`

Introduction
------------

This convention is for standardizing the names of particle species, e.g. in
particle physics.

These names are the values of the `speciesType` attribute of `mesh records`
and `particle groups`, which is defined in the [base standard](STANDARD.md).

Species Names
-------------

### Elementary Particles

Namings for fundamental fermions and their anti-matter particles.

Quarks:

- `up`, `anti-up`
- `down`, `anti-down`
- `charm`, `anti-charm`
- `strange`, `anti-strange`
- `top`, `anti-top`
- `bottom`, `anti-bottom`

Leptons:

- `electron`, `positron`
- `electron-neutrino`, `anti-electron-neutrino`
- `muon`, `anti-muon`
- `muon-neutrino`, `anti-muon-neutrino`
- `tau`, `anti-tau`
- `tau-neutrino`, `anti-tau-neutrino`

Gauge & Higgs Bosons:

- `photon`
- `gluon`
- `w-plus-boson`
- `w-minus-boson`
- `z-boson`
- `higgs`

### Hadrons and Jets

We currently do not define spellings of hadrons besides the commonly used ones
below.

- `proton`, `anti-proton`
- `neutron`, `anti-neutron`
- `pion+`, `pion-`, `pion0`
- `deuteron`, `anti-deuteron`
- `triton`, `anti-triton`
- `helion`, `anti-helion`

A `deuteron`, `triton` or `helion` is the nucleus of `#2H`, `#3H` or `#3He`.

Other hadrons are given by their PDG number (see *PDG Numbers* below).

### Atoms & Isotopes

Valid element names are the symbols of the periodic table, defined
by *The International Union of Pure and Applied Chemistry* (IUPAC).
An example would be `Si` for silicon.

The names are case sensitive.

Specifications of isotopes are denoted by a pound symbol `#` followed
by the isotopic number followed by an element, e.g.: `#3He` for
Helium-3.

The charge state is not encoded by the `speciesType` attribute.

The charge state ("ionization") is an attribute of an individual
particle, and therefore an implementation **should not** encode a
charge state as part of the `speciesType` in any way.
In the case that the implementation does treat the charge state
("ionization") as a global, unmodifiable property of the `speciesType`
it **may** encode a charge state in an implementation-defined way.

### Molecules

A molecule is written as its chemical formula: a sequence of atoms (elements
or isotopes, as above), each followed by the number of that atom in the
molecule. A count of one is left out. A group of atoms can be put in
parentheses `( )` or square brackets `[ ]`, followed by a count for the whole
group. The two mean the same, and groups can be nested.

Examples:

- `H2` for molecular hydrogen
- `H2O` for water
- `#2H2O` for heavy water (two deuterium atoms and one oxygen atom)
- `CH3COOH` for acetic acid
- `Ca(OH)2` for calcium hydroxide
- `K4[Fe(CN)6]` for potassium ferrocyanide

As for atoms, the names are case sensitive: `CO` is carbon monoxide and `Co`
is cobalt. A single atom with no count, such as `He` or `#3He`, is an atom and
not a molecule.

Only the number of each kind of atom matters. An atom that appears more than
once is counted each time, so `CH3COOH` and `C2H4O2` name the same species.
Isomers, which have the same atoms arranged differently, are not distinguished.

As for atoms, the charge state is not part of the formula (see above).

### PDG Numbers

A particle species not named in this document is written as `pdg:` followed by
its number in the [Monte Carlo particle numbering scheme][pdg-numbering] of the
Particle Data Group (PDG). An antiparticle has the negative of its particle's
number. Examples:

- `pdg:321` for a positive kaon, and `pdg:-321` for a negative kaon
- `pdg:3122` for a lambda baryon
- `pdg:3222` for a positive sigma baryon

Geant4, PYTHIA, HepMC and other Monte Carlo codes use the same numbers.

A species that this document names **should** be written by that name, not by
its PDG number: `proton`, not `pdg:2212`.

Unlike `other:`, a `pdg:` species can be used in a species list.

[pdg-numbering]: https://pdg.lbl.gov/2026/reviews/rpp2026-rev-monte-carlo-numbering.pdf
