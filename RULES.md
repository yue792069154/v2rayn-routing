# 规则目录

共 64 个规则组；顺序即优先级。

| 顺序 | 别名 | 出口 | 匹配项数 |
| --- | --- | --- | --- |
| 1 | yundou.ai、xixiapi.io｜直连（levon 2026-11-12 指令，压过代理名单命中） | direct | 2 |
| 2 | novarui.com 及子域名｜优先直连 | direct | 1 |
| 3 | Tailscale 控制面与 DERP 域名｜直连（防网关端点污染） | direct | 1 |
| 4 | Tailscale WireGuard(41641) 与 STUN(3478) 端口｜直连 | direct | 按端口/协议 |
| 5 | HTTP/3 与 QUIC（UDP 443）｜拦截 | block | 按端口/协议 |
| 6 | 自定义固定入口地址｜直连 | direct | 2 |
| 7 | LUAPI 指定入口｜直连 | direct | 5 |
| 8 | Cursor 与 XixiAPI｜代理 | proxy | 4 |
| 9 | LUAPI 指定服务｜直连 | direct | 6 |
| 10 | LUAPI 与长桥券商｜代理 | proxy | 10 |
| 11 | trade.skytigris.cn｜交易接口代理 | proxy | 1 |
| 12 | Skytigris 主域与子域｜直连 | direct | 2 |
| 13 | 政务、银行、交易所与老虎券商｜直连 | direct | 31 |
| 14 | 老虎券商指定域名｜代理 | proxy | 3 |
| 15 | 老虎社区｜直连 | direct | 3 |
| 16 | AI 服务与开发工具｜代理 | proxy | 49 |
| 17 | 券商服务域名｜代理 | proxy | 71 |
| 18 | 券商服务地址｜代理 | proxy | 63 |
| 19 | Notion 等指定海外服务｜代理 | proxy | 13 |
| 20 | 本机回环主机名｜直连 | direct | 1 |
| 21 | Apple Intelligence 与 Copilot｜代理 | proxy | 7 |
| 22 | 百度、阿里与指定下载域名｜直连 | direct | 7 |
| 23 | cdn.angruo.com｜代理 | proxy | 1 |
| 24 | download.jetbrains.com、file-igamecj.akamaized.net 等｜直连 | direct | 44 |
| 25 | battle.net｜代理 | proxy | 1 |
| 26 | bdatu.com、beitaichufang.com 等｜直连 | direct | 7 |
| 27 | blizzard.com｜代理 | proxy | 1 |
| 28 | bmj.com、booking.com 等｜直连 | direct | 53 |
| 29 | getpricetag.com｜代理 | proxy | 1 |
| 30 | gifshow.com、godic.net 等｜直连 | direct | 54 |
| 31 | m-team.cc｜代理 | proxy | 1 |
| 32 | madsrevolution.net、maoyan.com 等｜直连 | direct | 61 |
| 33 | AS132203 公告地址段｜直连（静态快照） | direct | 1161 |
| 34 | 国内 DNS 与指定服务域名｜直连 | direct | 14 |
| 35 | sciencemag.org｜代理 | proxy | 1 |
| 36 | scomper.me、scopus.com 等｜直连 | direct | 34 |
| 37 | teamviewer.com｜代理 | proxy | 1 |
| 38 | tencent-cloud.net、tencent.com 等｜直连 | direct | 70 |
| 39 | v2ex.com、scdn.co 等｜代理 | proxy | 166 |
| 40 | ykimg.com｜直连 | direct | 1 |
| 41 | medium.com、fast.com 等｜代理 | proxy | 40 |
| 42 | ChatGPT 指定服务器地址｜代理 | proxy | 5 |
| 43 | Telegram 域名｜代理 | proxy | 6 |
| 44 | Telegram 服务器网段｜代理 | proxy | 10 |
| 45 | DNS 泄漏检测站点｜代理 | proxy | 12 |
| 46 | 局域网与回环地址｜直连 | direct | 4 |
| 47 | 私有与保留地址（GeoIP private）｜直连 | direct | 1 |
| 48 | 局域网域名（Geosite private）｜直连 | direct | 1 |
| 49 | 国内 DNS 地址｜直连 | direct | 35 |
| 50 | 国内 DNS 服务域名｜直连 | direct | 4 |
| 51 | 路由器与局域网设备域名｜直连 | direct | 132 |
| 52 | 广告与追踪域名｜拦截 | block | 199522 |
| 53 | Google 服务（Geosite google）｜代理 | proxy | 1 |
| 54 | 国内与常用直连域名｜直连 | direct | 109722 |
| 55 | Apple iCloud 服务｜直连 | direct | 47 |
| 56 | Apple 服务域名｜直连 | direct | 164 |
| 57 | Google 补充域名｜代理 | proxy | 81 |
| 58 | GFW 列表域名｜代理 | proxy | 4229 |
| 59 | Telegram 补充服务器网段｜代理 | proxy | 9 |
| 60 | 海外服务域名｜代理 | proxy | 22629 |
| 61 | 中国 IPv4 / IPv6 网段｜直连 | direct | 9644 |
| 62 | 中国 IP（GeoIP cn）｜直连 | direct | 1 |
| 63 | 中国域名（Geosite cn）｜直连 | direct | 1 |
| 64 | 其余所有流量｜代理 | proxy | 按端口/协议 |
