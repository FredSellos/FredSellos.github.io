from pathlib import Path
import sys, re, posixpath, html
from urllib.parse import urljoin
root=Path(__file__).resolve().parent
base=sys.argv[1].rstrip('/')+'/'
urls=[]
for p in sorted(root.rglob('*.html')):
 r=p.relative_to(root).as_posix(); url=urljoin(base,r); urls.append(url)
 s=p.read_text(encoding='utf-8');s=re.sub(r'<link[^>]*rel="canonical"[^>]*>', '', s)
 s=re.sub(r'<link[^>]*rel="alternate"[^>]*>',lambda m:re.sub(r'href="([^"]+)"',lambda h:'href="'+urljoin(url,h[1])+'"',m[0]),s)
 s=s.replace('</head>','<link rel="canonical" href="'+url+'"></head>',1);p.write_text(s,encoding='utf-8')
(root/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+html.escape(u)+'</loc></url>' for u in urls)+'</urlset>')
(root/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+base+'sitemap.xml\n')
