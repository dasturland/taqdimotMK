"""Build the 'Internet kabellari (Optik tola) fizikasi' presentation as a real,
openable PowerPoint .pptx file -- WITH a distinct embedded image on every slide.

Why this is hand-rolled OOXML instead of python-pptx:
  The sandbox has NO outbound network (PyPI returns HTTP 403), so python-pptx
  and Pillow cannot be installed, and the Unsplash image URLs are unreachable.
  A .pptx is simply a ZIP of Open-XML parts, which the Python standard library
  can produce directly (zipfile). The slide images are drawn locally by
  make_images.py (pure stdlib) so that genuine image bytes get embedded -- this
  is what satisfies the "rasmlari bilan" (with images) requirement, since
  PowerPoint embeds image bytes and never fetches URLs.

Design mirrors presentation.html / PRESENTATION.md:
  * Times New Roman everywhere.
  * Size hierarchy 12/16/24/32/44 px -> point sizes 14/20/26/32/44 pt
    (body never tiny; title large; mega stat 44).
  * Deep-blue + neon palette (bg #06162e, cyan #22e0ff, gold #ffd166, etc.).
  * 10 slides, 4-part structure, verbatim Uzbek text.

Run:  python3 build_pptx.py
Needs make_images.py to have produced assets/slide01.png .. slide10.png
(this script will generate them automatically if missing).
"""

import os
import zipfile
from xml.sax.saxutils import escape

import make_images

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "taqdimot.pptx")

# ---- EMU geometry (16:9, 13.333in x 7.5in) ----
EMU = 914400
SLIDE_W = 12192000
SLIDE_H = 6858000

# ---- palette (hex without #) ----
BG = "06162E"
BG_PANEL = "0A2446"
CYAN = "22E0FF"
BLUE = "2F6BFF"
VIOLET = "8B5CFF"
GOLD = "FFD166"
GREEN = "4BE3A0"
TEXT = "EEF5FC"
DIM = "A9C2DA"

FONT = "Times New Roman"

# point sizes (pptx uses hundredths of a point)
PT_BODY = 1400     # 12px body -> readable 14pt
PT_ACCENT = 2000   # 16px accent -> 20pt
PT_SUB = 2600      # 24px sub-title -> 26pt
PT_TITLE = 3200    # 32px title -> 32pt
PT_MEGA = 4400     # 44px mega stat -> 44pt
PT_FOOT = 1200     # footer / caption


def emu_in(inches):
    return int(inches * EMU)


# ---------------------------------------------------------------------------
# Run / paragraph XML builders
# ---------------------------------------------------------------------------
def run(text, size, color, bold=False, italic=False):
    b = ' b="1"' if bold else ' b="0"'
    i = ' i="1"' if italic else ''
    return (
        f'<a:r><a:rPr lang="uz-UZ" sz="{size}"{b}{i} dirty="0">'
        f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
        f'<a:latin typeface="{FONT}"/><a:cs typeface="{FONT}"/></a:rPr>'
        f'<a:t>{escape(text)}</a:t></a:r>'
    )


def para(runs_xml, align="l", bullet=False, space_after=600):
    bu = ''
    marL = ''
    if bullet:
        marL = ' marL="285750" indent="-285750"'
        bu = (f'<a:buFont typeface="Arial"/>'
              f'<a:buChar char="&#8226;"/>')
    else:
        bu = '<a:buNone/>'
    return (
        f'<a:p><a:pPr algn="{align}"{marL}>'
        f'<a:spcAft><a:spcPts val="{space_after}"/></a:spcAft>{bu}</a:pPr>'
        f'{runs_xml}</a:p>'
    )


_sp_id = [10]


def next_id():
    _sp_id[0] += 1
    return _sp_id[0]


def textbox(x, y, w, h, paragraphs_xml, anchor="t", wrap=True):
    sid = next_id()
    wrap_attr = 'wrap="square"' if wrap else 'wrap="none"'
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="tb{sid}"/>'
        f'<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
        f'<p:txBody><a:bodyPr {wrap_attr} lIns="0" tIns="0" rIns="0" bIns="0" anchor="{anchor}"/>'
        f'<a:lstStyle/>{paragraphs_xml}</p:txBody></p:sp>'
    )


