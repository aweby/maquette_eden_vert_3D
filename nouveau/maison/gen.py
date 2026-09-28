import math, json, os
S=26; C=math.cos(math.radians(30))
def iso(x,y,z): return ((x-y)*C*S, (x+y)*0.5*S - z*S)
def P(pts): return 'M'+' L'.join(f'{a:.1f},{b:.1f}' for a,b in (iso(*p) for p in pts))+'Z'
out=[]
def poly(pts,fill,cls='',extra=''):
    out.append(f'<path d="{P(pts)}" fill="{fill}"{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} {extra}/>')
def box(x0,y0,z0,x1,y1,z1,top,fx,fy,cls=''):
    poly([(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)],fx,cls)
    poly([(x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1)],fy,cls)
    poly([(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],top,cls)
def raw(s): out.append(s)
def pt(x,y,z): a,b=iso(x,y,z); return a,b
W,D=10,6; WT=0.3   # largeur, profondeur, épaisseur des murs
LV={'cave':0.0,'rdc':6.8,'etage':13.6,'combles':20.8}
H=3.0
def tray(z, floor_top, floor_x, floor_y, wall_a, wall_b, slab=0.4, slab_front='#8C9098', slab_side='#A2A6AD'):
    # dalle
    box(0,0,z,W,D,z+slab,floor_top,slab_side,slab_front)
    # mur du fond x=0 (face intérieure visible) et y=0
    box(-WT,-WT,z,0,D,z+slab+H,'#FBFAF8',wall_a,'#C9C4BC')
    box(0,-WT,z,W,0,z+slab+H,'#FBFAF8','#C9C4BC',wall_b)
def window(x0,x1,zb,zt,z_off,y=0.0,frame='#FFFFFF',glass='#BFD7E6'):
    poly([(x0,y,zb),(x1,y,zb),(x1,y,zt),(x0,y,zt)],frame)
    poly([(x0+0.15,y,zb+0.15),(x1-0.15,y,zb+0.15),(x1-0.15,y,zt-0.15),(x0+0.15,y,zt-0.15)],glass)
def windowX(y0,y1,zb,zt,x=0.0,frame='#FFFFFF',glass='#BFD7E6'):
    poly([(x,y0,zb),(x,y1,zb),(x,y1,zt),(x,y0,zt)],frame)
    poly([(x,y0+0.15,zb+0.15),(x,y1-0.15,zb+0.15),(x,y1-0.15,zt-0.15),(x,y0+0.15,zt-0.15)],glass)

# ------- CAVE
z=LV['cave']
tray(z,'#B9B2A6','#A2A6AD','#8C9098',wall_a='#D8D3CB',wall_b='#CFC9BF')
fz=z+0.4
box(0.2,0.4,fz,1.2,3.6,fz+2.2,'#9C7B55','#8A6B48','#A7865F')   # étagère
for zz in (fz+0.7,fz+1.4): box(0.2,0.4,zz,1.25,3.6,zz+0.08,'#C9A77C','#A68560','#B89670')
box(5.5,0.3,fz,7.0,1.3,fz+1.1,'#8F9AA6','#77828E','#83909C')    # chaudière
for (bx,by) in [(3.0,1.0),(3.9,1.4)]: box(bx,by,fz,bx+0.8,by+0.8,fz+1.0,'#A0724A','#86603D','#946A44')  # tonneaux/cartons
raw(''.join(f'<path d="{P([(x0,0.05,fz+2.4),(x0+0.12,0.05,fz+2.4),(x0+0.12,0.05,fz+0.3),(x0,0.05,fz+0.3)])}" fill="#7C8792"/>' for x0 in (8.2,8.6)))
# rats
def rat(x,y,z,flip=1,cls='rat'):
    a,b=iso(x,y,z)
    return (f'<g class="{cls}" transform="translate({a:.1f},{b:.1f}) scale({flip},1)"><path class="tail" d="M-9,1 q-9,2 -14,-5" stroke="#6E6259" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="0" cy="-3" rx="10" ry="6" fill="#6E6259"/><ellipse cx="9" cy="-5" rx="5" ry="4" fill="#7A6D63"/><circle cx="7" cy="-9" r="2.4" fill="#8A7C71"/><circle cx="12" cy="-6" r="1" fill="#111"/><circle cx="14" cy="-4.6" r="1.1" fill="#E7A4A0"/></g>')
raw(rat(4.5,4.2,fz)); raw(rat(7.8,3.4,fz,-1,'rat rat2'))

# ------- RDC : cuisine (x 0..5) | salon (x 5..10)
z=LV['rdc']
tray(z,'#D9B48A','#A2A6AD','#8C9098',wall_a='#F1E4D3',wall_b='#EADBC8')
fz=z+0.4
# couleur salon sur la moitié droite du mur du fond
poly([(5,0,fz),(W,0,fz),(W,0,fz+H),(5,0,fz+H)],'#E3E8EE')
windowX(1.6,3.6,fz+1.3,fz+2.5); window(6.5,8.5,fz+1.1,fz+2.6,0)
box(5,0,fz,5.15,D,fz+H,'#FBFAF8','#D8D2C8','#C9C4BC')   # cloison
# cuisine
box(0,0,fz,4.6,1.0,fz+1.1,'#F7F4EF','#D7D1C7','#E6E0D6')   # plan de travail fond
box(0,1.0,fz,1.0,3.4,fz+1.1,'#F7F4EF','#E6E0D6','#D7D1C7')  # retour
box(2.2,0.1,fz+1.1,3.0,0.8,fz+1.18,'#B8C4CE','#9FACB6','#A9B5BF')  # évier
box(3.6,0.0,fz,4.6,1.0,fz+2.6,'#EDEFF1','#C9CDD2','#D8DCE0')  # frigo
box(2.0,2.6,fz,3.8,4.0,fz+0.95,'#B98E5E','#9E7549','#A97E52')  # table
# cafards + fourmis
raw('<g class="roaches">'+''.join(f'<g class="roach r{i}" transform="translate({iso(x,y,fz)[0]:.1f},{iso(x,y,fz)[1]:.1f}) rotate({rot})"><ellipse rx="4.2" ry="2.4" fill="#5A3319"/><path d="M-3,-2 l-2,-2 M-3,2 l-2,2 M0,-2.4 v-2 M0,2.4 v2" stroke="#3B200F" stroke-width=".8"/></g>' for i,(x,y,rot) in enumerate([(1.6,1.6,20),(2.4,1.3,-30),(1.3,3.8,60),(3.2,1.5,10)]))+'</g>')
a0=iso(0.9,4.6,fz); a1=iso(0.9,1.2,fz)
raw(f'<line class="ants" x1="{a0[0]:.1f}" y1="{a0[1]:.1f}" x2="{a1[0]:.1f}" y2="{a1[1]:.1f}" stroke="#1E1E1E" stroke-width="2.2" stroke-dasharray="1.5 4" stroke-linecap="round"/>')
# salon
poly([(6.0,2.2,fz+0.01),(9.4,2.2,fz+0.01),(9.4,5.2,fz+0.01),(6.0,5.2,fz+0.01)],'#EE5A1B" opacity="0.18')
box(5.6,0.3,fz,9.6,1.3,fz+0.9,'#3C4450','#2F3640','#353D48')   # canapé assise
box(5.6,0.3,fz+0.9,9.6,0.7,fz+1.7,'#464F5C','#353D48','#3C4450')  # dossier
box(8.0,3.6,fz,9.2,4.8,fz+0.35,'#C7A170','#A9855A','#B89264')  # panier
bx,by=iso(8.6,4.2,fz+0.35); raw(f'<g class="dog" transform="translate({bx:.1f},{by:.1f})"><ellipse cx="0" cy="-4" rx="13" ry="7" fill="#D39A5B"/><circle cx="10" cy="-10" r="6" fill="#D39A5B"/><path d="M12,-15 l4,-4 l1,6z" fill="#B97F43"/><circle cx="12" cy="-11" r="1" fill="#111"/></g>')
raw('<g class="fleas">'+''.join(f'<circle class="flea f{i}" cx="{bx+dx:.1f}" cy="{by+dy:.1f}" r="1.4" fill="#2A1C12"/>' for i,(dx,dy) in enumerate([(-14,-16),(-4,-22),(6,-20),(18,-18),(-18,-8)]))+'</g>')

# ------- ÉTAGE : chambre (x 0..6) | salle de bain (x 6..10) ; dalle épaisse = faux plafond
z=LV['etage']
SL=1.0
box(0,0,z,W,D,z+SL,'#CFA67A','#A2A6AD','#8C9098')
# coupe du faux plafond (face avant) : vide + isolant + souris
cav=[(0.6,D,z+0.2),(W-0.6,D,z+0.2),(W-0.6,D,z+0.8),(0.6,D,z+0.8)]
poly(cav,'#2E3339')
for i in range(9):
    x0=0.8+i*1.05; poly([(x0,D,z+0.55),(x0+0.8,D,z+0.55),(x0+0.8,D,z+0.78),(x0,D,z+0.78)],'#E9C55A')
mx,my=iso(4.2,D,z+0.2); raw(f'<g class="mouse" transform="translate({mx:.1f},{my:.1f})"><path class="tail" d="M-6,-3 q-8,0 -12,-5" stroke="#9A9A9A" stroke-width="1.4" fill="none" stroke-linecap="round"/><ellipse cx="0" cy="-3.5" rx="6.5" ry="3.8" fill="#A7A7A7"/><circle cx="5" cy="-6.5" r="2.6" fill="#B8B8B8"/><circle cx="7.6" cy="-4.6" r=".9" fill="#111"/></g>')
fz=z+SL
box(-WT,-WT,z,0,D,fz+H,'#FBFAF8','#F3E7DC','#C9C4BC')
box(0,-WT,z,W,0,fz+H,'#FBFAF8','#C9C4BC','#EFE3D6')
poly([(6,0,fz),(W,0,fz),(W,0,fz+H),(6,0,fz+H)],'#DCEBEF')
windowX(2.0,4.0,fz+1.2,fz+2.5); window(7.2,8.8,fz+1.4,fz+2.6,0)
box(6,0,fz,6.15,D,fz+H,'#FBFAF8','#D8D2C8','#C9C4BC')
# lit
box(0.3,0.4,fz,3.6,3.8,fz+0.7,'#EDE7DF','#CFC7BB','#DDD5C9')
box(0.3,0.4,fz+0.7,3.6,3.8,fz+0.95,'#EE7A45','#C85A2B','#D9663A')   # couette
box(0.4,0.5,fz+0.95,1.4,3.7,fz+1.2,'#FFFFFF','#E4E0DA','#F0ECE6')   # oreillers
box(0.0,0.4,fz,0.3,3.8,fz+2.0,'#9C7B55','#8A6B48','#A7865F')   # tête de lit
box(3.8,0.3,fz,4.6,1.0,fz+0.8,'#B98E5E','#9E7549','#A97E52')   # chevet
bx,by=iso(2.2,2.2,fz+0.95)
raw('<g class="bedbugs">'+''.join(f'<ellipse class="bb b{i}" cx="{bx+dx:.1f}" cy="{by+dy:.1f}" rx="2.4" ry="1.7" fill="#7A2E1C"/>' for i,(dx,dy) in enumerate([(-12,2),(-2,-4),(8,4),(16,-2),(2,8)]))+'</g>')
# salle de bain
box(7.2,0.3,fz,9.8,1.5,fz+0.9,'#FFFFFF','#DCE3E8','#EAF0F3')   # baignoire
box(7.45,0.5,fz+0.5,9.55,1.3,fz+0.91,'#BFD7E6','#BFD7E6','#BFD7E6')
box(9.0,3.4,fz,9.9,4.4,fz+1.0,'#F4F6F8','#D5DBE0','#E3E8EC')   # lavabo

# ------- COMBLES + TOIT
z=LV['combles']
box(0,0,z,W,D,z+0.4,'#C99A62','#A2A6AD','#8C9098')
fz=z+0.4
RH=D/2*math.tan(math.radians(55))   # hauteur du faîtage
# pignon gauche (triangle, face intérieure)
poly([(0,0,fz),(0,D,fz),(0,D/2,fz+RH)],'#E3C79E')
poly([(-WT,0,fz),(0,0,fz),(0,D/2,fz+RH),(-WT,D/2,fz+RH)],'#FBFAF8')
# versant arrière (sous-face visible) + chevrons
poly([(0,0,fz),(W,0,fz),(W,D/2,fz+RH),(0,D/2,fz+RH)],'#D7B07F')
for i in range(1,10):
    x0=i*W/10; poly([(x0-0.08,0,fz),(x0+0.08,0,fz),(x0+0.08,D/2,fz+RH),(x0-0.08,D/2,fz+RH)],'#B98A57')
# tuiles : épaisseur sur la coupe
poly([(W,-0.5,fz-0.3),(W,0,fz),(W,D/2,fz+RH),(W,D/2,fz+RH+0.45),(W,-0.5,fz+0.15)],'#C1502A')
poly([(0,D/2,fz+RH),(W,D/2,fz+RH),(W,D/2,fz+RH+0.45),(0,D/2,fz+RH+0.45)],'#A8431F')
poly([(0,-0.5,fz-0.3),(W,-0.5,fz-0.3),(W,-0.5,fz+0.15),(0,-0.5,fz+0.15)],'#A8431F')
# isolant + cartons + loir
for i in range(4): box(1.2+i*1.9,1.0,fz,2.8+i*1.9,2.2,fz+0.35,'#F0CF63','#D9B447','#E4C055')
box(6.6,3.2,fz,7.8,4.4,fz+0.9,'#C49A66','#A8804F','#B68D5A')
lx,ly=iso(4.4,3.8,fz)
raw(f'<g class="loir" transform="translate({lx:.1f},{ly:.1f})"><path class="tail" d="M-8,-2 q-14,-4 -14,-16" stroke="#8C8279" stroke-width="5" fill="none" stroke-linecap="round"/><ellipse cx="0" cy="-6" rx="9" ry="7" fill="#8C8279"/><circle cx="8" cy="-10" r="5.5" fill="#9A9087"/><circle cx="6" cy="-15" r="2.6" fill="#A8A097"/><circle cx="10" cy="-11" r="1.1" fill="#111"/><path d="M10,-8.5 q2,1 4,0" stroke="#111" stroke-width=".6" fill="none"/></g>')
# pigeons sur le faîtage
def pigeon(x,cls):
    a,b=iso(x,D/2,fz+RH+0.45)
    return f'<g class="{cls}" transform="translate({a:.1f},{b:.1f})"><ellipse cx="0" cy="-7" rx="9" ry="6" fill="#8E97A3"/><path d="M-8,-8 l-7,-2 l3,5z" fill="#6F7885"/><g class="head"><circle cx="8" cy="-13" r="4" fill="#7C8592"/><path d="M11.5,-13 l3,1 l-3,1z" fill="#E4A15A"/><circle cx="9" cy="-14" r=".9" fill="#111"/></g><path d="M-1,-1 v3 M2,-1 v3" stroke="#E08A7A" stroke-width="1.2"/></g>'
raw(pigeon(3.2,'pigeon')); raw(pigeon(5.6,'pigeon p2'))
# nid de guêpes sous le débord de toit (côté droit)
gx,gy=iso(W-0.3,-0.4,fz-0.4)
raw(f'<g class="waspnest"><ellipse cx="{gx:.1f}" cy="{gy+12:.1f}" rx="9" ry="12" fill="#D8C7A6"/><path d="M{gx-8:.1f},{gy+8:.1f} h16 M{gx-9:.1f},{gy+14:.1f} h18 M{gx-6:.1f},{gy+20:.1f} h12" stroke="#B8A686" stroke-width="1.3"/><circle cx="{gx:.1f}" cy="{gy+22:.1f}" r="2.2" fill="#3A2D20"/></g>')
raw('<g class="wasps">'+''.join(f'<g class="wp wp{i}" transform="translate({gx+dx:.1f},{gy+dy:.1f})"><ellipse rx="3.4" ry="2.1" fill="#F2C12E"/><path d="M-1,-2 v4 M1.3,-2 v4" stroke="#1F1A12" stroke-width="1"/></g>' for i,(dx,dy) in enumerate([(-16,10),(14,4),(12,26),(-12,28)]))+'</g>')

# ------- JARDIN (îlot à droite, au niveau du RDC)
zg=LV['rdc']
GO=2.8
GX0,GX1=11.5+GO,20.5+GO
box(GX0,0,zg-1.6,GX1,D,zg,'#9CC46B','#7A4E33','#8A5A3C',cls='soil')
# herbe : liseré
poly([(GX0,D,zg-0.25),(GX1,D,zg-0.25),(GX1,D,zg),(GX0,D,zg)],'#7FA653')
poly([(GX1,0,zg-0.25),(GX1,D,zg-0.25),(GX1,D,zg),(GX1,0,zg)],'#6E9446')
# galerie de taupe visible dans la coupe de terre (face avant y=D)
tun=[(15.8,D,zg-0.7),(17.0,D,zg-1.0),(18.2,D,zg-0.8),(19.4,D,zg-1.1),(20.4,D,zg-0.9)]
d='M'+' L'.join(f'{a:.1f},{b:.1f}' for a,b in (iso(*p) for p in tun))
raw(f'<path d="{d}" fill="none" stroke="#4A2F1E" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')
mx,my=iso(18.2,D,zg-0.8); raw(f'<g class="mole" transform="translate({mx:.1f},{my:.1f})"><ellipse rx="7" ry="4.5" fill="#2B2B2E"/><circle cx="6" cy="-1" r="1.6" fill="#F2B8A0"/></g>')
# mare + moustiques
pond=[(16.0,0.8,zg),(18.2,0.6,zg),(18.8,2.0,zg),(17.2,2.6,zg),(15.8,2.0,zg)]
poly(pond,'#7FB6D3'); poly([(16.4,1.0,zg),(17.8,0.9,zg),(18.2,1.9,zg),(17.1,2.2,zg),(16.3,1.8,zg)],'#9ACBE2')
px,py=iso(17.2,1.6,zg+1.6)
raw('<g class="mosq">'+''.join(f'<circle class="m m{i}" cx="{px+dx:.1f}" cy="{py+dy:.1f}" r="1.6" fill="#1F2226"/>' for i,(dx,dy) in enumerate([(-10,0),(6,-8),(12,6),(-4,10),(2,-2)]))+'</g>')
# taupinières
for (x,y) in [(21.4,4.6),(20.0,5.3),(22.2,3.4)]:
    cx,cy=iso(x,y,zg); raw(f'<ellipse class="molehill" cx="{cx:.1f}" cy="{cy-3:.1f}" rx="10" ry="5.5" fill="#7A4E33"/><ellipse cx="{cx-2:.1f}" cy="{cy-5:.1f}" rx="5" ry="2.4" fill="#936246"/>')
# arbre
tx,ty=17.6+GO,1.8
box(tx-0.25,ty-0.25,zg,tx+0.25,ty+0.25,zg+4.2,'#6B4A33','#6B4A33','#7C573D')
fx,fy=iso(tx,ty,zg+5.6)
raw(f'<g class="foliage"><circle cx="{fx-34:.1f}" cy="{fy+16:.1f}" r="34" fill="#5E8C3A"/><circle cx="{fx+30:.1f}" cy="{fy+12:.1f}" r="36" fill="#5E8C3A"/><circle cx="{fx:.1f}" cy="{fy-12:.1f}" r="44" fill="#6FA046"/><circle cx="{fx-14:.1f}" cy="{fy-24:.1f}" r="22" fill="#82B356"/></g>')
# nid de chenilles (cocon blanc) + procession sur le tronc
nx,ny=iso(tx-0.6,ty+0.4,zg+5.0); raw(f'<ellipse cx="{nx:.1f}" cy="{ny:.1f}" rx="12" ry="9" fill="#F4F1EA" stroke="#D9D2C3"/><path d="M{nx-10:.1f},{ny-3:.1f} q10,6 20,0 M{nx-9:.1f},{ny+3:.1f} q9,5 18,0" stroke="#D9D2C3" fill="none"/>')
t0=iso(tx+0.25,ty+0.25,zg+3.6); t1=iso(tx+0.25,ty+0.25,zg+0.3)
raw(f'<line class="procession" x1="{t0[0]:.1f}" y1="{t0[1]:.1f}" x2="{t1[0]:.1f}" y2="{t1[1]:.1f}" stroke="#8C6A2E" stroke-width="4" stroke-dasharray="5 3" stroke-linecap="round"/>')
# nid de frelons suspendu
hx,hy=iso(tx+1.2,ty+0.8,zg+4.3); raw(f'<line x1="{hx:.1f}" y1="{hy-26:.1f}" x2="{hx:.1f}" y2="{hy-12:.1f}" stroke="#4E3A28" stroke-width="2"/><ellipse cx="{hx:.1f}" cy="{hy:.1f}" rx="11" ry="14" fill="#C9B79A"/><path d="M{hx-10:.1f},{hy-4:.1f} h20 M{hx-11:.1f},{hy+3:.1f} h22 M{hx-8:.1f},{hy+9:.1f} h16" stroke="#A8957A" stroke-width="1.5"/><circle cx="{hx:.1f}" cy="{hy+11:.1f}" r="2.5" fill="#3A2D20"/>')
raw('<g class="hornets">'+''.join(f'<g class="hn hn{i}" transform="translate({hx+dx:.1f},{hy+dy:.1f})"><ellipse rx="3.2" ry="2" fill="#E8A21B"/><path d="M-1,-2 v4 M1.2,-2 v4" stroke="#1F1A12" stroke-width="1"/></g>' for i,(dx,dy) in enumerate([(-18,-6),(16,-10),(14,12)]))+'</g>')

# ------- liens pointillés entre étages (vue éclatée)
for x,y in [(0,D),(W,D),(W,0)]:
    for a,b in [('cave','rdc'),('rdc','etage'),('etage','combles')]:
        z0=LV[a]+0.4+H; z1=LV[b]
        if b=='etage': z0=LV['rdc']+0.4+H
        p0=iso(x,y,z0); p1=iso(x,y,z1)
        raw(f'<line x1="{p0[0]:.1f}" y1="{p0[1]:.1f}" x2="{p1[0]:.1f}" y2="{p1[1]:.1f}" stroke="#B9B4AC" stroke-width="1" stroke-dasharray="3 4"/>')

# ------- étiquettes d'étage
for k,lab in [('cave','Cave'),('rdc','Rez-de-chaussée'),('etage','Étage'),('combles','Combles')]:
    a,b=iso(0,D,LV[k]+0.2)
    raw(f'<text class="lvl" x="{a-14:.1f}" y="{b+4:.1f}" text-anchor="end">{lab}</text>')
# ------- zones (surbrillance) + repères
Z=[
 ('combles','Combles',[(0,0,LV['combles']+0.4),(W,0,LV['combles']+0.4),(W,D,LV['combles']+0.4),(0,D,LV['combles']+0.4)],(4.4,3.8,LV['combles']+1.5)),
 ('toiture','Toiture',None,(W-0.3,-0.4,LV['combles']+1.7)),
 ('chambre','Chambre',[(0,0,LV['etage']+SL),(6,0,LV['etage']+SL),(6,D,LV['etage']+SL),(0,D,LV['etage']+SL)],(2.2,2.2,LV['etage']+SL+1.8)),
 ('plafond','Faux plafond',[(0,D,LV['etage']),(W,D,LV['etage']),(W,D,LV['etage']+SL),(0,D,LV['etage']+SL)],(7.2,D,LV['etage']+0.5)),
 ('cuisine','Cuisine',[(0,0,LV['rdc']+0.4),(5,0,LV['rdc']+0.4),(5,D,LV['rdc']+0.4),(0,D,LV['rdc']+0.4)],(2.2,2.0,LV['rdc']+1.6)),
 ('salon','Salon',[(5,0,LV['rdc']+0.4),(W,0,LV['rdc']+0.4),(W,D,LV['rdc']+0.4),(5,D,LV['rdc']+0.4)],(8.6,4.2,LV['rdc']+1.9)),
 ('cave','Cave',[(0,0,0.4),(W,0,0.4),(W,D,0.4),(0,D,0.4)],(6.2,3.8,1.4)),
 ('arbre','Arbre',None,(tx,ty,zg+6.9)),
 ('mare','Jardin',None,(17.2,1.6,zg+2.6)),
 ('pelouse','Pelouse',None,(21.2,4.4,zg+1.2)),
]
zones=[]; marks=[]
for i,(k,label,pts,m) in enumerate(Z):
    if pts: zones.append(f'<path class="zone" data-zone="{k}" d="{P(pts)}"/>')
    a,b=iso(*m)
    marks.append(f'<g class="hot" data-zone="{k}" transform="translate({a:.1f},{b:.1f})" tabindex="0" role="button" aria-label="{label}"><circle class="hit" r="22"/><circle class="ring" r="15"/><circle class="dot" r="12"/><text dominant-baseline="central">{i+1}</text></g>')
# bornes
xs=[];ys=[]
for s in out+zones:
    import re
    for a,b in re.findall(r'(-?\d+\.\d),(-?\d+\.\d)',s): xs.append(float(a)); ys.append(float(b))
for a,b in [iso(*m) for *_,m in Z]: xs.append(a); ys.append(b-20)
x0,x1,y0,y1=min(xs)-30,max(xs)+30,min(ys)-30,max(ys)+20
svg=(f'<svg class="house" viewBox="{x0:.0f} {y0:.0f} {x1-x0:.0f} {y1-y0:.0f}" role="img" aria-label="Maison en coupe : où se cachent les nuisibles">'
     '<g class="scene">'+''.join(out)+'</g><g class="zones">'+''.join(zones)+'</g><g class="hots">'+''.join(marks)+'</g></svg>')
open(os.path.join(os.path.dirname(__file__),'scene.svg'),'w').write(svg); print(len(svg), f'viewBox {x1-x0:.0f}x{y1-y0:.0f}')
