---
name: coding-devops
description: Use when the user needs to operate the CODING DevOps platform (coding.net) via its OpenAPI or Git — verify an access token, list projects/repositories, browse repository files, read file content, list branches/commits/merge requests, or clone/pull/push code over SSH. Triggers include mentions of "CODING", "e.coding.net", "coding.net/help/openapi", "CODING OpenAPI", "DescribeCodingCurrentUser", "DescribeGitFiles", "personal access token 个人访问令牌", "CODING 项目/仓库/合并请求/MR", or any request to call CODING platform APIs with curl.
version: 1.0.0
license: MIT
compatibility: curl, git
---

# CODING DevOps 平台操作 Skill

基于 CODING 官方文档（https://coding.net/help 与 OpenAPI 规范 YAML）整理。所有接口名、参数与调用方式均来自 CODING OpenAPI 官方规范，调用统一走 `POST https://e.coding.net/open-api`，请求体为 JSON 且必含 `Action` 字段。

## 核心约定（先读）

- **API 地址**：`https://e.coding.net/open-api`（官方 servers 定义），请求方式一律 `POST`。
- **请求体**：`Content-Type: application/json`，JSON 体形如 `{"Action": "DescribeCodingCurrentUser", ...参数}`。
- **认证**：`Authorization` 头，三选一（见下节）。不传/传错认证头会得到 `UnauthorizedOperation` / `AuthFailure`。
- **限流**：单团队单接口**每秒最多 30 次**请求，触发后按错误码退避重试。
- **返回结构**：响应为 `{"Response": {...}, "RequestId": "..."}`，业务数据在 `Response` 下的对应字段（如 `User`、`Data`、`Items`）。

## 触发条件

- 用户提到 CODING / CODING DevOps / e.coding.net / CODING 开放平台。
- 要验证 CODING 访问令牌是否有效。
- 要列 CODING 项目、仓库，浏览仓库目录/文件内容，查分支、提交记录、合并请求。
- 要通过 SSH 克隆/推送 CODING 仓库代码。
- 要写脚本或给 agent 配工具来调用 CODING OpenAPI。

## 认证方式（三选一）

CODING OpenAPI 支持三种认证，按 `Authorization` 头区分：

| 方式 | Authorization 头 | 适用场景 | 令牌来源 |
|---|---|---|---|
| OAuth 2.0 | `Bearer {access_token}` | 第三方应用/生态接入 | 生态能力应用授权 |
| 个人访问令牌 | `token {访问令牌}` | Agent/个人脚本（最常用） | 个人账户设置 → 访问令牌 |
| 项目令牌 | `Basic {base64(用户名:密码)}` | 项目级受限操作 | 项目设置 → 开发者选项 → 项目令牌 |

### 个人访问令牌（推荐给 Agent 用）

- 创建：CODING 页面左下角**个人账户设置 → 访问令牌 → 新建访问令牌**，勾选所需权限后生成。
- **令牌只在创建那一刻完整显示一次**，刷新页面即消失；创建后任何人（含管理员）都无法再查看明文，务必立即妥善保存。忘记需删除后重新生成。
- 最多同时创建 **5 个**令牌；更换令牌时**先建新令牌再删旧令牌**。
- 最小权限原则：只勾选本次需要的权限点，能只读就选只读（`ro`）。

### OAuth 2.0（生态应用）

1. 团队设置 → 生态能力 → 发布应用 → 新建应用，拿到 Client ID / Client Secret，配置回调地址。
2. 引导用户浏览器访问授权页获取 code：

```
GET https://{your-team}.coding.net/oauth_authorize.html?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&state={state}&scope={scope}
```

3. 后端用 code 换 `access_token`（code 仅可用一次、有效期 5 分钟）：

```
POST https://{your-team}.coding.net/api/oauth/access_token
Content-Type: application/x-www-form-urlencoded

client_id={client_id}&client_secret={client_secret}&grant_type=authorization_code&code={code}
```

4. 用 `refresh_token`（有效期 90 天）刷新：`grant_type=refresh_token&refresh_token={refresh_token}`；刷新后旧 `access_token` 立即失效。

### 项目令牌（Basic 认证）

项目设置 → 开发者选项 → 项目令牌 → 新建项目令牌，勾选权限生成「用户名 + 密码」；将 `用户名:密码` 做 Base64 编码作为凭证。

## 快速上手：验证令牌

```bash
curl -s -X POST 'https://e.coding.net/open-api' \
  -H 'Authorization: token YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"Action": "DescribeCodingCurrentUser"}'
```

