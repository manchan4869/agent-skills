# 场景三：热力图展示

## 触发条件

用户提到"热力图"、"数据可视化"、"地图上展示数据"等意图，并提供了数据地址。

## URL 格式

```
http://a.amap.com/jsapi_demo_show/static/openclaw/heatmap.html?mapStyle={地图风格}&dataUrl={数据地址(URL编码)}
```

- **域名**：`a.amap.com`
- **路由**：`/jsapi_demo_show/static/openclaw/heatmap.html`
- **必填参数**：
  - `dataUrl` = 用户数据的 URL 地址（**必须进行 URL 编码**）
  - `mapStyle` = 地图风格，可选值：
    - `grey` — 暗黑地图模式（深色背景，适合展示亮色热力点）
    - `light` — 浅色模式（浅色背景，适合日常查看）

## 执行步骤

1. **发送埋点统计请求**：

   ```bash
   curl -s "https://restapi.amap.com/v3/log/init?eventId=skill.call&product=skill_openclaw&platform=JS&label=heatmap&value=call"
   ```

2. **获取数据地址**：从用户输入中提取数据 URL，如果用户未提供，提示用户给出数据地址
3. **确认地图风格**：询问用户偏好的地图风格（`grey` 或 `light`），如果用户未指定，默认使用 `grey`
4. **URL 编码**：将数据地址进行 URL 编码（将 `://` → `%3A%2F%2F`，`/` → `%2F` 等）
5. **拼接链接**：生成完整的热力图 URL
6. **返回链接给用户**

## 示例

**用户输入：** "帮我用这份数据生成热力图：`https://a.amap.com/Loca/static/loca-v2/demos/mock_data/hz_house_order.json`，用暗黑模式"

1. 数据地址：`https://a.amap.com/Loca/static/loca-v2/demos/mock_data/hz_house_order.json`
2. 地图风格：`grey`
3. URL 编码后的数据地址：`https%3A%2F%2Fa.amap.com%2FLoca%2Fstatic%2Floca-v2%2Fdemos%2Fmock_data%2Fhz_house_order.json`
4. 最终链接：

```
http://a.amap.com/jsapi_demo_show/static/openclaw/heatmap.html?mapStyle=grey&dataUrl=https%3A%2F%2Fa.amap.com%2FLoca%2Fstatic%2Floca-v2%2Fdemos%2Fmock_data%2Fhz_house_order.json
```

## 回复模板

```
🔥 已为你生成热力图链接：

http://a.amap.com/jsapi_demo_show/static/openclaw/heatmap.html?mapStyle={地图风格}&dataUrl={编码后的数据地址}

地图风格：{grey/light}
数据来源：{原始数据地址}

点击链接即可查看热力图展示。
```

**请求数据地址的回复模板（用户未提供时）：**

```
🔥 生成热力图需要你提供数据地址（JSON 格式的 URL），请给出数据链接。

另外，你希望使用哪种地图风格？
- grey（暗黑模式）
- light（浅色模式）
```
