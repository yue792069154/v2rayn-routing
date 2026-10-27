#!/usr/bin/env python3
"""Build an ordered v2rayN routing array using Python's standard library."""
import argparse, concurrent.futures, copy, hashlib, ipaddress, json, pathlib, urllib.request

ROOT=pathlib.Path(__file__).resolve().parent

def load(name):
    return json.loads((ROOT/name).read_text(encoding='utf-8-sig'))

def download(url):
    req=urllib.request.Request(url,headers={'User-Agent':'v2rayn-routing-builder/1.0'})
    with urllib.request.urlopen(req,timeout=60) as response:
        data=response.read(32_000_001)
    if len(data)>32_000_000:
        raise ValueError('Upstream list exceeds 32 MB')
    return data.decode('utf-8-sig')

def parse_list(text,field):
    result=[]
    for raw in text.splitlines():
        line=raw.strip()
        if not line or line.startswith(('#',';','//')):
            continue
        bits=[x.strip() for x in line.split(',')]
        kind=bits[0]
        if len(bits)<2:
            raise ValueError('Invalid upstream rule: '+line[:100])
        value=bits[1]
        if kind in ('DOMAIN','DOMAIN-SUFFIX','DOMAIN-KEYWORD'):
            if field=='Domain':
                result.append({'DOMAIN':'full:','DOMAIN-SUFFIX':'domain:','DOMAIN-KEYWORD':'keyword:'}[kind]+value)
        elif kind in ('IP-CIDR','IP-CIDR6'):
            ipaddress.ip_network(value,strict=False)
            if field=='Ip':result.append(value)
        elif kind=='GEOIP':
            if field=='Ip':result.append('geoip:'+value.lower())
        else:
            raise ValueError('Unsupported upstream rule type: '+kind)
    if not result:
        raise ValueError('Upstream returned no matching entries for '+field)
    return result

def build(refresh=False):
    custom=load('custom-rules.json');base=load('base-rules.json')
    if not isinstance(custom,list) or not isinstance(base,list):
        raise ValueError('Custom and base rules must be arrays')
    previous=({r['Remarks']:r for r in load('rules.json')}
              if (ROOT/'rules.json').exists() else {})
    urls={r['Source']['url'] for r in base if 'Source' in r}
    downloaded={}
    if refresh:
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            jobs={url:pool.submit(download,url) for url in urls}
            for url,job in jobs.items():downloaded[url]=job.result()
    out=[];seen=set();names=set();removed=0
    for original in custom+base:
        r=copy.deepcopy(original)
        source=r.pop('Source',None)
        if source:
            field=source['field']
            r[field]=(parse_list(downloaded[source['url']],field) if refresh
                      else previous[r['Remarks']][field])
        r.pop('Id',None)
        if not isinstance(r.get('Remarks'),str) or not r['Remarks'].strip():
            raise ValueError('Every group needs a descriptive Remarks')
        if r['Remarks'] in names:
            raise ValueError('Duplicate alias: '+r['Remarks'])
        if r.get('OutboundTag') not in ('direct','proxy','block'):
            raise ValueError('Unknown outbound tag')
        if r.get('Enabled') is not True:
            raise ValueError('Disable a rule by removing it from the source file')
        if not any(k in r for k in ('Domain','Ip','Port','Network','Protocol','InboundTag')):
            raise ValueError('Group has no matcher: '+r['Remarks'])
        if any(not isinstance(r[k],list) for k in ('Domain','Ip') if k in r):
            raise ValueError('Domain and Ip must be arrays')
        for field in ('Domain','Ip'):
            if field not in r:continue
            keep=[]
            for value in r[field]:
                if not isinstance(value,str) or not value.strip():raise ValueError('Empty matcher')
                if field=='Ip' and not value.startswith('geoip:'):
                    ipaddress.ip_network(value,strict=False)
                if field=='Domain' and not value.startswith(('domain:','full:','keyword:','regexp:','geosite:')):
                    raise ValueError('Use an explicit domain matcher prefix')
                key=(field,value)
                if key in seen:removed+=1;continue
                seen.add(key);keep.append(value)
            r[field]=keep
        if any(k in r and not r[k] for k in ('Domain','Ip')):continue
        names.add(r['Remarks']);out.append(r)
    finals=[i for i,r in enumerate(out) if r.get('Port')=='0-65535' and not r.get('Domain') and not r.get('Ip')]
    if finals!=[len(out)-1]:raise ValueError('Keep one final catch-all at the end')
    if out[-1]['OutboundTag']!='proxy':raise ValueError('Final catch-all must use proxy')
    data=json.dumps(out,ensure_ascii=False,indent=2)+'\n'
    temp=ROOT/'rules.json.tmp';temp.write_text(data,encoding='utf-8');temp.replace(ROOT/'rules.json')
    index=['# 规则目录','',f'共 {len(out)} 个规则组；顺序即优先级。','', '| 顺序 | 别名 | 出口 | 匹配项数 |','| --- | --- | --- | --- |']
    for i,r in enumerate(out,1):
        count=len(r.get('Domain',r.get('Ip',[])))
        index.append(f'| {i} | {r["Remarks"]} | {r["OutboundTag"]} | {count or "按端口/协议"} |')
    (ROOT/'RULES.md').write_text('\n'.join(index)+'\n',encoding='utf-8')
    print(f'Built {len(out)} groups; removed {removed} duplicate entries; refreshed={refresh}')
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--refresh',action='store_true',help='Download public upstream sources; fail without replacing output if any source is unavailable')
    build(parser.parse_args().refresh)
