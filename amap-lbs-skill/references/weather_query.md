# 高德地图天气查询 API

## 服务概述

通过城市 adcode/citycode 查询天气。**base 返回实况天气，all 返回预报天气**。实况每小时多次更新，预报每天 8/11/18 点更新约 3 次，以 `reporttime` 字段为准。

- **服务标识**: `weather`
- **官方文档**: <https://lbs.amap.com/api/webservice/guide/api-advanced/weatherinfo>

## API 调用

**GET** `https://restapi.amap.com/v3/weather/weatherInfo`

## 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|--------|------|------|--------|------|------|
| key | string | T | - | 高德 Web 服务 Key | `$AMAP_WEBSERVICE_KEY` |
| city | string | T | - | 城市 adcode（建议，精确），也支持 citycode/城市名。编码表见 `data/adcode_citycode.csv` 或 `references/code_tables.md` | 110000 |
| extensions | string | | base | `base` 返回实况天气（lives）；`all` 返回预报天气（forecasts） | all |
| output | string | | JSON | 返回格式 | JSON |
| appname | string | | - | 调用来源标识（skill 约定参数） | amap-lbs-skill |

## 请求示例

```bash
# 实况天气（extensions=base）
curl -s --get "https://restapi.amap.com/v3/weather/weatherInfo" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "city=110000" \
  --data-urlencode "extensions=base" \
  --data-urlencode "appname=amap-lbs-skill"

# 预报天气（extensions=all）
curl -s --get "https://restapi.amap.com/v3/weather/weatherInfo" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "city=110000" \
  --data-urlencode "extensions=all" \
  --data-urlencode "appname=amap-lbs-skill"
```

## 响应解析

```json
{
  "status": "1",
  "count": "1",
  "info": "OK",
  "lives": [
    {
      "province": "北京",
      "city": "北京市",
      "adcode": "110000",
      "weather": "晴",
      "temperature": "34",
      "winddirection": "西南",
      "windpower": "3",
      "humidity": "46",
      "reporttime": "2026-08-05 13:00:00"
    }
  ],
  "forecasts": [
    {
      "city": "北京市",
      "adcode": "110000",
      "province": "北京",
      "reporttime": "2026-08-05 13:03:03",
      "casts": [
        {
          "date": "2026-08-05",
          "week": "3",
          "dayweather": "多云",
          "nightweather": "晴",
          "daytemp": "35",
          "nighttemp": "25",
          "daywind": "南",
          "nightwind": "南",
          "daypower": "1-3",
          "nightpower": "1-3"
        }
      ]
    }
  ]
}
```

### 字段说明

**实况天气 `lives[0]`（extensions=base）：**
- `weather`：天气现象（晴/多云/雨等，枚举见天气对照表）
- `temperature`：温度（℃）
- `winddirection` / `windpower`：风向 / 风力等级
- `humidity`：相对湿度（%）
- `reporttime`：数据发布时间

**预报 `forecasts[0].casts[]`（extensions=all）：**
- `date` / `week`：日期 / 星期
- `dayweather` / `nightweather`：白天 / 夜间天气
- `daytemp` / `nighttemp`：白天 / 夜间温度（℃）
- `daywind` / `nightwind`：白天 / 夜间风向
- `daypower` / `nightpower`：白天 / 夜间风力

## 常见问题

**Q: extensions=base 和 all 有什么区别？**

A: `base` 返回实况天气（`lives[]`）；`all` 返回预报天气（`forecasts[]`）。两者需分别请求，响应无"天气指数"字段。

**Q: city 支持哪些格式？**

A: 建议使用城市 adcode（如 110000），最精确避免同名歧义；也支持 citycode（010）和城市名称。

**Q: lives 为空怎么办？**

A: 检查是否设置了 `extensions=base`（base 才返回 lives）；仍为空则可能该 key 无实时天气权限。

