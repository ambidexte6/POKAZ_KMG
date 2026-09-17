# -*- coding: utf-8 -*-
"""Страница «Бассейны» — показ пяти цифровых бассейновых моделей (геологи 17.09).
Каркас — цифры_кмг.html (шапка, палитра, низ, листание, ?с=N)."""
import io, json
R = './'   # запуск из корня: python инструменты/собрать_бассейны.py
база = io.open(R + 'цифры_кмг.html', encoding='utf-8').read()
голова = база[:база.index('</style>')]
голова = голова.replace('<title>КМГ · второй экран с цифрами</title>', '<title>КМГ · Геологоразведка — бассейны и цифровые модели</title>')
a = голова.index('/* Страница для геологов'); b = голова.index('*/', a) + 2
голова = голова[:a] + '''/* Показ бассейнов (геологи, обсуждение 17.09 и «Сценарий геологов.pptx»):
   открывается со строки «5 цифровых бассейновых моделей» на экране передела.
   Всё, что на экране, — материалы геологов: слои карты из их PDF (контур РК,
   15 осадочных бассейнов пунктиром, три категории бассейнов, структурные
   карты пяти моделей), их ролики из Petrel (карта, Прикаспий с проектами,
   3D-модель бассейна, сейсмика), карта портфеля ГРР — та же картинка, только
   перекрашенная под тёмный стиль. Ничего не сгенерировано (Адиль:
   «достоверность важна — если не получается достоверно, лучше не делай»).
   Первый слайд листается по кадрам (стрелка/клик): слой за слоем. */''' + голова[b:]
слои = json.load(io.open(R + 'медиа/геология/бассейны/слои.json', encoding='utf-8'))

