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

  - `subatomic:antimuon`
  - `subatomic:antiproton`
  - `subatomic:bottom`
  - `subatomic:charm-antiquark`
  - `subatomic:charm-quark`
  - `subatomic:deuteron`
  - `subatomic:down-antiquark`
  - `subatomic:down-quark`
  - `subatomic:electron`
  - `subatomic:electron-neutrino`
  - `subatomic:gluon`
  - `subatomic:graviton`
  - `subatomic:higgs-boson`
  - `subatomic:muon`
  - `subatomic:muon-neutrino`
  - `subatomic:neutron`
  - `subatomic:photon`
  - `subatomic:pion`
  - `subatomic:positron`
  - `subatomic:proton`
  - `subatomic:strange-antiquark`
  - `subatomic:strange-quark`
  - `subatomic:tao-antiquark`
  - `subatomic:tao-quark`
  - `subatomic:tao-neutrino`
  - `subatomic:top-antiquark`
  - `subatomic:top-quark`
  - `subatomic:up-antiquark`
  - `subatomic:up-quark`
  - `subatomic:w-boson`
  - `subatomic:z-boson`

### Atoms & Isotopes

Element namings follow the abbreviated namings of the periodic table, defined
by *The International Union of Pure and Applied Chemistry* (IUPAC).
They are prefixed with `element:`, e.g. `element:Si`.

Closer specifications of isotopes are denoted by a `isotope:` prefix followed
by the isotopic number followed by the chemical symbol, e.g.: `isotope:3He`
for Helium-3.

Charge states shall not be specified here but rather in `attributes`
(`mesh record`) or `records` or a `particle species`.

### Molecules

Use standard chemical notation with a `molecule:` prefix, e.g.: `molecule:H20`.
