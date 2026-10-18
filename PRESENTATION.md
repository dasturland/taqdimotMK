# Internet kabellari (Optik tola) fizikasi

> **Qit'alarni bog'lovchi suv osti kabellarida ma'lumotlarni yorug'lik tezligida uzatish texnologiyalari**

Ushbu hujjat **aniq 10 ta slayddan** iborat taqdimotning to'liq (chuqurlashtirilgan) matni, har bir slayd uchun dizayn ko'rsatmasi va embed qilingan haqiqiy rasmlarni o'z ichiga oladi. Taqdimot qat'iy **4 qismga** bo'lingan: **3 ta asosiy reja + 1 ta xulosa**.

- **Fan:** Axborot tizimlari
- **Mavzu:** Internet kabellari (Optik tola): Qit'alarni bog'lovchi suv osti kabellarida ma'lumotlar uzatilishi
- **Talaba:** Toshboʻriyeva Marjona (242_26 - guruh)
- **Universitet:** Jizzax davlat pedagogika universiteti tabiiy fanlar oliy maktabi

---

## Tuzilma (4 qism)

| Qism | Slaydlar | Mazmuni |
|------|----------|---------|
| Kirish qismi | 1–2 | Titul varag'i va reja (mundarija) |
| **1-reja** | 3–4 | Optik tola nima va u axborotni qanday o'qiydi? |
| **2-reja** | 5–6 | Yorug'likning to'liq ichki qaytish fizikasi va afzalliklari |
| **3-reja** | 7–8 | Qit'alararo suv osti kabellari (Global axborot tizimining asosi) |
| **Xulosa** | 9–10 | Optik tolaning axborot texnologiyalari kelajagidagi o'rni |

---

## Umumiy dizayn tizimi (barcha slaydlar uchun)

**Mavzu uslubi:** IT + fizika + yorug'lik tezligi + okean osti infratuzilmasi. "Apple/Microsoft keynote" darajasidagi hashamatli, zamonaviy kiber uslub — chuqur okean ko'k foni, neon siyan nurlar (glow), grid/flexbox tuzilmasi, yumaloq ramkali kartalar, chuqur ko'lankalar (box-shadow) va gradientlar.

### Rang palitrasi (to'q ko'k + neon)
| Element | Rang | HEX |
|---------|------|-----|
| Asosiy fon (chuqur okean) | To'q ko'k / qora-ko'k gradient | `#020b1a` → `#06162e` → `#0a2446` |
| Urg'u (optik tola nuri) | Yorqin neon siyan | `#22e0ff` |
| Ikkilamchi urg'u (lazer) | Elektrik moviy | `#2f6bff` |
| Uchlamchi (DWDM spektri) | Siyohrang (violet) | `#8b5cff` |
| Issiq urg'u (foton) | Oltin-sariq | `#ffd166` |
| Muvaffaqiyat / sig'im | Neon yashil | `#4be3a0` |
| Asosiy matn | Oq-moviy | `#eef5fc` |
| Yordamchi matn | Och kulrang-ko'k | `#a9c2da` |

### Shrift (QAT'IY talab)
Barcha matnlar uchun **Times New Roman** (`font-family: "Times New Roman", Times, Georgia, serif`). O'lchamlar quyidagi ierarxiyaga **qat'iy** amal qiladi — eng kichik asosiy matn **12px**:

| Element (daraja) | Shrift | O'lcham | Uslub |
|------------------|--------|---------|-------|
| Yirik raqam / statistika | Times New Roman | **44px** | Bold, rangli |
| Katta titul / sarlavha (H1) | Times New Roman | **32px** | Bold |
| Kichik sarlavha (sub-title) | Times New Roman | **24px** | Semi-bold / Italic |
| Urg'uli so'z, ichki sarlavha, yorliq, kicker | Times New Roman | **16px** | Bold / rangli urg'u |
| Asosiy matn (body — eng kichik) | Times New Roman | **12px** | Regular |
| Izoh / rasm sarlavhasi / kolontitul | Times New Roman | **12px** | Italic / och rang |

