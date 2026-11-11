#!/usr/bin/env python3
"""Build mihomo + Shadowrocket products from the same sources as build.py.

Inputs : custom-rules.json + base-rules.json (identical source of truth to
         the v2rayN build; this script never touches rules.json).
Outputs: mihomo/rules.yaml, mihomo/rule-providers.yaml, mihomo/manifest.json,
         shadowrocket/shadowrocket.conf, shadowrocket/rules.list
Safety : any upstream download failure, or any upstream rule count dropping
         more than 20% versus the previous manifest, aborts the whole run
         without writing any product (last good products stay in place).
"""
import json, pathlib, sys, urllib.request
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent

POLICY = {'direct': 'DIRECT', 'proxy': 'PROXY', 'block': 'REJECT'}

# (upstream file name, Source field) -> provider name; URL taken from the group.
PROVIDER_NAME = {
    ('Broker.list', 'Domain'): 'broker',
    ('Broker.list', 'Ip'): 'broker-ip',
    ('private.txt', 'Domain'): 'private',
    ('reject.txt', 'Domain'): 'reject',
    ('direct.txt', 'Domain'): 'direct',
    ('icloud.txt', 'Domain'): 'icloud',
    ('apple.txt', 'Domain'): 'apple',
    ('google.txt', 'Domain'): 'google',
    ('gfw.txt', 'Domain'): 'gfw',
    ('telegramcidr.txt', 'Ip'): 'telegramcidr',
    ('proxy.txt', 'Domain'): 'proxy',
    ('cncidr.txt', 'Ip'): 'cncidr',
}

# mihomo built-in geoip:private expansion (30 entries, gateway-verified order).
PRIVATE_EXPANSION = [
    '0.0.0.0/8', '10.0.0.0/8', '100.64.0.0/10', '127.0.0.0/8', '169.254.0.0/16',
    '172.16.0.0/12', '192.0.0.0/29', '192.0.0.170/31', '192.0.2.0/24',
    '192.31.196.0/24', '192.52.193.0/24', '192.88.99.0/24', '192.168.0.0/16',
    '192.175.48.0/24', '198.18.0.0/15', '198.51.100.0/24', '203.0.113.0/24',
    '224.0.0.0/4', '240.0.0.0/4', '255.255.255.255/32', '::/128', '::1/128',
    '64:ff9b::/96', '100::/64', '2001::/32', '2001:10::/28', '2001:db8::/32',
    'fc00::/7', 'fe80::/10', 'ff00::/8',
]

# Gateway-only line, inserted after the custom groups (Tailscale range guard).
GUARD_LINE = 'IP-CIDR,100.64.0.0/10,DIRECT,no-resolve'

GEOSITE_TO_PROVIDER = {'private': 'private', 'google': 'google', 'cn': 'direct'}

# Shadowrocket address-edition: nodes come from the airport subscription
# already added in the app; the proxy groups below reference the
# subscription's exact node names (same roster as the gateway subscription).
# Update this roster when the subscription's node names change.
SR_NODE_ROSTER = [
    'cloady-日本', 'plxx-德国', 'lustone-Hy2', 'lustone-TUIC', '华为SG-Hy2',
    '华为SG-TUIC', '美国CF | lustone-ws-443', '新加坡 | 华为',
    '香港优选 01 | lustone', '日本优选 01 | lustone', '美国优选 02 | lustone',
    '日本优选 03 | lustone', '日本优选 04 | lustone',
]
SR_US_NODES = [
    '美国优选 02 | lustone', '美国CF | lustone-ws-443', '日本优选 01 | lustone',
    '日本优选 03 | lustone', '日本优选 04 | lustone', 'lustone-Hy2',
    'lustone-TUIC',
]
SR_TEST_URL = 'http://www.gstatic.com/generate_204'


