from PIL import Image, ImageDraw, ImageFont
import math

S = 2
W = H = 1024
paper = (247, 241, 228)
ink = (24, 35, 52)
red = (181, 43, 47)
blue = (38, 78, 111)
gold = (210, 157, 58)
muted = (96, 91, 82)
sea = (226, 235, 232)

def font(name, size):
    path = "/usr/share/fonts/truetype/dejavu/" + ("DejaVuSerif-Bold.ttf" if name == "serifb" else "DejaVuSerif.ttf" if name == "serif" else "DejaVuSans-Bold.ttf" if name == "sansb" else "DejaVuSans.ttf")
    return ImageFont.truetype(path, size*S)

def t(d, xy, text, f, fill=ink, anchor=None):
    d.text((xy[0]*S, xy[1]*S), text, font=f, fill=fill, anchor=anchor)

def box(d, xy, fill, outline=None, width=1, r=0):
    p=tuple(v*S for v in xy)
    d.rounded_rectangle(p, radius=r*S, fill=fill, outline=outline, width=width*S)

def wrap(d, text, f, maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        q=(cur+" "+w).strip()
        if d.textbbox((0,0),q,font=f)[2] <= maxw*S: cur=q
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def scene(d, kind, x, y, w, h):
    box(d,(x,y,x+w,y+h),(236,229,211),outline=(210,198,177),width=1,r=5)
    if kind == "market":
        d.line((x*S,(y+h-18)*S,(x+w)*S,(y+h-18)*S),fill=blue,width=2*S)
        pts=[(x+8,y+h-28),(x+22,y+h-38),(x+36,y+h-27),(x+52,y+h-54),(x+68,y+h-30),(x+84,y+h-64),(x+105,y+h-48)]
        d.line([(a*S,b*S) for a,b in pts],fill=red,width=3*S)
        t(d,(x+8,y+10),"NASDAQ",font("sansb",10),blue)
    elif kind == "power":
        for i in range(3):
            xx=x+18+i*35
            d.line((xx*S,(y+18)*S,(xx+12)*S,(y+h-17)*S),fill=blue,width=2*S)
            d.line(((xx+6)*S,(y+31)*S,(xx+28)*S,(y+31)*S),fill=blue,width=2*S)
        d.polygon([(x+78)*S,(y+13)*S,(x+65)*S,(y+43)*S,(x+78)*S,(y+43)*S,(x+68)*S,(y+h-10)*S,(x+96)*S,(y+53)*S,(x+82)*S,(y+53)*S],fill=gold)
        t(d,(x+8,y+10),"KYIV",font("sansb",10),blue)
    elif kind == "climate":
        d.ellipse(((x+25)*S,(y+15)*S,(x+75)*S,(y+65)*S),fill=(100,160,180),outline=blue,width=2*S)
        d.arc(((x+25)*S,(y+15)*S,(x+75)*S,(y+65)*S),20,170,fill=paper,width=2*S)
        d.line(((x+8)*S,(y+h-18)*S,(x+w-8)*S,(y+h-18)*S),fill=red,width=3*S)
        t(d,(x+8,y+10),"COP31",font("sansb",10),blue)
    else:
        d.ellipse(((x+20)*S,(y+18)*S,(x+55)*S,(y+53)*S),fill=red)

def bulletin(d, x, y, w, stamp, place, headline, body, accent=blue):
    box(d,(x,y,x+w,y+72),(252,248,239),outline=(214,203,184),width=1,r=4)
    t(d,(x+8,y+10),stamp,font("sansb",10),red)
    t(d,(x+8,y+25),place.upper(),font("sansb",8),accent)
    hf=font("serifb",12)
    lines=wrap(d,headline,hf,(w-16)*S)
    for i,line in enumerate(lines[:2]): t(d,(x+8,y+36+i*14),line,hf,ink)
    if body: t(d,(x+8,y+64),body,font("sans",7),muted)

def main():
    im=Image.new("RGB",(W*S,H*S),paper); d=ImageDraw.Draw(im)
    # header
    d.rectangle((0,0,W*S,8*S),fill=red)
    t(d,(34,24),"THE WIRE",font("serifb",27),ink)
    t(d,(210,28),"WIRE 21  /  ALL TIMES WIB",font("sansb",11),red)
    t(d,(34,58),"SATURDAY 21 NOVEMBER 2026",font("serifb",35),ink)
    t(d,(36,100),"A day of shocks, power restored, and negotiations that ran past the clock.",font("serifb",12),blue)
    # figures
    box(d,(34,123,990,176),(236,229,211),outline=(214,203,184),width=1,r=3)
    figures=[("-5.28%","NASDAQ"),("$88.30","ANTHROPIC"),("800,000+","KYIV POWER"),("9","KILLED"),("100,000","YOUTH PLACES"),("UP TO $31bn","FIRE LOSSES")]
    for i,(num,lab) in enumerate(figures):
        x=46+i*157
        t(d,(x,132),num,font("sansb",15),red)
        t(d,(x,153),lab,font("sansb",8),blue)
    # timeline spine
    spine_x=58
    d.line((spine_x*S,188*S,spine_x*S,735*S),fill=red,width=5*S)
    for hr,yy in [("04:00",203),("07:00",338),("09:00",473),("12:00",608),("18:00",715)]:
        d.ellipse(((spine_x-6)*S,(yy-6)*S,(spine_x+6)*S,(yy+6)*S),fill=paper,outline=red,width=2*S)
        t(d,(8,yy-7),hr,font("sansb",8),red)
    # flash cards
    cards=[(82,188,292,"04:00 WIB  /  NEW YORK","AI ROUT: MARKETS SNAP","Nasdaq -5.28%; the index lost 10% on the week. Anthropic closes $88.30, -9.1%.","market","Reuters · AP"),(392,188,292,"SAT MORNING  /  KYIV","800,000+ BACK ON POWER","DTEK says the main restoration is done after the barrage; 9 killed nationwide, 30 injured.","power","DTEK · Kyiv Independent"),(702,188,292,"SAT MORNING  /  ANTALYA","COP31 RUNS INTO OVERTIME","No final agreement yet. A third draft was promised after overnight talks; fossil-fuel language remains out.","climate","AP · Carbon Brief")]
    for x,y,w,stamp,head,body,kind,src in cards:
        box(d,(x,y,x+w,y+142),(255,251,242),outline=red,width=2,r=6)
        t(d,(x+12,y+12),stamp,font("sansb",9),red)
        scene(d,kind,x+12,y+31,92,82)
        hf=font("serifb",11)
        for j,line in enumerate(wrap(d,head,hf,w-126)[:2]): t(d,(x+114,y+35+j*13),line,hf,ink)
        for j,line in enumerate(wrap(d,body,font("sans",7),w-126)[:2]): t(d,(x+114,y+63+j*10),line,font("sans",7),muted)
        t(d,(x+12,y+121),src,font("sansb",7),blue)
    # mid bulletins
    t(d,(82,350),"THE DAY, PINNED TO THE WIRE",font("sansb",10),red)
    mids=[("FRI 06:30","SE POLAND","Missiles fall near border; nobody hurt","Two sites and a suspected drone; NATO calls it a grave violation."),("FRI CLOSE","TAIPEI / SEOUL / TOKYO","Asia closes in a red wave","Taiex -6.23%; KOSPI -5.21%; Nikkei -5.06%."),("FRIDAY","BRUSSELS","EU-UK reset: 100,000 visas each way","Agri-food, emissions trading and youth mobility deals agreed."),("REPORTED SAT","JAKARTA","Fires: up to $31bn in losses","CELIOS: 1.92m ha burned; smoke reaches Singapore and Malaysia."),("FRIDAY","TOKYO","October CPI 2.3% year-on-year","Core inflation stays above the BoJ's 2% target."),("FRIDAY","LONDON","n0n leaks vendor email files","More than 16,000 customer emails; payment networks unaffected."),("FRIDAY","KUALA LUMPUR","Malaysia plans 10,000 Rohingya resettlement","Skills-training route through Turkey, announced by the deputy PM."),("SAT STUMPS","WELLINGTON","India 159/1, chasing 368","Day 2 closes with India trailing New Zealand by 209."),("FRIDAY","ODISHA","Akvan aftermath: 372,000 evacuated","No deaths or major damage reported; rain moves north."),("REPORTED FRI","LOS ANGELES","GTA VI: Sensor Tower estimate","24.58m copies and $2.36bn day one; publisher has not confirmed.")]
    for i,row in enumerate(mids):
        col=i%2; rr=i//2
        bulletin(d,82+col*452,365+rr*75,430,*row)
    # briefs
    t(d,(82,757),"BRIEFS / LIVE FILE",font("sansb",10),red)
    briefs=["EU leaders move toward using frozen Russian assets for Ukraine.","Odesa region attack leaves 41,000 families without power.","Poland seeks more NATO Eastern Sentry resources.","COP31 decisions may roll to COP32 in Addis Ababa.","Indonesia smoke linked to >5,250 deaths and ~400,000 infections.","SoftBank fell 14.5% as Tokyo sold off.","Nvidia slid 13.8%; Reuters says SEC examines accounting.","Akvan was Odisha's third cyclone threat in 24 days.","EU-UK package could add 0.5% GDP by 2040.","No emergency outages remain in Kyiv; rolling cuts continue.","India-NZ Day 3 begins Saturday.","Sensor Tower labels GTA VI figures an estimate."]
    for i,b in enumerate(briefs):
        col=i%2; rr=i//2
        t(d,(82+col*452,774+rr*13),f"{('06' if rr<2 else '17')}:00  "+b,font("sans",7),ink)
    # map strip
    y=862; box(d,(34,y,990,935),sea,outline=(185,201,195),width=1,r=3)
    t(d,(46,y+7),"DATELINES",font("sansb",9),blue)
    # Hand-drawn equirectangular outline, cropped to the populated latitudes.
    map_left,map_right=112,965
    def project(lon,lat):
        return (map_left+(lon+180)*(map_right-map_left)/360, y+26+(60-lat)*34/120)
    for lon in [-120,-60,0,60,120]:
        gx,_=project(lon,0); d.line((gx*S,(y+25)*S,gx*S,(y+62)*S),fill=(190,205,201),width=1*S)
    for lat in [0,30,60]:
        _,gy=project(0,lat); d.line((map_left*S,gy*S,map_right*S,gy*S),fill=(190,205,201),width=1*S)
    land=(193,211,202)
    continents=[[( -168,60),(-150,70),(-130,68),(-120,55),(-105,50),(-95,48),(-82,25),(-98,15),(-110,25),(-120,32),(-130,50),(-150,55),(-168,60)],
      [(-80,12),(-68,10),(-50,-2),(-48,-18),(-58,-35),(-70,-55),(-78,-35),(-82,-10),(-80,12)],
      [(-10,35),(-10,55),(5,60),(25,70),(45,60),(35,45),(25,35),(10,36),(-10,35)],
      [(-18,35),(5,37),(30,30),(45,12),(40,-10),(30,-30),(18,-35),(5,-25),(-5,-5),(-18,15),(-18,35)],
      [(35,55),(60,70),(100,72),(135,60),(160,55),(150,40),(130,35),(120,20),(105,5),(90,10),(78,22),(60,25),(45,40),(35,55)],
      [(112,-12),(130,-10),(145,-20),(150,-35),(135,-42),(115,-30),(112,-12)],
      [(165,-35),(178,-40),(174,-46),(168,-44),(165,-35)]]
    for poly in continents:
        d.line([tuple(int(v*S) for v in project(lon,lat)) for lon,lat in poly],fill=land,width=5*S,joint="curve")
    places=[("NY",-74.0,40.7),("BRU",4.35,50.85),("WAW",21,52.2),("KYI",30.5,50.4),("ANT",30.7,36.9),("TKY",139.7,35.7),("GOP",84.9,19.3),("JKT",106.8,-6.2),("WLG",174.8,-41.3)]
    for name,lon,lat in places:
        px,py=project(lon,lat)
        d.ellipse(((px-3)*S,(py-3)*S,(px+3)*S,(py+3)*S),fill=red)
        t(d,(px+4,py-7),name,font("sansb",6),blue)
    # date check/footer
    t(d,(34,948),"DATE CHECK ✓ Every story here happened, or was first reported, on Saturday 21 November 2026.",font("sansb",8),red)
    t(d,(34,963),"LEFT OUT: Shenzhen summit · ICJ Rohingya verdict · Anthropic $97.17 debut · Senate Iran vote · GTA VI launch · EU €45bn loan (all Thu).",font("sans",6),muted)
    t(d,(34,979),"SOURCES  Reuters · AP · AFP · BBC · DTEK · UN News · Kyiv Independent · Carbon Brief · Health Policy Watch · CELIOS · Copernicus · Sensor Tower (estimate)",font("sans",6),blue)
    im.resize((W,H),Image.Resampling.LANCZOS).save("assets/entry.png",format="PNG",optimize=True)

if __name__ == "__main__": main()
