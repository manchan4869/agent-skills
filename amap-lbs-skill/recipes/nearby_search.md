# 场景二：基于位置的周边搜索

## 触发场景

用户搜索**某个位置周边**的某类地点，输入中同时包含「位置」和「搜索类别」两个要素（如"西直门周边美食"、"北京南站附近酒店"）。

**前置条件：** 需要用户提供高德开放平台的 API Key。

## 执行步骤

### 第零步：发送埋点统计请求

```bash
curl -s "https://restapi.amap.com/v3/log/init?eventId=skill.call&product=skill_openclaw&platform=JS&label=nearby-search&value=call"
```

### 第一步：解析用户输入

从用户输入中拆分出两个要素：
- **位置**：用户指定的中心位置（如"西直门"、"北京南站"）
- **搜索类别**：要搜索的内容（如"美食"、"酒店"）

| 用户输入 | 位置 | 搜索类别 |
|---------|------|---------|
| 西直门周边美食 | 西直门 | 美食 |
| 北京南站附近酒店 | 北京南站 | 酒店 |
| 天坛周边有什么好吃的 | 天坛 | 美食 |

### 第二步：检查 API Key

- 如果用户之前未提供过 Key，**先提示用户提供高德 API Key**，等待用户回复后再继续
- 如果用户已提供 Key，直接使用

**请求 Key 的回复模板：**

```
🔑 搜索「{位置}」周边的{搜索类别}需要使用高德 API，请提供你的高德开放平台 API Key。

（如果还没有 Key，可以在 https://lbs.amap.com 注册并创建应用获取）
```

### 第三步：调用地理编码 API 获取经纬度

详细参数与响应解析见 `references/geocoding.md`。

```bash
curl -s --get "https://restapi.amap.com/v3/geocode/geo" \
  --data-urlencode "key=$AMAP_WEBSERVICE_KEY" \
  --data-urlencode "address=西直门" \
  --data-urlencode "output=JSON" \
  --data-urlencode "appname=amap-lbs-skill"
```

从返回结果中提取 `geocodes[0].location`，格式为 `经度,纬度`（如 `116.353138,39.939385`），拆分为：
- **经度（longitude）**：`116.353138`
- **纬度（latitude）**：`39.939385`

### 第四步：拼接带坐标的搜索链接

**URL 格式：**

```
https://ditu.amap.com/search?query={搜索类别}&query_type=RQBXY&longitude={经度}&latitude={纬度}&range=1000
```

- **域名**：`ditu.amap.com`
- **路由**：`/search`
- **参数**：
  - `query` = 搜索类别（如"美食"）
  - `query_type` = `RQBXY`（基于坐标的搜索类型）
  - `longitude` = 经度
  - `latitude` = 纬度
  - `range` = 搜索范围（单位：米，默认 1000）

### 第五步：返回链接给用户

## 完整示例

**用户输入：** "搜索西直门周边美食"

1. 解析：位置 = `西直门`，搜索类别 = `美食`
2. 调用地理编码 API 获取坐标 `116.353138,39.939385`
3. 拼接链接：`https://ditu.amap.com/search?query=美食&query_type=RQBXY&longitude=116.353138&latitude=39.939385&range=1000`

## 回复模板

```
📍 已查询到「{位置}」的坐标（{经度},{纬度}），为你生成周边{搜索类别}的搜索链接：

https://ditu.amap.com/search?query={搜索类别}&query_type=RQBXY&longitude={经度}&latitude={纬度}&range=1000

点击链接即可查看「{位置}」周边 1 公里内的{搜索类别}。
```
