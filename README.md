# taqdimotMK — Internet kabellari (Optik tola) fizikasi

Axborot tizimlari fani uchun **aniq 10 ta slayddan** iborat, chuqur ilmiy-texnik mazmunli va vizual jihatdan boy taqdimot. Har bir slaydda kamida 4–5 ta asoslangan gap, real raqamlar, fizika qonuniyatlari va **o'ziga xos haqiqiy rasm** mavjud.

- **Mavzu:** Internet kabellari (Optik tola): Qit'alarni bog'lovchi suv osti kabellarida ma'lumotlar uzatilishi
- **Talaba:** Toshboʻriyeva Marjona (242_26 - guruh)
- **Fan:** Axborot tizimlari
- **Universitet:** Jizzax davlat pedagogika universiteti tabiiy fanlar oliy maktabi

## Fayllar

| Fayl | Tavsif |
|------|--------|
| [`taqdimot.pptx`](taqdimot.pptx) | **PowerPoint taqdimot (.pptx).** 10 slayd, har birida embed qilingan (ichiga joylangan) o'ziga xos rasm. Times New Roman shrifti, to'q ko'k + neon dizayn. PowerPoint, LibreOffice Impress yoki Google Slides'da ochiladi. |
| [`presentation.html`](presentation.html) | **Flagman artefakt.** O'z-o'zidan yetarli (self-contained) HTML/CSS: "Apple/Microsoft keynote" uslubidagi to'q ko'k + neon dizayn, grid/flexbox tuzilma, yumaloq kartalar, box-shadow va gradientlar. Times New Roman + qat'iy o'lcham ierarxiyasi. Brauzerda mustaqil ochiladi; Print → PDF da har bir slayd alohida sahifa. |
| [`PRESENTATION.md`](PRESENTATION.md) | 10 slaydning to'liq (chuqurlashtirilgan) Uzbek matni, embed qilingan Unsplash rasmlari, har bir slayd uchun dizayn ko'rsatmasi va shrift/o'lcham hujjati. |
| [`build_pptx.py`](build_pptx.py) | `.pptx` faylini qayta yaratuvchi skript (toza Python standart kutubxonasi — tashqi kutubxonalarsiz). |
| [`make_images.py`](make_images.py) + [`pnglib.py`](pnglib.py) | Har bir slayd uchun mavzuga mos rasmni (`assets/slideNN.png`) lokal chizadi (gradient fon, tola kesimi, TIR nur diagrammasi, mis↔tola grafigi, global xarita, kabel yotqizuvchi kema, Yer shari tarmog'i va h.k.). |
| [`verify_pptx.py`](verify_pptx.py) | `.pptx` ni tekshiradi: 10 ta slayd, har birida kamida 1 ta embed rasm, XML to'g'riligi. |

### `.pptx` ni qayta yaratish

```bash
python3 build_pptx.py
```

> **Eslatma:** Rasmlar Unsplash havolalari o'rniga lokal chiziladi, chunki `.pptx` formati rasm baytlarini ichiga embed qiladi (URL'ni yuklamaydi) va build muhitida tashqi internet mavjud emas edi. Shu bois har bir slaydning o'ziga xos, mavzuga mos rasmi `make_images.py` orqali generatsiya qilinib, faylga joylangan.

## Tuzilma (4 qism, 10 slayd)

| Qism | Slaydlar | Mazmuni |
|------|----------|---------|
| Kirish | 1–2 | Titul varag'i va reja (mundarija) |
| **1-reja** | 3–4 | Optik tola nima va u axborotni qanday o'qiydi? (fotonlar, modulyatsiya, tola tuzilishi) |
| **2-reja** | 5–6 | To'liq ichki qaytish fizikasi va afzalliklari (Snell qonuni, kritik burchak, dB/km, DWDM) |
| **3-reja** | 7–8 | Qit'alararo suv osti kabellari (global infratuzilma va yotqizish texnologiyasi) |
| **Xulosa** | 9–10 | Optik tolaning kelajakdagi o'rni va "E'tiboringiz uchun rahmat" |

## Rasmlar

Har bir slaydda mavzuga mos, **o'ziga xos** Unsplash rasmi to'g'ridan-to'g'ri embed qilingan (`https://source.unsplash.com/1280x720/?...` ko'rinishida). Rasmlar brauzerda yuklanadi; "bu yerga rasm qo'ying" kabi placeholder'lar ishlatilmagan.

## Dizayn va shrift (qat'iy)

- **Palitra:** chuqur okean ko'ki (`#020b1a` → `#0a2446`) + neon siyan (`#22e0ff`), moviy (`#2f6bff`), violet (`#8b5cff`) va oltin (`#ffd166`) urg'ular.
- **Shrift:** barcha matnlar **Times New Roman**. O'lcham ierarxiyasi: body (eng kichik) **12px** → urg'u **16px** → kichik sarlavha **24px** → sarlavha **32px** → yirik raqam **44px**. Asosiy matn hech qachon 12px dan kichik emas.

## Ko'rish va chop etish

`presentation.html` faylini istalgan zamonaviy brauzerda oching (internet ulanishi bo'lsa rasmlar yuklanadi). PDF uchun brauzerda **Print → Save as PDF** — har bir slayd alohida sahifaga chiqadi.