css = '''
/* ===== бассейны: карта слоями ===== */
.бас_сетка{display:grid;grid-template-columns:520px 1fr;gap:30px;height:100%;min-height:0}
.бас_карта{position:relative;border-radius:22px;overflow:hidden;border:1px solid var(--грань);background:radial-gradient(900px 600px at 55% 45%, rgba(2,174,240,.10), transparent 70%), var(--фон0);min-height:0}
.бас_карта .полотно_слоёв{position:absolute;inset:0}
/* база — наша карта (контуры областей AIAN/KIOGE + рельеф), слои геологов ложатся поверх в той же проекции */
.бас_карта svg.база{opacity:1}
.бас_карта svg.база .рельеф{opacity:.55}
/* opacity:1 — общий .слой path гасит все пути до включения кадра, а база видна всегда */
.бас_карта svg.база path.область{fill:rgba(12,22,38,.35);stroke:rgba(175,192,216,.30);stroke-width:1.2;vector-effect:non-scaling-stroke;opacity:1}
.бас_карта svg.база path.граница{fill:none;stroke:var(--кмг);stroke-width:2.2;vector-effect:non-scaling-stroke;opacity:1;filter:drop-shadow(0 0 9px rgba(2,174,240,.85))}
.бас_карта img.слой.каспий{opacity:.55}
/* ролик Petrel с прозрачным фоном — «живая карта» последним кадром; слои под ним гаснут, чтобы две карты не спорили */
/* страна в кадре Petrel занимает ~9–96 % ширины, наша — 3,5–96,5 %: сдвиг влево на 2,5 % совмещает центры */
.бас_карта video.слой{object-fit:contain;transform:translateX(-2.5%)}
.бас_карта.живая img.слой,.бас_карта.живая svg.слой:not(.база){opacity:.10}
.бас_карта.живая svg.база{opacity:.35}
.бас_карта .подпись_ролика{position:absolute;left:22px;top:18px;padding:10px 14px;border-radius:12px;background:rgba(5,8,16,.78);border-left:4px solid var(--кмг);
  font-size:15px;font-weight:600;opacity:0;transition:opacity .6s}
.бас_карта .подпись_ролика small{display:block;font-size:12px;font-weight:400;color:var(--приглуш);margin-top:2px}
.бас_карта .подпись_ролика.включён{opacity:1}
.бас_карта img.слой,.бас_карта svg.слой,.бас_карта video.слой{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;opacity:0;transition:opacity .9s ease}
.бас_карта .слой.включён{opacity:1}
.бас_карта img.слой.пунктир{opacity:0}.бас_карта img.слой.пунктир.включён{opacity:.95}
.бас_карта img.слой.мало.включён{opacity:.75}
.бас_карта svg.слой path{fill:none;stroke-width:3;vector-effect:non-scaling-stroke;opacity:0;transition:opacity .9s ease}
.бас_карта svg.слой path.включён{opacity:1}
.бас_карта svg.слой path.пять{stroke:#FFD166;filter:drop-shadow(0 0 10px rgba(255,209,102,.8))}
.бас_карта svg.слой path.мнб{stroke:var(--мята);filter:drop-shadow(0 0 8px rgba(62,230,184,.7))}
.бас_карта svg.слой path.мало{stroke:rgba(175,192,216,.8);stroke-dasharray:8 6}
.бас_карта svg.слой text{font-family:'Golos Text',sans-serif;font-weight:600;fill:var(--текст);paint-order:stroke;stroke:rgba(5,8,16,.92);stroke-width:5px;stroke-linejoin:round;
  opacity:0;transition:opacity .9s ease;text-anchor:middle}
.бас_карта svg.слой text.включён{opacity:1}
.бас_карта svg.слой text.пять{fill:#FFD166;font-size:30px}.бас_карта svg.слой text.мнб{fill:var(--мята);font-size:26px}.бас_карта svg.слой text.мало{fill:var(--текст2);font-size:24px;font-weight:400}
.бас_карта .подпись{position:absolute;right:22px;top:18px;padding:10px 14px;border-radius:12px;background:rgba(5,8,16,.78);border:1px solid var(--грань);
  font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--кмг)}
.бас_карта .легенда{position:absolute;left:22px;bottom:18px;display:flex;flex-direction:column;gap:7px;padding:12px 16px;border-radius:14px;
  background:rgba(5,8,16,.78);border:1px solid var(--грань);opacity:0;transition:opacity .6s}
.бас_карта .легенда.включён{opacity:1}
.бас_карта .легенда div{display:flex;align-items:center;gap:10px;font-size:13px;color:var(--текст2)}
.бас_карта .легенда i{width:26px;height:4px;border-radius:2px;display:inline-block}
.бас_список{list-style:none;display:flex;flex-direction:column;gap:12px}
.бас_список li{display:grid;grid-template-columns:auto 1fr;gap:14px;align-items:start;padding:14px 18px;border-radius:16px;border:1px solid var(--грань);
  background:linear-gradient(180deg,rgba(12,22,38,.85),rgba(5,8,16,.55));opacity:0;transform:translateY(8px);transition:opacity .4s ease,transform .4s ease}
.бас_список li.включён{opacity:1;transform:none}
.бас_список b{font-family:'Unbounded',sans-serif;font-size:24px;line-height:1.1;font-weight:700;white-space:nowrap;min-width:110px;color:var(--кмг)}
.бас_список b i{font-style:normal;font-size:12px;font-family:'Golos Text',sans-serif;color:var(--приглуш);display:block;margin-top:4px;white-space:normal}
.бас_список span{font-size:14.5px;line-height:1.42;color:var(--текст2);padding-top:3px}
.бас_список span em{font-style:normal;color:var(--текст);font-weight:600}
.бас_список li.пять b{color:#FFD166}.бас_список li.мнб b{color:var(--мята)}.бас_список li.мало b{color:var(--текст2)}
/* ===== живые модели: видео из Petrel во весь кадр ===== */
.живо{position:relative;border-radius:22px;overflow:hidden;border:1px solid var(--грань);background:#000;height:100%;min-height:0}
.живо video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .8s ease}
.живо video.играет{opacity:1}
.живо .вуаль{position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,rgba(5,8,16,.55) 0%,rgba(5,8,16,0) 22%,rgba(5,8,16,0) 70%,rgba(5,8,16,.7) 100%)}
.живо .титр{position:absolute;left:28px;bottom:24px;max-width:70%;padding:12px 18px;border-radius:12px;background:rgba(5,8,16,.8);border-left:4px solid var(--кмг);
  font-size:20px;font-weight:600;color:var(--текст)}
.живо .титр small{display:block;margin-top:4px;font-size:13px;font-weight:400;color:var(--приглуш)}
.живо .счёт{position:absolute;right:22px;top:18px;padding:8px 14px;border-radius:12px;background:rgba(5,8,16,.78);border:1px solid var(--грань);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--кмг)}
.живо .источник{position:absolute;right:22px;bottom:24px;font-size:12px;color:var(--приглуш)}
.живая_сетка{display:grid;grid-template-columns:1fr 380px;gap:30px;height:100%;min-height:0}
/* ===== Прикаспий: две картинки геологов стопкой по кликам (структурная поверхность девона, очаг генерации) =====
   Общий механизм кадров включает все элементы с data-к ≤ текущего, а показать надо только верхний —
   включённые, за которыми идёт включённый сосед, гасятся через :has (Chrome 105+). Картинки на белом —
   это скрины Petrel/PetroMod как есть, фон бокса белый, чтобы не было тёмных полей по краям. */
.живо.стопка_карт{background:#fff}
.живо.стопка_карт img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;opacity:0;transition:opacity .8s ease}
.живо.стопка_карт img.включён{opacity:1}
.живо.стопка_карт img.включён:has(~ img.включён){opacity:0}
.живо.стопка_карт .титр{opacity:0;transition:opacity .8s ease}
.живо.стопка_карт .титр.включён{opacity:1}
.живо.стопка_карт .титр.включён:has(~ .титр.включён){opacity:0}
.живо.стопка_карт .источник{top:18px;bottom:auto;color:#4B5A70}   /* внизу справа у PetroMod свой логотип */
.живо.стопка_карт .вуаль{background:linear-gradient(180deg,rgba(5,8,16,0) 78%,rgba(5,8,16,.55) 100%)}
/* ===== портфель: участки ГРР поверх карты бассейнов (полигоны с карты геологов, портфель_в_проекции.py) ===== */
/* участки сгрудились на западе — весь холст (слои и SVG вместе) приближен к западной половине в 1,5 раза,
   шрифты подписей заданы с учётом масштаба (14 px × 1,5 ≈ 21 px на экране) */
.бас_карта.портфель .полотно_слоёв{transform:scale(1.5);transform-origin:24% 56%}
.бас_карта.портфель img.слой{opacity:.28}
.бас_карта.портфель img.слой.включён{opacity:.28}
.бас_карта svg.участки path{fill-opacity:.32;stroke-width:2.2;vector-effect:non-scaling-stroke;opacity:0;transition:opacity .7s ease}
.бас_карта svg.участки path.включён{opacity:1}
.бас_карта svg.участки path.действующие{fill:#3B8BEF;stroke:#7DB8FF;filter:drop-shadow(0 0 10px rgba(59,139,239,.9))}
.бас_карта svg.участки path.кмг{fill:#B266F0;stroke:#D9A6FF;filter:drop-shadow(0 0 10px rgba(178,102,240,.9))}
.бас_карта svg.участки path.партнёры{fill:#F6C48F;stroke:#FFE0B8;filter:drop-shadow(0 0 10px rgba(246,196,143,.9))}
.бас_карта svg.участки path.гин_зел,.бас_карта svg.участки path.гин_син{fill:var(--мята);fill-opacity:.12;stroke:var(--мята);stroke-dasharray:7 5;filter:drop-shadow(0 0 8px rgba(62,230,184,.6))}
.бас_карта svg.участки path.жылыой{fill:#3B8BEF;fill-opacity:.10;stroke:#7DB8FF;stroke-dasharray:4 4}
.бас_карта svg.участки path.включён.действующие,.бас_карта svg.участки path.включён.кмг,.бас_карта svg.участки path.включён.партнёры{animation:пульс_участка 2.6s ease-in-out 1}
@keyframes пульс_участка{0%{fill-opacity:.32}40%{fill-opacity:.75}100%{fill-opacity:.32}}
.бас_карта svg.участки text{font-family:'Golos Text',sans-serif;font-size:14px;font-weight:600;fill:var(--текст);paint-order:stroke;stroke:rgba(5,8,16,.92);stroke-width:3.5px;stroke-linejoin:round;opacity:0;transition:opacity .7s ease}
.бас_карта svg.участки text.включён{opacity:1}
.бас_карта svg.участки text.гин_син{font-size:12.5px;letter-spacing:.22em;text-transform:uppercase;fill:var(--мята);font-weight:700}
.бас_карта svg.участки text.гин_зел{fill:var(--мята)}
.бас_карта svg.участки text.партнёры{fill:#FFE0B8}.бас_карта svg.участки text.кмг{fill:#E4C4FF}.бас_карта svg.участки text.действующие{fill:#BFDCFF}
.бас_карта svg.участки line{stroke:rgba(255,255,255,.55);stroke-width:1.2;vector-effect:non-scaling-stroke;opacity:0;transition:opacity .7s ease}
.бас_карта svg.участки line.включён{opacity:1}
.бас_список li.действ b{color:#7DB8FF}.бас_список li.кмг b{color:#D9A6FF}.бас_список li.партн b{color:#FFE0B8}
.к_геораг{margin-top:auto;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:16px 20px;border-radius:16px;border:1px solid rgba(2,174,240,.55);background:rgba(2,174,240,.12);text-decoration:none;color:#fff;
  opacity:0;transform:translateY(8px);transition:opacity .4s ease,transform .4s ease}
.к_геораг.включён{opacity:1;transform:none}
.к_геораг:hover{background:rgba(2,174,240,.24)}
.к_геораг b{font-family:'Unbounded',sans-serif;font-size:15px;letter-spacing:.04em;text-transform:uppercase;font-weight:700}
.к_геораг small{display:block;margin-top:4px;font-family:'Golos Text',sans-serif;font-size:12.5px;color:var(--текст2);text-transform:none;letter-spacing:0}
.к_геораг span{font-size:26px;color:var(--кмг)}
'''
голова += css + '</style>'

