# qgis4-qt6-compat

PyQGIS compatibility guide for QGIS 4.x / Qt6.

## Overview

QGIS 4.x runs on Qt6 (PyQt6). Code written for QGIS 3.x (Qt5/PyQt5) frequently breaks with missing attributes, "unexpected type" argument errors, enum scoping errors, and removed modules. This skill documents the differences and provides a self-check script that verifies which APIs exist in your installed QGIS.

## What's Inside

- `SKILL.md` — the full compatibility guide: import rules, enum scoping table, removed/renamed methods, signature changes, common pitfalls
- `scripts/verify_qgis4_api.py` — environment self-check script; prints a PASS/FAIL report against the installed QGIS, covering enum scoping, renamed methods, removed APIs, writer signatures, and import rules

## Usage

1. Read `SKILL.md` before porting QGIS 3 code.
2. When unsure about the installed API, run `scripts/verify_qgis4_api.py` in `qgis_execute_code` or the QGIS Python console and adapt code per the reported FAILs.

## References

- QGIS Wiki migration guide: https://github.com/qgis/QGIS/wiki/Plugin-migration-to-be-compatible-with-Qt5-and-Qt6
- Plugins repo migrate guide: https://plugins.qgis.org/docs/migrate-qgis4
- PyQGIS 4.x API docs: https://qgis.org/pyqgis/4.2/
- Qt6 Porting Guide: https://doc.qt.io/qt-6/portingguide.html

## License

MIT
