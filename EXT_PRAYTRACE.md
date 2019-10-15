Domain-Specific Naming Conventions for Photon Raytracing Codes
===========================================================================

openPMD extension name: `PRAYTRACE`


Introduction
------------

This extension to the openPMD addresses the domain-specific requirements
met in raytracing codes (e.g. OASYS). Each ray has the information stored
in its own record, e.g. data/1/particles/rays/0...N/positions and therefore
has to have the same length.

Particle Based Records (Fields)
---------------------------

### Root attributes

- `openPMD`: `0.0.2`
- `openPMDextension`: `PRAYTRACE`
- `author`: `Aljosa Hafner <aljosa.hafner@ceric-eric.eu>`
- `date`: `10.10.2019 00:00:00 +0100`
- `nRays`
	- type: *(uintX)*
	- description: Number of initialised rays
	- scope: *required*
	- unitSI: 1.0
	- unitDimension: [unitless] (0., 0., 0., 0., 0., 0., 0.)

### Structure
data/1/particlesPath/rays/0...N/position...

### Attributes for the individual ray in 'particlesPath/rays/0...N/'

	- `position/`
		- `position/x`
			- type: *(floatX)*
			- description: *x-* coordinate
			- scope: *required*
			- unitSI: 1.0
			- unitDimension: [m] (1., 0., 0., 0., 0., 0., 0.)
		- `position/y`
			- type: *(floatX)*
			- description: *y-* coordinate
			- scope: *required*
			- unitSI: 1.0
			- unitDimension: [m] (1., 0., 0., 0., 0., 0., 0.)
		- `position/z`
			- type: *(floatX)*
			- description: *z-* coordinates
			- scope: *required*
			- unitSI: 1.0
			- unitDimension: [m] (1., 0., 0., 0., 0., 0., 0.)
	
	- `direction/'
		- `direction/x`
			- type: *(floatX)*
			- description: *x-* direction
			- scope: *required*
			- unitSI: 1.0
			- unitDimension: [m] (1., 0., 0., 0., 0., 0., 0.)
		- `direction/y`
			- type: *(floatX)*
			- description: *x-* direction
			- scope: *required*
			- unitSI: 1.0
			- unitDimension: [m] (1., 0., 0., 0., 0., 0., 0.)
		- `direction/z`
			- type: *(floatX)*
			- description: *x-* direction
			- scope: *required*
			- unitSI: 1.0
			- unitDimension: [m] (1., 0., 0., 0., 0., 0., 0.)

	- `eFieldSPolarisation/`
		- `eFieldSPolarisation/x`
			- type: *(complexX)*
			- description: S polarisation along *x-* coordinate
			- scope: *required*
			- unitSI: 1.0
			- unitDimension: [sqrt(V / m) = sqrt(kg m s^-3 A^-1)] (1/2, 1/2, -3/2, -1/2, 0., 0., 0.)
		- `eFieldSPolarisation/y`
			- type: *(complexX)*
			- description: S polarisation along *y-* coordinate
			- scope: *required*
			- unitSI: 1.0
			- unitDimension: [sqrt(V / m) = sqrt(kg m s^-3 A^-1)] (1/2, 1/2, -3/2, -1/2, 0., 0., 0.)
		- `eFieldSPolarisation/z`
			- type: *(complexX)*
			- description: S polarisation along *z-* coordinate
			- scope: *required*
			- unitSI: 1.0
			- unitDimension: [sqrt(V / m) = sqrt(kg m s^-3 A^-1)] (1/2, 1/2, -3/2, -1/2, 0., 0., 0.)
	
	- `eFieldPPolarisations/`
		- `eFieldPPolarisations/x`
			- type: *(complexX)*
			- description: P polarisation along *x-* coordinate
			- scope: *required*
			- unitSI: 1.0
			- unitDimension: [sqrt(V / m) = sqrt(kg m s^-3 A^-1)] (1/2, 1/2, -3/2, -1/2, 0., 0., 0.)
		- `eFieldPPolarisations/y`
			- type: *(complexX)*
			- description: P polarisation along *y-* coordinate
			- scope: *required*
			- unitSI: 1.0
			- unitDimension: [sqrt(V / m) = sqrt(kg m s^-3 A^-1)] (1/2, 1/2, -3/2, -1/2, 0., 0., 0.)
		- `eFieldPPolarisations/z`
			- type: *(complexX)*
			- description: P polarisation along *z-* coordinate
			- scope: *required*	
			- unitSI: 1.0
			- unitDimension: [sqrt(V / m) = sqrt(kg m s^-3 A^-1)] (1/2, 1/2, -3/2, -1/2, 0., 0., 0.)

	- `photonEnergy`
		- type: *(floatX)*
		- description: energy, self-explanatory
		- scope: *required*
		- unitSI: 1.602176634e−19
		- unitDimension: [J = kg m^2 s^-2] (2., 1., -2., 0., 0., 0., 0.)
	
	- `phase/`
		- `phase/sPol`
			- type: *(complexX)*
			- description: phase for S polarisation
			- scope: *required*
			- unitSI: 1.0
			- unitDimension: [unitless] (0., 0., 0., 0., 0., 0., 0.)
		- `phase/pPol`
			- type: *(complexX)*
			- description: phase for P polarisation
			- scope: *required*
			- unitSI: 1.0
			- unitDimension: [unitless] (0., 0., 0., 0., 0., 0., 0.)
	
### Additional Attributes for the Group `particlesPath`

The following additional attributes are optional.

	- `deadAlive`
		- type: *bool*
		- description: logical array whether ray is dead or alive
		- scope: *optional*
		- unitSI: 1.0
		- unitDimension: [unitless] (0., 0., 0., 0., 0., 0., 0.)
	
	- `opticalPath`
		- type: array *(string)*
		- description: The string representation of the beamline
		- scope: *optional*
					
	- `wavelength`
		- type: *(floatX)*
		- description: wavelength of the photons
		- scope: *optional*
		- unitSI: 1.0
		- unitDimension: [m] (1., 0., 0., 0., 0., 0., 0.)

	- `R`
		- type: *(floatX)*
		- description: sqrt(x^2 + y^2 + z^2)
		- scope *optional*
		- unitSI: 1.0
		- unitDimension: [m] (1., 0., 0., 0., 0., 0., 0.)
		
	- `grazingAngle`
		- type: *float64*
		- description: angle between *y-* axis and the photon direction
		- scope *optional*
		- unitSI: 1.0
		- unitDimension: [unitless] (0., 0., 0., 0., 0., 0., 0.)
	
	- `eFieldMagnitude`
		- type: *(floatX)*
		- description: |E_SPol| + |E_PPol|
		- scope *optional*
		- unitSI: 1.0
		- unitDimension: [sqrt(V m^-1) = sqrt(kg m s^-3 A^-1)] (1/2, 1/2, -3/2, -1/2, 0., 0., 0.)
		
	- `intensity/`
		- `intensity/total`
			- type: *(floatX)*
			- description: |E_SPol|^2 + |E_PPol|^2
			- scope *optional*
			- unitSI: 1.0
			- unitDimension: [V m^-1 = kg m s^-3 A^-1] (1., 1., -3., -1., 0., 0., 0.)
		- `intensity/sPol`
		-	 type: *(floatX)*
			- description: |E_SPol|^2
			- scope *optional*
			- unitSI: 1.0
			- unitDimension: [V m^-1 = kg m s^-3 A^-1] (1., 1., -3., -1., 0., 0., 0.)
		- `intensity/pPol`
			- type: *(floatX)*
			- description: |E_PPol|^2
			- scope *optional*
			- unitSI: 1.0
			- unitDimension: [V m^-1 = kg m s^-3 A^-1] (1., 1., -3., -1., 0., 0., 0.)
		
	- `wavevector/`
		- `wavevector/k`
			- type: *(complexX)*
			- description: |k|, magnitude of the wavevector
			- scope: *optional*
			- unitSI: 1.0
			- unitDimension: [m^-1] (-1., 0., 0., 0., 0., 0., 0.)
		- `wavevector/x`
			- type: *(floatX)*
			- description: k_x, *x-* component of the wavevector
			- scope: *optional*
			- unitSI: 1.0
			- unitDimension: [m^-1] (-1., 0., 0., 0., 0., 0., 0.)
		- `wavevector/y`
			- type: *(floatX)*
			- description: k_y, *y-* component of the wavevector
			- scope: *optional*
			- unitSI: 1.0
			- unitDimension: [m^-1] (-1., 0., 0., 0., 0., 0., 0.)
		- `wavevector/z`
			- type: *(floatX)*
			- description: k_z, *z-* component of the wavevector
			- scope: *optional*
			- unitSI: 1.0
			- unitDimension: [m^-1] (-1., 0., 0., 0., 0., 0., 0.)
	
	- `stokesParams/`
		- 'stokesParams/S0'
			- type: *(floatX)*
			- description: |E_SPol|^2 + |E_PPol|^2, same as total intensity
			- scope *optional*
			- unitSI: 1.0
			- unitDimension: [V m^-1 = kg m s^-3 A^-1] (1., 1., -3., -1., 0., 0., 0.)
		- 'stokesParams/S1'
			- type: *(floatX)*
			- description: |E_PPol|^2 - |E_SPol|^2
			- scope *optional*
			- unitSI: 1.0
			- unitDimension: [V m^-1 = kg m s^-3 A^-1] (1., 1., -3., -1., 0., 0., 0.)
		- 'stokesParams/S2'
			- type: *(floatX)*
			- description: 2|E_SPol||E_PPol|cos(phaseSPol - phasePPol)
			- scope *optional*
			- unitSI: 1.0
			- unitDimension: [V m^-1 = kg m s^-3 A^-1] (1., 1., -3., -1., 0., 0., 0.)
		- 'stokesParams/S3'
			- type: *(floatX)*
			- description: 2|E_SPol||E_PPol|sin(phaseSPol - phasePPol)
			- scope *optional*
			- unitSI: 1.0
			- unitDimension: [V m^-1 = kg m s^-3 A^-1] (1., 1., -3., -1., 0., 0., 0.)
	
	- `power`
		- type: *(floatX)*
		- description: intensity * energy
		- scope *optional*
		- unitSI: 1.602176634e−19
		- unitDimension: [V J m^-1 = kg^2 m^3 s^-5 A^-1] (3., 2., -5., -1., 0., 0., 0.)