def li(число, ед, текст, к, кл=''):
    ед = f'<i>{ед}</i>' if ед else ''
    return f'      <li data-к="{к}" class="{кл}"><b>{число}{ед}</b><span>{текст}</span></li>\n'

# --- слайд 1: карта слоями ---
def свг_группа(ключ, кадр):
    s = ''
    for о in слои[ключ]:
        s += f'        <path class="{ключ}" data-к="{кадр}" d="{о["путь"]}"/>\n'
    for о in слои[ключ]:
        x, y = о['центр']; имя = о['имя']
        if ' · ' in имя:   # три модели в одной области — три строки
            части = имя.split(' · ')
            for j, ч in enumerate(части):
                s += f'        <text class="{ключ}" data-к="{кадр}" x="{x}" y="{y - 40 + j * 40}">{ч}</text>\n'
        else:
            s += f'        <text class="{ключ}" data-к="{кадр}" x="{x}" y="{y + 8}">{имя}</text>\n'
    return s
def база_карты(н='1'):
    """Наша карта под слоями: рельеф в обрезке по областям, контуры областей, граница страны.
    н — суффикс id обрезки: карта стоит на двух слайдах, а id в документе должен быть один."""
    x, y, w, h = слои['рельеф']
    обр = ''.join(f'<path d="{d}"/>' for d in слои['области'].values())
    обл = ''.join(f'<path class="область" d="{d}"/>' for d in слои['области'].values())
    return f'''<svg class="слой база включён" viewBox="0 0 {слои['холст'][0]} {слои['холст'][1]}" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
            <defs><clipPath id="обрезка_кз_{н}">{обр}</clipPath></defs>
            <image class="рельеф" href="медиа/карта/рельеф.jpg" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="none" clip-path="url(#обрезка_кз_{н})"/>
            {обл}<path class="граница" d="{слои['рк']}"/>
          </svg>'''