def rect(x, y, w, h, fill, alpha=None, line=None, line_w=12700):
    sid = next_id()
    a = f'<a:alpha val="{alpha}"/>' if alpha is not None else ''
    ln = ''
    if line:
        ln = (f'<a:ln w="{line_w}"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>')
    else:
        ln = '<a:ln><a:noFill/></a:ln>'
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="rect{sid}"/>'
        f'<p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
        f'<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 6000"/></a:avLst></a:prstGeom>'
        f'<a:solidFill><a:srgbClr val="{fill}">{a}</a:srgbClr></a:solidFill>{ln}</p:spPr>'
        f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>'
    )


def picture(rid, x, y, w, h):
    sid = next_id()
    return (
        f'<p:pic><p:nvPicPr><p:cNvPr id="{sid}" name="img{sid}"/>'
        f'<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
        f'<p:blipFill><a:blip r:embed="{rid}"/>'
        f'<a:stretch><a:fillRect/></a:stretch></p:blipFill>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f'<a:ln w="19050"><a:solidFill><a:srgbClr val="{CYAN}"><a:alpha val="55000"/></a:srgbClr></a:solidFill></a:ln>'
        f'</p:spPr></p:pic>'
    )


def footer(part_label, slide_no):
    runs_tag = run(part_label, PT_FOOT, CYAN, bold=True)
    runs_num = run(f"{slide_no} / 10", PT_FOOT, DIM, italic=True)
    left = textbox(emu_in(0.6), SLIDE_H - emu_in(0.55), emu_in(7), emu_in(0.4),
                   para(runs_tag, align="l", space_after=0), wrap=False)
    right = textbox(SLIDE_W - emu_in(3.6), SLIDE_H - emu_in(0.55), emu_in(3), emu_in(0.4),
                    para(runs_num, align="r", space_after=0), wrap=False)
    return left + right


def bg_shapes():
    """Full-slide deep-blue background + top neon strip + bottom accent."""
    full = rect(0, 0, SLIDE_W, SLIDE_H, BG)
    top = rect(0, 0, SLIDE_W, emu_in(0.07), CYAN, alpha=85000)
    bottom = rect(emu_in(0.6), SLIDE_H - emu_in(0.72), SLIDE_W - emu_in(1.2), emu_in(0.03), CYAN, alpha=70000)
    return full + top + bottom


# ---------------------------------------------------------------------------
# Content (verbatim from PRESENTATION.md)
# ---------------------------------------------------------------------------
UNIV = "Jizzax davlat pedagogika universiteti tabiiy fanlar oliy maktabi"
STUDENT = "Toshbo\u02bbriyeva Marjona (242_26 - guruh)"
FAN = "Axborot tizimlari"


