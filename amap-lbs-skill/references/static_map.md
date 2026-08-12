# 高德地图静态地图 API

## 服务概述

通过 URL 生成静态地图图片（PNG），无需地图 SDK，可直接嵌入网页或展示。支持标注点、路线、标签、多图层叠加。

- **服务标识**: `static_map`
- **官方文档**: <https://lbs.amap.com/api/webservice/guide/api/staticmaps>

## API 调用

**GET** `https://restapi.amap.com/v3/staticmap`

## 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| key | string | T | - | 高德 Web 服务 Key | `$AMAP_WEBSERVICE_KEY` |
| location | string | | - | 地图中心点 `经度,纬度`（与 markers 至少传一个） | 116.397428,39.90923 |
| zoom | number | | - | 地图缩放级别 3-18，location 为必传时生效 | 13 |
| size | string | | 1024*1024 | 图片尺寸 `宽*高`，最大 1024*1024 | 400*400 |
| scale | number | | 1 | 输出比例（2 为高清图） | 2 |
| markers | string | | - | 标注点，多个用 `\|` 分隔。格式 `size,label,color:经度,纬度` 或 `mid,color:经度,纬度` | `mid,0xFF0000:116.397428,39.90923` |
| labels | string | | - | 文字标签，格式 `经度,纬度:文字:字号,颜色` | `116.397428,39.90923:故宫:14,0x0000FF` |
| paths | string | | - | 路线/多边形，多个用 `\|` 分隔。格式 `width,color:经度,纬度;经度,纬度` | `5,0xFF0000:116.397,39.909;116.42,39.92` |
| traffic | number | | - | 叠加实时路况图层（1 开启） | 1 |
| output | string | | - | 返回格式（png/jpg/gif） | png |
| appname | string | T | - | 调用来源标识 | amap-lbs-skill |

## 请求示例

```bash
# 中心点地图 + 标注 + 标签
curl -s --get "https://restapi.amap.com/v3/staticmap" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "location=116.397428,39.90923" \
  --data-urlencode "zoom=13" \
  --data-urlencode "size=400*400" \
  --data-urlencode "markers=mid,0xFF0000:116.397428,39.90923" \
  --data-urlencode "labels=116.397428,39.90923:天安门:14,0x0000FF" \
  --data-urlencode "appname=amap-lbs-skill"

# 保存图片到本地
curl -s --get "https://restapi.amap.com/v3/staticmap" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "location=116.397428,39.90923" \
  --data-urlencode "zoom=13" \
  --data-urlencode "size=400*400" \
  --data-urlencode "appname=amap-lbs-skill" \
  -o map.png
```

## 返回说明

- 成功返回图片二进制（PNG），可直接展示或 `-o` 保存
- 该接口不返回 JSON 状态码；检查 HTTP 状态与图片内容判断成功

## 常见问题

**Q: location 和 markers 怎么配合？**

A: 传 location+zoom 控制视野中心；markers 在图上打点。不传 location 时地图自动适配所有 markers 的范围。

**Q: 如何画路线或区域？**

A: 用 `paths` 参数传一组点串，可画折线（路线）或闭合多边形（区域），支持多组用 `|` 分隔。
