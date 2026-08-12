# 场景八：其他基础能力

输入提示、行政区划、坐标转换、IP 定位、静态地图、路径规划 2.0、距离测量等补充能力。**使用 curl 直接调用 REST API。**

## 输入提示（搜索框联想补全）

适用于"输入关键词给候选建议"场景（如"用户输入'天安'联想出'天安门'"）。完整参数见 `references/inputtips.md`。

```bash
curl -s --get "https://restapi.amap.com/v3/assistant/inputtips" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "keywords=天安" \
  --data-urlencode "city=北京" \
  --data-urlencode "datatype=poi" \
  --data-urlencode "appname=amap-lbs-skill"
```

## 行政区划查询

查询省市区的层级关系、adcode、中心点、边界坐标。完整参数见 `references/district.md`。

```bash
curl -s --get "https://restapi.amap.com/v3/config/district" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "keywords=北京" \
  --data-urlencode "subdistrict=2" \
  --data-urlencode "appname=amap-lbs-skill"
```

## 坐标转换

把 GPS（WGS-84）/百度（BD-09）坐标转为高德（GCJ-02）坐标。完整参数见 `references/coordinate_convert.md`。

```bash
curl -s --get "https://restapi.amap.com/v3/assistant/coordinate/convert" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "locations=116.481499,39.990475" \
  --data-urlencode "coordsys=gps" \
  --data-urlencode "appname=amap-lbs-skill"
```

## IP 定位

根据 IP 定位所在城市。完整参数见 `references/ip_location.md`。

```bash
curl -s --get "https://restapi.amap.com/v3/ip" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "ip=114.247.50.2" \
  --data-urlencode "appname=amap-lbs-skill"
```

## 静态地图

生成带标注/路线/标签的静态地图图片 URL。完整参数见 `references/static_map.md`。

```bash
curl -s --get "https://restapi.amap.com/v3/staticmap" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "location=116.397428,39.90923" \
  --data-urlencode "zoom=13" \
  --data-urlencode "size=400*400" \
  --data-urlencode "markers=mid,0xFF0000:116.397428,39.90923" \
  --data-urlencode "appname=amap-lbs-skill" \
  -o map.png
```

## 路径规划 2.0 / 距离测量

- 路径规划 2.0（v5）端点与策略差异见 `references/route_planning_v2.md`
- 批量距离测量（多个起点到一个终点）见 `references/route_planning.md` 的「距离测量」章节

## 错误码与天气对照

接口失败时对照 `references/error_codes.md` 排查（10001 key 无效、10003 日超限、10004 频率超限、20000 参数非法等），天气现象/风力/风向枚举对照也在此文件。

---

## 商业授权接口（普通 key 无权限）

以下接口需商务工单开通，skill 文档已收录供参考：

| 接口 | 文档 | 权限说明 |
|------|------|---------|
| 交通事件查询 | `references/traffic.md` | 需城市授权，et-api.amap.com |
| 交通态势查询 | `references/traffic.md` | 高级服务，约 41 城市 |
| 公交信息查询 | `references/bus_info.md` | 认证用户有体验配额 |
| 轨迹纠偏 | `references/track.md` | POST 接口，个人 1 万次/日 |
| 高级 IP 定位（v5） | 未收录 | 需商务申请，支持国外 IP |
| 未来路径规划（etd） | 未收录 | 企业开放，查未来 7 天 |
| 智能硬件定位 | 未收录 | 无系统硬件定位 |
| GeoHUB 数据检索 | 未收录 | 企业数据空间检索 |
