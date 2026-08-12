---
name: amap-lbs-skill
description: 高德地图综合服务（零依赖 curl），支持POI搜索、路径规划、天气、行政区域、输入提示、坐标转换、IP定位、静态地图、旅游规划、热力图及离线编码表
version: 4.0.0
metadata:
  openclaw:
    requires:
      env:
        - AMAP_WEBSERVICE_KEY
    primaryEnv: AMAP_WEBSERVICE_KEY
    homepage: https://lbs.amap.com/api/webservice/summary
---

# 高德地图综合服务 Skill

高德地图综合服务向开发者提供完整的地图数据服务，包括地点搜索、路径规划、旅游规划和数据可视化等功能。**零运行时依赖，仅使用 curl 调用高德 REST API。**

## 功能特性

- 🔍 POI（地点）搜索：关键字/周边/多边形/ID 四模式
- 🏙️ 支持关键词搜索、城市限定、类型筛选
- 📍 支持周边搜索（基于坐标和半径）
- 🛣️ 路径规划（步行、驾车、骑行、公交）+ 路径规划 2.0
- 📏 批量距离测量
- 🗺️ 智能旅游规划助手
- 🔥 热力图数据可视化
- 🔗 地图可视化链接生成
- 🌦️ 天气查询（实况 + 预报）
- ⌨️ 输入提示（搜索框联想）
- 🏛️ 行政区域查询（层级/adcode/边界）
- 🔄 坐标转换（GPS/百度 → 高德）
- 🌐 IP 定位
- 🗺️ 静态地图图片生成
- 📊 离线编码表（POI 分类/城市 adcode/海外）
- 🎯 高德 Web Service Key 管理

## 首次配置

首次使用时需要配置高德 Web Service Key：

