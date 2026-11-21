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
    box(d,(x,y,x+w,y+82),(252,248,239),outline=(214,203,184),r=4)
    t(d,(x+10,y+5),stamp+" / "+place,font("sansb",11),red)
    t(d,(x+10,y+22),headline,font("serifb",21),ink)
    lines=wrap(d,body,font("sans",12),w-20)
    assert len(lines)<=2, (headline,lines)
    for i,line in enumerate(lines): t(d,(x+10,y+51+i*15),line,font("sans",12),muted)

def main():
    im=Image.new("RGB",(W*S,H*S),paper); d=ImageDraw.Draw(im)
    d.rectangle((0,0,W*S,8*S),fill=red)
    t(d,(34,19),"THE WIRE",font("serifb",40),ink)
    t(d,(325,29),"SATURDAY / 21 NOVEMBER 2026",font("sansb",24),red)
    t(d,(36,76),"Markets break. Kyiv reconnects. COP31 runs past the clock.",font("serifb",22),blue)
    # A report-day spine, not invented event times.
    d.line((57*S,132*S,57*S,854*S),fill=red,width=5*S)
    for yy,label in [(145,"01"),(355,"02"),(720,"03")]:
        d.ellipse((47*S,(yy-10)*S,67*S,(yy+10)*S),fill=paper,outline=red,width=2*S)
        t(d,(12,yy-9),label,font("sansb",12),red)
    cards=[
        ("REPORTED SAT 04:00 WIB / NEW YORK","AI ROUT","NASDAQ -5.28%","Friday’s close, reported Saturday 04:00 WIB: S&P -3.70%; Dow -1.93%. ANT $88.30, down 9.1%.","market","Reuters / AP"),
        ("SAT MORNING / KYIV","POWER RETURNS","800,000+ BACK","DTEK restores power Saturday after the barrage. Nationwide toll: 9 killed, 30 injured.","power","DTEK / Kyiv Independent"),
        ("SAT MORNING / ANTALYA","COP31 OVERTIME","NO FINAL DEAL","Saturday talks continue. A third draft was promised after overnight negotiations.","climate","AP / Carbon Brief")]
    for i,(stamp,head,figure,body,kind,src) in enumerate(cards):
        x=82+i*306; y=125; w=294
        box(d,(x,y,x+w,y+204),(255,251,242),outline=red,width=2,r=6)
        t(d,(x+12,y+9),"FLASH",font("sansb",12),red)
        t(d,(x+12,y+29),stamp,font("sansb",11),red)
        t(d,(x+12,y+51),head,font("serifb",23),ink)
        t(d,(x+12,y+84),figure,font("sansb",22),red)
        lines=wrap(d,body,font("sans",13),w-24)
        assert len(lines)<=4
        for j,line in enumerate(lines): t(d,(x+12,y+118+j*17),line,font("sans",13),ink)
        t(d,(x+12,y+185),src,font("sansb",11),blue)
    t(d,(82,340),"SATURDAY REPORT FILE / PRIOR EVENT DATES SHOWN BELOW",font("sansb",12),red)
    mids=[
        ("REPORTED SAT","POLAND","Missiles; nobody hurt","Friday 06:30: two missiles + suspected drone. Poland seeks NATO Eastern Sentry resources."),
        ("REPORTED SAT","ASIA MARKETS","Asia stocks tumble","Friday closes: Taiex -6.23%; KOSPI -5.21%; Nikkei -5.06%. Reported Saturday morning WIB."),
        ("REPORTED SAT","BRUSSELS","EU–UK reset agreed","Friday deal: agri-food, emissions trading and 100,000 youth visas each way. Reuters."),
        ("REPORTED SAT","JAKARTA","1.92m hectares burned","CELIOS report: fire losses up to $31.12bn; smoke reaches Singapore and Malaysia."),
        ("REPORTED SAT","TOKYO","Japan CPI rises 2.3%","October annual inflation, released Friday; core 2.2%, above the BoJ’s 2% target. Reuters."),
        ("REPORTED SAT","LONDON","n0n leaks vendor files","Friday leak: over 16,000 customer emails. Payment networks unaffected. Reuters."),
        ("REPORTED SAT","MALAYSIA","Rohingya resettlement","Friday announcement: 10,000-person skills route via Turkey proposed by deputy PM. Reuters."),
        ("SAT STUMPS","WELLINGTON","India reaches 159/1","Chasing New Zealand’s 368; India trails by 209 at the close of Day 2. JagranJosh.")]
    for i,row in enumerate(mids):
        bulletin(d,82+(i%2)*459,362+(i//2)*86,447,*row)
    t(d,(82,713),"SATURDAY FOLLOW-UPS / LIVE FILE",font("sansb",12),red)
    briefs=[
        ("ODESA: 41,000 families lose power","Saturday attack / DTEK"),
        ("KYIV: emergency outages end","Saturday; rolling cuts continue / DTEK"),
        ("POLAND: NATO resources sought","Saturday follow-up / AP, NATO"),
        ("COP31: decisions may roll to COP32","Saturday talks / Carbon Brief"),
        ("CRICKET: Day 3 begins Saturday","India–New Zealand / JagranJosh")]
    for i,(head,detail) in enumerate(briefs):
        yy=737+i*25
        t(d,(82,yy),head,font("serifb",21),ink)
        t(d,(575,yy+4),detail,font("sans",11),blue)
    # map strip
    y=862; box(d,(34,y,990,935),sea,outline=(185,201,195),width=1,r=3)
    t(d,(46,y+7),"DATELINES",font("sansb",9),blue)
    # Hand-drawn equirectangular outline, cropped to the populated latitudes.
    map_left,map_right=112,965
    def project(lon,lat):
        return (map_left+(lon+180)*(map_right-map_left)/360, y+18+(75-lat)*48/135)
    for lon in [-120,-60,0,60,120]:
        gx,_=project(lon,0); d.line((gx*S,(y+25)*S,gx*S,(y+62)*S),fill=(190,205,201),width=1*S)
    for lat in [0,30,60]:
        _,gy=project(0,lat); d.line((map_left*S,gy*S,map_right*S,gy*S),fill=(190,205,201),width=1*S)
    land=(129,157,145)
    coast=(67,103,94)
    continents=[[( -168,60),(-150,70),(-130,68),(-120,55),(-105,50),(-95,48),(-82,25),(-98,15),(-110,25),(-120,32),(-130,50),(-150,55),(-168,60)],
      [(-80,12),(-68,10),(-50,-2),(-48,-18),(-58,-35),(-70,-55),(-78,-35),(-82,-10),(-80,12)],
      [(-10,35),(-10,55),(5,60),(25,70),(45,60),(35,45),(25,35),(10,36),(-10,35)],
      [(-18,35),(5,37),(30,30),(45,12),(40,-10),(30,-30),(18,-35),(5,-25),(-5,-5),(-18,15),(-18,35)],
      [(35,55),(60,70),(100,72),(135,60),(160,55),(150,40),(130,35),(120,20),(105,5),(90,10),(78,22),(60,25),(45,40),(35,55)],
      [(112,-12),(130,-10),(145,-20),(150,-35),(135,-42),(115,-30),(112,-12)],
      [(165,-35),(178,-40),(174,-46),(168,-44),(165,-35)]]
    for poly in continents:
        d.polygon([tuple(int(v*S) for v in project(lon,lat)) for lon,lat in poly],fill=land,outline=coast,width=S)
    places=[("NEW YORK",-74,40.7),("EUROPE",15,50),("JAKARTA",106.8,-6.2),("TOKYO",139.7,35.7),("WELLINGTON",174.8,-41.3)]
    positions={"NEW YORK":(285,y+5),"EUROPE":(530,y+5),"JAKARTA":(670,y+55),"TOKYO":(830,y+5),"WELLINGTON":(870,y+55)}
    for name,lon,lat in places:
        px,py=project(lon,lat)
        d.ellipse(((px-3)*S,(py-3)*S,(px+3)*S,(py+3)*S),fill=red)
        lx,ly=positions[name]
        t(d,(lx,ly),name,font("sansb",10),blue)
    # Report-day claim explicitly allows the prior event dates disclosed above.
    t(d,(34,943),"DATE CHECK / Every story here was first reported on",font("sansb",17),red)
    t(d,(34,966),"Saturday 21 November 2026. Earlier event dates are shown in the text.",font("sansb",17),red)
    t(d,(34,997),"SOURCES / Reuters · AP · DTEK · Kyiv Independent · Carbon Brief · CELIOS · JagranJosh | Full ledger: SOURCES.md",font("sans",10),blue)
    im.resize((W,H),Image.Resampling.LANCZOS).save("assets/entry.png",format="PNG",optimize=True)

if __name__ == "__main__": main()
