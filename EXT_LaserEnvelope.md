Domain-Specific Naming Conventions for a laser envelope profile
===============================================================

openPMD extension name: `LaserEnvelope`


Introduction
------------

This extension is specifically designed for the modeling laser beam propagation.

Mesh Based Records (Fields)
---------------------------

### Naming Conventions for `mesh record`s (field records)

The laser pulse is represented as a single complex field $\mathcal{E}$, describing the envelope of the laser electric field in the paraxial approximation:

```math
   \begin{aligned}
   E_x &= \operatorname{Re}\left( \mathcal{E} e^{-i\omega_0t}p_x\right)\\
   E_y &= \operatorname{Re}\left( \mathcal{E} e^{-i\omega_0t}p_y\right)\\
   E_z &= 0\\
   B_x &= -c E_y\\
   B_y &= c E_x\\
   B_z &= 0\end{aligned}
```

where $\operatorname{Re}$ stands for real part,  $E_x$ (resp. $E_y$) is the laser electric field in the x (resp. y) direction, $\mathcal{E}$ is the complex laser envelope described in the standard, $\omega_0 = 2\pi c/\lambda_0$ is the angular frequency defined from the laser wavelength $\lambda_0$ and $(p_x,p_y)$ is the (complex and normalized) polarization vector. The polarization state (linear, circular, elliptical) is controlled by the phase of the polarization vector. For instance, if $arg(p_x) = arg(p_y)$, the polarization is linear. If $arg(p_x) = arg(p_y) + \pi/2$, the polarization is circular.

When added to an output, the following naming conventions shall be used for complex electric field `mesh records`.

- `laser_envelope/`
  - type: *(complexX)*
  - scope: *(required)*
  - decription: Scalar field for the envelope (in V/m). See above for description.
  - unitDimension = `(1., 1., -3., -1., 0., 0., 0.)` $(V/m = kg . m / (A . s^3))$

### Additional attributes on the `mesh record` named `electricField`

On the `series` object, set the following attributes:

  - `angularFrequency`
    - type: *(floatX)*
    - description: Angular frequency $\omega_0$ at which the laser envelope is defined.
    - scope: *required*
    - `unitDimension = (0., 0., -1., 0., 0., 0., 0.)` (rad/s)


  - `polarization`
    - type: *(floatX)*
    - description: Polarization vector. This vector is normalized (so its modulus is 1) and contains all information to account for polarization states and carrier-envelope phase (CEP).
    - scope: *required*
    - components:
      - `x/`
      - `y/`
    - `unitDimension = (0., 0., 0., 0., 0., 0., 0.)` (unitless)


  - `propagationDirection`
    - type: *(floatX)*
    - scope: *optional*
    - description: Propagation direction for the laser pulse. Default is (0,0,1), i.e. propagation along the z coordinate.
    - components:
      - `x/`
      - `y/`
      - `z/`
    - `unitDimension = (1., 0., 0., 0., 0., 0., 0.)` (length)
