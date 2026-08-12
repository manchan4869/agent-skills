# 高德地图编码表（离线数据）

## 服务概述

高德官方的三个编码表离线数据，存于 `data/` 目录（CSV，UTF-8 带 BOM）。用于线下查询 POI 分类编码、城市 adcode/citycode、海外城市编码。

> **重要提示**：官方明确说明编码表**仅供线下查询，请勿作为缓存写死在程序中**。编码会不定期更新，建议生产环境通过地理编码/逆地理编码等线上服务实时获取 adcode。此数据文件可周期性从官方下载页更新。

- **官方下载页**: <https://lbs.amap.com/api/webservice/download>

## 数据文件

| 文件 | 内容 | 数据行数 | 列 |
|------|------|---------|-----|
| `data/poi_category.csv` | POI 分类编码表（中英文） | ~915 | 序号, NEW_TYPE, 大类, 中类, 小类, Big Category, Mid Category, Sub Category |
| `data/adcode_citycode.csv` | 国内城市编码表 | ~3240 | 中文名, adcode, citycode |
| `data/overseas_adcode.csv` | 海外城市编码表（1/2 级行政区划） | ~3251 | adcode, level, name, en_name, country_adcode, country_name, country_en_name |

> 城市编码表暂不支持台湾省行政区域编码查询。

## 使用方法

**POI 类型编码查询**（搜"咖啡"对应编码，用于 `types` 参数）：

```bash
grep "咖啡" data/poi_category.csv
# 283,050500,美食,咖啡厅,咖啡厅,Food & Beverages,Coffee House,Coffee House
# 284,050501,美食,咖啡厅,星巴克咖啡,Food & Beverages,Coffee House,Starbucks Coffee
# => types=050500 或 050501
```

**城市 adcode/citycode 查询**（用于 `city`/`region`/`adcode` 参数）：

```bash
grep "北京市" data/adcode_citycode.csv
# 北京市,110000,010
# => adcode=110000, citycode=010
```

**海外城市编码查询**（level=1 国家，level=2 省级）：

```bash
grep "日本" data/overseas_adcode.csv
```

## 注意事项

- POI 分类编码（typecode）用于 `types` 参数，大类包含其所有小类（如 050000 涵盖全部 0505xx 咖啡厅）
- 省市从属：海外表中 `country_adcode` 为国家 adcode，`level=1` 为国家、`level=2` 为下一级行政区划
- 需最新数据时从官方下载页重新获取 xlsx 并转换
- adcode 用于行政区域查询（`references/district.md`）、天气查询（`references/weather_query.md`）、坐标转换等接口