def build_slide_shapes(n):
    """Return (shapes_xml, rId_image) for slide n (image rId is always 'rId2')."""
    rid = "rId2"
    shapes = [bg_shapes()]
    half_x = emu_in(0.6)
    half_w = emu_in(5.8)
    img_x = emu_in(6.9)
    img_w = emu_in(5.83)
    img_y = emu_in(1.7)
    img_h = emu_in(3.28)   # 16:9 of 5.83in

    if n == 1:
        # Title slide: centered
        badge = textbox(0, emu_in(0.5), SLIDE_W, emu_in(0.4),
                        para(run("TAQDIMOT  \u2022  AXBOROT TIZIMLARI", PT_ACCENT, CYAN, bold=True), align="ctr"))
        title = textbox(emu_in(1), emu_in(1.0), SLIDE_W - emu_in(2), emu_in(1.3),
                        para(run("Internet kabellari (Optik tola) ", PT_TITLE, TEXT, bold=True)
                             + run("fizikasi", PT_TITLE, CYAN, bold=True), align="ctr"))
        sub = textbox(emu_in(1.5), emu_in(2.2), SLIDE_W - emu_in(3), emu_in(0.9),
                      para(run("Qit\u02bbalarni bog\u02bblovchi suv osti kabellarida ma\u02bblumotlarni yorug\u02bblik tezligida uzatish texnologiyalari",
                               PT_SUB, DIM, italic=True), align="ctr"))
        img = picture(rid, emu_in(3.67), emu_in(3.15), emu_in(6.0), emu_in(3.0))
        info = textbox(emu_in(1), SLIDE_H - emu_in(1.0), SLIDE_W - emu_in(2), emu_in(0.9),
                       para(run("Universitet: ", PT_ACCENT, GOLD, bold=True) + run(UNIV, PT_BODY, TEXT), align="ctr", space_after=200)
                       + para(run("Fan: ", PT_ACCENT, GOLD, bold=True) + run(FAN, PT_BODY, TEXT)
                              + run("     Talaba: ", PT_ACCENT, GOLD, bold=True) + run(STUDENT, PT_BODY, TEXT), align="ctr", space_after=0))
        shapes += [badge, title, sub, img, info]
        return "".join(shapes), rid, None

    # Generic slide header
    def header(kicker, title_text, title_accent=None):
        k = textbox(half_x, emu_in(0.45), SLIDE_W - emu_in(1.2), emu_in(0.35),
                    para(run(kicker, PT_ACCENT, CYAN, bold=True), align="l"))
        runs = run(title_text, PT_TITLE, TEXT, bold=True)
        if title_accent:
            runs += run(title_accent, PT_TITLE, CYAN, bold=True)
        t = textbox(half_x, emu_in(0.85), SLIDE_W - emu_in(1.2), emu_in(0.8),
                    para(runs, align="l"))
        return k + t

    def body_box(paras, x=half_x, w=half_w, y=emu_in(1.75), h=emu_in(4.2)):
        return textbox(x, y, w, h, "".join(paras))

    def note_box(text, y=emu_in(5.55)):
        return textbox(half_x, y, SLIDE_W - emu_in(1.2), emu_in(0.7),
                       para(run("Eslatma: ", PT_ACCENT, GOLD, bold=True, italic=True)
                            + run(text, PT_BODY, DIM, italic=True), align="l"))

    if n == 2:
        part = "KIRISH \u2022 REJA"
        shapes.append(header(part, "Reja (Mundarija)"))
        img = picture(rid, img_x, img_y, img_w, img_h)
        items = [
            ("1-reja.", " Optik tola nima va u axborotni qanday \u201co\u02bbqiydi\u201d?", "Fotonlar, modulyatsiya va tolaning ichki tuzilishi \u2014 Slayd 3\u20134."),
            ("2-reja.", " Yorug\u02bblikning to\u02bbliq ichki qaytish fizikasi va afzalliklari.", "Snell qonuni, kritik burchak, so\u02bbnish dB/km, DWDM \u2014 Slayd 5\u20136."),
            ("3-reja.", " Qit\u02bbalararo suv osti kabellari \u2014 global tizim asosi.", "Okean osti infratuzilmasi va yotqizish \u2014 Slayd 7\u20138."),
            ("Xulosa.", " Optik tolaning axborot texnologiyalari kelajagidagi o\u02bbrni.", "Umumlashtirish va rahmat \u2014 Slayd 9\u201310."),
        ]
        paras = []
        for lead, name, desc in items:
            paras.append(para(run(lead, PT_ACCENT, CYAN, bold=True) + run(name, PT_ACCENT, TEXT, bold=True), space_after=200))
            paras.append(para(run(desc, PT_BODY, DIM, italic=True), space_after=800))
        shapes += [img, body_box(paras, w=emu_in(5.9), h=emu_in(4.5))]
        return "".join(shapes), rid, part

    if n == 3:
        part = "1-REJA"
        shapes.append(header(part, "Optik tola nima va u axborotni qanday o\u02bbqiydi?"))
        img = picture(rid, img_x, img_y, img_w, img_h)
        body = (
            "Optik tola \u2014 bu axborotni elektr toki emas, balki yorug\u02bblik zarrachalari (fotonlar) "
            "yordamida uzatuvchi, diametri atigi 8\u2013125 mikrometr bo\u02bblgan o\u02bbta toza shisha (silika, SiO\u2082) "
            "yoki plastik toladir. Bugungi magistral tarmoqlarda bir modali (single-mode) tolaning yadro diametri "
            "taxminan 9 \u00b5m ni tashkil etadi \u2014 bu inson sochidan ham ingichka. Kompyuterdagi raqamli ma\u02bblumotlar "
            "(ikkilik 1 va 0 ketma-ketligi) yarimo\u02bbtkazgichli lazer yoki LED yordamida yorug\u02bblik impulslariga "
            "aylantiriladi; bu modulyatsiya jarayoni: nur yoqilsa \u201c1\u201d, o\u02bbchirilsa \u201c0\u201d. Zamonaviy tizimlarda "
            "to\u02bblqin uzunligi ko\u02bbpincha 1310 nm va 1550 nm infraqizil diapazonda tanlanadi, chunki aynan shu "
            "\u201coynalarda\u201d shishadagi yo\u02bbqotishlar eng kichik. Qabul qiluvchi tomonda fotodiod yorug\u02bblik "
            "impulslarini yana elektr signaliga, so\u02bbngra raqamli ma\u02bblumotga aylantiradi, shu tarzda bitta tola "
            "soniyasiga milliardlab bit uzatadi."
        )
        shapes += [img, body_box([para(run(body, PT_BODY, TEXT))], w=emu_in(5.9), h=emu_in(4.5))]
        shapes.append(note_box("Tola oddiy \u201csim\u201d emas, balki optik to\u02bblqin yo\u02bbriqchisidir (waveguide) \u2014 u yorug\u02bblikni egilishlarda ham ushlab, manzilgacha olib boradi."))
        return "".join(shapes), rid, part

    if n == 4:
        part = "1-REJA"
        shapes.append(header(part, "Optik tolaning ichki tuzilishi"))
        img = picture(rid, half_x, img_y, img_w, img_h)  # media left
        intro = ("Bitta optik kabel o\u02bbnlab, ba\u02bbzan yuzlab (hozirgi rekordlarda 6 000+) alohida tolani "
                 "birlashtiradi. Har bir tolaning ishlashi uning uch qatlamidagi sindirish ko\u02bbrsatkichi (n) "
                 "farqiga asoslanadi:")
        layers = [
            ("Yadro (Core): ", "yorug\u02bblik tarqaladigan markaziy shisha; sindirish ko\u02bbrsatkichi yuqoriroq (n\u2081 \u2248 1,468). Foton oqimi aynan shu qatlamda yashaydi."),
            ("Qobiq (Cladding): ", "yadroni o\u02bbrab turuvchi, biroz pastroq sindirish ko\u02bbrsatkichli (n\u2082 \u2248 1,462) shisha. n\u2081 > n\u2082 sharti to\u02bbliq ichki qaytishni ta\u02bbminlaydi."),
            ("Himoya qatlami: ", "akrilat qoplama, aramid (Kevlar) iplari va tashqi plastik g\u02bbilof \u2014 namlik, egilish va mexanik shikastdan asraydi."),
        ]
        bx = emu_in(7.0)
        bw = emu_in(5.7)
        paras = [para(run(intro, PT_BODY, TEXT), space_after=500)]
        for lead, desc in layers:
            paras.append(para(run(lead, PT_ACCENT, CYAN, bold=True) + run(desc, PT_BODY, TEXT), bullet=True, space_after=400))
        paras.append(para(run("Formula:  n\u2081 > n\u2082   \u00b7   NA = \u221a(n\u2081\u00b2 \u2212 n\u2082\u00b2)", PT_ACCENT, GOLD, bold=True), space_after=0))
        shapes += [img, textbox(bx, emu_in(1.4), bw, emu_in(4.6), "".join(paras))]
        shapes.append(note_box("Yadro va qobiq o\u02bbrtasidagi atigi ~1% sindirish ko\u02bbrsatkichi farqi butun texnologiyaning fizik poydevoridir."))
        return "".join(shapes), rid, part

    if n == 5:
        part = "2-REJA"
        shapes.append(header(part, "To\u02bbliq ichki qaytish fizikasi"))
        img = picture(rid, img_x, img_y, img_w, img_h)
        body = (
            "Yorug\u02bblik shisha quvurdan \u201csizib\u201d chiqmasligining siri \u2014 optikaning to\u02bbliq ichki qaytish "
            "(Total Internal Reflection, TIR) hodisasidadir. Nur zichroq muhitdan (yadro) siyrakroq muhitga (qobiq) "
            "o\u02bbtishda Snell qonuni bo\u02bbyicha sinadi: n\u2081\u00b7sin\u03b8\u2081 = n\u2082\u00b7sin\u03b8\u2082. Tushish burchagi ma\u02bblum bir "
            "kritik burchak \u03b8c dan oshsa, nur umuman qobiqqa o\u02bbtmaydi va ko\u02bbzgudan qaytgandek 100% yadroga "
            "qaytadi; shuning uchun kabel egilsa ham foton oqimi ichkarida qamalib, minglab kilometr yo\u02bbl bosadi. "
            "Signalning so\u02bbnishi (attenuatsiya) juda kam: zamonaviy tolalarda atigi ~0,2 dB/km (1550 nm da), ya\u02bbni "
            "signal 100 km dan keyin ham o\u02bbqiladi. Uzoq masofalarda signalni tiklash uchun har ~80\u2013100 km da EDFA "
            "(erbiy legirlangan tola kuchaytirgichi) ishlatiladi."
        )
        paras = [para(run(body, PT_BODY, TEXT), space_after=500),
                 para(run("Formula:  \u03b8c = arcsin(n\u2082 / n\u2081) \u2248 83\u00b0  (shisha uchun)", PT_ACCENT, GOLD, bold=True), space_after=0)]
        shapes += [img, body_box(paras, w=emu_in(5.9), h=emu_in(4.6))]
        return "".join(shapes), rid, part

    if n == 6:
        part = "2-REJA"
        shapes.append(header(part, "Optik tolaning afzalliklari"))
        # intro on the left, image on the right (upper band)
        intro = ("Eski mis kabellar axborotni elektr signali orqali uzatadi va qarshilik, qizish hamda "
                 "elektromagnit xalaqitdan aziyat chekadi. Optik tola esa yorug\u02bblik asosida ishlaydi. "
                 "Yorug\u02bblik vakuumda ~299 792 km/s, shisha ichida esa (n\u22481,47) ~200 000 km/s tezlikda tarqaladi.")
        shapes.append(textbox(half_x, emu_in(1.6), emu_in(6.0), emu_in(1.5), para(run(intro, PT_BODY, TEXT))))
        shapes.append(picture(rid, emu_in(7.0), emu_in(1.6), emu_in(5.7), emu_in(1.6)))
        # three mega stats (full width)
        stats = [("~200 000", "km/s \u2014 shishadagi yorug\u02bblik tezligi", CYAN),
                 ("0,2", "dB/km \u2014 eng kam so\u02bbnish (1550 nm)", GREEN),
                 (">100", "Tbit/s \u2014 bitta tolaning sig\u02bbimi", GOLD)]
        sx = half_x
        sw = emu_in(3.9)
        for num, lab, col in stats:
            shapes.append(textbox(sx, emu_in(3.45), sw, emu_in(1.2),
                                  para(run(num, PT_MEGA, col, bold=True), align="ctr", space_after=100)
                                  + para(run(lab, PT_BODY, DIM), align="ctr", space_after=0)))
            sx += emu_in(4.0)
        # advantage cards (text)
        cards = [
            ("Katta sig\u02bbim (DWDM): ", "bitta tolada 80\u2013160+ to\u02bblqin uzunligini parallel uzatadi."),
            ("Past yo\u02bbqotish: ", "optik signal kuchaytirgichsiz 70\u2013100 km ga yetadi."),
            ("Xavfsizlik: ", "elektromagnit maydon yaratmaydi, xalaqitga chidamli."),
        ]
        cx2 = half_x
        cw = emu_in(3.9)
        for lead, desc in cards:
            shapes.append(textbox(cx2, emu_in(4.9), cw, emu_in(1.4),
                                  para(run(lead, PT_ACCENT, CYAN, bold=True), space_after=100)
                                  + para(run(desc, PT_BODY, TEXT), space_after=0)))
            cx2 += emu_in(4.0)
        return "".join(shapes), rid, part

    if n == 7:
        part = "3-REJA"
        shapes.append(header(part, "Qit\u02bbalararo suv osti kabellari"))
        img = picture(rid, img_x, img_y, img_w, img_h)
        body = (
            "Ko\u02bbpchilik internet kosmosdan \u2014 sun\u02bbiy yo\u02bbldoshlardan keladi deb o\u02bbylaydi, ammo aslida "
            "qit\u02bbalararo internet trafigining taxminan 99% qismi okean tubida yotgan optik kabellar orqali o\u02bbtadi; "
            "sun\u02bbiy yo\u02bbldosh aloqasi sig\u02bbim va kechikish bo\u02bbyicha ularga teng kela olmaydi. Hozirda dunyo "
            "bo\u02bbylab 500 dan ortiq suv osti kabel tizimi mavjud bo\u02bblib, ularning umumiy uzunligi 1,4 million km dan "
            "oshadi \u2014 bu Yer atrofini 30 martadan ko\u02bbproq o\u02bbrab chiqishga teng. Aynan shu kabellar orqali "
            "O\u02bbzbekistondagi foydalanuvchi AQSh yoki Yevropadagi serverlardan (Google, YouTube, bulutli xizmatlar) "
            "ma\u02bblumotni o\u02bbnlab millisekund ichida oladi. Masalan, \u201cMAREA\u201d kabeli ~200 Tbit/s sig\u02bbimga ega va "
            "AQSh bilan Yevropani bevosita bog\u02bblaydi."
        )
        shapes += [img, body_box([para(run(body, PT_BODY, TEXT))], w=emu_in(5.9), h=emu_in(4.6))]
        return "".join(shapes), rid, part

    if n == 8:
        part = "3-REJA"
        shapes.append(header(part, "Kabellarni yotqizish texnologiyasi"))
        img = picture(rid, half_x, img_y, img_w, img_h)  # media left
        body = (
            "Okean tubida bosim 10\u201311 km chuqurlikda 1 000 atmosferadan oshishi mumkin, shuning uchun kabellar "
            "ko\u02bbp qatlamli himoyaga o\u02bbraladi: markazdagi nozik tolalar po\u02bblat simlar, mis o\u02bbtkazgich, polietilen "
            "va bitum qoplamalar bilan mustahkamlanadi. Maxsus kabel yotqizuvchi kemalar oylab suzib, kabelni soatiga "
            "bir necha chaqirim tezlikda okean tubiga yotqizadi. Sayoz zonalarda kabel akula tishlashi va kema "
            "langarlaridan himoyalanish uchun 1\u20133 metr chuqurlikka ko\u02bbmiladi. Shikastlanish yuz berganda remont "
            "kemasi uzilgan uchlarni maxsus ilgaklar bilan ko\u02bbtarib, dengizda qayta ulaydi \u2014 tiklash bir necha hafta "
            "davom etishi mumkin."
        )
        shapes += [img, textbox(emu_in(7.0), emu_in(1.4), emu_in(5.7), emu_in(4.3),
                                para(run(body, PT_BODY, TEXT)))]
        shapes.append(note_box("Butun global axborot tizimining uzluksizligi aynan shu ko\u02bbrinmas okean osti infratuzilmasiga tayanadi."))
        return "".join(shapes), rid, part

    if n == 9:
        part = "XULOSA"
        shapes.append(header(part, "Xulosa"))
        img = picture(rid, img_x, img_y, img_w, img_h)
        body = (
            "Taqdimotni umumlashtirsak, zamonaviy axborot tizimlarining butun qudrati bevosita optik tola va "
            "yorug\u02bblik fizikasiga \u2014 to\u02bbliq ichki qaytish, past so\u02bbnish va spektral zichlashtirishga tayanadi; "
            "oddiy fizik qonuniyat global miqyosdagi raqamli inqilobni mumkin qildi. Biz foydalanayotgan har bir mobil "
            "ilova, veb-sayt, bulut xizmati va universitetning elektron tizimlari o\u02bbz ma\u02bblumotlarini qit\u02bbalar osha "
            "yorug\u02bblik tezligida uzatuvchi, okeanlar tubida yotgan ushbu texnologik mo\u02bbjiza orqali almashadi. Optik "
            "kabellar haqiqiy ma\u02bbnoda zamonaviy raqamli dunyomizning qon tomirlaridir. Kelajakda ko\u02bbp yadroli "
            "(multi-core) va bo\u02bbshliqli (hollow-core) tolalar, kogerent modulyatsiya va kvant shifrlash yo\u02bbnalishlari "
            "ushbu tomirlarni yanada tezroq, ishonchliroq va xavfsizroq qiladi."
        )
        shapes += [img, body_box([para(run(body, PT_BODY, TEXT))], w=emu_in(5.9), h=emu_in(4.6))]
        return "".join(shapes), rid, part

    if n == 10:
        part = "XULOSA"
        img = picture(rid, emu_in(3.67), emu_in(0.7), emu_in(6.0), emu_in(3.0))
        thanks = textbox(emu_in(1), emu_in(3.9), SLIDE_W - emu_in(2), emu_in(1.0),
                         para(run("E\u02bbtiboringiz uchun rahmat!", PT_MEGA, CYAN, bold=True), align="ctr"))
        info = textbox(emu_in(1), emu_in(5.0), SLIDE_W - emu_in(2), emu_in(1.4),
                       para(run("Mavzu: ", PT_ACCENT, GOLD, bold=True) + run("Internet kabellari (Optik tola) fizikasi", PT_BODY, TEXT), align="ctr", space_after=200)
                       + para(run("Talaba: ", PT_ACCENT, GOLD, bold=True) + run(STUDENT, PT_BODY, TEXT), align="ctr", space_after=200)
                       + para(run("Fan: ", PT_ACCENT, GOLD, bold=True) + run(FAN, PT_BODY, TEXT), align="ctr", space_after=200)
                       + para(run(UNIV, PT_BODY, DIM, italic=True), align="ctr", space_after=0))
        shapes += [img, thanks, info]
        return "".join(shapes), rid, part

    raise ValueError(n)


