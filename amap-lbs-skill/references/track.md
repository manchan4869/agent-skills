# 高德地图轨迹纠偏 API

## 服务概述

将稀疏的 GPS 轨迹点纠偏到道路上，返回平滑的道路轨迹。适用于轨迹回放、里程统计、物流配送等场景。个人认证每日 10000 次，大批量推荐猎鹰轨迹服务。

> **接口现状**：本文收录的 `/v4/grasproad/driving` 为**现行有效**的轨迹纠偏服务。官方文档明确：**原有"抓路服务" API 已由轨迹纠偏服务替代**——停用的是更早的"抓路服务"（autograsp），不是本接口。详见官方文档注释。

- **服务标识**: `grasproad`
- **官方文档**: <https://lbs.amap.com/api/webservice/guide/api/grasproad>

## API 调用

**POST** `https://restapi.amap.com/v4/grasproad/driving`

> 注意：此接口为 **POST**，业务参数放 body（JSONArray），`key` 放 queryString——与其它 GET 接口完全不同。

## 输入参数

**QueryString：**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| key | string | T | 高德 Web 服务 Key |

**Body（JSONArray，每个 JSONObject 一个定位点）：**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| x | number | T | 经度，小数≤6位 |
| y | number | T | 纬度 |
| ag | number | T | 与正北夹角（0-360 度），非法值易致失败 |
| tm | number | T | 时间（秒）：首点为 1970 年 0 点，后续为相对首点的秒差 |
| sp | number | T | 速度（km/h），不合理值易致失败 |

最多 500 个点。

## 请求示例

```bash
curl -s -X POST "https://restapi.amap.com/v4/grasproad/driving?key=$AMAP_WEBSERVICE_KEY" \
  -H "Content-Type: application/json" \
  -d '[{"x":116.478928,"y":39.997761,"sp":19,"ag":0,"tm":1478031031},{"x":116.478907,"y":39.998422,"sp":10,"ag":0,"tm":2},{"x":116.479384,"y":39.998546,"sp":10,"ag":110,"tm":3}]'
```

## 响应解析

```json
{
  "errcode": 0,
  "errmsg": "OK",
  "data": {
    "distance": 321.5,
    "points": [ { "x": 116.478928, "y": 39.997761 } ]
  }
}
```

- `data.distance`：纠偏后总距离（米）
- `data.points[]`：纠偏后的轨迹点
- `errcode=30001`：抓路失败（通常点数过少/过于稀疏）

## 注意事项

- 定位点间隔 5-10 秒纠偏效果最优
- `ag`（角度）、`sp`（速度）传入非法值大概率导致纠偏失败
