Convention for Specifying Particle Species 
==========================================

openPMD extension name: `SpeciesType`

Introduction
------------

This convention is for standardizing the names of particle species, e.g. in
particle physics.

Additional Record Attribute
---------------------------

The following additional attribute for openPMD `mesh records` and
`particle groups` is defined in this extension:

- `speciesType`
  - type: *(string)*
  - scope: *optional*
  - description: particle species in this record. If there are multiple
                 species to be specified, they can be specified using a
                 semicolon separated list.
  - allowed values:
    - a single *particle species*, which is one of the list entries below
    - a *particle species list*, which is multiple entries of the
      list below separated by a single semicolon character `;`.
      A trailing semicolon `;` is allowed, but not required.
  - examples:
    - `electron` (e.g. on an electron `particle record` or an electron
                  density `mesh record`)
    - `electron;proton;#12C` (e.g. on a `mesh record` for a plasma's
                              local charge density)
    - `other:apple` (e.g. for an apple `particle record`)

This attribute can be used with any `record` (including `mesh records`).

A particle species list containing only a single item **must** be
treated as a single species.

> Note that `other:` can *only* be used for single species, it is
> forbidden in lists.
>
> The list separator is a sole `;`. Neither spaces around it nor empty
> list items (two semicolons following each other `;;`) are allowed.
> However, a single trailing semicolon `;` **must** be ignored.

The following values **should not** be used by an implementation, even if
they are allowed above:

- `other:`, as it does not specify any content.
- Trailing spaces, as they can lead to ambiguous display.

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

For particle species not mentioned here we suggest to use `other:`
with namings from the [particle data group (PDG)](http://pdg.lbl.gov).

Examples:

- `proton`, `anti-proton`
- `neutron`, `anti-neutron`
- `other:sigma`, `other:anti-sigma`
- `other:kaon`, ...
  
> Keep in mind that particle species with `other:` can't be used in
> particle species lists.

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
