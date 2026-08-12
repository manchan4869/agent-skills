# QGIS 4 / Qt6 API 环境自检脚本
# 用途：在 qgis_execute_code 中粘贴运行，或在 QGIS Python 控制台运行，
#       验证当前安装的 QGIS 版本上哪些 API 可用/已删除，输出 PASS/FAIL 报告。
# 遇到 FAIL 时，按 qgis4-qt6-compat SKILL.md 的映射改写，不要按 QGIS3 记忆写。
# 作者：opencode build agent（2026-08）


def _check(name, fn):
    try:
        ok = fn()
        print(f"{'PASS' if ok else 'FAIL'} {name}")
        return ok
    except Exception as e:
        print(f"FAIL {name}  ({type(e).__name__}: {e})")
        return False


def run():
    from qgis.core import (
        QgsProject,
        Qgis,
        QgsVectorLayer,
        QgsLayoutItemScaleBar,
        QgsLayoutMeasurement,
        QgsVectorFileWriter,
    )
    from qgis.PyQt.QtCore import QMetaType
    from qgis.PyQt.QtGui import QFont, QPainter

    print("=== 环境 ===")
    try:
        from qgis.core import QgsApplication

        print("QGIS 版本:", QgsApplication.instance().version())
    except Exception:
        pass
    try:
        print("Qgis version:", Qgis.version())
    except Exception:
        pass

    print("=== 1. 枚举作用域（scoped enums）===")
    _check("QFont.Weight.Bold", lambda: hasattr(QFont.Weight, "Bold"))
    _check(
        "QPainter.CompositionMode.CompositionMode_Multiply",
        lambda: hasattr(QPainter.CompositionMode, "CompositionMode_Multiply"),
    )
    _check("Qgis.BlendMode.Multiply", lambda: hasattr(Qgis.BlendMode, "Multiply"))
    _check(
        "QgsMapLayer.LayerType.VectorLayer",
        lambda: hasattr(QgsVectorLayer.LayerType, "VectorLayer"),
    )
    _check("Qgis.MessageLevel.Critical", lambda: hasattr(Qgis.MessageLevel, "Critical"))
    _check(
        "QMetaType.Type.QString",
        lambda: QMetaType.Type.QString == QMetaType.Type.QString,
    )

    print("=== 2. 新增/改名方法存在性 ===")
    _check(
        "QgsLayoutItemScaleBar.setUnitsPerSegment",
        lambda: hasattr(QgsLayoutItemScaleBar, "setUnitsPerSegment"),
    )
    _check(
        "QgsLayoutItemScaleBar.unitsPerSegment",
        lambda: hasattr(QgsLayoutItemScaleBar, "unitsPerSegment"),
    )
    _check(
        "QgsLayoutMeasurement(float, Qgis.LayoutUnit)",
        lambda: QgsLayoutMeasurement(10.0, Qgis.LayoutUnit.Millimeters) is not None,
    )

    print("=== 3. 已删除方法应为 False（QGIS3 旧 API）===")
    _check(
        "QgsLayoutItemScaleBar.segmentSize (removed)",
        lambda: not hasattr(QgsLayoutItemScaleBar, "segmentSize"),
    )
    _check(
        "QgsLayoutItemScaleBar.mapUnitsPerSegment (removed)",
        lambda: not hasattr(QgsLayoutItemScaleBar, "mapUnitsPerSegment"),
    )

    print("=== 4. QgsVectorFileWriter 签名 ===")
    _check(
        "writeAsVectorFormatV3 存在",
        lambda: hasattr(QgsVectorFileWriter, "writeAsVectorFormatV3"),
    )
    _check(
        "writeAsVectorFormatV2 存在",
        lambda: hasattr(QgsVectorFileWriter, "writeAsVectorFormatV2"),
    )
    # V3 第三参必须是 QgsCoordinateTransformContext
    from qgis.core import QgsCoordinateTransformContext

    _check(
        "QgsCoordinateTransformContext 可构造",
        lambda: QgsCoordinateTransformContext() is not None,
    )

    print("=== 5. import 规则 ===")
    from qgis.PyQt.QtCore import QRegularExpression

    _check("QRegularExpression 可导入", lambda: QRegularExpression("x") is not None)
    try:
        import PyQt5  # noqa: F401

        _check("PyQt5 不可用（Qt6 下应 FAIL）", lambda: False)
    except ImportError:
        _check("PyQt5 不可用（Qt6 下应 PASS）", lambda: True)


if __name__ == "__main__":
    run()
