# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## 2.0.14
### Added
- Adds support for coreir `float_CW` lib
  https://github.com/leonardt/pycoreir/pull/95
 
## 2.0.8 - 2019-04-22
### Added
- Added libcoreir-rtlil to distributed wheel

## 2.0.8 - 2019-04-22
### Added
- Added OSX build to travis

## 2.0.7 - 2019-04-22
### Changed
- Changed SimulatorState interface to match CoreIRType

## 2.0.0 - 2019-03-11
### Changed
- Changed dependency from bit_vector package to hwtypes package

## 1.0.2 - 2019-02-28
### Changed
- Update simulator bindings for changes in the coreir API
  (https://github.com/leonardt/pycoreir/pull/71)

## 1.0.1 - 2019-02-28
### Added
- Added `inline_instance`, `Context.new_namespace`, and `Module.params` methods.
  (https://github.com/leonardt/pycoreir/pull/70)
 
## 1.0.0 - 2019-02-04
### Added
- Added `__hash__` and `__eq__` for CoreIRType based on the underlying C
  pointer value.
