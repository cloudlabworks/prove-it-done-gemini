# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Verifier baseline check (fail before, pass after), synced from issaquahd/prove-it-done#7 into `skills/prove-it-done/`. A receipt that already passes on the pre-change state is VACUOUS and not counted; `baseline=REF`, `keep=` and `before=` set the pre-change state; `--require-baseline` makes VACUOUS a failure (#7).
- `CONTRIBUTING.md`: contributions are released under the repository's MIT licence, and commits carry a DCO sign-off (#6).
- Skill sync checker, `scripts/check_skill_sync.py`, with tests (#5).
- README and `GEMINI.md`: Windows verifier commands (#4).

## [0.1.0] - 2026-10-11

### Added

- prove-it-done as a Gemini CLI extension: `gemini-extension.json`, `GEMINI.md` and the `/prove:check` command.
- A copy of the prove-it-done skill in `skills/prove-it-done/`: `SKILL.md`, the receipt verifier `scripts/verify_receipts.py`, references, four examples, `SECURITY.md` and `LICENSE`.

[Unreleased]: https://github.com/cloudlabworks/prove-it-done-gemini/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/cloudlabworks/prove-it-done-gemini/releases/tag/v0.1.0
