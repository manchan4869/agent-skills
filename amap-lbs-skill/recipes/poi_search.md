# 场景四：POI 详细搜索

## 触发场景

用户搜索地点但需要**结构化结果**（返回 JSON 数据而非链接），或需要按类型/周边/多边形/ID 精确检索 POI。**使用 curl 直接调用 REST API。**

## 执行步骤

1. **发送埋点统计请求**：

   ```bash
   curl -s "https://restapi.amap.com/v3/log/init?eventId=skill.call&product=skill_openclaw&platform=JS&label=poi-search&value=call"
   ```

2. **选择搜索模式**：POI 2.0 提供四种模式，完整参数见 `references/poi_search.md`。

   | 用户需求 | 模式 | 端点 |
   |---------|------|------|
   | 关键词/结构化地址 | 关键字搜索 | `/v5/place/text` |
   | 坐标周边一定范围 | 周边搜索 | `/v5/place/around` |
   | 不规则区域内的 POI | 多边形搜索 | `/v5/place/polygon` |
   | 已知 id 查详情 | ID 搜索 | `/v5/place/detail` |
   | 搜索框补全联想 | 输入提示 | `/v3/assistant/inputtips` |

3. **执行请求**：

   ```bash
   # 关键字搜索（关键词 + 城市）
   curl -s --get "https://restapi.amap.com/v5/place/text" \
     --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
     --data-urlencode "keywords=肯德基" \
     --data-urlencode "region=北京" \
     --data-urlencode "city_limit=true" \
     --data-urlencode "offset=10" \
     --data-urlencode "appname=amap-lbs-skill"

   # 周边搜索（圆心 + 半径）
   curl -s --get "https://restapi.amap.com/v5/place/around" \
     --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
     --data-urlencode "location=116.397428,39.90923" \
     --data-urlencode "radius=1000" \
     --data-urlencode "sortrule=distance" \
     --data-urlencode "appname=amap-lbs-skill"
   ```

4. **解析结果**：`status == "1"` 成功，`pois[]` 含 `name/location/address/type/rating/cost/distance` 等字段（详见 `references/poi_search.md`）。

## 常见错误

- `status != "1"`：检查 `info` 字段，对照 `references/error_codes.md`（10001 key 无效、10003 日超限、20000 参数非法等）
- `show_fields` 未传时评分/营业时间等不返回