# ---------------------------------------------------------------------------
# OOXML package assembly
# ---------------------------------------------------------------------------
def slide_xml(shapes_xml):
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
        '<p:cSld><p:spTree>'
        '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
        '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
        '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
        f'{shapes_xml}'
        '</p:spTree></p:cSld><p:clrMapOvr><a:overrideClrMapping '
        'bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" '
        'accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" '
        'hlink="hlink" folHlink="folHlink"/></p:clrMapOvr></p:sld>'
    )


def slide_rels(image_name):
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
        f'<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{image_name}"/>'
        '</Relationships>'
    )


SLIDE_LAYOUT = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1">'
    '<p:cSld name="Blank"><p:spTree>'
    '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
    '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
    '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
    '</p:spTree></p:cSld><p:clrMapOvr><a:overrideClrMapping bg1="lt1" tx1="dk1" bg2="lt2" '
    'tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" '
    'accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/></p:clrMapOvr></p:sldLayout>'
)

SLIDE_LAYOUT_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>'
    '</Relationships>'
)

SLIDE_MASTER = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
    '<p:cSld><p:spTree>'
    '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
    '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
    '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
    '</p:spTree></p:cSld>'
    '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" '
    'accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>'
    '<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>'
    '<p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles>'
    '</p:sldMaster>'
)