слайд1 = f'''
<section class="слайд виден" id="с1" aria-label="Осадочные бассейны Казахстана">
  <div class="бровь">Геологоразведка · поиск и оценка участков</div>
  <h2 class="заголовок дисплей">15 осадочных бассейнов — пять из них в цифре</h2>
  <div class="полотно">
    <div class="бас_сетка">
      <ul class="бас_список">
{li('15', 'бассейнов', 'осадочных бассейнов на территории Казахстана — контуры на карте пунктиром', 1)}{li('6', 'бассейнов', 'малоизученные: Тенизский, Балхашский, Илийский, Зайсанский, Алакольский, Северо-Казахстанский', 2, 'мало')}{li('4', 'бассейна', 'с доказанной нефтегазоносностью: Прииртышский, Северо-Торгайский, Аральский, Сырдарьинский', 3, 'мнб')}{li('5', 'моделей', '<em>цифровые бассейновые модели</em>: Прикаспийский, Устюрт-Бозашинский, Мангышлакский, Южно-Торгайский, Шу-Сарысуский — структурные карты и очаги генерации УВ', 4, 'пять')}{li('748', 'млн т ЖУ', 'остаточные извлекаемые запасы (ABC1 на 01.01.2026) — основа в этих бассейнах; на карте — живая модель из Petrel', 5)}      </ul>
      <div class="бас_карта" id="бас_карта">
        <div class="полотно_слоёв">
          {база_карты()}
          <img class="слой пунктир" data-к="1" src="медиа/геология/бассейны/бассейны_15_пунктир.png" alt="">
          {''.join(f'<img class="слой мало" data-к="2" src="медиа/геология/бассейны/мало_{i}.png" alt="">' for i in range(len(слои['мало'])))}
          {''.join(f'<img class="слой мнб" data-к="3" src="медиа/геология/бассейны/мнб_{i}.png" alt="">' for i in range(len(слои['мнб'])))}
          {''.join(f'<img class="слой пять" data-к="4" src="медиа/геология/бассейны/пять_{i}.png" alt="">' for i in range(len(слои['пять'])))}
          <svg class="слой включён" viewBox="0 0 {слои['холст'][0]} {слои['холст'][1]}" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
{свг_группа('мало', 2)}{свг_группа('мнб', 3)}{свг_группа('пять', 4)}          </svg>
          <!-- ролик геологов из Petrel (карта бассейнов, белый фон выбит, туда-обратно 32 с) — «наслаивается гифкой» (Адиль 17.09) -->
          <video class="слой петля" data-к="5" src="медиа/геология/petrel/карта_бассейнов_петля.webm" muted loop playsinline preload="auto"></video>
        </div>
        <div class="подпись">Карта — Департамент геологоразведки КМГ · контуры областей — наша проекция</div>
        <div class="подпись_ролика" data-к="5">Живая карта бассейнов из Petrel<small>структурные карты пяти моделей и профили сейсморазведки</small></div>
        <div class="легенда" data-к="2">
          <div><i style="background:#FFD166"></i>цифровые бассейновые модели</div>
          <div><i style="background:var(--мята)"></i>доказанная нефтегазоносность</div>
          <div><i style="background:rgba(175,192,216,.8)"></i>малоизученные</div>
        </div>
      </div>
    </div>
  </div>
</section>
'''

