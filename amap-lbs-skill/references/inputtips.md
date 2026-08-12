# 高德地图输入提示 API

## 服务概述

根据用户输入的关键词返回地点/公交建议列表（联想提示），常用于搜索框自动补全。支持 POI、公交站点、公交线路三种数据类型。

- **服务标识**: `inputtips`
- **官方文档**: <https://lbs.amap.com/api/webservice/guide/api-advanced/inputtips>

## API 调用

**GET** `https://restapi.amap.com/v3/assistant/inputtips`

## 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| key | string | T | - | 高德 Web 服务 Key | `$AMAP_WEBSERVICE_KEY` |
| keywords | string | T | - | 查询关键词（前缀匹配） | 仙林 |
| type | string | | - | POI 分类过滤，多个用 `\|` 分隔，建议用分类代码 | 050000 |
| location | string | | - | 坐标 `经度,纬度`，在此附近优先返回；city 非空时生效 | 118.791199,32.086331 |
| city | string | | - | 搜索城市：citycode/adcode/城市名，不支持县级市 | 010 |
| citylimit | boolean | | false | true 时仅返回指定城市数据 | true |
| datatype | string | | all | 返回数据类型：all/poi/bus/busline，用 `\|` 分隔 | poi |
| output | string | | JSON | 返回格式 | JSON |
| appname | string | T | - | 调用来源标识 | amap-lbs-skill |

## 请求示例

```bash
curl -s --get "https://restapi.amap.com/v3/assistant/inputtips" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "keywords=天安" \
  --data-urlencode "city=北京" \
  --data-urlencode "datatype=poi" \
  --data-urlencode "appname=amap-lbs-skill"
```

## 响应解析

```json
{
  "status": "1",
  "info": "OK",
  "count": "10",
  "tips": [
    {
      "id": "B000A8UIN8",
      "name": "天安门广场",
      "district": "北京市东城区",
      "adcode": "110101",
      "location": "116.397428,39.90923",
      "address": "东长安街"
    }
  ]
}
```

- `tips[].id`：数据 ID（POI 类型为 POI id，可用于 POI ID 搜索）
- `tips[].name`：名称；`tips[].district`：省+市+区；`tips[].location`：坐标；`tips[].address`：详细地址
- `busline` 类型的数据无 `location` 字段

## 常见问题

**Q: 输入提示和关键字搜索有什么区别？**

A: 输入提示做前缀联想（边输入边补全，返回简短建议），关键字搜索做完整文本匹配（返回完整 POI 详情）。建议先用输入提示获取精确 id，再用 ID 搜索取详情。

**Q: type 参数为什么不建议用名称？**

A: 官方建议传分类代码而非分类名称，名称解析可能出现不符合预期的结果。
