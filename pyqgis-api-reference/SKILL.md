---
name: pyqgis-api-reference
description: Use when writing QGIS 4 plugins or scripts and need exact PyQGIS API signatures, parameters, enums, return types, or deprecation status for QGIS 4.2; when the local QGIS-Documentation cookbook (4.4-dev) may drift from 4.2; or when checking whether an API changed between QGIS 3 and QGIS 4. Do NOT use for user-manual behavior questions (use qgis-docs instead).
version: 1.0.0
---

# PyQGIS API Reference (qgis.org/pyqgis)

## Overview

The authoritative, version-pinned reference for the QGIS **4.2** Python API is the Sphinx-generated site at `https://qgis.org/pyqgis/4.2/`. It is built from Doxygen comments in the QGIS C++ source, so signatures there are exact. Local QGIS-Documentation cookbook = 4.4 dev — **may drift from 4.2**. When precision matters, verify against pyqgis/4.2.

## URL Patterns (no trial-and-error needed)

```
https://qgis.org/pyqgis/4.2/{module}/QgsClassName.html     # class page
https://qgis.org/pyqgis/4.2/{module}/index.html             # module class list
https://qgis.org/pyqgis/4.2/genindex.html                   # full class index
```

Modules: `core`, `gui`, `analysis`, `processing`, `server`, `_3d`. Class pages for functions/methods too (e.g. `core/qgsfunction.html`).

**Mistakes to avoid:**
- NO `qgis.core.` prefix: `qgis.core.QgsVectorLayer.html` → 404. Use `core/QgsVectorLayer.html`.
- Version-pin `4.2` explicitly; `master` = dev API, `3.44` = LTR.
- A URL like `https://qgis.org/pyqgis/4.2/core/QgsVectorLayer.html` returns 200 and contains the signature.

## Workflow

1. **Cookbook first**: consult local qgis-docs cookbook for usage patterns, then this reference for exact signatures.
2. **Fetch the class page** (webfetch). Pages are HUGE (100KB+, e.g. QgsVectorLayer) — the fetch is auto-truncated and the full output saved to a tool-output file.
3. **Search the saved file** with `rg`/Grep instead of reading it whole. Or dispatch an `explore` subagent: "grep `__init__|writeAsVectorFormatV3|Deprecated` in <tool-output file>" to keep context clean.
4. **Cross-check deprecation**: `Deprecated since` markers can render misaligned next to signatures. When ambiguous, consult the C++ header on the `release-4_2` branch of `github.com/qgis/QGIS` (e.g. `src/core/vector/qgsvectorlayer.h`) — the `\deprecated` / `\since` comments adjacent to the declaration are the ground truth.

## QGIS 4 vs 3 Pitfalls (verified against 4.2)

- `QgsVectorLayer(path, name, provider, options)` — `encoding` arg REMOVED in 4.0; use `setProviderEncoding()`.
- Save vector files via `QgsVectorFileWriter.writeAsVectorFormatV3(layer, fileName, transformContext, SaveVectorOptions)` — V2 deprecated since 3.20, V1 since 3.40.
- Python-bound signatures differ from C++: defaults (e.g. `providerLib=''` in Python vs `"ogr"` in C++), `abstract` markers on pure-virtuals, SIP annotations (SIP_HOLDGIL etc.) are irrelevant to Python callers.
- Bindings are PyQt6-based (`from qgis.PyQt import ...` shim works).

## Common Mistakes

- Quoting a signature from memory instead of fetching — always fetch and cite the URL.
- Using the cookbook (4.4 dev) signature for 4.2 code without cross-checking.
- Reading a truncated fetch and missing the method you need — grep the full saved file.
