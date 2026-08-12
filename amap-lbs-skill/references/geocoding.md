# 高德地图地理编码 API

## 服务概述

将结构化地址（省/市/区/街道/门牌号）解析为对应的经纬度坐标。地址结构越完整，解析精度越高。也支持逆地理编码（坐标转地址）。

- **服务标识**: `geocoding`
- **官方文档**: <https://lbs.amap.com/api/webservice/guide/api/georegeo>

## 地理编码（地址 → 坐标）

**GET** `https://restapi.amap.com/v3/geocode/geo`

### 输入参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| key | string | T | 高德 Web 服务 Key | `$AMAP_WEBSERVICE_KEY` |
| address | string | T | 待解析的地址，支持两种格式：1、标准结构化地址；2、"*路与*路交叉口"描述方式 | 北京市朝阳区阜通东大街6号 |
| city | string | | 指定地址所在城市：中文/citycode(010)/adcode(110000)，多城市有同名地址时起过滤作用；不支持县级市 | 北京市 |
| output | string | | 返回格式：JSON / XML，默认 JSON | JSON |
| callback | string | | 回调函数（JSONP） | - |
| appname | string | | 调用来源标识（skill 约定参数） | amap-lbs-skill |

### 请求示例

```bash
curl -s --get "https://restapi.amap.com/v3/geocode/geo" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "address=北京市朝阳区阜通东大街6号" \
  --data-urlencode "city=北京市" \
  --data-urlencode "output=JSON" \
  --data-urlencode "appname=amap-lbs-skill"
```

### 响应解析

```json
{
  "status": "1",
  "info": "OK",
  "geocodes": [
    {
      "formatted_address": "北京市朝阳区望京街道阜通东大街6号",
      "country": "中国",
      "province": "北京市",
      "citycode": "010",
      "city": "北京市",
      "district": "朝阳区",
      "township": "望京街道",
      "adcode": "110105",
      "level": "门牌号",
      "location": "116.481028,39.989643"
    }
  ]
}
```

- `status` 为 `"1"` 表示成功；`geocodes[0].location` 为坐标，格式 `经度,纬度`
- `level` 表示匹配精度：`门牌号` > `道路` > `POI` > `区县` 等
- 多个结果时按匹配度排序，`geocodes[0]` 为最优解
- `count` 字段为解析出的结果数量

## 逆地理编码（坐标 → 地址）

**GET** `https://restapi.amap.com/v3/geocode/regeo`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| key | string | T | - | 高德 Web 服务 Key | `$AMAP_WEBSERVICE_KEY` |
| location | string | T | - | 坐标，格式 `经度,纬度`，小数≤6位 | 116.481028,39.989643 |
| radius | number | | 1000 | 搜索半径（米），范围 0-3000 | 1000 |
| extensions | string | | base | `base` 返回基本地址；`all` 额外返回附近 POI、道路、交叉口 | all |
| poitype | string | | - | 指定附近 POI 类型（需 extensions=all），多个用 `\|` 分隔 | 050000 |
| roadlevel | number | | - | 道路等级过滤（需 extensions=all）：0 全部道路，1 仅主干道 | 1 |
| homeorcorp | number | | 0 | 附近 POI 排序优化（需 extensions=all）：0 不干扰，1 居家优先，2 公司优先 | 1 |
| output | string | | JSON | 返回格式：JSON / XML | JSON |
| appname | string | | - | 调用来源标识（skill 约定参数） | amap-lbs-skill |

### 请求示例

```bash
curl -s --get "https://restapi.amap.com/v3/geocode/regeo" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "location=116.481028,39.989643" \
  --data-urlencode "extensions=all" \
  --data-urlencode "appname=amap-lbs-skill"
```

### 响应解析

```json
{
  "status": "1",
  "regeocode": {
    "formatted_address": "北京市朝阳区望京街道阜通东大街6号",
    "addressComponent": {
      "country": "中国",
      "province": "北京市",
      "city": "北京市",
      "district": "朝阳区",
      "township": "望京街道",
      "streetNumber": { "street": "阜通东大街", "number": "6号" },
      "neighborhood": { "name": "方恒国际中心", "type": "商务住宅;楼宇" }
    },
    "roads": [],
    "roadinters": [],
    "pois": [],
    "aois": []
  }
}
```

- `regeocode.formatted_address` 为结构化地址
- `regeocode.addressComponent` 含各级行政区划（省/市/区/乡镇/街道/门牌）
- `extensions=all` 时额外返回 `pois`（附近兴趣点）、`roads`（道路）、`roadinters`（路口）、`aois`（行政区划面）

## 常见问题

**Q: 如何判断解析精度？**

A: 看 `level` 字段，`门牌号`/`道路` 为高精度，`区县` 为低精度。`geocodes` 为空或 `status != "1"` 说明解析失败，检查 Key 或地址完整性。

**Q: location 坐标顺序？**

A: 高德所有 location 均为 `经度,纬度`（lng,lat），与部分平台相反，注意区分。

**Q: 解析出的坐标发生偏移怎么办？**

A: 偏移原因多为数据挂错节点/索引缺失。处理：
1. 以"地址 + 正确坐标"格式提工单，标题注明"地理编码解析坐标发生偏移"（能提供正确坐标最好）
2. 正常 5 个工作日内修复
3. 若检索的多是 POI 名称（如"首开广场"），建议改用关键字搜索 API（`references/poi_search.md`），避免地址解析的节点误差