# --- слайд 1б: Прикаспий в цифре — девон и очаг генерации (слайды 5–6 их pptx 17_09_2) ---
слайд1б = '''
<section class="слайд" id="с1б" aria-label="Прикаспийский бассейн в цифре">
  <div class="бровь">Геологоразведка · цифровая бассейновая модель · Прикаспий</div>
  <h2 class="заголовок дисплей">Прикаспий в цифре: от поверхности девона до очага генерации</h2>
  <div class="полотно">
    <div class="живая_сетка">
      <div class="живо стопка_карт">
        <img src="медиа/геология/кейсы/прикаспий_девон.jpg" data-к="1" alt="Структурная поверхность девона (D3), Прикаспийский бассейн">
        <img src="медиа/геология/кейсы/очаг_генерации.jpg" data-к="2" alt="3D-модель бассейна в PetroMod: фации и очаг генерации УВ">
        <div class="вуаль"></div>
        <div class="титр" data-к="1"><span>Структурная поверхность девона (D3)</span><small>глубины от −4 000 до −14 000 м · Petrel</small></div>
        <div class="титр" data-к="2"><span>Очаг генерации УВ</span><small>3D-модель бассейна, фации по разрезу · PetroMod</small></div>
        <div class="источник">Департамент геологоразведки КМГ</div>
      </div>
      <ul class="бас_список">
''' + li('1', '', '<em>Структурная поверхность девона</em> — карта глубин кровли девона по всему бассейну; поверх неё контуры участков и месторождения', 1, 'пять') + li('2', '', '<em>Очаг генерации УВ</em> — объёмная модель бассейна: где нефть образовалась, куда мигрировала и где могла скопиться', 2, 'мнб') + li('34', '%', 'территории страны покрыто пятью цифровыми бассейновыми моделями', 2) + '''      </ul>
    </div>
  </div>
</section>
'''

