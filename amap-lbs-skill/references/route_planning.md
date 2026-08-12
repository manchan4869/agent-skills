# 高德地图路径规划 API

## 服务概述

根据起终点坐标规划不同出行方式的路线：步行、驾车、骑行、公交（含步行换乘）。返回距离、耗时、路线分段、途经点、费用等信息。

- **服务标识**: `route_planning`
- **官方文档**: <https://lbs.amap.com/api/webservice/guide/api/direction>

## 各出行方式 API 端点

| 路线类型 | API 端点 | 成功判断字段 |
|---------|---------|-------------|
| walking 步行 | `https://restapi.amap.com/v3/direction/walking` | `status == "1"` |
| driving 驾车 | `https://restapi.amap.com/v3/direction/driving` | `status == "1"` |
| riding 骑行 | `https://restapi.amap.com/v4/direction/bicycling` | `errcode == 0` |
| transfer 公交 | `https://restapi.amap.com/v3/direction/transit/integrated` | `status == "1"` |

**通用参数（所有端点）：**

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| key | string | T | 高德 Web 服务 Key | `$AMAP_WEBSERVICE_KEY` |
| origin | string | T | 起点坐标 `经度,纬度` | 116.397428,39.90923 |
| destination | string | T | 终点坐标 `经度,纬度` | 116.427281,39.903719 |
| appname | string | T | 调用来源标识 | amap-lbs-skill |

---

## 1. 驾车路线规划

**GET** `https://restapi.amap.com/v3/direction/driving`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| strategy | number | | 0 | 驾车策略（v1）：0-9 单方案，10-20 多方案。0 速度优先、1 费用优先、2 距离优先、3 不走高速、4 躲避拥堵、5 不走高速且躲避拥堵、6 高速优先且躲避拥堵、7 不走高速且躲避拥堵且费用优先、10 综合推荐 |
| waypoints | string | | - | 途经点坐标，多个用 `;` 分隔，最多 16 个 |
| extensions | string | T | - | `base` 返回基本路径信息，`all` 返回详细分段与导航指引（官方标注必填） |
| originid | string | | - | 起点 POI id，起点为 POI 时建议填写提升精度 |
| destinationid | string | | - | 终点 POI id，同上 |
| avoidpolygons | string | | - | 避让区域，多个坐标点对闭合多边形，最多 32 个/16 顶点 |
| avoidroad | string | | - | 避让道路名称，只支持一条 |
| province | string | | - | 车牌省份简称（汉字，如"京"），配合 number 判断限行 |
| number | string | | - | 车牌字母数字（大写，不含省份），支持 6 位传统/7 位新能源 |
| cartype | number | | - | 车辆类型：0 普通汽车，1 纯电，2 插电混动 |
| ferry | number | | - | 是否避开轮渡：0 用轮渡，1 不用 |
| nosteps | number | | - | 设为 1 时响应不含 steps |

### 请求示例

```bash
curl -s --get "https://restapi.amap.com/v3/direction/driving" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "origin=116.301449,40.050881" \
  --data-urlencode "destination=116.453903,39.931370" \
  --data-urlencode "strategy=10" \
  --data-urlencode "extensions=base" \
  --data-urlencode "appname=amap-lbs-skill"
```

### 响应解析

```json
{
  "status": "1",
  "route": {
    "origin": "116.301449,40.050881",
    "destination": "116.453903,39.931370",
    "taxi_cost": "80",
    "paths": [
      {
        "distance": "27135",
        "duration": "3314",
        "strategy": "速度最快",
        "tolls": "0",
        "traffic_lights": "5",
        "steps": [ { "instruction": "沿XX路行驶...", "road": "XX路" } ]
      }
    ]
  }
}
```

- `route.taxi_cost`：打车预估费用（元）
- `route.paths[0].distance`：距离（米）；`duration`：耗时（秒）；`tolls`：过路费（元）；`traffic_lights`：红绿灯数
- `extensions=all` 时 `paths[0].steps[]` 含每段导航指引（`instruction` 文字指令、`road` 道路名、`distance`、`duration`）

---

## 2. 步行路线规划

**GET** `https://restapi.amap.com/v3/direction/walking`

### 输入参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| origin | string | T | 起点坐标 |
| destination | string | T | 终点坐标 |

### 请求示例

```bash
curl -s --get "https://restapi.amap.com/v3/direction/walking" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "origin=116.397428,39.90923" \
  --data-urlencode "destination=116.427281,39.903719" \
  --data-urlencode "appname=amap-lbs-skill"
```

### 响应解析

