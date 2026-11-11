# 规则目录

共 63 个规则组；顺序即优先级。

| 顺序 | 别名 | 出口 | 匹配项数 |
| --- | --- | --- | --- |
| 1 | novarui.com 及子域名｜优先直连 | direct | 1 |
| 2 | Tailscale 控制面与 DERP 域名｜直连（防网关端点污染） | direct | 1 |
| 3 | Tailscale WireGuard(41641) 与 STUN(3478) 端口｜直连 | direct | 按端口/协议 |
| 4 | HTTP/3 与 QUIC（UDP 443）｜拦截 | block | 按端口/协议 |
| 5 | 自定义固定入口地址｜直连 | direct | 2 |
| 6 | LUAPI 指定入口｜直连 | direct | 5 |
| 7 | Cursor 与 XixiAPI｜代理 | proxy | 5 |
| 8 | LUAPI 指定服务｜直连 | direct | 6 |
| 9 | LUAPI 与长桥券商｜代理 | proxy | 10 |
| 10 | trade.skytigris.cn｜交易接口代理 | proxy | 1 |
| 11 | Skytigris 主域与子域｜直连 | direct | 2 |
| 12 | 政务、银行、交易所与老虎券商｜直连 | direct | 31 |
| 13 | 老虎券商指定域名｜代理 | proxy | 3 |
| 14 | 老虎社区｜直连 | direct | 3 |
| 15 | AI 服务与开发工具｜代理 | proxy | 49 |
| 16 | 券商服务域名｜代理 | proxy | 71 |
| 17 | 券商服务地址｜代理 | proxy | 63 |
| 18 | Notion 等指定海外服务｜代理 | proxy | 13 |
| 19 | 本机回环主机名｜直连 | direct | 1 |
| 20 | Apple Intelligence 与 Copilot｜代理 | proxy | 7 |
| 21 | 百度、阿里与指定下载域名｜直连 | direct | 7 |
| 22 | cdn.angruo.com｜代理 | proxy | 1 |
| 23 | download.jetbrains.com、file-igamecj.akamaized.net 等｜直连 | direct | 44 |
| 24 | battle.net｜代理 | proxy | 1 |
| 25 | bdatu.com、beitaichufang.com 等｜直连 | direct | 7 |
| 26 | blizzard.com｜代理 | proxy | 1 |
| 27 | bmj.com、booking.com 等｜直连 | direct | 53 |
| 28 | getpricetag.com｜代理 | proxy | 1 |
| 29 | gifshow.com、godic.net 等｜直连 | direct | 54 |
| 30 | m-team.cc｜代理 | proxy | 1 |
| 31 | madsrevolution.net、maoyan.com 等｜直连 | direct | 61 |
| 32 | AS132203 公告地址段｜直连（静态快照） | direct | 1161 |
| 33 | 国内 DNS 与指定服务域名｜直连 | direct | 14 |
| 34 | sciencemag.org｜代理 | proxy | 1 |
| 35 | scomper.me、scopus.com 等｜直连 | direct | 34 |
| 36 | teamviewer.com｜代理 | proxy | 1 |
| 37 | tencent-cloud.net、tencent.com 等｜直连 | direct | 70 |
| 38 | v2ex.com、scdn.co 等｜代理 | proxy | 166 |
| 39 | ykimg.com｜直连 | direct | 1 |
| 40 | medium.com、fast.com 等｜代理 | proxy | 40 |
| 41 | ChatGPT 指定服务器地址｜代理 | proxy | 5 |
| 42 | Telegram 域名｜代理 | proxy | 6 |
| 43 | Telegram 服务器网段｜代理 | proxy | 10 |
| 44 | DNS 泄漏检测站点｜代理 | proxy | 12 |
| 45 | 局域网与回环地址｜直连 | direct | 4 |
| 46 | 私有与保留地址（GeoIP private）｜直连 | direct | 1 |
| 47 | 局域网域名（Geosite private）｜直连 | direct | 1 |
| 48 | 国内 DNS 地址｜直连 | direct | 35 |
| 49 | 国内 DNS 服务域名｜直连 | direct | 4 |
| 50 | 路由器与局域网设备域名｜直连 | direct | 132 |
| 51 | 广告与追踪域名｜拦截 | block | 197590 |
| 52 | Google 服务（Geosite google）｜代理 | proxy | 1 |
| 53 | 国内与常用直连域名｜直连 | direct | 109722 |
| 54 | Apple iCloud 服务｜直连 | direct | 47 |
| 55 | Apple 服务域名｜直连 | direct | 164 |
| 56 | Google 补充域名｜代理 | proxy | 81 |
| 57 | GFW 列表域名｜代理 | proxy | 4229 |
| 58 | Telegram 补充服务器网段｜代理 | proxy | 9 |
| 59 | 海外服务域名｜代理 | proxy | 22629 |
| 60 | 中国 IPv4 / IPv6 网段｜直连 | direct | 9644 |
| 61 | 中国 IP（GeoIP cn）｜直连 | direct | 1 |
| 62 | 中国域名（Geosite cn）｜直连 | direct | 1 |
| 63 | 其余所有流量｜代理 | proxy | 按端口/协议 |