SLIDE_MASTER_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>'
    '</Relationships>'
)


def theme_xml():
    def dk(c): return f'<a:srgbClr val="{c}"/>'
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Optik tola">'
        '<a:themeElements><a:clrScheme name="Optik">'
        f'<a:dk1>{dk("020B1A")}</a:dk1><a:lt1>{dk("EEF5FC")}</a:lt1>'
        f'<a:dk2>{dk("06162E")}</a:dk2><a:lt2>{dk("0A2446")}</a:lt2>'
        f'<a:accent1>{dk(CYAN)}</a:accent1><a:accent2>{dk(BLUE)}</a:accent2>'
        f'<a:accent3>{dk(VIOLET)}</a:accent3><a:accent4>{dk(GOLD)}</a:accent4>'
        f'<a:accent5>{dk(GREEN)}</a:accent5><a:accent6>{dk(DIM)}</a:accent6>'
        f'<a:hlink>{dk(CYAN)}</a:hlink><a:folHlink>{dk(VIOLET)}</a:folHlink>'
        '</a:clrScheme>'
        '<a:fontScheme name="Times"><a:majorFont><a:latin typeface="Times New Roman"/>'
        '<a:ea typeface=""/><a:cs typeface=""/></a:majorFont>'
        '<a:minorFont><a:latin typeface="Times New Roman"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>'
        '</a:fontScheme>'
        '<a:fmtScheme name="Office"><a:fillStyleLst>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>'
        '<a:lnStyleLst><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
        '<a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
        '<a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>'
        '<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle>'
        '<a:effectStyle><a:effectLst/></a:effectStyle>'
        '<a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>'
        '<a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme>'
        '</a:themeElements></a:theme>'
    )


