# 高德地图坐标转换 API

## 服务概述

将非高德坐标（GPS/高德 mapbar/百度 baidu）转换为高德坐标。高德坐标系为 GCJ-02（国测局加密坐标），GPS 为 WGS-84，百度为 BD-09。

- **服务标识**: `coordinate_convert`
- **官方文档**: <https://lbs.amap.com/api/webservice/guide/api/convert>

## API 调用

**GET** `https://restapi.amap.com/v3/assistant/coordinate/convert`

## 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| key | string | T | - | 高德 Web 服务 Key | `$AMAP_WEBSERVICE_KEY` |
| locations | string | T | - | 坐标点 `经度,纬度`，多个用 `\|` 分隔，最多 40 对 | 116.481499,39.990475 |
| coordsys | string | | autonavi | 原坐标系：`gps`（WGS-84）、`mapbar`、`baidu`（BD-09）、`autonavi`（不转换） | gps |
| output | string | | JSON | 返回格式 | JSON |
| appname | string | T | - | 调用来源标识 | amap-lbs-skill |

## 请求示例

```bash
# GPS 坐标转高德坐标
curl -s --get "https://restapi.amap.com/v3/assistant/coordinate/convert" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "locations=116.481499,39.990475" \
  --data-urlencode "coordsys=gps" \
  --data-urlencode "appname=amap-lbs-skill"

# 百度坐标批量转高德坐标
curl -s --get "https://restapi.amap.com/v3/assistant/coordinate/convert" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "locations=116.403847,39.915426|116.410054,39.921935" \
  --data-urlencode "coordsys=baidu" \
  --data-urlencode "appname=amap-lbs-skill"
```

## 响应解析

```json
{
  "status": "1",
  "info": "OK",
  "locations": "116.487585177952,39.991754014757"
}
```

- `status` 为 `"1"` 表示成功
- `locations`：转换后的坐标，多个坐标用 `;` 分隔，格式仍为 `经度,纬度`

## 常见问题

**Q: 为什么要转换坐标？**

A: 不同平台使用不同坐标系：GPS 设备输出 WGS-84、百度地图使用 BD-09、高德使用 GCJ-02。用第三方坐标直接调用高德 API 会导致位置偏移几百米，需先转换。

**Q: coordsys=autonavi 是什么意思？**

A: 表示输入的本来就是高德坐标，不做转换直接返回。
