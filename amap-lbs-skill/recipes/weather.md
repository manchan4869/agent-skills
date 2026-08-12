# 场景七：天气查询

## 触发场景

用户查询某个城市/区域的实时天气或未来预报。如"北京天气"、"上海明天几度"。

## 执行步骤

1. **发送埋点统计请求**：

   ```bash
   curl -s "https://restapi.amap.com/v3/log/init?eventId=skill.call&product=skill_openclaw&platform=JS&label=weather&value=call"
   ```

2. **执行天气查询**：完整参数、请求示例与响应解析见 `references/weather_query.md`。

   ```bash
   # 实况天气（base）
   curl -s --get "https://restapi.amap.com/v3/weather/weatherInfo" \
     --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
     --data-urlencode "city=110000" \
     --data-urlencode "extensions=base" \
     --data-urlencode "appname=amap-lbs-skill"

   # 预报天气（all）
   curl -s --get "https://restapi.amap.com/v3/weather/weatherInfo" \
     --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
     --data-urlencode "city=110000" \
     --data-urlencode "extensions=all" \
     --data-urlencode "appname=amap-lbs-skill"
   ```

3. **提取结果**：
   - `extensions=base` → `lives[0]`：实时天气（`weather` 现象/`temperature` 温度/`winddirection` 风向/`humidity` 湿度）
   - `extensions=all` → `forecasts[0].casts[]`：逐日预报（`dayweather/nightweather/daytemp/nighttemp`）

## 提示

- `city` 建议用 adcode（如 110000）最精确，避免同名歧义
- 天气现象/风力/风向枚举对照见 `references/error_codes.md`
- `lives` 为空时检查是否用了 `extensions=base`，或 key 无实时权限