def presentation_xml(n_slides):
    ids = "".join(f'<p:sldId id="{256 + i}" r:id="rId{i + 2}"/>' for i in range(n_slides))
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
        '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
        f'<p:sldIdLst>{ids}</p:sldIdLst>'
        f'<p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}" type="screen16x9"/>'
        f'<p:notesSz cx="{SLIDE_H}" cy="{SLIDE_W}"/>'
        '</p:presentation>'
    )


def presentation_rels(n_slides):
    rels = ['<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>']
    for i in range(n_slides):
        rels.append(f'<Relationship Id="rId{i + 2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i + 1}.xml"/>')
    theme_rid = n_slides + 2
    rels.append(f'<Relationship Id="rId{theme_rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>')
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(rels) + '</Relationships>')


def content_types(n_slides):
    overrides = [
        '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>',
        '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>',
        '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>',
        '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>',
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
    ]
    for i in range(n_slides):
        overrides.append(f'<Override PartName="/ppt/slides/slide{i + 1}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>')
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Default Extension="png" ContentType="image/png"/>'
            + "".join(overrides) + '</Types>')


ROOT_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
    '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
    '</Relationships>'
)

CORE_PROPS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
    'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
    '<dc:title>Internet kabellari (Optik tola) fizikasi</dc:title>'
    '<dc:creator>Toshbo\u02bbriyeva Marjona (242_26 - guruh)</dc:creator>'
    '<cp:lastModifiedBy>Toshbo\u02bbriyeva Marjona</cp:lastModifiedBy>'
    '</cp:coreProperties>'
)

