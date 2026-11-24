Convention for Specifying Particle Species 
==========================================

openPMD extension name: `SpeciesType`

Introduction
------------

This convention is for standardizing the names of particle species, e.g. in
particle physics.

This document uses ABNF as specified by [RFC 5234][rfc5234]. Quoted strings
such as `"He"` are case insensitive in ABNF. A string written `%s"He"` is case
sensitive, as specified by [RFC 7405][rfc7405].

[rfc5234]: https://datatracker.ietf.org/doc/html/rfc5234
[rfc7405]: https://datatracker.ietf.org/doc/html/rfc7405

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
    species-single = elementary / hadron-or-jet / atom / molecule
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
quark-anti = "anti-" quark-normal
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
element = %s"H" / %s"He" / %s"Li" / %s"Be" / %s"B" / %s"C" / %s"N" / %s"O" / %s"F" / %s"Ne" / %s"Na" / %s"Mg" / %s"Al" / %s"Si" / %s"P" / %s"S" / %s"Cl" / %s"Ar" / %s"K" / %s"Ca" / %s"Sc" / %s"Ti" / %s"V" / %s"Cr" / %s"Mn" / %s"Fe" / %s"Co" / %s"Ni" / %s"Cu" / %s"Zn" / %s"Ga" / %s"Ge" / %s"As" / %s"Se" / %s"Br" / %s"Kr" / %s"Rb" / %s"Sr" / %s"Y" / %s"Zr" / %s"Nb" / %s"Mo" / %s"Tc" / %s"Ru" / %s"Rh" / %s"Pd" / %s"Ag" / %s"Cd" / %s"In" / %s"Sn" / %s"Sb" / %s"Te" / %s"I" / %s"Xe" / %s"Cs" / %s"Ba" / %s"La" / %s"Ce" / %s"Pr" / %s"Nd" / %s"Pm" / %s"Sm" / %s"Eu" / %s"Gd" / %s"Tb" / %s"Dy" / %s"Ho" / %s"Er" / %s"Tm" / %s"Yb" / %s"Lu" / %s"Hf" / %s"Ta" / %s"W" / %s"Re" / %s"Os" / %s"Ir" / %s"Pt" / %s"Au" / %s"Hg" / %s"Tl" / %s"Pb" / %s"Bi" / %s"Po" / %s"At" / %s"Rn" / %s"Fr" / %s"Ra" / %s"Ac" / %s"Th" / %s"Pa" / %s"U" / %s"Np" / %s"Pu" / %s"Am" / %s"Cm" / %s"Bk" / %s"Cf" / %s"Es" / %s"Fm" / %s"Md" / %s"No" / %s"Lr" / %s"Rf" / %s"Db" / %s"Sg" / %s"Bh" / %s"Hs" / %s"Mt" / %s"Ds" / %s"Rg" / %s"Cn" / %s"Nh" / %s"Fl" / %s"Mc" / %s"Lv" / %s"Ts" / %s"Og"
```


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

ABNF:

```
molecule = 1*( ( atom / "(" molecule ")" / "[" molecule "]" ) [ count ] )
count = ( %x32-39 *DIGIT ) / ( "1" 1*DIGIT )  ; an integer of 2 or more
```
