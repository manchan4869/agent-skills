# CODING DevOps 平台操作 Skill

通过 CODING OpenAPI 与 Git 操作 [CODING DevOps](https://coding.net) 平台的技能：验证访问令牌、列出项目/仓库、浏览仓库文件、读取文件内容、查询分支/提交/合并请求，以及通过 SSH 克隆推送代码。内容依据 CODING 官方文档与 OpenAPI 规范整理，接口名与参数均真实可查。

**核心能力：**

- OpenAPI 统一调用方式：`POST https://e.coding.net/open-api` + JSON body（`Action` 字段）
- 三种认证：个人访问令牌（`Authorization: token {token}`，推荐 Agent 用）、OAuth 2.0（Bearer）、项目令牌（Basic）
- 令牌获取与安全建议：只读最小权限、令牌仅创建时可见一次、先建后删
- 常用接口：`DescribeCodingCurrentUser`（验证令牌）、`DescribeCodingProjects`、`DescribeMyDepots`、`DescribeProjectDepots`、`DescribeGitFiles`、`DescribeGitBlobRaw`、`DescribeGitBranches`、`DescribeProjectDepotCommits`、`DescribeDepotMergeRequests`
- SSH 访问：`ssh -T git@e.coding.net`、密钥生成、个人公钥/部署公钥/团队部署公钥区别
- curl 与 git 命令示例、限流（单团队单接口 30 次/秒）与常见陷阱清单

**使用方式：** 详见解锁的 `SKILL.md`（中文）。

---

# CODING DevOps Platform Skill (English Summary)

An agent skill for operating the [CODING DevOps](https://coding.net) platform via its OpenAPI and Git. All action names and parameters are sourced from the official CODING OpenAPI specification (served at `https://e.coding.net/open-api`) and the help docs.

**Capabilities:**

- Unified API call: `POST https://e.coding.net/open-api` with a JSON body containing an `Action` field
- Three auth methods: personal access token (`Authorization: token {token}` — recommended for agents), OAuth 2.0 (`Bearer`), project token (`Basic`)
- Token lifecycle & security: least-privilege read-only scopes, token visible only once at creation, create-new-before-delete-old
- Key actions: `DescribeCodingCurrentUser` (token verification), `DescribeCodingProjects`, `DescribeMyDepots`, `DescribeProjectDepots`, `DescribeGitFiles`, `DescribeGitBlobRaw`, `DescribeGitBranches`, `DescribeProjectDepotCommits`, `DescribeDepotMergeRequests`
- SSH access: `ssh -T git@e.coding.net`, key generation, differences between account SSH key / deploy key / team deploy key
- curl & git examples, rate-limit notes (30 req/s per team per API) and a pitfalls checklist

**Usage:** see the unlocked `SKILL.md` (Chinese) for the full reference.

## 参考资料 / References

- CODING 帮助中心: https://coding.net/help
- CODING OpenAPI 文档: https://coding.net/help/openapi
- SSH 公钥配置: https://coding.net/help/docs/repo/ssh/config.html

## 来源声明 / Attribution

本技能为对 CODING 官方公开文档与 OpenAPI 规范的整理，接口事实信息（Action 名/参数/字段）源自 CODING 官方文档，非官方产品，使用须遵守其服务条款。编译版权 (c) manchan4869。

This skill is an independent compilation based on CODING's public documentation and OpenAPI specification. API facts (action names/parameters/fields) are sourced from CODING official docs; this is not an official product. Compilation copyright (c) manchan4869. Use subject to CODING's terms of service.