def load(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8-sig'))


def group_lines(group, providers):
    """Convert one repo rule group to mihomo rule lines (gateway semantics)."""
    policy = POLICY[group['OutboundTag']]
    source = group.get('Source')
    if source:
        url = source['url']
        fname = url.rstrip('/').split('/')[-1]
        name = PROVIDER_NAME[(fname, source['field'])]
        providers.setdefault(name, url)
        return [f'RULE-SET,{name},{policy}']
    if group.get('Port') == '0-65535':
        return [f'MATCH,{policy}']
    lines = []
    if group.get('Network') == 'udp' and group.get('Port'):
        for port in str(group['Port']).split(','):
            lines.append(f'AND,((NETWORK,UDP),(DST-PORT,{port.strip()})),{policy}')
    for value in group.get('Domain', []):
        if value.startswith('domain:'):
            lines.append(f'DOMAIN-SUFFIX,{value[7:]},{policy}')
        elif value.startswith('full:'):
            lines.append(f'DOMAIN,{value[5:]},{policy}')
        elif value.startswith('keyword:'):
            lines.append(f'DOMAIN-KEYWORD,{value[8:]},{policy}')
        elif value.startswith('geosite:'):
            lines.append(f'GEOSITE,{value[8:]},{policy}')
        else:
            raise ValueError(f'Unsupported domain matcher: {value}')
    for value in group.get('Ip', []):
        if value == 'geoip:private':
            lines += [f'IP-CIDR,{cidr},{policy}' for cidr in PRIVATE_EXPANSION]
        elif value.startswith('geoip:'):
            lines.append(f'GEOIP,{value[6:].upper()},{policy}')
        else:
            if '/' not in value:  # bare host address -> host prefix (gateway form)
                value += '/128' if ':' in value else '/32'
            lines.append(f'IP-CIDR,{value},{policy}')
    return lines


def build_rules():
    custom, base = load('custom-rules.json'), load('base-rules.json')
    providers = {}
    lines = []
    for g in custom:
        lines += group_lines(g, providers)
    lines.append(GUARD_LINE)
    for g in base:
        lines += group_lines(g, providers)
    return lines, providers


def download(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'v2rayn-routing-products/1.0'})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode('utf-8-sig')


def count_rules(text):
    n = 0
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith(('DOMAIN', 'IP-CIDR', 'GEOIP', 'IP-ASN')):
            n += 1
    return n


def fetch_counts(providers):
    counts = {}
    for name, url in providers.items():
        if url in counts.get('_by_url', {}):
            counts[name] = counts['_by_url'][url]
            continue
        c = count_rules(download(url))
        counts.setdefault('_by_url', {})[url] = c
        counts[name] = c
    counts.pop('_by_url', None)
    return counts


def guard_counts(new_counts):
    prev_file = ROOT / 'mihomo' / 'manifest.json'
    if not prev_file.exists():
        return
    prev = json.loads(prev_file.read_text(encoding='utf-8')).get('providers', {})
    for name, old in prev.items():
        new = new_counts.get(name)
        if new is not None and old and new < old * 0.8:
            raise ValueError(f'Upstream {name} count dropped {old} -> {new} (>20%); aborting')


# Shadowrocket keeps levon's own Tailscale handling (his current config):
# the 100.64.0.0/10 range and ts.net names go to the TAILSCALE policy of the
# built-in Tailscale module — never plain DIRECT. Two lines, guard position.
SR_TAILSCALE_LINES = [
    'IP-CIDR,100.64.0.0/10,TAILSCALE,no-resolve',
    'DOMAIN-SUFFIX,ts.net,TAILSCALE',
]


def shadowrocket_lines(mihomo_lines, providers):
    out, seen = [], set()
    for line in mihomo_lines:
        if line == GUARD_LINE:
            out += SR_TAILSCALE_LINES
            continue
        if line == 'IP-CIDR,100.64.0.0/10,DIRECT':
            # Same range inside the geoip:private expansion. Unreachable in
            # Shadowrocket (the TAILSCALE line above matches first) and it
            # must not appear as a plain DIRECT rule for this range.
            continue
        if line.startswith('RULE-SET,'):
            _, name, policy = line.split(',')
            new = f'RULE-SET,{providers[name]},{policy}'
        elif line.startswith('GEOSITE,'):
            _, site, policy = line.split(',')
            new = f'RULE-SET,{providers[GEOSITE_TO_PROVIDER[site]]},{policy}'
        elif line.startswith('GEOIP,'):
            _, code, policy = line.split(',')
            if code != 'CN':
                raise ValueError(f'Unsupported GEOIP in shadowrocket build: {line}')
            new = f'RULE-SET,{providers["cncidr"]},{policy}'
        elif line.startswith('AND,((NETWORK,UDP)'):
            new = line.replace('NETWORK,UDP', 'PROTOCOL,UDP')
        elif line.startswith('MATCH,'):
            new = f'FINAL,{line.split(",")[1]}'
        else:
            new = line
        if new.startswith('RULE-SET,'):
            if new in seen:
                continue
            seen.add(new)
        out.append(new)
    return out


