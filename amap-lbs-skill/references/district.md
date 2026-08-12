# 高德地图行政区域查询 API

## 服务概述

根据行政区名称/citycode/adcode 查询中国行政区划信息，支持多级层级（国家>省>市>区>街道）和行政区边界坐标。适用于地址分析、区划树构建、区域过滤等场景。

- **服务标识**: `district`
- **官方文档**: <https://lbs.amap.com/api/webservice/guide/api/district>

## API 调用

**GET** `https://restapi.amap.com/v3/config/district`

## 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| key | string | T | - | 高德 Web 服务 Key | `$AMAP_WEBSERVICE_KEY` |
| keywords | string | | - | 行政区名称/citycode/adcode（只支持单个关键词）。编码表见 `data/adcode_citycode.csv` | 北京 |
| subdistrict | number | | 1 | 返回下级行政区级数：0 不返回、1 下一级、2 下两级、3 下三级 | 2 |
| page | number | | 1 | 页码（外层最多 20 条一页） | 1 |
| offset | number | | 20 | 外层返回个数 | 20 |
| extensions | string | | base | `base` 不返回边界坐标；`all` 返回当前查询区划边界（不含子节点，街道级不支持） | all |
| filter | string | | - | 按 adcode 过滤，只返回该省/直辖市 | 110000 |
| output | string | | JSON | 返回格式 | JSON |
| appname | string | T | - | 调用来源标识 | amap-lbs-skill |

## 请求示例

```bash
# 查询北京及下两级行政区
curl -s --get "https://restapi.amap.com/v3/config/district" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "keywords=北京" \
  --data-urlencode "subdistrict=2" \
  --data-urlencode "appname=amap-lbs-skill"

# 查询带边界坐标的行政区
curl -s --get "https://restapi.amap.com/v3/config/district" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "keywords=朝阳区" \
  --data-urlencode "extensions=all" \
  --data-urlencode "appname=amap-lbs-skill"
```

## 响应解析

```json
{
  "status": "1",
  "info": "OK",
  "districts": [
    {
      "citycode": "010",
      "adcode": "110000",
      "name": "北京市",
      "polyline": "116.463857,40.037554;116.4411,40.023188;...",
      "center": "116.407387,39.904179",
      "level": "province",
      "districts": [
        { "name": "北京城区", "adcode": "110100", "level": "city", "center": "116.407387,39.904179" }
      ]
    }
  ]
}
```

### 字段说明

- `districts[].adcode`：区域编码（街道无独立 adcode，继承区县）
- `districts[].name`：行政区名称；`center`：区域中心点
- `districts[].level`：级别枚举 `country/province/city/district/street`
- `districts[].polyline`：边界坐标串（extensions=all 时返回），多地块用 `|` 分隔
- `districts[].districts`：下级行政区列表（受 subdistrict 控制）

## 注意事项

- 街道级别不返回边界 polyline；东莞、文昌市等省直辖县在市级下直接显示街道
- 不支持台湾省详细区划查询
- 乡镇/街道级 center 是边界上的形点，非实际中心

## 常见问题

**Q: 如何获取某个区的街道列表？**

A: `keywords=历下区&subdistrict=1`，返回区及其街道子级。

**Q: 边界坐标怎么来的？**

A: `extensions=all` 时返回 `polyline`，为 `经度,纬度` 点串，分号分隔。

**Q: 为什么未返回子级行政区信息？**

A: 部分城市不设区（县）层级但实际含街道（"直筒子市"），此类城市 API 暂时无法返回街道级数据。典型：广东东莞、海南文昌市。

**Q: 有哪些省直辖县？**

A: 省直辖县（由省直接管辖、不在市下）包括：
- 河南省：济源市
- 湖北省：仙桃市、潜江市、天门市、神农架林区
- 海南省：五指山市、文昌市、琼海市、万宁市、东方市、定安县、屯昌县、澄迈县、临高县、琼中黎族苗族自治县、保亭黎族苗族自治县、白沙黎族自治县、昌江黎族自治县、乐东黎族自治县、陵水黎族自治县
- 新疆维吾尔自治区：阿拉尔市、图木舒克市、五家渠市、北屯市、铁门关市、双河市、可克达拉市、昆玉市、石河子市、胡杨河市、新星市
