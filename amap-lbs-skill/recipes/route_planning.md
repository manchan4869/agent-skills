# 场景五：路径规划

## 触发场景

用户规划不同出行方式的路线（驾车/步行/骑行/公交），或批量测量距离。**使用 curl 直接调用高德方向 API。**

## 执行步骤

1. **发送埋点统计请求**：

   ```bash
   curl -s "https://restapi.amap.com/v3/log/init?eventId=skill.call&product=skill_openclaw&platform=JS&label=route-planning&value=call"
   ```

2. **选择出行方式**：完整参数、请求示例与响应解析见 `references/route_planning.md`。

   | 路线类型 | API 端点 | 成功判断字段 |
   |---------|---------|-------------|
   | walking 步行 | `https://restapi.amap.com/v3/direction/walking` | `status == "1"` |
   | driving 驾车 | `https://restapi.amap.com/v3/direction/driving` | `status == "1"` |
   | riding 骑行 | `https://restapi.amap.com/v4/direction/bicycling` | `errcode == 0` |
   | transfer 公交 | `https://restapi.amap.com/v3/direction/transit/integrated` | `status == "1"` |
   | 距离测量 | `https://restapi.amap.com/v3/distance` | `status == "1"` |

3. **执行请求**：

   ```bash
   # 驾车路线
   curl -s --get "https://restapi.amap.com/v3/direction/driving" \
     --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
     --data-urlencode "origin=116.397428,39.90923" \
     --data-urlencode "destination=116.427281,39.903719" \
     --data-urlencode "strategy=10" \
     --data-urlencode "extensions=base" \
     --data-urlencode "appname=amap-lbs-skill"

   # 批量距离测量（多起点→一终点）
   curl -s --get "https://restapi.amap.com/v3/distance" \
     --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
     --data-urlencode "origins=116.481028,39.989643|116.465302,40.004717" \
     --data-urlencode "destination=116.427281,39.903719" \
     --data-urlencode "type=1" \
     --data-urlencode "appname=amap-lbs-skill"
   ```

4. **解析结果**：
   - 驾车/步行：`route.paths[0].distance`（米）、`duration`（秒）、`tolls`（过路费）
   - 公交：`route.transits[0].cost/duration/walking_distance`
   - 距离测量：`results[]` 与 origins 一一对应，含 `distance/duration`

## 高级用法

- **路径规划 2.0（v5）**：新策略枚举、show_fields 机制、电动车规划，见 `references/route_planning_v2.md`
- **路线详情**：驾车 `extensions=all` 返回每段导航指引（instruction/road/polyline/tmcs 实时路况）

## 常见错误

- `status != "1"`：对照 `references/error_codes.md`，`20800` 不在中国大陆、`20801` 附近无道路、`20802` 路线计算失败
- 骑行接口成功判断是 `errcode == 0`（与其它不同）
