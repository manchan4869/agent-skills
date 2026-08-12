---
name: qgis4-qt6-compat
description: Use when writing PyQGIS code for QGIS 4.x (Qt6) via qgis_execute_code or scripts, or when facing errors like "has no attribute", "unexpected type", "no attribute", "cannot import name", "argument ... has unexpected type", "arguments did not match any overloaded call", PyQt5 import errors, or deprecated API removals in QGIS 4 / Qt 6. Also use when porting QGIS 3.x PyQGIS code or plugins to QGIS 4.x Qt6.
---

# QGIS 4 / Qt6 PyQGIS Compatibility

## Overview

QGIS 4.x runs on Qt6 (PyQt6). Code written for QGIS 3.x (Qt5/PyQt5) frequently breaks with: missing attributes, "unexpected type" argument errors, enum scoping errors, and removed modules. Always target the **installed** QGIS's API, not QGIS 3 docs.

**Check first:** run `qgis_diagnose` to confirm QGIS version, then use `print(SomeClass.method.__doc__)` or `dir(SomeClass)` in `qgis_execute_code` BEFORE calling an unfamiliar method. PyQt6 method signatures are stricter than PyQt5 — type errors are common.

## Critical Import Rules

- **NEVER** `from PyQt5.X import ...` → QGIS 4 raises `ImportError: PyQt5 classes cannot be imported in a QGIS build based on Qt6`.
- Use version-independent `from qgis.PyQt.QtCore import ...`, `qgis.PyQt.QtGui`, `qgis.PyQt.QtWidgets`.
- `QRegExp` was **removed** in Qt6 → use `QRegularExpression` (from `qgis.PyQt.QtCore`).
- `qgis_execute_code` namespace does NOT pre-import everything. Explicitly import each class: `from qgis.core import QgsField, QgsPointXY, ...`. Missing → `NameError: name 'X' is not defined`.
- `import processing` is required separately for `processing.run` — it is not auto-available.

## Enum Scoping (QGIS 3 vs QGIS 4)

QGIS 3: `EnumClass.MEMBER` (unscoped). QGIS 4: `EnumClass.Scope.MEMBER` (scoped).

| QGIS 3 (breaks) | QGIS 4 (works) |
|---|---|
| `QFont.Bold` | `QFont.Weight.Bold` |
| `QPainter.CompositionMode_Multiply` | `QPainter.CompositionMode.CompositionMode_Multiply` |
| `QgsMapLayer.VectorLayer` | `QgsMapLayer.LayerType.VectorLayer` |
| `Qgis.Critical` (as message level) | `Qgis.MessageLevel.Critical` |
| `QgsWkbTypes.PolygonGeometry` | `QgsWkbTypes.GeometryType.PolygonGeometry` |
| `QMessageBox.Ok` | `QMessageBox.StandardButton.Ok` |
| `Qt.UserRole` | `Qt.ItemDataRole.UserRole` |
| `Qt.WaitCursor` | `Qt.CursorShape.WaitCursor` |
| `Qt.blue` | `Qt.GlobalColor.blue` |

**Set blend mode (raster opacity):** use `layer.setBlendMode(Qgis.BlendMode.Multiply)` — passing a raw `int` or old enum fails with `unexpected type`.

## Field Types (QVariant removed-style)

QGIS 3: `QgsField("name", QVariant.String)` still works in QGIS 4 (kept for compat), but prefer Qt6 form:

```python
from qgis.PyQt.QtCore import QMetaType
f = QgsField("name", QMetaType.Type.QString)   # String
# QMetaType.Type.Int / Double / Bool / QDate / QDateTime / LongLong
```

## Removed / Renamed Methods

These DO NOT exist in QGIS 4 — use the replacement shown:

| Removed in QGIS 4 | Replacement |
|---|---|
| `layer.setLayerOpacity(...)` | `layer.setOpacity(...)` (or tree layer node) |
| `layer.pendingFields()` | `layer.fields()` |
| `layout.refreshLayout()` | `layout.refresh()` |
| `legend.setStyleEnabled(...)` | removed — style via `QgsLegendStyle` / item settings |
| `scalebar.segmentSize()` / `scalebar.mapUnitsPerSegment()` / `scalebar.size()` | `scalebar.setUnitsPerSegment(x)` / `scalebar.unitsPerSegment()` |
| `pictureItem.hasPicture()` | removed — check `pictureItem.picturePath()` or existing items list |
| `QgsLayerTreeLayer.setOpacity` | removed — use `layer.setOpacity` on the layer itself |

