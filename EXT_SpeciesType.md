Convention for Specifying Particle Species 
==========================================

openPMD extension name: `SpeciesType`

openPMD extension ID: `4`


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

### SubAtomic Particles

  - `antimuon`
  - `antiproton`
  - `bottom`
  - `charm-antiquark`
  - `charm-quark`
  - `deuteron`
  - `down-antiquark`
  - `down-quark`
  - `electron`
  - `electron-neutrino`
  - `gluon`
  - `graviton`
  - `higgs-boson`
  - `muon`
  - `muon-neutrino`
  - `neutron`
  - `photon`
  - `pion`
  - `positron`
  - `proton`
  - `strange-antiquark`
  - `strange-quark`
  - `tao-antiquark`
  - `tao-quark`
  - `tao-neutrino`
  - `top-antiquark`
  - `top-quark`
  - `up-antiquark`
  - `up-quark`
  - `w-boson`
  - `z-boson`

### Atoms & Isotopes

Element namings follow the abbreviated namings of the periodic table, defined
by *The International Union of Pure and Applied Chemistry* (IUPAC).
An example would be `Si` for silicon.

Specifications of isotopes are denoted by a pound symbol `#` followed
by the isotopic number followed by the chemical symbol, e.g.: `#3He`
for Helium-3.

Charge states shall not be encoded here.
An extension that specifies `charge` can further define its appropriate
location (e.g. `attribute` or `constant particle record`).

### Molecules

Use standard chemical notation, e.g.: `H20`.

The isotope prefix can be used with molecules as well.
Examples for heavy water: `#2H2O` for two deuterium and `#2HHO` for one
deuterium.