# --- слайд 2: живые модели ---
слайд2 = '''
<section class="слайд" id="с2" aria-label="Цифровые бассейновые модели живьём">
  <div class="бровь">Геологоразведка · цифровые бассейновые модели</div>
  <h2 class="заголовок дисплей">Бассейновое моделирование: живая цифровая модель недр</h2>
  <div class="полотно">
    <div class="живая_сетка">
      <div class="живо" id="живо">
        <!-- Адиль 17.09: «главный ролик, который хотел увидеть ПП, — на 5-м слайде pptx» —
             это 3D-модель бассейна с очагом генерации УВ (media3); идёт первым -->
        <video src="медиа/геология/petrel/модель_3d.mp4" poster="медиа/геология/petrel/модель_3d.jpg" muted playsinline preload="auto"
          data-титр="3D-модель бассейна и очаг генерации УВ" data-под="Где нефть образовалась, куда мигрировала и где скопилась — литология, разрез, очаги генерации"></video>
        <video src="медиа/геология/petrel/карта_бассейнов.mp4" poster="медиа/геология/petrel/карта_бассейнов.jpg" muted playsinline preload="auto"
          data-титр="Пять бассейнов в одной цифровой среде" data-под="Структурные карты по поверхностям, профили сейсморазведки"></video>
        <video src="медиа/геология/petrel/прикаспий_проекты.mp4" poster="медиа/геология/petrel/прикаспий_проекты.jpg" muted playsinline preload="auto"
          data-титр="Прикаспийский бассейн: проекты программы ГРР поверх модели" data-под="Берёзовский, Мугоджары, Каратон — видно, почему каждый проект стоит именно здесь"></video>
        <div class="вуаль"></div>
        <div class="титр" id="титр"><span></span><small></small></div>
        <div class="счёт" id="счёт_видео">1 / 3</div>
        <div class="источник">Petrel · Департамент геологоразведки КМГ</div>
      </div>
      <ul class="бас_список">
''' + li('5', 'моделей', 'цифровых бассейновых моделей — <em>34 %</em> территории страны', 1, 'пять') + li('10', 'лет', 'цифровизация геологии начата не сегодня — основной результат: живая модель вместо бумажных карт', 2) + li('23', 'проекта', 'программы ГРР до 2030 года лежат слоем поверх модели', 3) + li('4,7', 'млрд т у.т.', 'потенциальная геологическая ресурсная база проектов', 4) + '''      </ul>
    </div>
  </div>
</section>
'''

# --- слайд 3: сейсмика ---
слайд3 = '''
<section class="слайд" id="с3" aria-label="Сейсморазведка и интерпретация">
  <div class="бровь">Геологоразведка · обработка и интерпретация 2D/3D</div>
  <h2 class="заголовок дисплей">Сейсморазведка — «УЗИ недр»: от куба данных до модели ловушки</h2>
  <div class="полотно">
    <div class="живая_сетка">
      <div class="живо" id="сейсмика">
        <video src="медиа/геология/petrel/сейсмика.mp4" poster="медиа/геология/petrel/сейсмика.jpg" muted playsinline preload="auto" loop class="играет"></video>
        <div class="вуаль"></div>
        <div class="титр" id="титр_сейсмика"><span>Сейсмический куб</span><small>разрезы через толщу пород</small></div>
        <div class="источник">Petrel · Департамент геологоразведки КМГ</div>
      </div>
      <ul class="бас_список">
''' + li('1', '', '<em>Сейсмический куб</em> — акустический «снимок» недр по площади', 1) + li('2', '', '<em>Разрезы</em> — геолог читает слои и разломы', 2) + li('3', '', '<em>Интерпретация горизонтов</em> — здесь помогут ML и нейросети (в работе)', 3, 'пять') + li('4', '', '<em>Структура-ловушка</em> — где нефть могла скопиться', 4) + li('5', '', '<em>Геологическая модель</em> — основа для точки бурения и оценки запасов', 5, 'мнб') + '''      </ul>
    </div>
  </div>
</section>
'''

