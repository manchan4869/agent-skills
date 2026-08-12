# 高德地图 POI 搜索 API

## 服务概述

POI 搜索 2.0 提供四种搜索模式，均返回名称、地址、坐标、类型、电话、评分、距离等信息：

| 模式 | 端点 | 适用场景 |
|------|------|---------|
| 关键字搜索 | `GET /v5/place/text` | 文本关键词/结构化地址检索 |
| 周边搜索 | `GET /v5/place/around` | 以圆心+半径检索 |
| 多边形搜索 | `GET /v5/place/polygon` | 任意多边形区域检索 |
| ID 搜索 | `GET /v5/place/detail` | 已知 POI id 查详情 |

> 注意：同请求参数翻页最多支持 200 条数据，不支持全量返回。
> 返回的 POI 字段中，`children/business/indoor/navi/photos` 等需通过 `show_fields` 参数指定才返回。

- **服务标识**: `poi_search`
- **官方文档**: <https://lbs.amap.com/api/webservice/guide/api-advanced/newpoisearch>

---

## 模式一：关键字搜索

**GET** `https://restapi.amap.com/v5/place/text`

## 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| key | string | T | - | 高德 Web 服务 Key | `$AMAP_WEBSERVICE_KEY` |
| keywords | string | T | - | 检索关键词。规则：多个关键词用 `|` 分隔；关键词可设类型（`关键词:类型`）；citylimit=true 时必填；默认只要 keywords、types、location 中一项即可 | 肯德基 |
| types | string | | - | POI 类型编码，多个用 `\|` 分隔，可设子类型。编码表见 `data/poi_category.csv` 或 `references/code_tables.md` | 050000 |
| region | string | | - | 城市名称或 adcode，默认全国搜索 | 北京 |
| city_limit | boolean | | false | 是否仅返回城市内数据（true/false），true 时 keywords 必填 | true |
| location | string | | - | 中心点坐标 `经度,纬度`，配合 radius 做周边搜索 | 116.397428,39.90923 |
| radius | number | | - | 周边搜索半径（米），默认无限制 | 1000 |
| sortrule | string | | - | 排序规则：`distance`（距离最近，需 location）或 `weight`（综合权重，默认） | distance |
| page | number | | 1 | 页码 | 1 |
| offset | number | | 20 | 每页记录数，**最大 25** | 10 |
| show_fields | string | | - | 额外返回字段，逗号分隔：`business`（营业状态）、`photos`（图片）、`rating`（评分）、`cost`（人均）等 | business,rating |
| output | string | | JSON | 返回格式 | JSON |
| appname | string | | - | 调用来源标识，必填 | amap-lbs-skill |

## 请求示例

**基础搜索（关键词 + 城市）：**

```bash
curl -s --get "https://restapi.amap.com/v5/place/text" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "keywords=肯德基" \
  --data-urlencode "region=北京" \
  --data-urlencode "city_limit=true" \
  --data-urlencode "offset=10" \
  --data-urlencode "appname=amap-lbs-skill"
```

**周边搜索（坐标 + 半径 + 距离排序）：**

```bash
curl -s --get "https://restapi.amap.com/v5/place/text" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "keywords=酒店" \
  --data-urlencode "location=116.397428,39.90923" \
  --data-urlencode "radius=1000" \
  --data-urlencode "sortrule=distance" \
  --data-urlencode "appname=amap-lbs-skill"
```

**按类型搜索 + 评分/营业状态：**

```bash
curl -s --get "https://restapi.amap.com/v5/place/text" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "types=060100" \
  --data-urlencode "region=北京" \
  --data-urlencode "show_fields=business,rating,cost" \
  --data-urlencode "appname=amap-lbs-skill"
```

## 响应解析

```json
{
  "status": "1",
  "info": "OK",
  "count": "520",
  "pois": [
    {
      "name": "星巴克咖啡(某店)",
      "id": "B000A7BD4D",
      "location": "116.394158,39.999868",
      "address": "北京市朝阳区某街9号",
      "type": "餐饮服务;咖啡厅",
      "tel": "010-12345678",
      "distance": 320,
      "business": "营业中",
      "rating": "4.5",
      "cost": "32.00"
    }
  ]
}
```

- `status` 为 `"1"` 表示成功，`count` 为结果总数，`pois[]` 为结果列表
- 每条 POI：`name`（名称）、`location`（坐标，`经度,纬度`）、`address`（地址）、`type`（类型）、`tel`（电话）、`distance`（距中心距离，周边搜索时返回）
- `show_fields` 未开启时 `business/rating/cost/photos` 等不返回
- 失败时检查 `status` 与 `info` 字段（如 `QUOTA_EXHAUSTED` 为配额超限，`INVALID_USER_KEY` 为 Key 无效）

---

## 模式二：周边搜索

以指定坐标为中心，按半径检索周边 POI。

