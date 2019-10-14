Domain-Specific Naming Conventions for Photon Raytracing Codes
===========================================================================

openPMD extension name: `PRAYTRACE`


Introduction
------------

This extension to the openPMD addresses the domain-specific requirements
met in raytracing codes (e.g. OASYS).

Particle Based Records (Fields)
---------------------------

### Root attributes

- `openPMD`: `0.0.1`
- `openPMDextension`: `PRAYTRACE`
- `author`: `Aljosa Hafner <aljosa.hafner@ceric-eric.eu>`
- `date`: `10.10.2019 00:00:00 +0100`

### Attributes for the Group 'particlesPath'

	- `nRays`
		- type: *(uintX)*
		- description: Number of initialised rays
		- scope: *required*
	
	- `rayPositions`
		- `X`
			- type: 1 x N array *(floatX)*
			- description: *x-* coordinates of *N* rays
			- scope: *required*
		- `Y`
			- type: 1 x N array *(floatX)*
			- description: *y-* coordinates of *N* rays
			- scope: *required*
		- `Z`
			- type: 1 x N array *(floatX)*
			- description: *z-* coordinates of *N* rays
			- scope: *required*
	
	- `rayDirections`
		- `Xd`
			- type: 1 x N array *(floatX)*
			- description: *x-* directions of *N* rays
			- scope: *required*
		- `Yd`
			- type: 1 x N array *(floatX)*
			- description: *x-* directions of *N* rays
			- scope: *required*
		- `Zd`
			- type: 1 x N array *(floatX)*
			- description: *x-* directions of *N* rays
			- scope: *required*

	- `eFieldSPolarisations`
		- `X`
			- type: 1 x N array *(complexX)*
			- description: S polarisations of *N* rays along *x-* coordinate
			- scope: *required*
		- `Y`
			- type: 1 x N array *(complexX)*
			- description: S polarisations of *N* rays along *y-* coordinate
			- scope: *required*
		- `Z`
			- type: 1 x N array *(complexX)*
			- description: S polarisations of *N* rays along *z-* coordinate
			- scope: *required*	
	
	- `eFieldPPolarisations`
		- `X`
			- type: 1 x N array *(complexX)*
			- description: P polarisations of *N* rays along *x-* coordinate
			- scope: *required*
		- `Y`
			- type: 1 x N array *(complexX)*
			- description: P polarisations of *N* rays along *y-* coordinate
			- scope: *required*
		- `Z`
			- type: 1 x N array *(complexX)*
			- description: P polarisations of *N* rays along *z-* coordinate
			- scope: *required*	

	- `photonEnergy`
		- type: *(floatX)*
		- description: energy, self-explanatory
		- scope: *required*
	
	- `phase`
		- `sPol`
			- type: 1 x N array *(complexX)*
			- description: phases of *N* rays for S polarisation
			- scope: *required*
		- `pPol`
			- type: 1 x N array *(complexX)*
			- description: phases of *N* rays for P polarisation
			- scope: *required*
	
### Additional Attributes for the Group `particlesPath`

The following additional attributes are optional.

	- `deadAlive`
		- type: 1 x N array *bool*
		- description: logical array whether the *N-*th ray is dead or alive
		- scope: *optional*
	
	- `opticalPath`
		- type: array *(string)*
		- description: The string representation of the beamline
		- scope: *optional*
			
	- `wavelength`
		- type: *(floatX)*
		- description: wavelength of the photons
		- scope: *optional*

	- `R`
		- type: 1 x N array *(floatX)*
		- description: sqrt(X^2 + Y^2 + Z^2)
		- scope *optional*
		
	- `grazingAngle`
		- type: 1 x N array *float64*
		- description: angle between *y-* axis and *N* photons
		- scope *optional*
	
	- `eFieldMagnitude`
		- type: 1 x N array *(floatX)*
		- description: |E_SPol| + |E_PPol|
		- scope *optional*
		
	- `intensity`
		- `total`
			- type: 1 x N array *(floatX)*
			- description: |E_SPol|^2 + |E_PPol|^2
			- scope *optional*
		- `sPol`
		-	 type: 1 x N array *(floatX)*
			- description: |E_SPol|^2
			- scope *optional*
		- `pPol`
			- type: 1 x N array *(floatX)*
			- description: |E_PPol|^2
			- scope *optional*
		
	- `wavevector`
		- `k`
			- type: 1 x N array *(complexX)*
			- description: |k|, magnitude of the wavevector
			- scope: *optional*
		- `x`
			- type: 1 x N array *(floatX)*
			- description: k_x, *x-* component of the wavevector
			- scope: *optional*
		- `y`
			- type: 1 x N array *(floatX)*
			- description: k_y, *y-* component of the wavevector
			- scope: *optional*
		- `z`
			- type: 1 x N array *(floatX)*
			- description: k_z, *z-* component of the wavevector
			- scope: *optional*
	
	- `stokesParams`
		- 'S0'
			- type: 1 x N array *(floatX)*
			- description: |E_SPol|^2 + |E_PPol|^2, same as total intensity
			- scope *optional*
		- 'S1'
			- type: 1 x N array *(floatX)*
			- description: |E_PPol|^2 - |E_SPol|^2
			- scope *optional*
		- 'S2'
			- type: 1 x N array *(floatX)*
			- description: 2|E_SPol||E_PPol|cos(phaseSPol - phasePPol)
			- scope *optional*
		- 'S3'
			- type: 1 x N array *(floatX)*
			- description: 2|E_SPol||E_PPol|sin(phaseSPol - phasePPol)
			- scope *optional*
	
	- `power`
		- type: 1 x N array *(floatX)*
		- description: intensity * energy
		- scope *optional*