> **Ierarxiya mantiqi:** 12 (body) → 16 (urg'u) → 24 (sub-title) → 32 (sarlavha) → 44 (yirik raqam). Mutanosiblik qat'iy saqlanadi, asosiy matn hech qachon 12px dan kichik emas.

### Takrorlanuvchi grafik elementlar
- Har bir slayd pastida ingichka **neon siyan optik tola chizig'i** (glow effekti) va yuqorida ko'p rangli neon chekka — brend elementi.
- Har bir slaydda **o'ziga xos, mavzuga mos haqiqiy rasm** (Unsplash) grid/flex layoutda joylashtirilgan.
- Kolontitulda qism nomi va slayd raqami (12px, italic).

---

# SLAYD 1 — Titul varag'i

**Dizayn ko'rsatmasi:** Markazlashtirilgan titul; yuqorida "pill" ko'rinishidagi neon badge, so'ng yirik sarlavha va kursiv kichik sarlavha, markazda keng rasm bandi, pastda universitet/talaba ma'lumotlari. Fon — chuqur okean gradienti.

![Optik tola kabellari va yorug'lik oqimi](https://source.unsplash.com/1280x720/?fiber,optic,cable,network)

**Matn elementlari:**
- **Sarlavha** — *Times New Roman, 32px, Bold; "fizikasi" so'zi neon siyan `#22e0ff`:*
  > Internet kabellari (Optik tola) fizikasi
- **Kichik sarlavha** — *24px, Semi-bold/Italic, och ko'k:*
  > Qit'alarni bog'lovchi suv osti kabellarida ma'lumotlarni yorug'lik tezligida uzatish texnologiyalari
- **Ma'lumot bloki** — *body 12px, yorliqlar 16px Bold oltin:*
  > **Universitet:** Jizzax davlat pedagogika universiteti tabiiy fanlar oliy maktabi
  > **Fan:** Axborot tizimlari
  > **Talaba:** Toshboʻriyeva Marjona (242_26 - guruh)

---

# SLAYD 2 — Reja (Mundarija)

**Qism:** Kirish | **Dizayn:** Ikki ustunli grid — chapda shisha tolalar makro rasmi, o'ngda yumaloq ramkali, chap chekkasi neon siyan bo'lgan reja kartalari. Har bir reja punkti ostida qisqa izoh.

![Shisha optik tolalarning makro ko'rinishi](https://source.unsplash.com/1280x720/?fiber,optic,glass,strands)

**Reja (sarlavha 32px, punkt nomi 16px Bold siyan, tavsif 12px):**
1. **1-reja.** Optik tola nima va u axborotni qanday "o'qiydi"? *(Fotonlar, modulyatsiya va tolaning ichki tuzilishi — Slayd 3–4.)*
2. **2-reja.** Yorug'likning to'liq ichki qaytish fizikasi va afzalliklari. *(Snell qonuni, kritik burchak, so'nish dB/km, DWDM — Slayd 5–6.)*
3. **3-reja.** Qit'alararo suv osti kabellari — global tizim asosi. *(Okean osti infratuzilmasi va yotqizish — Slayd 7–8.)*
4. **Xulosa.** Optik tolaning axborot texnologiyalari kelajagidagi o'rni. *(Umumlashtirish va rahmat — Slayd 9–10.)*

---

# SLAYD 3 — 1-reja (Optik tola nima)

**Qism:** 1-reja | **Dizayn:** Ikki ustunli grid — chapda matn, o'ngda lazer/yorug'lik texnologiyasi rasmi. Pastda neon ta'kid-izoh (note) qutisi.

![Lazer nuri va raqamli ma'lumot impulslari](https://source.unsplash.com/1280x720/?laser,light,technology,data)

**To'liq matn (kamida 4–5 gap, body 12px, urg'ular 16px):**

Optik tola — bu axborotni elektr toki emas, balki **yorug'lik zarrachalari (fotonlar)** yordamida uzatuvchi, diametri atigi 8–125 mikrometr bo'lgan o'ta toza shisha (silika, SiO₂) yoki plastik toladir. Bugungi magistral tarmoqlarda bir modali (single-mode) tolaning yadro diametri taxminan **9 µm**ni tashkil etadi — bu inson sochidan ham ingichka. Kompyuterdagi raqamli ma'lumotlar (ikkilik **1** va **0** ketma-ketligi) yarimo'tkazgichli lazer yoki LED yordamida yorug'lik impulslariga aylantiriladi; bu *modulyatsiya* jarayoni: nur yoqilsa "1", o'chirilsa "0". Zamonaviy tizimlarda to'lqin uzunligi ko'pincha **1310 nm** va **1550 nm** infraqizil diapazonda tanlanadi, chunki aynan shu "oynalarda" shishadagi yo'qotishlar eng kichik. Qabul qiluvchi tomonda fotodiod yorug'lik impulslarini yana elektr signaliga, so'ngra raqamli ma'lumotga aylantiradi, shu tarzda bitta tola soniyasiga milliardlab bit uzatadi.

> *Note:* Tola oddiy "sim" emas, balki optik to'lqin yo'riqchisidir (waveguide) — u yorug'likni egilishlarda ham ushlab, manzilgacha olib boradi.

---

# SLAYD 4 — 1-reja (Ichki tuzilish)

**Qism:** 1-reja | **Dizayn:** Grid (media chapda) — chapda tola kesimi rasmi, o'ngda uch qatlamli raqamlangan ro'yxat, formula qutisi va note. Yadro = oltin, qobiq = siyan, himoya = kulrang kodda.

![Optik kabelning ichki qatlamlari](https://source.unsplash.com/1280x720/?fiber,optic,wire,cross-section)

**To'liq matn (body 12px, qatlam nomlari 16px Bold):**

Bitta optik kabel o'nlab, ba'zan **yuzlab (hozirgi rekordlarda 6 000+)** alohida tolani birlashtiradi. Har bir tolaning ishlashi uning uch qatlamidagi *sindirish ko'rsatkichi (n)* farqiga asoslanadi:

1. **Yadro (Core):** yorug'lik tarqaladigan markaziy shisha; sindirish ko'rsatkichi yuqoriroq (n₁ ≈ 1,468). Foton oqimi aynan shu qatlamda yashaydi.
2. **Qobiq (Cladding):** yadroni o'rab turuvchi, biroz pastroq sindirish ko'rsatkichli (n₂ ≈ 1,462) shisha. **n₁ > n₂** sharti to'liq ichki qaytishni ta'minlab, nurni yadro ichida ushlab turadi.
3. **Himoya qatlami (Coating / Buffer / Jacket):** akrilat qoplama, kuchlantiruvchi aramid (Kevlar) iplari va tashqi plastik g'ilof — namlik, egilish va mexanik shikastdan asraydi.

**Formula:** `n₁ > n₂` · Sonli apertura **NA = √(n₁² − n₂²)**

> *Note:* Yadro va qobiq o'rtasidagi atigi ~1% sindirish ko'rsatkichi farqi butun texnologiyaning fizik poydevoridir.

---

# SLAYD 5 — 2-reja (To'liq ichki qaytish fizikasi)

**Qism:** 2-reja | **Dizayn:** Grid — chapda fizika matni va formula qutisi, o'ngda yorug'lik qaytishi rasmi.

![Yorug'lik nurining qaytishi](https://source.unsplash.com/1280x720/?light,reflection,beam,physics)

**To'liq matn (body 12px, urg'ular 16px):**

Yorug'lik shisha quvurdan "sizib" chiqmasligining siri — optikaning **to'liq ichki qaytish (Total Internal Reflection, TIR)** hodisasidadir. Nur zichroq muhitdan (yadro) siyrakroq muhitga (qobiq) o'tishda *Snell qonuni* bo'yicha sinadi: **n₁·sin θ₁ = n₂·sin θ₂**. Tushish burchagi ma'lum bir **kritik burchak θc** dan oshsa, nur umuman qobiqqa o'tmaydi va ko'zgudan qaytgandek 100% yadroga qaytadi; shuning uchun kabel egilsa ham foton oqimi ichkarida qamalib, minglab kilometr yo'l bosadi. Signalning so'nishi (attenuatsiya) juda kam: zamonaviy tolalarda atigi **~0,2 dB/km** (1550 nm da), ya'ni signal 100 km dan keyin ham o'qiladi. Uzoq masofalarda signalni tiklash uchun har ~80–100 km da *EDFA (erbiy legirlangan tola kuchaytirgichi)* ishlatiladi.

**Formula:** **θc = arcsin (n₂ / n₁) ≈ 83°** (shisha uchun)

---

# SLAYD 6 — 2-reja (Afzalliklar)

**Qism:** 2-reja | **Dizayn:** Yuqorida kirish matni, o'rtada 3 ta statistik "stat" lavha (yirik 44px raqamlar), pastda 3 ustunli karta grid (DWDM / masofa / xavfsizlik).

![Mis va optik kabellarni taqqoslash](https://source.unsplash.com/1280x720/?copper,wire,fiber,comparison)

**To'liq matn (body 12px, raqamlar 44px, yorliqlar 16px):**

Eski mis kabellar axborotni elektr signali orqali uzatadi va qarshilik, qizish hamda elektromagnit xalaqitdan aziyat chekadi. Optik tola esa yorug'lik asosida ishlaydi va fizik jihatdan bir necha ustunlikka ega. Yorug'lik vakuumda **~299 792 km/s**, shisha ichida esa (n≈1,47 tufayli) **~200 000 km/s** tezlikda tarqaladi — bu kechikishni (latensiyani) minimallashtiradi.

**Statistik ko'rsatkichlar:**
- **~200 000 km/s** — shishadagi yorug'lik tezligi
- **0,2 dB/km** — eng kam so'nish (1550 nm)
- **>100 Tbit/s** — bitta tolaning hozirgi sig'imi

**Afzalliklar (karta ko'rinishida):**
- **Katta sig'im (DWDM):** spektral zichlashtirish texnologiyasi bitta tolada **80–160+** turli to'lqin uzunligini (rangni) parallel uzatadi — millionlab videoqo'ng'iroq bir vaqtda sig'adi.
- **Past yo'qotish, uzoq masofa:** mis kabel har necha yuz metrda zaiflashadi; optik signal esa kuchaytirgichsiz **70–100 km** ga yetadi.
- **Xavfsizlik va halolik:** yorug'lik elektromagnit maydon yaratmaydi — tashqi xalaqit ta'sir qilmaydi, signalni sezdirmay ushlab olish deyarli imkonsiz.

---

# SLAYD 7 — 3-reja (Suv osti kabellari)

**Qism:** 3-reja | **Dizayn:** Grid — chapda statistik dalillarga boy matn, o'ngda global tarmoq xaritasi rasmi.

![Qit'alarni bog'lovchi global tarmoq xaritasi](https://source.unsplash.com/1280x720/?world,map,network,connection)

**To'liq matn (body 12px, "99%" va raqamlar 16px/urg'u):**

Ko'pchilik internet kosmosdan — sun'iy yo'ldoshlardan keladi deb o'ylaydi, ammo aslida qit'alararo internet trafigining taxminan **99%** qismi okean tubida yotgan optik kabellar orqali o'tadi; sun'iy yo'ldosh aloqasi sig'im va kechikish bo'yicha ularga teng kela olmaydi. Hozirda dunyo bo'ylab **500 dan ortiq** suv osti kabel tizimi mavjud bo'lib, ularning umumiy uzunligi **1,4 million km** dan oshadi — bu Yer atrofini 30 martadan ko'proq o'rab chiqishga teng. Aynan shu kabellar orqali O'zbekistondagi foydalanuvchi AQSh yoki Yevropadagi serverlardan (Google, YouTube, bulutli xizmatlar) ma'lumotni **o'nlab millisekund** ichida oladi. Masalan, Atlantika okeani ostidagi zamonaviy "MAREA" kabeli **~200 Tbit/s** sig'imga ega va AQSh bilan Yevropani bevosita bog'laydi.

---

# SLAYD 8 — 3-reja (Yotqizish texnologiyasi)

**Qism:** 3-reja | **Dizayn:** Grid (media chapda) — chapda kabel yotqizuvchi kema rasmi, o'ngda matn, ro'yxat va note.

![Okeanda kabel yotqizuvchi kema](https://source.unsplash.com/1280x720/?ship,ocean,deep,sea)

**To'liq matn (body 12px, urg'ular 16px):**

Okean tubida bosim 10–11 km chuqurlikda **1 000 atmosferadan** oshishi mumkin, shuning uchun kabellar ko'p qatlamli himoyaga o'raladi: markazdagi nozik tolalar po'lat simlar, mis o'tkazgich (quruqlikdagi kuchaytirgichlarni oziqlantirish uchun), polietilen va bitum qoplamalar bilan mustahkamlanadi. Maxsus *kabel yotqizuvchi kemalar* (cable-laying ships) oylab suzib, kabelni soatiga bir necha chaqirim tezlikda okean tubiga yotqizadi. Sayoz zonalarda kabel akula tishlashi va kema langarlaridan himoyalanish uchun suv osti plug va robotlar yordamida **1–3 metr** chuqurlikka ko'miladi. Shikastlanish yuz berganda remont kemasi uzilgan uchlarni maxsus ilgaklar bilan ko'tarib, dengizda qayta ulaydi — tiklash bir necha hafta davom etishi mumkin.

> *Note:* Butun global axborot tizimining uzluksizligi aynan shu ko'rinmas okean osti infratuzilmasiga tayanadi.

---

# SLAYD 9 — Xulosa

**Qism:** Xulosa | **Dizayn:** Grid — chapda umumlashtiruvchi matn, o'ngda yorug'lik tarmog'i bilan o'ralgan Yer shari rasmi.

![Yorug'lik tarmog'i bilan o'ralgan Yer shari](https://source.unsplash.com/1280x720/?earth,global,network,technology)

**To'liq matn (body 12px, urg'u 16px oltin):**

Taqdimotni umumlashtirsak, zamonaviy axborot tizimlarining butun qudrati bevosita optik tola va yorug'lik fizikasiga — to'liq ichki qaytish, past so'nish va spektral zichlashtirishga tayanadi; oddiy fizik qonuniyat global miqyosdagi raqamli inqilobni mumkin qildi. Biz foydalanayotgan har bir mobil ilova, veb-sayt, bulut xizmati va universitetning elektron tizimlari o'z ma'lumotlarini qit'alar osha yorug'lik tezligida uzatuvchi, okeanlar tubida yotgan ushbu texnologik mo'jiza orqali almashadi. Optik kabellar haqiqiy ma'noda **zamonaviy raqamli dunyomizning qon tomirlaridir**. Kelajakda ko'p yadroli (multi-core) va bo'shliqli (hollow-core) tolalar, kogerent modulyatsiya va kvant shifrlash yo'nalishlari ushbu tomirlarni yanada tezroq, ishonchliroq va xavfsizroq qiladi.

---

# SLAYD 10 — E'tibor uchun rahmat

**Qism:** Xulosa | **Dizayn:** Yuqorida keng abstrakt optik tola rasmi, markazda yirik (44px) neon siyan "Rahmat" sarlavhasi, pastda ma'lumot bloki.

![Optik tola abstrakt neon fon](https://source.unsplash.com/1280x720/?fiber,optic,blue,abstract)

**Matn (sarlavha 44px neon siyan; yorliqlar 16px Bold oltin; body 12px):**

> # E'tiboringiz uchun rahmat!
>
> **Mavzu:** Internet kabellari (Optik tola) fizikasi
> **Talaba:** Toshboʻriyeva Marjona (242_26 - guruh)
> **Fan:** Axborot tizimlari
> Jizzax davlat pedagogika universiteti tabiiy fanlar oliy maktabi

---

## Ishlab chiqarish uchun eslatma

- Ushbu Markdown hujjat to'liq matn va dizayn ko'rsatmalarini o'z ichiga oladi; barcha rasmlar Unsplash havolalari orqali to'g'ridan-to'g'ri embed qilingan va brauzerda yuklanadi.
- Flagman artefakt — [`presentation.html`](presentation.html): xuddi shu kontentni **Times New Roman** shriftida, aniq o'lcham ierarxiyasida (12 / 16 / 24 / 32 / 44 px), to'q ko'k + neon dizaynda ko'rsatadi va chop etishda (Print → PDF) har bir slayd alohida sahifaga chiqadi.