**GET** `https://restapi.amap.com/v5/place/around`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| key | string | T | - | 高德 Web 服务 Key | `$AMAP_WEBSERVICE_KEY` |
| location | string | T | - | 中心点坐标 `经度,纬度` | 116.397428,39.90923 |
| keywords | string | | - | 检索关键词（可选，与 types 至少传一个） | 肯德基 |
| types | string | | - | POI 类型编码，多个用 `\|` 分隔；keywords/types 均空时默认 050000+070000+120000 | 050000 |
| radius | number | | 5000 | 搜索半径（米），范围 0-50000 | 1000 |
| sortrule | string | | distance | 排序：`distance`（距离）或 `weight`（综合权重） | distance |
| region | string | | - | 区域限制，配合 city_limit 使用 | 北京 |
| city_limit | boolean | | false | 仅召回 region 内数据 | true |
| show_fields | string | | - | 附加返回字段：business,rating,cost 等 | business,rating |
| page_size | number | | 10 | 每页条数 1-25 | 10 |
| page_num | number | | 1 | 页码 | 1 |
| output | string | | JSON | 返回格式 | JSON |
| appname | string | T | - | 调用来源标识 | amap-lbs-skill |

### 请求示例

```bash
curl -s --get "https://restapi.amap.com/v5/place/around" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "location=116.397428,39.90923" \
  --data-urlencode "radius=1000" \
  --data-urlencode "sortrule=distance" \
  --data-urlencode "keywords=咖啡" \
  --data-urlencode "show_fields=business,rating,cost" \
  --data-urlencode "appname=amap-lbs-skill"
```

### 响应解析

- 与关键字搜索相同：`status/count/pois[]`
- `pois[].distance`：距中心点距离（米），按 sortrule 排序

---

## 模式三：多边形搜索

检索任意多边形区域内的 POI。

**GET** `https://restapi.amap.com/v5/place/polygon`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| key | string | T | - | 高德 Web 服务 Key | `$AMAP_WEBSERVICE_KEY` |
| polygon | string | T | - | 多边形坐标对，用 `\|` 分隔；矩形可传左上右下两顶点，其他形状首尾需相同 | `116.460988,40.006919\|116.48231,40.007381\|...` |
| keywords | string | | - | 检索关键词（与 types 至少传一个） | 肯德基 |
| types | string | | - | POI 类型编码，多个用 `\|` 分隔；默认 120000+150000 | 050000 |
| show_fields | string | | - | 附加返回字段 | business,rating |
| page_size | number | | 10 | 每页条数 1-25 | 10 |
| page_num | number | | 1 | 页码 | 1 |
| output | string | | JSON | 返回格式 | JSON |
| appname | string | T | - | 调用来源标识 | amap-lbs-skill |

### 请求示例

```bash
curl -s --get "https://restapi.amap.com/v5/place/polygon" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "polygon=116.460988,40.006919|116.48231,40.007381|116.47516,39.99713|116.472596,39.985227|116.45669,39.984989|116.460988,40.006919" \
  --data-urlencode "keywords=肯德基" \
  --data-urlencode "appname=amap-lbs-skill"
```

---

## 模式四：ID 搜索

通过 POI id 查询指定地点详情。id 可通过关键字搜索、周边搜索或输入提示接口获取。

**GET** `https://restapi.amap.com/v5/place/detail`

### 输入参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| key | string | T | 高德 Web 服务 Key | `$AMAP_WEBSERVICE_KEY` |
| id | string | T | POI 唯一标识，最多 10 个，用 `\|` 分隔 | B0FFF2Q42K |
| show_fields | string | | 附加返回字段 | business,rating,cost |
| output | string | | 返回格式 | JSON |
| appname | string | T | 调用来源标识 | amap-lbs-skill |

### 请求示例

```bash
curl -s --get "https://restapi.amap.com/v5/place/detail" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "id=B0FFF2Q42K" \
  --data-urlencode "show_fields=business,rating,cost" \
  --data-urlencode "appname=amap-lbs-skill"
```

### 响应解析

- `count` 为返回的 POI 数，`pois[0]` 为详情
- 开启 `show_fields=business` 后有营业时间（`opentime_today/opentime_week`）、电话（`tel`）；`rating` 为评分，`cost` 为人均消费

---

**Q: 一次最多能拿多少条结果？**

A: `offset` 最大 25。需要更多结果时翻页（page 递增）。

**Q: keywords / types / location 如何取舍？**

A: 三选一即可发起请求。关键词精确搜索用 keywords；按行业分类用 types；按范围用 location+radius。

**Q: 如何确保结果都在指定城市内？**

A: 同时传 `region` 和 `city_limit=true`，可严格限制召回城市内数据。

**Q: 指定多个类型时结果反而比单一类型少？**

A: 正常现象，原因是**子 POI 聚合到父 POI 之下**。例如多边形搜索 `type=150501`（地铁出入口）返回 15 条，而 `type=150500|150501`（地铁站+出入口）只返回 4 条——多类型请求召回了地铁主站，出入口被聚合到主站 POI 上，结果数变少。搜索时注意父/子类型对结果量的影响。
