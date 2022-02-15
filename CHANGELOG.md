# Changelog for `magodo`

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog], and this project adheres to
[Semantic Versioning].

[Keep a Changelog]: https://keepachangelog.com/en/1.0.0/
[Semantic Versioning]: https://semver.org/


## [Unreleased](https://github.com/bbugyi200/magodo/compare/0.8.5...HEAD)

No notable changes have been made.


## [0.8.5](https://github.com/bbugyi200/magodo/compare/0.8.4...0.8.5) - 2022-02-14

### Fixed

* Fix bug when adding multiple todos dynamically (i.e. using editor).


## [0.8.4](https://github.com/bbugyi200/magodo/compare/0.8.3...0.8.4) - 2022-02-13

### Miscellaneous

* Convert `Metadata` type from `list[str]|str` to `str`.

### Removed

* List splitting functionality of metatags---values with commas in them used to
  be split into lists.


## [0.8.3](https://github.com/bbugyi200/magodo/compare/0.8.2...0.8.3) - 2022-02-13

### Added

* Add pre and post todo spells.


## [0.8.2](https://github.com/bbugyi200/magodo/compare/0.8.1...0.8.2) - 2022-02-12

### Fixed

* Fix `group_tags()` spell so it tries harder (i.e. gives up less).


## [0.8.1](https://github.com/bbugyi200/magodo/compare/0.8.0...0.8.1) - 2022-02-09

### Added

* Add `magodo.from_date()` function to public API.


## [0.8.0](https://github.com/bbugyi200/magodo/compare/0.7.1...0.8.0) - 2022-02-08

### Changed

* *BREAKING CHANGE*: Multiple potentially breaking changes have been made in this release.


## [0.7.1](https://github.com/bbugyi200/magodo/compare/0.7.0...0.7.1) - 2022-01-23

### Changed

* The `AbstractMagicTodo` protocol now accepts a type variable bound on `AbstractTodo`.


## [0.7.0](https://github.com/bbugyi200/magodo/compare/0.6.0...0.7.0) - 2022-01-17

### Added

* New `AbstractMagicTodo.to_line_spells` and `AbstractMagicTodo.from_line_spells` attributes.

### Changed

* *BREAKING CHANGE*: Renamed `AbstractMagicTodo.spells` to `AbstractMagicTodo.todo_spells`.

### Removed

* *BREAKING CHANGE*: Remove `MagicTodo` from API.
* *BREAKING CHANGE*: Remove `AbstractMagicTodo.pre_spells` and `AbstractMagicTodo.post_spells` attributes.


## [0.6.0](https://github.com/bbugyi200/magodo/compare/0.5.3...0.6.0) - 2022-01-15

### Changed

* *BREAKING CHANGE*: Move default spells from `MagicTodoMixin` to `MagicTodo`.


## [0.5.3](https://github.com/bbugyi200/magodo/compare/0.5.2...0.5.3) - 2022-01-15

### Fixed

* Don't allow duplicate tags.


## [0.5.2](https://github.com/bbugyi200/magodo/compare/0.5.1...0.5.2) - 2022-01-15

## Changed

* Use 'id' in sorting algorithm.
* Take 'ctime' metadata tag into account when sorting.

### Fixed

* Fix `spells.group_tags()`.
* Fix missing space after priority.


## [0.5.1](https://github.com/bbugyi200/magodo/compare/0.5.0...0.5.1) - 2022-01-14

### Fixed

* Fix extra space bug in `group_tags()` spell.


## [0.5.0](https://github.com/bbugyi200/magodo/compare/0.4.1...0.5.0) - 2022-01-13

### Added

* Many new features.


## [0.4.1](https://github.com/bbugyi200/magodo/compare/0.4.0...0.4.1) - 2022-01-12

### Added

* Migrated all code from old "bbugyi200/todotxt" GitHub repo to the new "bbugyi200/magodo" repo.


## [0.4.0](https://github.com/bbugyi200/magodo/releases/tag/0.4.0) - 2022-01-12

### Changed

* *BREAKING CHANGE*: Changed name of package from "todotxt" to "magodo".

### Miscellaneous

* *WARNING*: Not a real release. Only claims the "magodo" PyPI package name.


## [0.3.1](https://github.com/bbugyi200/todotxt/compare/0.3.0...0.3.1) - 2022-01-11

### Fixed

* Fix recursion bug with `TodoGroup.from_path()`.


## [0.3.0](https://github.com/bbugyi200/todotxt/compare/0.2.0...0.3.0) - 2022-01-11

### Added

* Add new `TodoGroup` class.

### Fixed

* Fixed multiple bugs with `Todo` class.

### Removed

* Remove old `read_todos_from_file()` function.


## [0.2.0](https://github.com/bbugyi200/todotxt/compare/0.1.0...0.2.0) - 2022-01-10

### Added

* Add `todotxt.Todo` class.
* Add `todotxt.read_todos_from_file()` function.

### Miscellaneous

* Brought test coverage up to 99%!
* First _real_ release.


## [0.1.0](https://github.com/bbugyi200/todotxt/releases/tag/0.1.0) - 2022-01-10

### Miscellaneous

* First release.
