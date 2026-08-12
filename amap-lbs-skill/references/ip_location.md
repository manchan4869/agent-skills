# 高德地图 IP 定位 API

## 服务概述

根据 IP 地址定位所在城市/省份。仅支持国内 IPv4，不支持国外 IP。不传 IP 时自动用请求来源 IP 定位。

- **服务标识**: `ip_location`
- **官方文档**: <https://lbs.amap.com/api/webservice/guide/api/ipconfig>

## API 调用

**GET** `https://restapi.amap.com/v3/ip`

## 输入参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| key | string | T | 高德 Web 服务 Key | `$AMAP_WEBSERVICE_KEY` |
| ip | string | | 待定位 IP（仅支持国内 IPv4）；不填则取请求来源 IP | 114.247.50.2 |
| output | string | | 返回格式 | JSON |
| appname | string | T | 调用来源标识 | amap-lbs-skill |

## 请求示例

```bash
# 指定 IP 定位
curl -s --get "https://restapi.amap.com/v3/ip" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "ip=114.247.50.2" \
  --data-urlencode "appname=amap-lbs-skill"

# 用请求来源 IP 定位（不传 ip 参数）
curl -s --get "https://restapi.amap.com/v3/ip" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "appname=amap-lbs-skill"
```

## 响应解析

```json
{
  "status": "1",
  "info": "OK",
  "infocode": "10000",
  "province": "北京市",
  "city": "北京市",
  "adcode": "110000",
  "rectangle": "115.419537,39.44223;117.507348,41.062872"
}
```

- `status` 为 `"1"` 表示成功
- `province` / `city`：省/市名称（局域网 IP 返回"局域网"，国外/非法 IP 返回空）
- `adcode`：城市 adcode；`rectangle`：城市矩形范围（左下右上坐标对，分号分隔）

## 注意事项

- 免费版 IP 定位精度到城市级，无法精确定位到街道
- 局域网 IP、国外 IP、非法 IP 会返回空 city