## Method Signature Changes (argument types tightened)

| Call | Fix |
|---|---|
| `setFrameStrokeWidth(QgsLayoutSize)` | pass `QgsLayoutMeasurement` — QGIS 4.2 signature is `QgsLayoutMeasurement(length: float, units: Qgis.LayoutUnit = Qgis.LayoutUnit.Millimeters)` (use `Qgis.LayoutUnit`, NOT `QgsUnitTypes.LayoutMillimeters`) |
| `QFont("Fam", 12.5)` | second arg (pointSize) must be `int` — cast it |
| `QFont` weight | use `QFont.Weight.Bold` (see enums) |
| `QgsVectorFileWriter.writeAsVectorFormatV2/V3` | V3 signature: `writeAsVectorFormatV3(layer, fileName, transformContext, options)` — 3rd arg is a `QgsCoordinateTransformContext`, 4th a `QgsVectorFileWriter.SaveVectorOptions`. Passing a CRS or `SaveVectorOptions` in the wrong slot → `unexpected type`. |
| `layout item .style()` (e.g. scalebar/legend) | some `style()` getters now require an argument; check `__doc__` |

## Environment Self-Check Tool

**REQUIRED when unsure of the installed QGIS's API, when facing a new/unknown error, or when the user reports an API mismatch:** run the bundled self-check script first — it reports which QGIS4/Qt6 APIs exist and which QGIS3 APIs are removed in the current install.

Locate the script at `scripts/verify_qgis4_api.py` in this skill directory (works regardless of where the skill is installed), then paste its content into `qgis_execute_code`, or read it with your local file tools and execute it in the QGIS Python console:

```python
src = open(r"<path-to-this-skill>/scripts/verify_qgis4_api.py", encoding="utf-8").read()
exec(compile(src, "verify_qgis4_api.py", "exec"))
run()
```

It prints a PASS/FAIL report across enum scoping, renamed methods, removed APIs, writer signatures, and import rules. A FAIL tells you to adapt the code per the mappings above — never rely on QGIS3 memory.

## Safe Method Discovery

Before calling any method you are unsure about, in `qgis_execute_code`:

```python
from qgis.core import QgsLayoutItemScaleBar  # example
print(QgsLayoutItemScaleBar.setUnitsPerSegment.__doc__)
# or list members:
print([m for m in dir(obj) if 'segment' in m.lower()])
```

## Common Pitfalls

- **`argument 1 has unexpected type 'QgsTextFormat'`** (e.g. `legend.setStyleFont(...)`): passing a Python type the SIP overloads don't accept — check the target type with `__doc__`, often it wants a `QFont` or the method was removed entirely.
- **North arrow / embedded resources** (e.g. `:/images/north_arrows/default_north_arrow.svg`) may not render in QGIS 4.2 — list `:/images/north_arrows/` first, or load a local SVG with `QgsLayoutItemPicture`.
- **`QgsMapToPixel.toMapCoordinates`** overloads reject `QgsPointXY`/floats in some QGIS 4 builds — pass the int pair or use canvas `mapToLayerCoordinates`; verify via `__doc__`.
- **`QgsCoordinateTransformContext` vs `QgsCoordinateTransform`**: writer/processing APIs expect the *Context* object, not a single transform.

## References

- QGIS Wiki migration guide (official): https://github.com/qgis/QGIS/wiki/Plugin-migration-to-be-compatible-with-Qt5-and-Qt6
- Plugins repo migrate guide + pyqgis4-checker: https://plugins.qgis.org/docs/migrate-qgis4
- PyQGIS 4.2 API docs (check THIS, not 3.x): https://qgis.org/pyqgis/4.2/
- Qt6 Porting Guide: https://doc.qt.io/qt-6/portingguide.html
- PyQt5→PyQt6 differences: https://www.riverbankcomputing.com/static/Docs/PyQt6/pyqt5_differences.html
