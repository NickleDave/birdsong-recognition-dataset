# Changelog
All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
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