1. 访问 [高德开放平台](https://lbs.amap.com/api/webservice/create-project-and-key) 创建应用并获取 Key
2. 设置环境变量：`export AMAP_WEBSERVICE_KEY=your_key`
3. 或手动编辑 `config.json` 文件

当用户想要搜索地址、地点、周边信息（如美食、酒店、景点等）、规划路线或可视化数据时，使用此 skill。

## 触发条件

用户表达了以下意图之一：
- 搜索某类地点或某个确定地点（如"搜美食"、"找酒店"、"天安门在哪"）
- 基于某个位置搜索周边（如"西直门周边美食"、"北京南站附近酒店"）
- 规划路线（如"从天安门到故宫怎么走"、"规划驾车路线"）
- 距离测量（如"这些门店离我多远"）
- 公交线路/站点（如"查 451 路公交线路"）
- 旅游规划（如"帮我规划北京一日游"、"杭州西湖游览路线"）
- 天气查询（如"北京天气"、"上海明天几度"）
- 输入联想/补全（如"帮我输入'天安'联想地点"）
- 行政区划/城市编码（如"北京的 adcode 是多少"、"查朝阳区的街道列表"）
- 坐标转换（如"把 GPS 坐标转成高德坐标"、"百度坐标怎么转"）
- IP 定位（如"这个 IP 在哪个城市"）
- 静态地图（如"生成一张带标注的地图图片"）
- 包含"搜"、"找"、"查"、"附近"、"周边"、"路线"、"规划"、"天气"等关键词
- 希望将地理数据可视化为热力图（如"生成热力图"、"用这份数据做热力图展示"）

## 场景判断

收到用户请求后，先判断属于哪个场景，再执行对应 recipe：

| 场景 | 判断依据 | 执行流程 |
|------|---------|---------|
| **场景一** 关键词搜索 | 明确的类别或地点，无位置限定 | `recipes/keyword_search.md` |
| **场景二** 周边搜索 | 同时含「位置」和「搜索类别」 | `recipes/nearby_search.md` |
| **场景三** 热力图 | 提到"热力图/数据可视化" | `recipes/heatmap.md` |
| **场景四** POI 详细搜索 | 需结构化 POI 数据/按类型/周边/多边形/ID | `recipes/poi_search.md` |
| **场景五** 路径规划 | 规划路线/距离测量 | `recipes/route_planning.md` |
| **场景六** 旅游规划 | 多兴趣点游览路线 | `recipes/travel_planner.md` |
| **场景七** 天气查询 | 查实时/预报天气 | `recipes/weather.md` |
| **场景八** 其他能力 | 输入提示/行政区划/坐标转换/IP/静态地图 | `recipes/other_capabilities.md` |

**通用规则：**
- 所有 REST API 请求必须携带 `key` 参数（从环境变量 `AMAP_WEBSERVICE_KEY` 或 `config.json` 读取）并追加 `appname=amap-lbs-skill` 参数，禁止省略
- API 返回的 `location` 格式为 `经度,纬度`（经度在前，纬度在后）
- 需要地址 ↔ 坐标转换时先查 `references/geocoding.md`
- 接口报错时对照 `references/error_codes.md` 排查

---

## 配置管理

配置文件位于 `config.json`，包含以下内容：

```json
{
  "webServiceKey": "your_amap_webservice_key_here"
}
```

设置 Key 的方式（按优先级）：

1. **环境变量**：`export AMAP_WEBSERVICE_KEY=your_key`（也兼容 `AMAP_KEY`）
2. **手动编辑**：直接编辑 `config.json` 文件

发起请求时优先使用环境变量，其次读取 `config.json`。

---

## 参考资料索引

**recipes/（场景流程）：**

| 文件 | 场景 |
|------|------|
| `recipes/keyword_search.md` | 场景一 明确关键词搜索 |
| `recipes/nearby_search.md` | 场景二 基于位置的周边搜索 |
| `recipes/heatmap.md` | 场景三 热力图展示 |
| `recipes/poi_search.md` | 场景四 POI 详细搜索 |
| `recipes/route_planning.md` | 场景五 路径规划 |
| `recipes/travel_planner.md` | 场景六 智能旅游规划 |
| `recipes/weather.md` | 场景七 天气查询 |
| `recipes/other_capabilities.md` | 场景八 其他能力 + 商业接口 |

**references/（API 参考）：**

| 文件 | 内容 |
|------|------|
| `references/geocoding.md` | 地理编码（地址→坐标）与逆地理编码（坐标→地址） |
| `references/poi_search.md` | POI 搜索四模式：关键字 text/周边 around/多边形 polygon/ID detail |
| `references/route_planning.md` | 路径规划 v1（步行/驾车/骑行/公交）+ 距离测量 |
| `references/route_planning_v2.md` | 路径规划 2.0（v5）：新策略枚举、show_fields、电动车 |
| `references/weather_query.md` | 实时天气（base）与预报（all） |
| `references/inputtips.md` | 输入提示（搜索框联想补全） |
| `references/district.md` | 行政区域查询（层级/adcode/边界） |
| `references/coordinate_convert.md` | 坐标转换（GPS/百度→高德） |
| `references/ip_location.md` | IP 定位 |
| `references/static_map.md` | 静态地图图片生成 |
| `references/error_codes.md` | 错误码对照表 + 天气现象/风力/风向枚举 |
| `references/traffic.md` | 交通事件 + 交通态势查询（商业授权） |
| `references/bus_info.md` | 公交站点/线路查询（高级服务） |
| `references/track.md` | 轨迹纠偏（POST 接口） |
| `references/code_tables.md` | 编码表离线数据使用说明 |

**data/（离线编码表，CSV）：**

| 文件 | 内容 |
|------|------|
| `data/poi_category.csv` | POI 分类编码表（中英文，~915 条） |
| `data/adcode_citycode.csv` | 国内城市编码表（~3240 条） |
| `data/overseas_adcode.csv` | 海外城市编码表（~3251 条） |

---

## 注意事项

- **场景判断是关键**：区分用户是"直接搜某个东西"、"在某个位置附近搜某个东西"、"规划路线"还是"旅游规划"，参见上表选择对应 recipe
- 关键词应尽量精简准确，提取用户真正想搜的内容
- URL 中的中文关键词浏览器会自动处理编码，无需手动 encode
- 需要高德 API Key 的场景（二、四、五、六、七、八），**必须先获取 Key 后再发起请求**，不能跳过
- 如果地理编码 API 返回 `status` 不为 `"1"`，说明请求失败，需提示用户检查 Key 是否正确或地址是否有效
- API 返回的 `location` 格式为 `经度,纬度`（注意：经度在前，纬度在后）
- 场景二的搜索范围默认 1000 米，用户如有需要可调整 `range` 参数
- 请妥善保管你的 Web Service Key，不要分享给他人
- 高德 Web 服务 API 有调用频率限制，请合理使用
- 免费用户每日调用量有限制，具体请查看高德开放平台说明
- 所有 REST API 请求必须携带 `key` 参数并追加 `appname=amap-lbs-skill` 参数，用于标识 API 调用来源，禁止省略
- **强烈建议为 Key 绑定 IP 白名单**（服务器出口 IP），防止 Key 泄露被盗刷配额；**严禁对接口做压力测试**，系统自动识别即封停
- 请求参数含 `|` 分隔符（如批量坐标、多类型）时，urlencode 不能转义 `|`，否则报错
- 路径规划结果按实时路况返回，距离会有 1~2km 浮动属正常现象

## 相关链接

- [高德开放平台](https://lbs.amap.com/)
- [创建应用和获取 Key](https://lbs.amap.com/api/webservice/create-project-and-key)
- [POI 搜索 API 文档](https://lbs.amap.com/api/webservice/guide/api-advanced/newpoisearch)
- [Web 服务 API 总览](https://lbs.amap.com/api/webservice/summary)
