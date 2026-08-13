# pyqgis-api-reference

Find exact QGIS 4.2 PyQGIS API signatures, parameters, enums, and deprecation status.

## Overview

The authoritative, version-pinned reference for the PyQGIS Python API is the Sphinx-generated site at `https://qgis.org/pyqgis/{version}/` (built from Doxygen comments in the QGIS C++ source). This skill removes trial-and-error from looking up classes: it encodes the URL patterns, the big-page reading strategy, and verified QGIS 3→4 API differences (e.g. removed `encoding` constructor args, `writeAsVectorFormatV3`, PyQt6).

Target version is resolved by probing the machine instead of guessing: existing env vars (`OSGEO4W_ROOT`, `QGIS_PREFIX_PATH`) with path parsing or `qgis-bin.exe --version`, `qgis --version` on PATH, or the QGIS MCP instance's reported version — falling back to the current stable.

## What's Inside

- `SKILL.md` — lookup workflow: URL patterns per module (`core`/`gui`/`analysis`/`processing`/`server`/`_3d`), version pinning, how to read 100KB+ class pages (grep the saved fetch, use `release-4_2` C++ headers to resolve misaligned deprecation markers), and verified QGIS 4 vs 3 pitfalls.

## Usage

1. When a QGIS 4 plugin/script needs an exact signature or deprecation status, load this skill.
2. Resolve the target version per the probing chain (env vars → `qgis --version` → MCP instance → default stable).
3. Follow the URL pattern directly — no guessing: `https://qgis.org/pyqgis/{version}/{module}/QgsClassName.html`.
3. For ambiguous deprecation markers, cross-check the C++ header on the `release-4_2` branch of `github.com/qgis/QGIS`.

## References

- PyQGIS 4.2 API docs: https://qgis.org/pyqgis/4.2/
- QGIS user docs / cookbook (docs.qgis.org) for usage patterns: local `qgis-docs` skill

## License

MIT