# --- слайд 4: портфель поверх карты бассейнов ---
портфель = json.load(io.open(R + 'медиа/геология/бассейны/портфель.json', encoding='utf-8'))
КАДР_КЛАССА = {'действующие': 1, 'кмг': 2, 'партнёры': 3, 'гин_зел': 4, 'гин_син': 4, 'жылыой': 1}
# подписи: смещение от центра полигона (px холста) и выравнивание; в кластере Жылыоя — выноски
ПОДПИСИ = {
  'Березовский': (0, -22, 'middle'), 'Мугоджары Южный': (28, 5, 'start'), 'Шыгыс': (24, 5, 'start'),
  'Тайсойган': (-24, -2, 'end'), 'Уаз-Кондыбай': (-24, 8, 'end'), 'Каспий Северный': (-16, -30, 'end'),
  'Большой Жамбыл': (-24, 20, 'end'), 'Жылыой': (-30, 52, 'end'), 'Каратон подсолевой': (110, 20, 'start'),
  'Тажигали ПЗ · Сазтобе ПЗ': (110, -8, 'start'), 'Береке': (26, -10, 'start'), 'Болашак': (30, 34, 'start'),
  'Жаркын': (-24, 5, 'end'), 'Устюрт 1,2': (30, 5, 'start'), 'Озен Палеозой': (-24, 28, 'end'), 'Озен Северный': (30, -12, 'start'),
  'Белес': (0, -22, 'middle'), 'Тургай ПЗ-2': (0, 32, 'middle'), 'Шу-Сарысу': (30, 5, 'start'),
  'ГИН Торгай Северный': (40, 0, 'start'), 'Прикаспий палеозой (ГИН)': (-40, -70, 'middle'),
}
def свг_участки():
    s = ''
    for пр in портфель['проекты']:
        к = КАДР_КЛАССА.get(пр['класс'], 1)
        for д in пр['пути']: s += f'        <path class="{пр["класс"]}" data-к="{к}" d="{д}"/>\n'
    for пр in портфель['проекты']:
        к = КАДР_КЛАССА.get(пр['класс'], 1); x, y = пр['центр']; dx, dy, анк = ПОДПИСИ.get(пр['имя'], (0, 0, 'middle'))
        if abs(dx) + abs(dy) > 34:   # выноска
            s += f'        <line class="{пр["класс"]}" data-к="{к}" x1="{x}" y1="{y}" x2="{x + dx - (8 if анк == "start" else -8 if анк == "end" else 0)}" y2="{y + dy - 6}"/>\n'
        s += f'        <text class="{пр["класс"]}" data-к="{к}" x="{x + dx}" y="{y + dy}" text-anchor="{анк}">{пр["имя"]}</text>\n'
    return s
слайд4 = f'''
<section class="слайд" id="с4" aria-label="Портфель проектов ГРР">
  <div class="бровь">Геологоразведка · программа ГРР до 2030 года</div>
  <h2 class="заголовок дисплей">Портфель разведочных проектов на карте бассейнов</h2>
  <div class="полотно">
    <div class="бас_сетка">
      <ul class="бас_список">
{li('23', 'проекта', 'на разных стадиях подготовки · <em>26</em> поисковых скважин, проходка 89 тыс. м · синим — участки с действующими контрактами', 1, 'действ')}{li('6', 'проектов', 'страновой значимости · <em>13</em> — социальной · фиолетовым — участки, планируемые к получению контракта за счёт КМГ', 2, 'кмг')}{li('2D · 3D', '', 'сейсморазведка <em>6 250 км</em> и <em>2 540 км²</em> · региональная 2D по Прикаспию — 60 тыс. км · бежевым — участки с привлечением партнёров', 3, 'партн')}{li('4,7', 'млрд т у.т.', 'потенциальная геологическая ресурсная база программы · пунктиром — региональные исследования (ГИН): Прикаспий палеозой, Торгай Северный', 4, 'пять')}        <a class="к_геораг" data-к="5" href="геораг.html"><div><b>Дальше — KMG Geo AI</b><small>ИИ-ассистент геолога: как накопленные данные работают на решения</small></div><span>→</span></a>
      </ul>
      <div class="бас_карта портфель">
        <div class="полотно_слоёв">
          {база_карты('4')}
          {''.join(f'<img class="слой мало включён" src="медиа/геология/бассейны/мало_{i}.png" alt="">' for i in range(len(слои['мало'])))}
          {''.join(f'<img class="слой мнб включён" src="медиа/геология/бассейны/мнб_{i}.png" alt="">' for i in range(len(слои['мнб'])))}
          {''.join(f'<img class="слой пять включён" src="медиа/геология/бассейны/пять_{i}.png" alt="">' for i in range(len(слои['пять'])))}
          <svg class="слой участки включён" viewBox="0 0 {слои['холст'][0]} {слои['холст'][1]}" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
{свг_участки()}          </svg>
        </div>
        <div class="подпись">Участки — карта портфеля ГРР, Департамент геологоразведки КМГ · поверх бассейнов</div>
        <div class="легенда включён">
          <div><i style="background:#3B8BEF"></i>действующие контракты на недропользование</div>
          <div><i style="background:#B266F0"></i>планируемые к получению контракта за счёт КМГ</div>
          <div><i style="background:#F6C48F"></i>планируемые с привлечением партнёров</div>
          <div><i style="background:var(--мята)"></i>региональные исследования (ГИН)</div>
        </div>
      </div>
    </div>
  </div>
</section>
'''

