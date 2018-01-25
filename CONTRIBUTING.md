Contributing to the openPMD standard
======================================

The openPMD standard can evolve in order to accommodate the needs of the community. This results in successive [*versions* of the standard](https://github.com/openPMD/openPMD-standard/blob/1.0.1/STANDARD.md#the-versions-of-this-standard). This document explains the process through which the standard evolves, and how to contribute to it.

Update Cycle
------------

The updates of the openPMD standard go through a 3-step process:

- **Issues:** Anyone can propose changes to the standard, request new features,
ask for clarification, etc. by opening a new issue
[here](https://github.com/openPMD/openPMD-standard/issues). The proposed
changes/features/question will then be discussed by the members of the
openPMD community (or anyone interested, really) in the `Comments` section of
this issue. The openPMD admins will usually add a label specifying the version
of the standard in which this should be implemented.

- **Pull requests:** Once an issue is well-understood and a clear solution
emerges, anyone can volunteer to implement it in the text of the standard. This
is done by creating a pull request (see below for more details on how to
create a pull request). Pull requests are then reviewed by the community, and
eventually merged by the openPMD admins (@ax3l and @RemiLehe) into the
`upcoming-*` branch (where `*` is replaced by the number of the next upcoming
version), so that the corresponding changes will be included in the next release.

- **New releases:** Once all the issues that have been labeled for the next
upcoming version have been resolved (e.g. via pull requests), the openPMD
admins will create a new official version (by merging the `upcoming-*` on top
of the `latest` branch and tagging it with a new **official version number**.)
Tools that use the openPMD standard should then be adapted, so that they can
properly parse openPMD files that conform to this new official version.

Note that this 3-step process in reflected in the [Projects
tab](https://github.com/openPMD/openPMD-standard/projects). This page
lists the upcoming versions that are being considered, and, for each
upcoming version, tracks the corresponding issues and their status (from
`proposed` to `accepted` to `implemented`). It is important for
the prioritization and organization of tasks.

How to implement a change, using a pull request
-----------------------------------------------

License Model
-------------

All contributions in text, image or multimedia format are agreed
to be shared by all authors under the
[CC-BY 4.0](http://creativecommons.org/licenses/by/4.0/) license
(see [LICENSE](LICENSE)).

Scripts and source code is contributed under the
[ISC](https://www.isc.org/downloads/software-support-policy/isc-license/)
license, if not explicitly stated otherwise (see [ISC_LICENSE](ISC_LICENSE)).

Listed trademarks, names and logos are excluded from the above agreement
and remain property of their respective owners. By contributing those you
agree that implementors and/or users of the *openPMD standard* are
granted the non-exclusive right to use *your* trademark, name and/or logo
in a reference to the community of the *openPMD standard* when promoting
their third-party product(s) and/or project(s).
