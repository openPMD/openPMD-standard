Convention for Specifying Particle Species 
==========================================

openPMD extension name: `SpeciesType`


Introduction
------------

This convention is for standardizing the names of particle species, e.g. in
particle physics.


Additional Record Attribute
---------------------------

The following additional attribute for openPMD `records` is defined in this
extension:

- `SpeciesType`
  - type: *(string)*
  - scope: *optional*
  - description: particle species in this record. If there are multiple
                 species to be specified, they can be specified using a
                 semicolon separated list.
  - allowed values:
    - *see the lists below* and additionally
    - `other` if none of the ones below applies, user are free to append a
      free text after a colon, e.g. `other:neutralino` or `other:cherry`
  - examples:
    - `electron` (e.g. on an electron `particle record` or an electron
                  density `mesh record`)
    - `electron;proton;#12C` (e.g. on a `mesh record` for a plasma's
                              local charge density)
    - `other:apple;other:orange` (for a `record` mixing apples & oranges)

This attribute can be used with any `record` (including `mesh records`).

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
  - `w-boson`
  - `z-boson`
  - `higgs`

### Hadrons and Jets

We currently do not define spellings of hadrons besides the commonly used ones
below and suggest for this version to use `other:` with namings from the
[particle data group (PDG)](http://pdg.lbl.gov/). Other means of grouping e.g.
jets can be used, e.g. additional attributes outside of the definition of this
extension.

Examples:
  - `proton`, `anti-proton`
  - `other:neutron`, `other:anti-neutron`
  - `other:kaon`, ...

### Atoms & Isotopes

Element namings follow the abbreviated namings of the periodic table, defined
by *The International Union of Pure and Applied Chemistry* (IUPAC).
An example would be `Si` for silicon.

Specifications of isotopes are denoted by a pound symbol `#` followed
by the isotopic number followed by the chemical symbol, e.g.: `#3He`
for Helium-3.

The charge state is not encoded by the `SpeciesType` attribute.
Any extension using this standard can define how to specify the charge state.

### Molecules

Use standard chemical notation, e.g.: `H20`.

The isotope prefix can be used with molecules as well.
Examples for heavy water: `#2H2O` for two deuterium and `#2HHO` for one
deuterium.
