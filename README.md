# v2rayN 综合分流规则

由 Shadowrocket 规则与 V4 绕过大陆白名单合并，包含 novarui.com 及所有子域名优先直连。
分流规则按顺序匹配。自定义具体规则优先，保留广告拦截、Google 代理、局域网和国内 DNS 直连、中国域名/IP 直连以及最终代理。

## URL 导入

仓库发布到 GitHub 后，在 `rules.json` 文件页点击 **Raw**，复制其地址。
地址格式为 `https://raw.githubusercontent.com/yue792069154/v2rayn-routing/main/rules.json`。

在 v2rayN 的“设置 → 路由设置”中编辑综合分流方案，把 Raw 地址填入可选的订阅 URL，再执行“从订阅 URL 中导入规则”。域名策略使用 `AsIs`。

这是路由规则 URL，导入位置是路由设置。节点订阅不使用此地址。

GitHub 更新后，在 v2rayN 中再次从该 URL 导入即可获得最新版。仅更新节点订阅不会更新这里的路由。

## 添加自己的规则

日常编辑 **custom-rules.json**。文件小，可直接在 GitHub 网页编辑；这里的规则优先于基础规则。

例如，增加一个直连域名及其子域名：

```json
{
  "Remarks": "example.com 及子域名｜直连",
  "OutboundTag": "direct",
  "Enabled": true,
  "Domain": ["domain:example.com"]
}
```

`domain:` 匹配主域和子域；`full:` 仅匹配完整主机名；`keyword:` 按关键字匹配。
`OutboundTag` 可用 `direct`（直连）、`proxy`（代理）、`block`（拦截）。每组别名应唯一且说明用途。

提交到 main 分支后，GitHub Actions 会下载公开上游列表、生成 rules.json，并提交结果。
需要立即更新上游时，打开 Actions → 更新分流规则 → Run workflow。没有设置定时任务。
构建失败时不会用不完整结果替换 rules.json；先查看失败日志，再重试。

## 文件

| 文件 | 用途 |
| --- | --- |
| custom-rules.json | 日常维护的优先规则，目前含 novarui.com 直连 |
| base-rules.json | 已整理的基础规则、白名单规则和公开上游地址 |
| rules.json | v2rayN 通过 URL 下载的最终规则；由脚本生成 |
| RULES.md | 各规则别名、顺序及匹配项数 |
| build.py | Python 标准库构建脚本，无额外依赖 |

本地执行 `python build.py --refresh` 可更新公开上游。执行 `python build.py` 使用现有 rules.json 中的上游快照，适合离线核对；调整优先规则后应使用 --refresh 重新生成完整列表。

## 来源与兼容性

公开上游来自 [Loyalsoldier/surge-rules](https://github.com/Loyalsoldier/surge-rules) 与 [Arthur-vx/broker-rules](https://github.com/Arthur-vx/broker-rules)。使用及再分发应遵守各上游仓库的许可条件。参考 [v2rayN 自定义路由格式](https://github.com/2dust/v2rayN/wiki/Description-of-custom-routing-rules)。

仓库只包含分流数据及构建文件。原软件数据库、节点、订阅、个人专属更新 URL 和本机备份不在发布范围内。
原文件的私人动态列表仅保留此前已融合的匹配结果；公开仓库不会访问原专属更新地址。
AS132203 保留迁移时的 RIPE RIS 地址快照，未随公开域名列表刷新。Shadowrocket User-Agent 规则和 URL Rewrite 不支持等价迁移。
沿用 AsIs 策略，Xray 对域名连接的 GEOIP/no-resolve 行为与 Shadowrocket 存在差异。

具体规则 trade.skytigris.cn 代理先于 skytigris.cn 父域直连；novarui.com 直连先于 UDP 443 拦截。