正常返回示例：

```json
{
  "Response": {
    "User": { "Id": 183478, "Email": "you@example.com", "GlobalKey": "yourglobalkey", "Name": "你的名字", "TeamId": 1 },
    "RequestId": "133e152f-8852-4d99-b704-c7ff245a1640"
  }
}
```

拿到 `User` 即令牌有效；报 `AuthFailure`/`UnauthorizedOperation` 说明令牌错误、过期或缺少 `user:profile:ro` 权限。

## 常用接口速查

以下接口与参数均取自 CODING OpenAPI 官方规范，`Action` 大小写必须一致。

### 用户与团队

| Action | 作用 | 关键参数 |
|---|---|---|
| `DescribeCodingCurrentUser` | 当前用户信息（验证令牌） | 无 |

### 项目

| Action | 作用 | 关键参数 |
|---|---|---|
| `DescribeCodingProjects` | 项目列表 | `PageNumber`(必), `PageSize`(必), `ProjectName`(可选), `QueryArchived`(默认 false) |

### 仓库

| Action | 作用 | 关键参数 |
|---|---|---|
| `DescribeMyDepots` | 当前用户有读权限的仓库列表 | `PageNumber`(必), `PageSize`(必) |
| `DescribeProjectDepots` | 某项目下仓库列表 | `ProjectId`(必), `DepotType`(必，如 `CODING`) |

### 代码内容（仓库文件）

| Action | 作用 | 关键参数 |
|---|---|---|
| `DescribeGitFiles` | 分支目录结构（文件和文件夹名） | `DepotId` 或 `DepotPath`, `Ref`(分支名,必), `Path`(目录,默认根目录) |
| `DescribeGitBlobRaw` | 读取文件 Blob 原始文本 | `BlobSha`(必), `DepotId` 或 `DepotPath` |

### 分支 / 提交 / 合并请求

| Action | 作用 | 关键参数 |
|---|---|---|
| `DescribeGitBranches` | 仓库下所有分支 | `DepotId`(必) 或 `DepotPath`, `KeyWord`, `PageNumber`, `PageSize`(默认10) |
| `DescribeProjectDepotCommits` | 分支下的提交列表 | `ProjectId`(必), `Id`(仓库Id,必), `DepotType`(必), `Branch`(必) |
| `DescribeDepotMergeRequests` | 仓库合并请求(MR)列表 | `DepotId`(必), `PageNumber`, `PageSize`, `Status`(OPEN/CLOSE/ALL/ACCEPTED), `SourceBranches`, `TargetBranches`, `Sort`(created_at/merged_at/action_at) |

其他可用 Action（规范中存在）：`DescribeGitCommitInfo(s)`、`DescribeGitBlameInfo`、`DescribeGitTree`、`DescribeGitTag(s)`、`DescribeGitFileContent`、`DescribeMergeReqInfo`、`DescribeMergeRequestFileDiff`、`CreateGitFile(s)`、`CreateGitCommit`、`ModifyGitFiles`、`DeleteGitFiles`、`CreateGitBranch`、`CreateGitTag`、`CreateGitMergeRequest`、`ModifyMergeMR`、`ModifyCloseMR` 等。**只使用上面列出的、已在本表或本节出现的 Action 名，不要臆造。**

## 具体命令示例

### 1. 列项目

```bash
curl -s -X POST 'https://e.coding.net/open-api' \
  -H 'Authorization: token YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"Action": "DescribeCodingProjects", "PageNumber": 1, "PageSize": 10}'
# 项目在 Response.Data.ProjectList[]，含 Id/Name/DisplayName/Archived
```

### 2. 列当前用户可读的仓库

```bash
curl -s -X POST 'https://e.coding.net/open-api' \
  -H 'Authorization: token YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"Action": "DescribeMyDepots", "PageNumber": 1, "PageSize": 20}'
# 仓库在 Response.Payload.Depots[]，含 Id/Name/ProjectName/ProjectId/HttpsUrl/SshUrl
```

### 3. 列某项目下的仓库

```bash
curl -s -X POST 'https://e.coding.net/open-api' \
  -H 'Authorization: token YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"Action": "DescribeProjectDepots", "ProjectId": 123456, "DepotType": "CODING"}'
# 仓库在 Response.Data.DepotList[]，含 Id/Name/DepotSshUrl/DepotHttpsUrl
```

### 4. 浏览仓库目录（master 分支根目录）

