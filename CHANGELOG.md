Changelog for the openPMD Standard
==================================

1.0.1
-----
**Date:** 2017-12-01

Typo and wording changes since the 1.0.0 release.

This release improves wordings, common questions and example snippets.
Keywords and logic are unchanged and backwards compatible for revision releases.

## Changes to "1.0.0"

### Base Standard

- **backwards compatible changes:**
  - better examples for `axisLabels` #153
  - unspecified (user-chosen) `float`/`uint`/`int` are now called `floatX`/`uintX`/`intX` throughout the standard #152
  - note to store non-openPMD information outside the `basePath` #115
  - particle position: update python example #119 #127
  - particle patches: typo in reference to `positionOffset` #135

### Extension

- `ED-PIC`:
  - **backwards compatible changes:**
    - `fieldSmoothing`: typo in allowed values #131
    - `fieldSolver`: typo in PSATD description #133
    - reference updated to unspecified (user-chosen) `float`/`uint`/`int` as in base standard #152

### Data Converter

No data conversion needed.
