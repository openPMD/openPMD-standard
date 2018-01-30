Contributing to the openPMD standard
======================================

The openPMD standard can evolve in order to accommodate the needs of the community. This results in successive [*versions* of the standard](https://github.com/openPMD/openPMD-standard/blob/1.0.1/STANDARD.md#the-versions-of-this-standard). This document explains the process by which the standard evolves, and how to contribute to it.

Update Cycle
------------

The updates of the openPMD standard go through a 3-step process:

- **Issues:** Anyone can propose changes to the standard, request new features,
ask for clarification, etc. by opening a new issue
[here](https://github.com/openPMD/openPMD-standard/issues). The proposed
changes/features/question will then be discussed by the members of the
openPMD community (or anyone interested, really) in the `Comments` section of
this issue. The openPMD maintainers will usually add a label specifying the
scope and impact of the change. Also, the maintainers will usually organize
the issue in the [Projects tab](https://github.com/openPMD/openPMD-standard/projects)
(see more below), and specify the upcoming version of the standard in which
this issue should tentatively be implemented. (This may be the next upcoming
version, or a later one.)

- **Pull requests:** Once an issue is well-understood and a clear solution
emerges, anyone can volunteer to implement it in the text of the standard. This
is done by creating a pull request (see below for more details on how to
create a pull request). Pull requests are then reviewed by the community, and
eventually merged by the openPMD maintainers (@ax3l and @RemiLehe) into the
`upcoming-*` branch (where `*` is replaced by the number of the next upcoming
version), so that the corresponding changes will be included in the next release.

- **New releases:** Once all the issues that have been labeled for the next
upcoming version have been resolved (e.g. via pull requests), the openPMD
maintainers will create a new official version (by merging the `upcoming-*` on top
of the `latest` branch and tagging it with a new **official version number**.)
Tools that use the openPMD standard should then be adapted, so that they can
properly parse openPMD files that conform to this new official version.

Note that this 3-step process is reflected in the [Projects
tab](https://github.com/openPMD/openPMD-standard/projects). The Projects tab is important for the prioritization and organization of tasks. It
lists the upcoming versions that are being considered, and, for each
upcoming version, tracks the corresponding issues and their status (from
`proposed` to `accepted` to `implemented`). Note that issues evolve and can be
postponed for later releases, or sometimes even dismissed.
(It does *not* mean that the issue is bad or irrelevant, but rather e.g.
that no clear solution emerged yet, or that a solution exists but does not
benefit from being standardized in openPMD.)

How to implement a change, through a pull request
-------------------------------------------------

In order to implement a change in the text of the standard,
please follow this process (*Note*: this assumes familiarity with `git`):

- **Fork the [official repository of the openPMD
standard](https://github.com/openPMD/openPMD-standard)**.
("Forking" means creating a local copy of the official repository, in
your personal Github account.) This is done by clicking the `Fork` button
in the upper right corner of [this page](https://github.com/openPMD/openPMD-standard).

 - **Clone the fork to your local computer, and a create a new branch**:
    * `git clone git@github.com:<YourUserName>/openPMD-standard.git`
    * `cd openPMD-standard`
    * `git remote add mainline git@github.com:openPMD/openPMD-standard.git` (add the official repository for updates)
    * `git fetch mainline` (get latest updates from official repository)
    * `git checkout mainline/upcoming-<versionNumber> -b <newBranch>`: where
    `<versionNumber>` should be replaced by the number of the next upcoming
    version (see [this
    page](https://github.com/openPMD/openPMD-standard/branches)),
    and where `<newBranch>` should be replaced by a name that is representative
    of the change that you wish to implement.

- **Implement changes in the files, and commit them using `git`**

- Once you are done with the implementation: **push the changes to your fork**:
    `git push -u origin`

- **Create a pull request**:
    * Point your web browser to `https://github.com/<YourUserName>/openPMD-standard/pulls`, where `<YourUserName>` should be replaced by your Github username.
    * Click the button `New pull request`
    * For `base fork`, select `upcoming-*` ; for `head fork`, select the name
    of your new branch.
    * Click `Create pull request`
    * In the description section of the pull request, briefly describe the
    changes that you are making. Please link the Github issue that this is
    related to. You can use [this template](https://github.com/openPMD/openPMD-standard/blob/upcoming-1.1.0/.github/PULL_REQUEST_TEMPLATE.md) in order to explain how this affects other
    tools that rely on the openPMD standard.
    * Click again `Create pull request`

Note that pull request should only be created for the **next** upcoming version.
In other words, we only work on **one** version/release of the standard at a given time.


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
