# Changelog
All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.3.2 -- 2022-05-14
### Changed
- require Python >= 3.8, 
  to adhere to [NEP-29](https://numpy.org/neps/nep-0029-deprecation_policy.html)
  [#16](https://github.com/NickleDave/koumura/pull/16).
  Fixes [#15](https://github.com/NickleDave/birdsong-recognition-dataset/issues/15).

## 0.3.1 -- 2022-04-02
### Added
- add full citation to dataset, including DOI + url
  [7eb131f](https://github.com/NickleDave/birdsong-recognition-dataset/commit/7eb131fdea53836772d040d07ce7b93cf6d7e545)
  [72b58b3](https://github.com/NickleDave/birdsong-recognition-dataset/commit/72b58b3fa3d42f7466ad19d7b3b596a78c88bd76)

## 0.3.0 -- 2021-12-31
### Changed
- switch to using `flit` for development
  [#10](https://github.com/NickleDave/koumura/pull/10)  
- raise minimum required Python to 3.7
  [12](https://github.com/NickleDave/koumura/pull/12)  
- change package and library name, from `koumura` 
  to `birdsong-recognition-dataset` (distribution package name) 
  and `birdsongrec` (import package name)
  [13](https://github.com/NickleDave/koumura/pull/13).
  Fixes [#11](https://github.com/NickleDave/birdsong-recognition-dataset/issues/11).

## 0.2.1.post1 -- 2021-03-04
### Changed
- add metadata to pyproject.toml so that README is used as "long description" 
  and appears on PyPI
  [f37e051](https://github.com/NickleDave/crowsetta/commit/f37e05187aa87ea3ed9e5c59f66140b0141fc9b3)

## 0.2.1 -- 2021-03-04
### Changed
- switch to using GitHub Actions for continuous integration
  [309a367](https://github.com/NickleDave/koumura/commit/309a3673bd6c52b12970388a556b694704260373)

### Fixed
- change dependencies and required Python so they are not pinned to major version
  [3709eda](https://github.com/NickleDave/koumura/commit/3709eda3358429be3bb757d2b52a17f92848a225)


## 0.2.0
### Added
- add build status badge to README
  [b13045b](https://github.com/NickleDave/koumura/commit/b13045beaa286159dacd469db3e717470757b054)
- add `__about__.py` with package metadata
  [4305c6e](https://github.com/NickleDave/koumura/commit/4305c6ea262061072ad86bba39bda35da5171661)
- add version and license badges at top of README
  [3a5ca61](https://github.com/NickleDave/koumura/commit/3a5ca61c739d41361da5d62e9de5b994dfbe85b9)

### Changed
- switch to `poetry` for dev
  [7d179b6](https://github.com/NickleDave/koumura/commit/7d179b6d157014597f58742d40a0e5aecfb46505)

### Fixed
- fix links to other libraries in README
  [98f497f](https://github.com/NickleDave/koumura/commit/98f497f135a9687f525a334cec36218363faef02)
- fix date in LICENSE
  [57c537d](https://github.com/NickleDave/koumura/commit/57c537d7d5db2e2dbe6757280f1fa5414f431574)

## 0.1.1a1
- Initial version after excising from hvc 
(https://github.com/NickleDave/hybrid-vocal-classifier/commits/0c50144d75e3a3205db82add8b48302edbbed511/hvc/koumura.py)

### changed
- The library now limits itself to returning annotation in a data structure
similar to what's used in the BirdsongRecognition code.
  + e.g. `parse_xml` no longer returns an "annotation dictionary"
  + instead, the [conbirt package](https://github.com/NickleDave/conbirt)
  handles translating the data structures to the "annotation dictionary"
  structure that it uses internally
- Convert tests to Python unittest format (instead of using PyTest library)

### added
+ Write README.md with usage
+ to help work with `conbirt` package, the `parse_xml` function 
now has parameters to allow returning the paths to the .wav files as 
absolute paths, but by default it returns just the file names, as 
specified in the `Annotation.xml` files.