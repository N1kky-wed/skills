# pick a 6th voice colour: most distinct from the other tracks and from the reserved/neutral colours, in both lights
import math

def srgb(h):
    h = h.lstrip('#'); return [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
def lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def lum(h): r, g, b = map(lin, srgb(h)); return 0.2126*r + 0.7152*g + 0.0722*b
def cr(a, b): la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)
def lab(h):
    r, g, b = map(lin, srgb(h))
    x = (0.4124*r + 0.3576*g + 0.1805*b) / 0.95047; y = 0.2126*r + 0.7152*g + 0.0722*b; z = (0.0193*r + 0.1192*g + 0.9505*b) / 1.08883
    f = lambda t: t ** (1/3) if t > 216/24389 else (24389/27*t + 16) / 116
    fx, fy, fz = f(x), f(y), f(z)
    return 116*fy - 16, 500*(fx - fy), 200*(fy - fz)
def de(h1, h2):  # CIEDE2000
    L1, a1, b1 = lab(h1); L2, a2, b2 = lab(h2)
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2); Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb**7 / (Cb**7 + 25**7)))
    a1p, a2p = a1*(1+G), a2*(1+G); C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360; h2p = math.degrees(math.atan2(b2, a2p)) % 360
    dL, dC = L2 - L1, C2p - C1p
    dh = 0 if C1p*C2p == 0 else (h2p - h1p if abs(h2p - h1p) <= 180 else (h2p - h1p - 360 if h2p > h1p else h2p - h1p + 360))
    dH = 2*math.sqrt(C1p*C2p)*math.sin(math.radians(dh/2))
    Lb, Cbp = (L1 + L2)/2, (C1p + C2p)/2
    hb = h1p + h2p if C1p*C2p == 0 else ((h1p + h2p)/2 if abs(h1p - h2p) <= 180 else ((h1p + h2p + 360)/2 if h1p + h2p < 360 else (h1p + h2p - 360)/2))
    T = 1 - 0.17*math.cos(math.radians(hb-30)) + 0.24*math.cos(math.radians(2*hb)) + 0.32*math.cos(math.radians(3*hb+6)) - 0.20*math.cos(math.radians(4*hb-63))
    SL = 1 + 0.015*(Lb-50)**2/math.sqrt(20+(Lb-50)**2); SC = 1 + 0.045*Cbp; SH = 1 + 0.015*Cbp*T
    RT = -2*math.sqrt(Cbp**7/(Cbp**7+25**7))*math.sin(math.radians(60*math.exp(-((hb-275)/25)**2)))
    return math.sqrt((dL/SL)**2 + (dC/SC)**2 + (dH/SH)**2 + RT*(dC/SC)*(dH/SH))
def hexof(L, C, H):  # from CIE LCh (D65) to hex, None if out of gamut
    a, b = C*math.cos(math.radians(H)), C*math.sin(math.radians(H))
    fy = (L + 16) / 116; fx, fz = fy + a/500, fy - b/200
    inv = lambda t: t**3 if t**3 > 216/24389 else (116*t - 16) / (24389/27)
    x, y, z = inv(fx)*0.95047, inv(fy), inv(fz)*1.08883
    rl = 3.2406*x - 1.5372*y - 0.4986*z; gl = -0.9689*x + 1.8758*y + 0.0415*z; bl = 0.0557*x - 0.2040*y + 1.0570*z
    out = []
    for c in (rl, gl, bl):
        if c < -0.001 or c > 1.001: return None
        c = min(1, max(0, c)); c = 12.92*c if c <= 0.0031308 else 1.055*c**(1/2.4) - 0.055
        out.append(round(c*255))
    return '#%02x%02x%02x' % tuple(out)

DAY = dict(violet='#6a4de6', blue='#2f6ad8', teal='#0b7f78', rose='#c93a80', fuchsia='#9b35b5', indigo='#4043c2', plum='#7d4f93',
           ink3='#555770', ink2='#474a64', rec='#e5484d', rectext='#c9353a', hand='#f2a51f', warn='#9a6100', green='#1f9d64')
NIGHT = dict(violet='#9b84ff', blue='#6f9dff', teal='#3cc6b8', rose='#ff72b4', fuchsia='#d884f2', indigo='#9295ff', plum='#c9a3dc',
             ink3='#aaa6cd', ink2='#cdc9ea', rec='#f0555a', rectext='#ff8a8e', hand='#f2a51f', warn='#f4b544', green='#3fcf8e')

def best(refs, ok):
    res = []
    for H in range(0, 360, 3):
        top = None
        for L in range(30, 86, 2):
            for C in range(20, 110, 4):
                h = hexof(L, C, H)
                if not h or not ok(h): continue
                d = min(de(h, r) for r in refs.values())
                if not top or d > top[0]: top = (d, h, L, C)
        if top: res.append((H, *top))
    return res

day = best(DAY, lambda h: cr(h, '#ffffff') >= 4.6 and cr(h, '#fbfaff') >= 4.5 and cr('#ffffff', h) >= 4.5)
night = best(NIGHT, lambda h: cr(h, '#16142a') >= 4.6 and cr(h, '#211e3b') >= 4.5)
print('hue  day: minDE hex  nearest            | night: minDE hex nearest')
for (H, d1, h1, *_), (_, d2, h2, *_) in zip(day, night):
    n1 = min(DAY, key=lambda k: de(h1, DAY[k])); n2 = min(NIGHT, key=lambda k: de(h2, NIGHT[k]))
    print(f'{H:3d}  {d1:5.1f} {h1} {n1:9s}          | {d2:5.1f} {h2} {n2}')
print('slate now: day', round(min(de('#566781', v) for v in DAY.values()), 1), 'night', round(min(de('#a7b4d6', v) for v in NIGHT.values()), 1))
