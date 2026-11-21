from PIL import Image, ImageDraw, ImageFont

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

def main():
    im=Image.new("RGB",(W*S,H*S),paper); d=ImageDraw.Draw(im)
    d.rectangle((0,0,W*S,8*S),fill=red)
    t(d,(34,15),"THE WIRE",font("serifb",40),ink)
    t(d,(325,25),"SATURDAY / 21 NOVEMBER 2026",font("sansb",24),red)
    t(d,(36,67),"A live tape from 22 distinct threads. Earlier event dates stay on the record.",font("serifb",20),blue)

    stories=[
        ("FLASH 04:00 WIB","AI ROUT / NASDAQ -5.28%","Friday: S&P -3.70%, Dow -1.93%; ANT $88.30 (-9.1%).","Reuters / AP"),
        ("FLASH / KYIV","800,000+ BACK ON POWER","DTEK update; toll: 9 dead, 30 injured.","DTEK / Kyiv Independent"),
        ("FLASH / ANTALYA","COP31 OVERTIME","No final deal; third draft promised after overnight talks.","AP / Carbon Brief"),
        ("REPORTED SAT","POLAND AIRSPACE VIOLATION","Friday missiles; Warsaw seeks NATO support.","AP / NATO"),
        ("REPORTED SAT","EU–UK RESET AGREED","Friday food, emissions and youth deals.","Reuters / Euronext"),
        ("REPORTED SAT","INDONESIA FIRES / 1.92m ha","CELIOS: losses up to $31.12bn.","CELIOS"),
        ("REPORTED SAT","JAPAN CPI / 2.3%","October; core 2.2%; released Friday.","Reuters"),
        ("REPORTED SAT","n0n VENDOR FILES LEAKED","Over 16,000 customer emails exposed.","Reuters"),
        ("REPORTED SAT","ROHINGYA SKILLS ROUTE","Friday plan proposes 10,000 resettlements in Turkey.","Reuters"),
        ("SAT STUMPS","INDIA 159/1 AT WELLINGTON","Day 2: trails New Zealand by 209.","JagranJosh"),
        ("SATURDAY / ODESA","41,000 ODESA FAMILIES","Saturday attack cuts power.","DTEK"),
        ("SATURDAY / RIYADH","RIYADH MISSILES INTERCEPTED","Coalition reports three destroyed.","Reuters"),
        ("REPORTED SAT","PERU QUAKE / M6.8","Friday tremor; no early casualties reported.","Reuters / Peru Geophysical Institute"),
        ("REPORTED SAT","AKVAN AFTERMATH","Saturday fog disrupted traffic in Ganjam.","Odisha TV"),
        ("REPORTED SAT","GENEVA WEAPONS TALKS SLIP","Friday deadline ran into Saturday.","Reuters"),
        ("REPORTED SAT","IOWA DETONATION PAUSED","Friday court stay halts Army blast plan.","AP"),
        ("REPORTED SAT","PALISADES FIRE VERDICT","Friday jury convicts; first trial deadlocked.","AP"),
        ("REPORTED SAT","INSIDER-TRADING EXTRADITION","Singaporean appeared in Boston Friday.","Reuters / US Department of Justice"),
        ("REPORTED SAT","AUSTRIA CYBER BREACH","Ministry records viewed; access stopped Nov 13.","Reuters / Austrian Foreign Ministry"),
        ("REPORTED SAT","FBI DATABASE BREACH PROBED","FBI investigates suspected NCIC access.","Reuters citing CNN"),
        ("REPORTED SAT","CONTRACTORS AND CONGRESS","Order flags contractor probes.","Reuters / White House"),
        ("REPORTED SAT","HOUSE VOTE RULING","Friday: proxy rule breached the quorum clause.","Reuters / Fifth Circuit")
    ]
    assert len(stories)==22
    top=99; step=35; spine_x=58
    d.line((spine_x*S,top*S,spine_x*S,(top+(len(stories)-1)*step+13)*S),fill=red,width=5*S)
    for i,(stamp,head,body,src) in enumerate(stories):
        y=top+i*step
        if i<3: box(d,(78,y-2,990,y+31),(255,248,234),outline=(220,196,155),width=1,r=3)
        d.ellipse(((spine_x-5)*S,(y+5)*S,(spine_x+5)*S,(y+15)*S),fill=gold if i<3 else paper,outline=red,width=2*S)
        t(d,(83,y),stamp,font("sansb",10),red)
        hf=font("serifb",24)
        hbox=d.textbbox((0,0),head,font=hf)
        assert hbox[2] <= 742*S, (head,hbox[2]/S)
        title_x=238
        t(d,(title_x,y+2),head,hf,ink)
        bf=font("sans",13)
        bbox=d.textbbox((0,0),body,font=bf)
        body_x=title_x+hbox[2]/S+10
        # Keep a clear gutter for the right-edge tape index.
        assert body_x+bbox[2]/S <= 980, (head,body,body_x+bbox[2]/S)
        t(d,(body_x,y+7),body,bf,muted)
        t(d,(1000,y+5),str(i+1).zfill(2),font("sansb",10),blue,anchor="ra")

    # Small world map strip anchoring the wire's datelines.
    y=875; map_x=34; box(d,(map_x,y,990,y+61),sea,outline=(185,201,195),width=1,r=3)
    t(d,(45,y+6),"DATELINES",font("sansb",10),blue)
    land=(129,157,145); coast=(67,103,94)
    shapes=[[(120,13),(185,8),(221,14),(208,25),(177,30),(159,24),(141,30),(125,22)],
      [(216,30),(232,30),(237,40),(229,51),(220,45)],
      [(423,15),(456,10),(481,14),(474,22),(447,24),(430,21)],
      [(439,24),(470,24),(482,33),(472,45),(457,50),(446,39)],
      [(480,14),(526,10),(574,15),(606,19),(594,27),(560,27),(548,36),(525,29),(504,24),(486,23)],
      [(559,38),(579,36),(597,43),(591,51),(572,49)],
      [(642,47),(661,43),(676,48),(670,53),(652,53)]]
    for poly in shapes:
        d.polygon([((map_x+px)*S,(y+py)*S) for px,py in poly],fill=land,outline=coast)
    labels=[("NEW YORK",113),("LIMA",250),("EUROPE",402),("RIYADH",527),("JAKARTA",658),("TOKYO",757),("WELLINGTON",856)]
    for name,lx in labels:
        t(d,(lx,y+45),name,font("sansb",10),blue)
    for px,py in [(174,20),(226,40),(456,20),(522,28),(574,43),(600,23),(670,50)]:
        d.ellipse(((map_x+px-3)*S,(y+py-3)*S,(map_x+px+3)*S,(y+py+3)*S),fill=red)

    t(d,(34,941),"DATE CHECK / Every story here was first reported on",font("sansb",22),red)
    t(d,(34,968),"Saturday 21 November 2026. Earlier event dates are shown in the text.",font("sansb",22),red)
    t(d,(34,1002),"SOURCES / Reuters · AP · DTEK · Kyiv Independent · Carbon Brief · CELIOS · JagranJosh · Odisha TV | Full ledger: SOURCES.md",font("sans",10),blue)
    im.resize((W,H),Image.Resampling.LANCZOS).save("assets/entry.png",format="PNG",optimize=True)

if __name__ == "__main__": main()
