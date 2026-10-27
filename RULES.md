# 规则目录

共 61 个规则组；顺序即优先级。

| 顺序 | 别名 | 出口 | 匹配项数 |
| --- | --- | --- | --- |
| 1 | novarui.com 及子域名｜优先直连 | direct | 1 |
| 2 | HTTP/3 与 QUIC（UDP 443）｜拦截 | block | 按端口/协议 |
| 3 | 自定义固定入口地址｜直连 | direct | 2 |
| 4 | LUAPI 指定入口｜直连 | direct | 5 |
| 5 | Cursor 与 XixiAPI｜代理 | proxy | 5 |
| 6 | LUAPI 指定服务｜直连 | direct | 6 |
| 7 | LUAPI 与长桥券商｜代理 | proxy | 10 |
| 8 | trade.skytigris.cn｜交易接口代理 | proxy | 1 |
| 9 | Skytigris 主域与子域｜直连 | direct | 2 |
| 10 | 政务、银行、交易所与老虎券商｜直连 | direct | 31 |
| 11 | 老虎券商指定域名｜代理 | proxy | 3 |
| 12 | 老虎社区｜直连 | direct | 3 |
| 13 | AI 服务与开发工具｜代理 | proxy | 49 |
| 14 | 券商服务域名｜代理 | proxy | 71 |
| 15 | 券商服务地址｜代理 | proxy | 63 |
| 16 | Notion 等指定海外服务｜代理 | proxy | 13 |
| 17 | 本机回环主机名｜直连 | direct | 1 |
| 18 | Apple Intelligence 与 Copilot｜代理 | proxy | 7 |
| 19 | 百度、阿里与指定下载域名｜直连 | direct | 7 |
| 20 | cdn.angruo.com｜代理 | proxy | 1 |
| 21 | download.jetbrains.com、file-igamecj.akamaized.net 等｜直连 | direct | 44 |
| 22 | battle.net｜代理 | proxy | 1 |
| 23 | bdatu.com、beitaichufang.com 等｜直连 | direct | 7 |
| 24 | blizzard.com｜代理 | proxy | 1 |
| 25 | bmj.com、booking.com 等｜直连 | direct | 53 |
| 26 | getpricetag.com｜代理 | proxy | 1 |
| 27 | gifshow.com、godic.net 等｜直连 | direct | 54 |
| 28 | m-team.cc｜代理 | proxy | 1 |
| 29 | madsrevolution.net、maoyan.com 等｜直连 | direct | 61 |
| 30 | AS132203 公告地址段｜直连（静态快照） | direct | 1161 |
| 31 | 国内 DNS 与指定服务域名｜直连 | direct | 14 |
| 32 | sciencemag.org｜代理 | proxy | 1 |
| 33 | scomper.me、scopus.com 等｜直连 | direct | 34 |
| 34 | teamviewer.com｜代理 | proxy | 1 |
| 35 | tencent-cloud.net、tencent.com 等｜直连 | direct | 70 |
| 36 | v2ex.com、scdn.co 等｜代理 | proxy | 166 |
| 37 | ykimg.com｜直连 | direct | 1 |
| 38 | medium.com、fast.com 等｜代理 | proxy | 40 |
| 39 | ChatGPT 指定服务器地址｜代理 | proxy | 5 |
| 40 | Telegram 域名｜代理 | proxy | 6 |
| 41 | Telegram 服务器网段｜代理 | proxy | 10 |
| 42 | DNS 泄漏检测站点｜代理 | proxy | 12 |
| 43 | 局域网与回环地址｜直连 | direct | 4 |
| 44 | 私有与保留地址（GeoIP private）｜直连 | direct | 1 |
| 45 | 局域网域名（Geosite private）｜直连 | direct | 1 |
| 46 | 国内 DNS 地址｜直连 | direct | 35 |
| 47 | 国内 DNS 服务域名｜直连 | direct | 4 |
| 48 | 路由器与局域网设备域名｜直连 | direct | 132 |
| 49 | 广告与追踪域名｜拦截 | block | 193205 |
| 50 | Google 服务（Geosite google）｜代理 | proxy | 1 |
| 51 | 国内与常用直连域名｜直连 | direct | 109774 |
| 52 | Apple iCloud 服务｜直连 | direct | 47 |
| 53 | Apple 服务域名｜直连 | direct | 164 |
| 54 | Google 补充域名｜代理 | proxy | 81 |
| 55 | GFW 列表域名｜代理 | proxy | 4222 |
| 56 | Telegram 补充服务器网段｜代理 | proxy | 9 |
| 57 | 海外服务域名｜代理 | proxy | 22594 |
| 58 | 中国 IPv4 / IPv6 网段｜直连 | direct | 10008 |
| 59 | 中国 IP（GeoIP cn）｜直连 | direct | 1 |
| 60 | 中国域名（Geosite cn）｜直连 | direct | 1 |
| 61 | 其余所有流量｜代理 | proxy | 按端口/协议 |
