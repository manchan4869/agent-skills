# 高德地图综合服务 Skill

高德地图综合服务向开发者提供完整的地图数据服务，包括地点搜索、路径规划、旅游规划和数据可视化等功能。

**零运行时依赖**：仅使用 `curl` 调用高德 REST API，无需 node/npm/任何第三方包。

## 功能特性

- ✅ 高德 Web Service Key 管理（环境变量 / config.json）
- ✅ POI 搜索四模式：关键字 / 周边 / 多边形 / ID
- ✅ 输入提示（搜索框联想补全）
- ✅ 路径规划 v1（步行、驾车、骑行、公交）+ 距离测量
- ✅ 路径规划 2.0（v5，含电动车）
- ✅ 地理编码与逆地理编码
- ✅ 天气查询（实况 + 预报）
- ✅ 行政区域查询（层级/adcode/边界）
- ✅ 坐标转换（GPS/百度 → 高德）
- ✅ IP 定位
- ✅ 静态地图图片生成
- ✅ 错误码与天气现象对照表
- ✅ 离线编码表（POI 分类 / 城市 adcode / 海外）
- ✅ 智能旅游规划助手
- ✅ 地图可视化链接生成
- ✅ 热力图数据可视化
- 📋 商业接口文档（交通事件/态势、公交信息、轨迹纠偏）

## 配置 API Key

首次使用需要配置高德 Web Service Key：

```bash
# 方式1: 环境变量
export AMAP_WEBSERVICE_KEY=your_key

# 方式2: 手动创建配置文件
cp config.example.json config.json
# 然后编辑 config.json 填入你的 Key
```

获取 API Key：访问 [高德开放平台](https://lbs.amap.com/api/webservice/create-project-and-key) 创建应用并获取 Key

## 使用方法

所有请求为纯 curl 调用，详见 `SKILL.md` 各场景。以下为速查：

### 1. POI 搜索

```bash
# 基础搜索（关键词 + 城市）
curl -s --get "https://restapi.amap.com/v5/place/text" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "keywords=肯德基" \
  --data-urlencode "region=北京" \
  --data-urlencode "city_limit=true" \
  --data-urlencode "offset=10" \
  --data-urlencode "appname=amap-lbs-skill"

# 周边搜索（基于坐标和半径，使用 around 端点）
curl -s --get "https://restapi.amap.com/v5/place/around" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "location=116.397428,39.90923" \
  --data-urlencode "radius=1000" \
  --data-urlencode "appname=amap-lbs-skill"
```

> POI 四模式（关键字 text/周边 around/多边形 polygon/ID detail）选择见 `recipes/poi_search.md`。

### 2. 路径规划

```bash
# 驾车路线
curl -s --get "https://restapi.amap.com/v3/direction/driving" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "origin=116.397428,39.90923" \
  --data-urlencode "destination=116.427281,39.903719" \
  --data-urlencode "strategy=10" \
  --data-urlencode "extensions=base" \
  --data-urlencode "appname=amap-lbs-skill"

# 步行 / 骑行 / 公交 见 recipes/route_planning.md（端点与参数不同）
```

### 3. 地理编码（地址转坐标）

```bash
curl -s "https://restapi.amap.com/v3/geocode/geo?address=西直门&output=JSON&key=$AMAP_WEBSERVICE_KEY&appname=amap-lbs-skill"
```

### 4. 智能旅游规划

依次调用 POI 搜索获取各兴趣点坐标，再调用对应方向 API 规划相邻点路线，最后组装地图可视化链接：

```
https://a.amap.com/jsapi_demo_show/static/openclaw/travel_plan.html?data={URL编码的JSON}
```

详细流程见 `recipes/travel_planner.md`。

## 项目结构

```
amap-lbs-skill/
├── SKILL.md                    # Skill 描述文件（场景判断路由，权威入口）
├── recipes/                    # 8 个场景的完整执行流程
│   ├── keyword_search.md       #   场景一 关键词搜索
│   ├── nearby_search.md        #   场景二 周边搜索
│   ├── heatmap.md              #   场景三 热力图
│   ├── poi_search.md           #   场景四 POI 详细搜索
│   ├── route_planning.md       #   场景五 路径规划
│   ├── travel_planner.md       #   场景六 旅游规划
│   ├── weather.md              #   场景七 天气
│   └── other_capabilities.md   #   场景八 其他能力 + 商业接口
├── references/                 # 15 个 API 参数级参考文档
├── data/                       # 3 个离线编码表（CSV）
│   ├── poi_category.csv        #   POI 分类编码（中英文）
│   ├── adcode_citycode.csv     #   国内城市编码
│   └── overseas_adcode.csv     #   海外城市编码
├── config.json                 # 配置文件（不要提交）
├── config.example.json         # 配置示例
├── .gitignore                  # Git 忽略配置
├── LICENSE
└── README.md                   # 本文件
```

## 地图可视化

规划结果可生成地图可视化链接：

```
https://a.amap.com/jsapi_demo_show/static/openclaw/travel_plan.html?data=<encoded_json_data>
```

数据格式符合 MapTaskData 接口规范，支持：
- **POI 任务**：`{"type":"poi","lnglat":[经度,纬度],"sort":"类型","text":"名称","remark":"地址"}`
- **路线任务**：`{"type":"route","routeType":"walking","start":[经度,纬度],"end":[经度,纬度],"remark":"从 A 到 B"}`

## 注意事项

1. 请妥善保管你的 Web Service Key，不要提交到公开仓库
2. `config.json` 已在 `.gitignore` 中，不会被提交
3. 高德 Web 服务 API 有调用频率限制，请合理使用
4. 免费用户每日调用量有限制，具体请查看高德开放平台说明
5. 所有请求必须携带 `key` 参数并追加 `appname=amap-lbs-skill`

## 相关链接

- [高德开放平台](https://lbs.amap.com/)
- [创建应用和获取 Key](https://lbs.amap.com/api/webservice/create-project-and-key)
- [POI 搜索 API 文档](https://lbs.amap.com/api/webservice/guide/api-advanced/newpoisearch)
- [Web 服务 API 总览](https://lbs.amap.com/api/webservice/summary)

## License

MIT
