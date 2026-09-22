from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import csv

ROOT=Path(__file__).parent; V=ROOT/'visuals'; V.mkdir(exist_ok=True)
font=ImageFont.load_default(); bold=font
def chart(path,title,series,ylabel):
    W,H=1200,650; im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im); L,T,R,B=100,70,1150,560
    d.text((L,25),title,fill='black',font=bold); d.text((20,300),ylabel,fill='black',font=font)
    vals=[v for a in series.values() for v in a[1]]; lo=min(vals); hi=max(vals); pad=(hi-lo)*.1 or .1; lo-=pad; hi+=pad
    d.line((L,T,L,B),fill='black',width=2); d.line((L,B,R,B),fill='black',width=2)
    colors=['#1f77b4','#d62728','#2ca02c','#9467bd','#ff7f0e','#17becf','#8c564b']
    xs=list(range(len(next(iter(series.values()))[0]))); n=max(xs) or 1
    for j,(name,(labels,arr)) in enumerate(series.items()):
        pts=[]
        for i,v in enumerate(arr):
            x=L+(R-L)*i/n; y=B-(B-T)*(v-lo)/(hi-lo); pts.append((x,y))
        d.line(pts,fill=colors[j%len(colors)],width=4)
        d.text((900,80+j*25),name,fill=colors[j%len(colors)],font=font)
    for i,l in enumerate(next(iter(series.values()))[0]):
        if i%2==0: d.text((L+(R-L)*i/n-15,B+10),str(l),fill='black',font=font)
    im.save(path)

with open(Path('..')/'output'/'rolling_pca_yearly_returns_sector_average.csv',newline='') as f:
    rows=list(csv.DictReader(f))
labels=[r['year'] for r in rows]
series={k:(labels,[float(r[k])*100 for r in rows]) for k in ['monthly','quarterly','half_yearly','yearly']}
chart(V/'rolling_annual_returns.png','Rolling PCA annual return: sector average',series,'Return (%)')

with open(Path('..')/'output'/'holdout_returns.csv',newline='') as f: rows=list(csv.DictReader(f))
sectors=[]; vals={}
for r in rows:
    if r['method'] in ('maximum_sharpe','eigen'):
        if r['sector'] not in sectors: sectors.append(r['sector'])
        vals.setdefault(r['method'],[]).append(float(r['six_month_return'])*100)
W,H=1200,650; im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im); L,T,R,B=100,70,1150,560; d.text((L,25),'Fixed portfolio six-month holdout return by sector',fill='black',font=bold); d.line((L,T,L,B),fill='black',width=2); d.line((L,B,R,B),fill='black',width=2)
lo=min(min(v) for v in vals.values()); hi=max(max(v) for v in vals.values()); scale=(B-T)/(hi-lo+10); zero=B-(-lo)*scale
for i,s in enumerate(sectors):
 x=L+40+i*(R-L-80)/len(sectors); a=vals['maximum_sharpe'][i]; b=vals['eigen'][i]
 for off,v,c in [(-12,a,'#d62728'),(12,b,'#1f77b4')]:
  y=zero-v*scale; d.rectangle((x+off-8,min(zero,y),x+off+8,max(zero,y)),fill=c)
 d.text((x-25,B+10),s[:8],fill='black',font=font)
d.text((900,80),'Maximum Sharpe',fill='#d62728',font=font); d.text((900,105),'Eigen',fill='#1f77b4',font=font); im.save(V/'fixed_holdout_sector_returns.png')
print('created visuals')
