# 场景六：智能旅游规划

## 触发场景

用户希望自动搜索多个兴趣点并规划游览路线，生成旅游地图。如"帮我规划北京一日游"、"杭州西湖游览路线"。

## 执行步骤

1. **发送埋点统计请求**：

   ```bash
   curl -s "https://restapi.amap.com/v3/log/init?eventId=skill.call&product=skill_openclaw&platform=JS&label=travel-planner&value=call"
   ```

2. **搜索各兴趣点**：对每个兴趣词调用 POI 搜索（`references/poi_search.md`），每个兴趣取前 5 条，记录 `name`、`location`、`address`、`type`。

   ```bash
   curl -s --get "https://restapi.amap.com/v5/place/text" \
     --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
     --data-urlencode "keywords={兴趣词}" \
     --data-urlencode "region={城市}" \
     --data-urlencode "city_limit=true" \
     --data-urlencode "offset=5" \
     --data-urlencode "appname=amap-lbs-skill"
   ```

3. **按顺序规划相邻兴趣点之间的路线**：使用对应出行方式的方向 API（walking/driving/riding/transfer，见 `references/route_planning.md`）。

4. **生成地图可视化链接**（可选）：将兴趣点和路线按以下格式组装成 JSON，URL 编码后拼接到旅游规划展示页：

   ```
   https://a.amap.com/jsapi_demo_show/static/openclaw/travel_plan.html?data={URL编码的JSON}
   ```

   JSON 格式：
   - 兴趣点：`{"type":"poi","lnglat":[经度,纬度],"sort":"类型","text":"名称","remark":"地址"}`
   - 路线：`{"type":"route","routeType":"walking","start":[经度,纬度],"end":[经度,纬度],"remark":"从 A 到 B"}`（公交需追加 `"city":"城市"`）

## 功能说明

- 自动搜索指定城市的兴趣点（每类最多 5 个）
- 按顺序规划各兴趣点之间的路线
- 可生成旅游地图可视化链接