def main():
    generated_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    lines, providers = build_rules()
    counts = fetch_counts(providers)          # raises on any download failure
    guard_counts(counts)                      # raises on >20% drop
    total_provider_rules = sum(counts.values())

    header = (f'# Generated by build_products.py — do not edit by hand.\n'
              f'# Generated at: {generated_at}\n'
              f'# Static rules: {len(lines)}; rule providers: {len(providers)} '
              f'({total_provider_rules} upstream rules)\n')

    rules_yaml = header + 'rules:\n' + ''.join(f'  - {json.dumps(l)}\n' for l in lines)

    prov_yaml = header + 'rule-providers:\n'
    for name, url in providers.items():
        prov_yaml += (f'  {name}:\n    type: http\n    behavior: classical\n'
                      f'    format: text\n    url: "{url}"\n    interval: 86400\n'
                      f'    path: ./providers/{name}.yaml\n')

    sr_lines = shadowrocket_lines(lines, providers)
    conf = header.replace('#', '#', 1)
    conf += ('# Shadowrocket rule config (address edition). Nodes are NOT in\n'
             '# this file: they come from the airport subscription already\n'
             '# added in the app. The proxy groups below reference that\n'
             '# subscription\'s exact node names.\n'
             '# The QUIC block uses an AND/PROTOCOL logic rule; if your app\n'
             '# version rejects it, delete that single line.\n'
             '# Tailscale: 100.64.0.0/10 and ts.net keep the TAILSCALE policy\n'
             '# of the built-in Tailscale module, as in the current config.\n\n'
             '[General]\n'
             'bypass-system = true\n'
             'skip-proxy = 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12, localhost, *.local\n'
             'dns-server = system\n\n'
             '[Proxy]\n'
             '# Intentionally empty: nodes come from the in-app subscription.\n\n'
             '[Proxy Group]\n'
             'PROXY = select, 美国优先, 全部节点, DIRECT\n'
             '美国优先 = fallback, ' + ', '.join(SR_US_NODES) +
             f', interval=120, timeout=5, url={SR_TEST_URL}\n'
             '全部节点 = url-test, ' + ', '.join(SR_NODE_ROSTER) +
             f', interval=120, timeout=5, url={SR_TEST_URL}\n\n'
             '[Rule]\n' + '\n'.join(sr_lines) + '\n')

    list_body = [l for l in sr_lines if not l.startswith(('RULE-SET,', 'FINAL,'))]
    rules_list = (header + '# Plain rule lines only (no RULE-SET / FINAL);\n'
                  '# the QUIC AND line lives in shadowrocket.conf only.\n'
                  + '\n'.join(l for l in list_body if not l.startswith('AND,')) + '\n')

    manifest = {
        'generated_at': generated_at,
        'static_rules': len(lines),
        'providers': counts,
        'provider_rules_total': total_provider_rules,
    }

    outputs = {
        'mihomo/rules.yaml': rules_yaml,
        'mihomo/rule-providers.yaml': prov_yaml,
        'mihomo/manifest.json': json.dumps(manifest, ensure_ascii=False, indent=2) + '\n',
        'shadowrocket/shadowrocket.conf': conf,
        'shadowrocket/rules.list': rules_list,
    }
    tmps = []
    for rel, content in outputs.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + '.tmp')
        tmp.write_text(content, encoding='utf-8')
        tmps.append((tmp, path))
    for tmp, path in tmps:
        tmp.replace(path)
    print(f'Built {len(lines)} static rules; {len(providers)} providers; '
          f'{total_provider_rules} upstream rules; shadowrocket {len(sr_lines)} lines')
    return 0


if __name__ == '__main__':
    sys.exit(main())