низ = '''
<div class="низ">
  <img id="лого" src="медиа/лого_кмг.png" alt="КазМунайГаз">
  <div class="точки" id="точки" role="tablist" aria-label="Слайды"></div>
  <div class="счётчик" id="счётчик"></div>
</div>
</div>
</div>
'''
# скрипт листания — из цифры_кмг (без автопрокрутки и видео-слоя)
a = база.index('<script>\n(function(){\n  "use strict";'); b = база.index('</script>', a) + len('</script>')
листание = база[a:b].replace('window.__геологи', 'window.__бассейны')
видео = '''
<script>
(function(){
  /* Ролики Petrel по очереди: закончился один — следующий, по кругу
     (геологи 17.09: «чтобы на фоне всё это было как гифка, зациклено, по очереди»).
     Пускаются, когда слайд виден; на уходе — пауза, чтобы не жечь кадры. */
  var бокс = document.getElementById("живо"), видео = [].slice.call(бокс.querySelectorAll("video")), i = 0;
  var титр = document.getElementById("титр"), счёт = document.getElementById("счёт_видео");
  function пустить(n){
    видео.forEach(function(в, k){ в.classList.toggle("играет", k === n); if(k !== n){ в.pause(); } });
    var в = видео[n]; в.currentTime = 0; в.play().catch(function(){});
    титр.querySelector("span").textContent = в.dataset.титр; титр.querySelector("small").textContent = в.dataset.под;
    счёт.textContent = (n + 1) + " / " + видео.length;
  }
  видео.forEach(function(в, k){ в.addEventListener("ended", function(){ i = (k + 1) % видео.length; пустить(i); }); });
  var секция = document.getElementById("с2"), сейсм = document.getElementById("сейсмика").querySelector("video"), с3 = document.getElementById("с3");
  var наблюдатель = new MutationObserver(function(){
    if(секция.classList.contains("виден")){ if(видео[i].paused) пустить(i); } else видео.forEach(function(в){ в.pause(); });
    if(с3.classList.contains("виден")){ сейсм.play().catch(function(){}); } else сейсм.pause();
  });
  наблюдатель.observe(секция, { attributes:true, attributeFilter:["class"] });
  наблюдатель.observe(с3, { attributes:true, attributeFilter:["class"] });
  if(секция.classList.contains("виден")) пустить(0);
  /* слайд 1: ролик-петля Petrel — играет только пока включён его кадр (5-й); слои под ним гаснут */
  var бокс1 = document.getElementById("бас_карта"), петля = бокс1.querySelector("video.петля");
  function петляСостояние(){
    var вкл = петля.classList.contains("включён") && document.getElementById("с1").classList.contains("виден");
    бокс1.classList.toggle("живая", вкл);
    if(вкл){ петля.play().catch(function(){}); } else { петля.pause(); }
  }
  new MutationObserver(петляСостояние).observe(петля, { attributes:true, attributeFilter:["class"] });
  new MutationObserver(петляСостояние).observe(document.getElementById("с1"), { attributes:true, attributeFilter:["class"] });
  петляСостояние();   // ?к=5 ставит класс до того, как наблюдатели повешены
  if(с3.classList.contains("виден")) сейсм.play().catch(function(){});
  /* титры сейсмики — по времени ролика */
  /* 17.09 (Адиль): вместо нарезки — первые 90 с записи геологов как есть; титры по тому, что на экране */
  var ТИТРЫ = [[0,"Сейсмический куб","3D-куб данных: разрезы через толщу пород"],[14,"Разрезы","геолог читает слои, складки и разломы"],[50,"Интерпретация горизонта","отражающая граница прослеживается по кубу — здесь помогут ML (в работе)"],[64,"Структурная поверхность","горизонт в 3D: где могла сформироваться ловушка"]];
  var тс = document.getElementById("титр_сейсмика");
  setInterval(function(){ if(сейсм.paused) return; var t = сейсм.currentTime, к = ТИТРЫ[0]; ТИТРЫ.forEach(function(х){ if(t >= х[0]) к = х; });
    if(тс.querySelector("span").textContent !== к[1]){ тс.querySelector("span").textContent = к[1]; тс.querySelector("small").textContent = к[2]; } }, 250);
})();
</script>
'''
страница = голова + '\n</head>\n<body>\n<div id="обёртка">\n<div id="кадр">\n' + слайд1 + слайд1б + слайд2 + слайд3 + слайд4 + низ + листание + видео + '\n</body>\n</html>\n'
io.open(R + 'бассейны.html', 'w', encoding='utf-8').write(страница)
print('ok', len(страница))