```bash
curl -s -X POST 'https://e.coding.net/open-api' \
  -H 'Authorization: token YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"Action": "DescribeGitFiles", "DepotId": 789, "Ref": "master"}'
# 目录项在 Response.Items[]，每项含 Mode/Name/Path/Sha；Path 参数可下钻子目录
```

### 5. 读取文件内容（先拿 BlobSha）

```bash
# 用 DescribeGitFiles 拿到目标文件的 Sha 后：
curl -s -X POST 'https://e.coding.net/open-api' \
  -H 'Authorization: token YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"Action": "DescribeGitBlobRaw", "DepotId": 789, "BlobSha": "<上一步的Sha>"}'
# 文件文本在 Response.Content
```

### 6. 查分支下的提交记录

```bash
curl -s -X POST 'https://e.coding.net/open-api' \
  -H 'Authorization: token YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"Action": "DescribeProjectDepotCommits", "ProjectId": 123456, "Id": 789, "DepotType": "CODING", "Branch": "master"}'
# 提交在 Response.Data.DepotDetailList[]，含 Name(提交说明)/Sha
```

### 7. 查仓库合并请求

```bash
curl -s -X POST 'https://e.coding.net/open-api' \
  -H 'Authorization: token YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"Action": "DescribeDepotMergeRequests", "DepotId": 789, "PageNumber": 1, "PageSize": 10, "Status": "OPEN"}'
# MR 在 Response.Data.List[]，含 Id/MergeId/Title/SourceBranch/TargetBranch/Status/Author/Reviewers
```

## SSH 访问代码仓库

- 校验 SSH 是否连通：`ssh -T git@e.coding.net`
- 生成密钥（官方文档推荐）：`ssh-keygen -m PEM -t ed25519 -C "your.email@example.com"`（不支持 Ed25519 时用 `ssh-keygen -m PEM -t rsa -b 4096 -C "your.email@example.com"`）
- 添加位置：
  - **个人账户 SSH 公钥**（个人账户设置 → SSH 公钥）：拥有该账户所有代码仓库的读写权限。
  - **部署公钥**（仓库 → 设置 → 部署公钥）：默认只读，可在公钥设置里勾选「授予推送权限」。
  - **团队部署公钥**（团队设置中心 → 功能设置 → 代码仓库 → 团队设置公钥）：仅拉取权限。
  - 同一个公钥**不能**既作个人账户公钥又作部署公钥。
- 克隆：在仓库浏览页复制 SSH 地址（形如 `git@e.coding.net:<团队>/<项目>/<仓库>.git`），本地 `git clone <地址>` 即可；日常 `git pull` / `git push` 与标准 Git 一致。

## 常见陷阱与注意事项

- **Action 名必须与规范完全一致**，大小写敏感（如 `DescribeCodingCurrentUser` 不是 `describeCodingCurrentUser`）。
- **认证头写错**：个人令牌是 `Authorization: token xxx`；OAuth 是 `Authorization: Bearer xxx`；项目令牌是 `Authorization: Basic base64...`。把 token 误写成 Bearer 会 401。
- **请求体必须带 `Content-Type: application/json`**，Action 放在 JSON 体里，不是 URL query。
- **先查项目/仓库 ID**：多数接口要 `ProjectId`/`DepotId`，可先用 `DescribeCodingProjects` + `DescribeMyDepots`/`DescribeProjectDepots` 拿到。
- **`DepotId` 与 `DepotPath` 二选一**：`DepotPath` 形如 `团队/项目/仓库`（如 `coding/repo/1`），部分接口两者都支持。
- **分页**：返回体里的 `TotalCount`/`TotalRow` 是总数，长列表记得翻页。
- **限流**：单团队单接口每秒 30 次；批量脚本加延时或遇到限流错误码退避。
- **令牌安全**：只在创建时可见一次，不要提交到仓库、不要写进日志；生产环境放环境变量/密钥管理；只授权必要的权限点（能只读就别给读写）。
- **响应解析**：业务数据在 `Response` 对象内（`Response.User`、`Response.Data`、`Response.Items`、`Response.Payload`），不要到顶层找。
- 涉及项目协同（issue）、制品库、CI/CD 等其他模块时，先到 https://coding.net/help/openapi 确认对应 Action 名与参数，勿凭印象猜测。

## 参考资料

- CODING 帮助中心：https://coding.net/help
- CODING OpenAPI 文档：https://coding.net/help/openapi
- SSH 公钥配置：https://coding.net/help/docs/repo/ssh/config.html
- 通过 SSH 推拉代码：https://coding.net/help/docs/repo/ssh/pull-push.html