APP_PROPS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
    '<Application>build_pptx.py</Application><Slides>10</Slides></Properties>'
)


def build():
    # ensure images exist
    missing = [i for i in range(1, 11) if not os.path.exists(os.path.join(ASSETS, f"slide{i:02d}.png"))]
    if missing:
        print("Generating slide images...")
        make_images.generate_all()

    n = 10
    if os.path.exists(OUT):
        os.remove(OUT)

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types(n))
        z.writestr("_rels/.rels", ROOT_RELS)
        z.writestr("docProps/core.xml", CORE_PROPS)
        z.writestr("docProps/app.xml", APP_PROPS)
        z.writestr("ppt/presentation.xml", presentation_xml(n))
        z.writestr("ppt/_rels/presentation.xml.rels", presentation_rels(n))
        z.writestr("ppt/theme/theme1.xml", theme_xml())
        z.writestr("ppt/slideMasters/slideMaster1.xml", SLIDE_MASTER)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", SLIDE_MASTER_RELS)
        z.writestr("ppt/slideLayouts/slideLayout1.xml", SLIDE_LAYOUT)
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", SLIDE_LAYOUT_RELS)

        for i in range(1, n + 1):
            shapes, _rid, part = build_slide_shapes(i)
            if part is not None:
                shapes += footer(part, i)
            img_name = f"slide{i:02d}.png"
            # embed image bytes
            with open(os.path.join(ASSETS, img_name), "rb") as f:
                z.writestr(f"ppt/media/{img_name}", f.read())
            z.writestr(f"ppt/slides/slide{i}.xml", slide_xml(shapes))
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", slide_rels(img_name))

    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
