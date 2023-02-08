Domain-Specific Naming Conventions for a laser envelope profile
===============================================================

openPMD extension name: `LaserEnvelope`


Introduction
------------

This extension is specifically designed for the modeling laser beam propagation.

Mesh Based Records (Fields)
---------------------------

### Naming Conventions for `mesh record`s (field records)

The laser pulse is represented as a single complex field $\mathcal{E}$, describing the envelope of the laser electric field:

```math
   \begin{aligned}
   E_x &= \operatorname{Re}\left( \mathcal{E} e^{-i\omega_0t}p_x\right)\\
   E_y &= \operatorname{Re}\left( \mathcal{E} e^{-i\omega_0t}p_y\right)\\
\end{aligned}
```

where $\operatorname{Re}$ stands for real part,  $E_x$ (resp. $E_y$) is the laser electric field in the x (resp. y) direction, $\mathcal{E}$ is the complex laser envelope described in the standard, $\omega_0 = 2\pi c/\lambda_0$ is the angular frequency defined from the laser wavelength $\lambda_0$ and $(p_x,p_y)$ is the (complex and normalized) polarization vector. The polarization state (linear, circular, elliptical) is controlled by the phase of the polarization vector. For instance, if $arg(p_x) = arg(p_y)$, the polarization is linear. If $arg(p_x) = arg(p_y) + \pi/2$, the polarization is circular.

When added to an output, the following naming conventions shall be used for complex electric field `mesh records`.

  - `<laser envelope name>/`
    - type: *(complexX)*
    - scope: *required*
    - description: Scalar field for the envelope (as a field strength). See above for description. The name is arbitrary, allowing a single series to store multiple laser pulses.
    - unitDimension = `(1., 1., -3., -1., 0., 0., 0.)` $(V/m = kg . m / (A . s^3))$

### Additional attributes on the `mesh record` named `<laser envelope name>`

On the `series` object, set the following attributes:

  - `isLaserEnvelope`
    - type: *(boolean)*
    - description: Whether the mesh record is of type laserEnvelope.
    - scope: *optional*

  - `angularFrequency`
    - type: *(floatX)*
    - description: Angular frequency $\omega_0$ at which the laser envelope is defined (rad/s).
    - scope: *required*

  - `polarization`
    - type: 1-dimensional array containing 2 *(complexX)*
    - description: polarization vector, 2 values for the 2 transverse components x and y. This vector is normalized (so its modulus is 1) and contains all information to account for polarization states and carrier-envelope phase (CEP).