- `route.paths[0].distance`：距离（米）；`duration`：耗时（秒）
- `route.paths[0].steps[]`：分段步导（`instruction` 文字指令）

---

## 3. 骑行路线规划

**GET** `https://restapi.amap.com/v4/direction/bicycling`

### 输入参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| origin | string | T | 起点坐标 |
| destination | string | T | 终点坐标 |

### 请求示例

```bash
curl -s --get "https://restapi.amap.com/v4/direction/bicycling" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "origin=116.397428,39.90923" \
  --data-urlencode "destination=116.427281,39.903719" \
  --data-urlencode "appname=amap-lbs-skill"
```

### 响应解析

- 成功判断用 `errcode == 0`（注意与驾车/步行的 `status` 不同）
- `data.paths[0].distance`：距离（米）；`data.paths[0].cost.duration`：耗时（秒）

---

## 4. 公交路线规划

**GET** `https://restapi.amap.com/v3/direction/transit/integrated`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| city | string | T | - | 起点城市：名称/citycode（如 010）/adcode |
| cityd | string | | - | 终点城市（跨城公交必填），格式同 city |
| strategy | number | | 0 | 公交策略：0 最快捷，1 最经济，2 最少换乘，3 最少步行，5 不乘地铁 |
| nightflag | number | | 0 | 是否计算夜班车（0/1） |
| date | string | | - | 出发日期，`yyyy-mm-dd` |
| time | string | | - | 出发时间（24 小时制，如 22:34） |
| extensions | string | | base | `base` 基本信息，`all` 详细分段 |

### 请求示例

```bash
curl -s --get "https://restapi.amap.com/v3/direction/transit/integrated" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "origin=116.301449,40.050881" \
  --data-urlencode "destination=116.453903,39.931370" \
  --data-urlencode "city=北京" \
  --data-urlencode "strategy=0" \
  --data-urlencode "appname=amap-lbs-skill"
```

### 响应解析

```json
{
  "status": "1",
  "route": {
    "transits": [
      {
        "cost": "6.0",
        "duration": "4254",
        "walking_distance": "680",
        "steps": [
          { "walking": { "distance": "680", "duration": "600" } },
          { "bus": { "buslines": [ { "name": "地铁10号线", "departure_stop": "上地站" } ] } }
        ]
      }
    ]
  }
}
```

- `route.transits[0].cost`：费用（元）；`duration`：总耗时（秒）；`walking_distance`：步行距离（米）
- `steps[]` 按序分段：`walking`（步行）、`bus`（公交/地铁，含 `buslines[]` 线路名与起止站）
- 多套方案时 `transits[]` 按推荐度排序

---

## 5. 距离测量

批量计算一组点到目标点的距离和耗时。适用于"哪个门店离我最近"类场景。

**GET** `https://restapi.amap.com/v3/distance`

### 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| key | string | T | - | 高德 Web 服务 Key |
| origins | string | T | - | 起点坐标组，多个用 `\|` 分隔，最多 100 个 |
| destination | string | T | - | 终点坐标 `经度,纬度` |
| type | number | | 1 | 距离类型：0 直线距离，1 驾车导航距离，3 步行距离（≤5km） |
| appname | string | T | - | 调用来源标识 |

### 请求示例

```bash
curl -s --get "https://restapi.amap.com/v3/distance" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "origins=116.481028,39.989643|116.465302,40.004717" \
  --data-urlencode "destination=116.427281,39.903719" \
  --data-urlencode "type=1" \
  --data-urlencode "appname=amap-lbs-skill"
```

### 响应解析

- `results[]` 与 origins 一一对应：`origin_id`、`dest_id`、`distance`（米）、`duration`（秒）、`info`、`code`

---

## 常见问题

**Q: 如何选择驾车策略？**

A: 默认 `strategy=10`（综合推荐）。赶时间用 0（速度优先），省钱用 1（费用优先），走高速用 6。

**Q: 骑行接口返回结构与其他不同？**

A: 骑行 v4 接口用 `errcode` 和 `data.paths`，成功条件是 `errcode==0`，与 v3 接口的 `status`/`route` 不同，解析时注意区分。

**Q: 公交支持指定出发/到达时间吗？**

A: 支持。`date` + `time` 指定时刻，`datatype=1` 时 `time` 表示期望到达时间。

**Q: 获取到的距离/耗时为什么会变动？**

A: 正常现象。路径规划按实时路况返回结果，距离会有 1~2km 浮动，耗时随路况波动更明显。同一路线不同时刻请求结果可能不同。

**Q: polyline 道路节点的选取规则？**

A: 根据路线情况每隔一段距离取一个点，取点间隔/密度随路况变化（拥堵段取点更密）。
