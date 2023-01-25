Convention for Specifying Particle Species 
==========================================

openPMD extension name: `SpeciesType`

Introduction
------------

This convention is for standardizing the names of particle species, e.g. in
particle physics.

This document uses ABNF as specified by [RFC 5234][rfc5234].

[rfc5234]: https://datatracker.ietf.org/doc/html/rfc5234

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
    - a single *particle species*, which is either:
      - one of the list entries below, or
      - `other:` followed by any number of spaces (ascii 0x20) or
        visible ("printing") ascii characters, i.e. ascii 0x21 to 0x7e
    - a *particle species list*, which is multiple entries of the
      list below separated by a single semicolon character `;`.
      A trailing semicolon `;` is allowed, but not required.
  - ABNF:
    ```
    species-type = species-single / species-list / species-other
    species-other = "other:" *( VCHAR / SP )
    species-list = species-single *( ";" species-single ) [ ";" ]
    species-single = elementary / hadron-or-jet / atom
    ```
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
- `w-boson`
- `z-boson`
- `higgs`
  
ABNF:

```
elementary = quark / lepton / boson

quark = quark-anti / quark-normal
qurak-anti = "anti-" quark-normal
quark-normal = "up" / "down" / "charm" / "strange" / "top" / "bottom"

lepton = lepton-anti / lepton-normal
lepton-anti = "positron" / "anti-electron-neutrino" / "anti-muon" / "anti-muon-neutrino" / "anti-tau" / "anti-tau-neutrino"
lepton-normal = "electron" / "electron-neutrino" / "muon" / "muon-neutrino" / "tau" / "tau-neutrino"

boson = "photon" / "gluon" / "w-boson" / "z-boson" / "higgs"
```

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

ABNF:

```
hadron-or-jet = hadron-or-jet-normal / hadron-or-jet-anti
hadron-or-jet-anti = "anti-" hadron-or-jet-normal
hadron-or-jet-normal = "proton" / "neutron"
```

### Atoms & Isotopes

Valid element names are the symbols of the periodic table, defined
by *The International Union of Pure and Applied Chemistry* (IUPAC).
An example would be `Si` for silicon.

The names are case sensitive.

Specifications of isotopes are denoted by a pound symbol `#` followed
by the isotopic number followed by an element, e.g.: `#3He` for
Helium-3.

ABNF:

```
atom = element / isotope
isotope = "#" 1*DIGIT element
element = "H" / "He" / "Li" / "Be" / "B" / "C" / "N" / "O" / "F" / "Ne" / "Na" / "Mg" / "Al" / "Si" / "P" / "S" / "Cl" / "Ar" / "K" / "Ca" / "Sc" / "Ti" / "V" / "Cr" / "Mn" / "Fe" / "Co" / "Ni" / "Cu" / "Zn" / "Ga" / "Ge" / "As" / "Se" / "Br" / "Kr" / "Rb" / "Sr" / "Y" / "Zr" / "Nb" / "Mo" / "Tc" / "Ru" / "Rh" / "Pd" / "Ag" / "Cd" / "In" / "Sn" / "Sb" / "Te" / "I" / "Xe" / "Cs" / "Ba" / "La" / "Ce" / "Pr" / "Nd" / "Pm" / "Sm" / "Eu" / "Gd" / "Tb" / "Dy" / "Ho" / "Er" / "Tm" / "Yb" / "Lu" / "Hf" / "Ta" / "W" / "Re" / "Os" / "Ir" / "Pt" / "Au" / "Hg" / "Tl" / "Pb" / "Bi" / "Po" / "At" / "Rn" / "Fr" / "Ra" / "Ac" / "Th" / "Pa" / "U" / "Np" / "Pu" / "Am" / "Cm" / "Bk" / "Cf" / "Es" / "Fm" / "Md" / "No" / "Lr" / "Rf" / "Db" / "Sg" / "Bh" / "Hs" / "Mt" / "Ds" / "Rg" / "Cn" / "Nh" / "Fl" / "Mc" / "Lv" / "Ts" / "Og"
```


The charge state is not encoded by the `speciesType` attribute.

The charge state ("ionization") is an attribute of an individual
particle, and therefore an implementation **should not** encode a
charge state as part of the `speciesType` in any way.
In the case that the implementation does treat the charge state
("ionization") as a global, unmodifiable property of the `speciesType`
it **may** encode a charge state in an implementation-defined way.

### Molecules
Molecules are not supported by the `speciesType` attribute.

However, an implementation **may** encode molecules using an
implementation-defined syntax. In this case typical chemical notation
**should** be accepted, e.g. `H2O` for water.
