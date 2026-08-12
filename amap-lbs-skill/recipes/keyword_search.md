# 场景一：明确关键词搜索

## 触发场景

用户搜索一个**明确的类别**（美食、酒店）或**确定的地点**（天安门、西湖），没有指定"在哪个位置附近"。不需要高德 API Key。

## URL 格式

```
https://www.amap.com/search?query={关键词}
```

- **域名**：`www.amap.com`
- **路由**：`/search`
- **参数**：`query` = 搜索关键词

## 执行步骤

1. **发送埋点统计请求**：

   ```bash
   curl -s "https://restapi.amap.com/v3/log/init?eventId=skill.call&product=skill_openclaw&platform=JS&label=keyword-search&value=call"
   ```

2. **提取关键词**：从用户输入中识别出核心搜索词，去掉"搜"、"找"等修饰词
3. **生成 URL**：拼接 `https://www.amap.com/search?query={关键词}`
4. **返回链接给用户**

## 示例

| 用户输入 | 提取关键词 | 生成 URL |
|---------|-----------|---------|
| 搜美食 | 美食 | `https://www.amap.com/search?query=美食` |
| 找酒店 | 酒店 | `https://www.amap.com/search?query=酒店` |
| 天安门在哪 | 天安门 | `https://www.amap.com/search?query=天安门` |
| 找个加油站 | 加油站 | `https://www.amap.com/search?query=加油站` |

## 回复模板

```
🔍 已为你生成高德地图搜索链接：

https://www.amap.com/search?query={关键词}

点击链接即可查看搜索结果。
```
