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
.бас_сетка{display:grid;grid-template-columns:620px 1fr;gap:30px;height:100%;min-height:0}
.бас_карта{position:relative;border-radius:22px;overflow:hidden;border:1px solid var(--грань);background:radial-gradient(900px 600px at 55% 45%, rgba(2,174,240,.10), transparent 70%), var(--фон0);min-height:0}
.бас_карта .полотно_слоёв{position:absolute;inset:0}
/* база — наша карта (контуры областей AIAN/KIOGE + рельеф), слои геологов ложатся поверх в той же проекции */
.бас_карта svg.база{opacity:1}
.бас_карта svg.база .рельеф{opacity:.55}
/* opacity:1 — общий .слой path гасит все пути до включения кадра, а база видна всегда */
.бас_карта svg.база path.область{fill:rgba(12,22,38,.35);stroke:rgba(175,192,216,.30);stroke-width:1.2;vector-effect:non-scaling-stroke;opacity:1}
.бас_карта svg.база path.граница{fill:none;stroke:var(--кмг);stroke-width:2.2;vector-effect:non-scaling-stroke;opacity:1;filter:drop-shadow(0 0 9px rgba(2,174,240,.85))}
.бас_карта img.слой.каспий{opacity:.55}
/* автопоказ слайда 1: на такте «гаснет» слои и карточки уходят вместе, потом цикл начинается заново */
/* гаснет только карта: карточки и легенда выходят один раз и остаются (Адиль 18.09) */
#с1.гаснет .слой:not(.база),#с1.гаснет svg.слой path,#с1.гаснет svg.слой text{opacity:0!important;transition:opacity .8s ease!important}
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
.бас_карта svg.слой text.пять{fill:#FFD166;font-size:35.5px}.бас_карта svg.слой text.мнб{fill:var(--мята);font-size:30.5px}.бас_карта svg.слой text.мало{fill:var(--текст2);font-size:28.5px;font-weight:400}
.бас_карта .подпись{position:absolute;right:22px;top:18px;padding:10px 14px;border-radius:12px;background:rgba(5,8,16,.78);border:1px solid var(--грань);
  font-size:16px;letter-spacing:.14em;text-transform:uppercase;color:var(--кмг)}
.бас_карта .легенда{position:absolute;left:22px;bottom:18px;display:flex;flex-direction:column;gap:7px;padding:12px 16px;border-radius:14px;
  background:rgba(5,8,16,.78);border:1px solid var(--грань);opacity:0;transition:opacity .6s}
.бас_карта .легенда.включён{opacity:1}
.бас_карта .легенда div{display:flex;align-items:center;gap:10px;font-size:17.5px;color:var(--текст2)}
.бас_карта .легенда i{width:26px;height:4px;border-radius:2px;display:inline-block}
.бас_список{list-style:none;display:flex;flex-direction:column;gap:12px}
.бас_список li{display:grid;grid-template-columns:auto 1fr;gap:14px;align-items:center;padding:14px 18px;border-radius:16px;border:1px solid var(--грань);
  background:linear-gradient(180deg,rgba(12,22,38,.85),rgba(5,8,16,.55));opacity:0;transform:translateY(8px);transition:opacity .4s ease,transform .4s ease}
.бас_список li.включён{opacity:1;transform:none}
.бас_список b{font-family:'Unbounded',sans-serif;font-size:28.5px;line-height:1.1;font-weight:700;white-space:nowrap;min-width:110px;color:var(--кмг);text-align:center}
.бас_список b i{font-style:normal;font-size:16px;font-family:'Golos Text',sans-serif;color:var(--приглуш);display:block;margin-top:4px;white-space:normal}
.бас_список span{font-size:18.5px;line-height:1.42;color:var(--текст2);padding-top:3px}
.бас_список span em{font-style:normal;color:var(--текст);font-weight:600}
.бас_список li.пять b{color:#FFD166}.бас_список li.мнб b{color:var(--мята)}.бас_список li.мало b{color:var(--текст2)}
/* ===== живые модели: видео из Petrel во весь кадр ===== */
.живо{position:relative;border-radius:22px;overflow:hidden;border:1px solid var(--грань);background:#000;height:100%;min-height:0}
/* 18.09 (Адиль): «видео покажи полностью» — кадр целиком, без обрезки по бокам */
.живо video{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;opacity:0;transition:opacity .8s ease}
.живо video.играет{opacity:1}
.живо .вуаль{position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,rgba(5,8,16,.55) 0%,rgba(5,8,16,0) 22%,rgba(5,8,16,0) 70%,rgba(5,8,16,.7) 100%)}
.живо .титр{position:absolute;left:28px;bottom:24px;max-width:70%;padding:12px 18px;border-radius:12px;background:rgba(5,8,16,.8);border-left:4px solid var(--кмг);
  font-size:25.5px;font-weight:600;color:var(--текст)}
.живо .титр small{display:block;margin-top:4px;font-size:17.5px;font-weight:400;color:var(--приглуш)}
.живо .счёт{position:absolute;right:22px;top:18px;padding:8px 14px;border-radius:12px;background:rgba(5,8,16,.78);border:1px solid var(--грань);font-size:16px;letter-spacing:.14em;text-transform:uppercase;color:var(--кмг)}
.живо .источник{position:absolute;right:22px;bottom:24px;font-size:16px;color:var(--приглуш)}
.живая_сетка{display:grid;grid-template-columns:1fr 520px;gap:30px;height:100%;min-height:0}
.живая_сетка.одна{grid-template-columns:1fr}
.живая_сетка.девон{grid-template-columns:1fr 620px}
.девон_карта{position:relative;border-radius:22px;overflow:hidden;border:1px solid var(--грань);background:#fff;min-height:0}
.девон_карта img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain}
.девон_карта .титр{position:absolute;left:18px;bottom:18px;right:18px;padding:12px 16px;border-radius:12px;background:rgba(5,8,16,.86);border-left:4px solid var(--мята);font-size:21px;line-height:1.35;font-weight:600;color:var(--текст)}
.девон_карта .титр small{display:block;font-size:14px;font-weight:400;color:var(--приглуш);margin-top:3px}
.мл_текст{min-width:0;padding-top:6px;display:flex;flex-direction:column}
.мл_текст .к_геораг{margin-top:auto}
.мл_текст .метка_мл{display:inline-block;padding:7px 14px;border-radius:999px;border:1px solid rgba(240,174,74,.6);color:var(--янтарь);font-size:14px;letter-spacing:.14em;text-transform:uppercase;font-weight:700}
.мл_текст h3{margin-top:14px;font-size:30px;line-height:1.22;font-weight:700}
.мл_текст ul{list-style:none;margin:20px 0 0;padding:0}
.мл_текст li{position:relative;padding-left:26px;margin-top:14px;font-size:21px;line-height:1.42;color:var(--текст2)}
.мл_текст li::before{content:"";position:absolute;left:0;top:12px;width:10px;height:10px;border-radius:50%;background:var(--мята);box-shadow:0 0 10px rgba(62,230,184,.7)}
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
/* ===== программа ГРР: участки поверх приглушённых бассейнов (полигоны с карты геологов, портфель_в_проекции.py) ===== */
.бас_сетка.программа{grid-template-columns:640px 1fr}
.бас_карта.портфель .полотно_слоёв{transform:scale(1.45);transform-origin:26% 56%}
.бас_сетка.программа .левая{display:flex;flex-direction:column;min-height:0;gap:14px}
.бас_сетка.программа .бас_список li{padding:8px 16px}
.бас_сетка.программа .бас_список{gap:8px}
.бас_сетка.программа .бас_список span{font-size:16px}
.список_проектов{display:grid;grid-template-columns:1fr 1fr;gap:8px 18px;padding:12px 16px;border-radius:16px;border:1px solid var(--грань);background:linear-gradient(180deg,rgba(12,22,38,.85),rgba(5,8,16,.55));opacity:0;transition:opacity .5s}
.список_проектов.включён{opacity:1}
.список_проектов .колонка{min-width:0;display:flex;flex-direction:column;gap:10px}
.список_проектов .имя_группы{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--приглуш);margin-bottom:3px}
.список_проектов span{display:flex;align-items:center;gap:8px;font-size:14.5px;line-height:1.25;color:var(--текст);padding:1px 0}
.список_проектов span b{font-family:'Unbounded',sans-serif;font-size:11.5px;min-width:26px;height:21px;line-height:21px;text-align:center;border-radius:11px;flex:0 0 auto;color:#0A1220}
.список_проектов .действ span b{background:#7DB8FF}.список_проектов .кмг span b{background:#D9A6FF}.список_проектов .партн span b{background:#FFE0B8}.список_проектов .гин span b{background:var(--мята)}.список_проектов .жыл span b{background:#BFDCFF}
.бас_карта svg.участки g.номер.жыл circle{fill:#BFDCFF}
.бас_сетка.программа .к_геораг{margin-top:4px}   /* сразу под списком (Адиль: «под карточками»), не у логотипа */
/* бассейны под участками — приглушены и обесцвечены, чтобы участки читались первыми */
.бас_карта.портфель img.слой,.бас_карта.портфель img.слой.включён{opacity:.16;filter:saturate(.35) brightness(.8)}
.бас_карта.портфель svg.база .рельеф{opacity:.3}
.бас_карта.портфель svg.база path.граница{opacity:.5}
.бас_карта svg.участки path{fill-opacity:.42;stroke-width:2.4;vector-effect:non-scaling-stroke;opacity:0;transition:opacity .7s ease}
.бас_карта svg.участки path.включён{opacity:1}
.бас_карта svg.участки path.действующие{fill:#3B8BEF;stroke:#7DB8FF;filter:drop-shadow(0 0 10px rgba(59,139,239,.9))}
.бас_карта svg.участки path.кмг{fill:#B266F0;stroke:#D9A6FF;filter:drop-shadow(0 0 10px rgba(178,102,240,.9))}
.бас_карта svg.участки path.партнёры{fill:#F6C48F;stroke:#FFE0B8;filter:drop-shadow(0 0 10px rgba(246,196,143,.9))}
.бас_карта svg.участки path.гин_зел,.бас_карта svg.участки path.гин_син{fill:var(--мята);fill-opacity:.07;stroke:var(--мята);stroke-dasharray:7 5;filter:drop-shadow(0 0 8px rgba(62,230,184,.6))}
/* номера участков: кружок цвета класса, тёмная цифра */
.бас_карта svg.участки g.номер{opacity:0;transition:opacity .7s ease}
.бас_карта svg.участки g.номер.включён{opacity:1}
.бас_карта svg.участки g.номер circle{stroke:rgba(5,8,16,.9);stroke-width:2;vector-effect:non-scaling-stroke}
.бас_карта svg.участки g.номер text{font-family:'Unbounded',sans-serif;font-size:14px;font-weight:700;fill:#0A1220;text-anchor:middle;paint-order:normal;stroke:none;opacity:1}
.бас_карта svg.участки g.номер.действ circle{fill:#7DB8FF}.бас_карта svg.участки g.номер.кмг circle{fill:#D9A6FF}.бас_карта svg.участки g.номер.партн circle{fill:#FFE0B8}.бас_карта svg.участки g.номер.гин circle{fill:var(--мята)}
.бас_карта svg.участки path.жылыой{fill:#3B8BEF;fill-opacity:.10;stroke:#7DB8FF;stroke-dasharray:4 4}
.бас_карта svg.участки path.включён.действующие,.бас_карта svg.участки path.включён.кмг,.бас_карта svg.участки path.включён.партнёры{animation:пульс_участка 2.6s ease-in-out 1}
@keyframes пульс_участка{0%{fill-opacity:.32}40%{fill-opacity:.75}100%{fill-opacity:.32}}
.бас_карта svg.участки text{font-family:'Golos Text',sans-serif;font-size:19px;font-weight:600;fill:var(--текст);paint-order:stroke;stroke:rgba(5,8,16,.92);stroke-width:3.5px;stroke-linejoin:round;opacity:0;transition:opacity .7s ease}
.бас_карта svg.участки text.включён{opacity:1}
.бас_карта svg.участки text.гин_син{font-size:17px;letter-spacing:.22em;text-transform:uppercase;fill:var(--мята);font-weight:700}
.бас_карта svg.участки text.гин_зел{fill:var(--мята)}
.бас_карта svg.участки text.партнёры{fill:#FFE0B8}.бас_карта svg.участки text.кмг{fill:#E4C4FF}.бас_карта svg.участки text.действующие{fill:#BFDCFF}
.бас_карта svg.участки line{stroke:rgba(255,255,255,.55);stroke-width:1.2;vector-effect:non-scaling-stroke;opacity:0;transition:opacity .7s ease}
.бас_карта svg.участки line.включён{opacity:1}
.бас_список li.действ b{color:#7DB8FF}.бас_список li.кмг b{color:#D9A6FF}.бас_список li.партн b{color:#FFE0B8}
.к_геораг{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:16px 20px;border-radius:16px;border:1px solid rgba(2,174,240,.55);background:rgba(2,174,240,.12);text-decoration:none;color:#fff;
  opacity:0;transform:translateY(8px);transition:opacity .4s ease,transform .4s ease}
.к_геораг.включён{opacity:1;transform:none}
.к_геораг:hover{background:rgba(2,174,240,.24)}
.к_геораг b{font-family:'Unbounded',sans-serif;font-size:19px;letter-spacing:.04em;text-transform:uppercase;font-weight:700}
.к_геораг small{display:block;margin-top:4px;font-family:'Golos Text',sans-serif;font-size:17px;color:var(--текст2);text-transform:none;letter-spacing:0}
.к_геораг span{font-size:30.5px;color:var(--кмг)}
'''
голова += css + '</style>'

def li(число, ед, текст, к, кл=''):
    ед = f'<i>{ед}</i>' if ед else ''
    return f'      <li data-к="{к}" class="{кл}"><b>{число}{ед}</b><span>{текст}</span></li>\n'
def li_т(число, ед, текст, такт, кл=''):
    """карточка автопоказа (слайд 1): выходит на своём такте, а не по клику"""
    ед = f'<i>{ед}</i>' if ед else ''
    return f'      <li data-такт="{такт}" class="{кл}"><b>{число}{ед}</b><span>{текст}</span></li>\n'
def li_0(число, ед, текст, кл=''):
    """карточка без кадра: видна сразу, как только слайд показан"""
    ед = f'<i>{ед}</i>' if ед else ''
    return f'      <li class="{кл} включён"><b>{число}{ед}</b><span>{текст}</span></li>\n'

# --- слайд 1: карта слоями ---
def свг_группа(ключ, кадр):
    s = ''
    for о in слои[ключ]:
        s += f'        <path class="{ключ}" data-такт="{кадр}" d="{о["путь"]}"/>\n'
    for о in слои[ключ]:
        x, y = о['центр']; имя = о['имя']
        if ' · ' in имя:   # три модели в одной области — три строки
            части = имя.split(' · ')
            for j, ч in enumerate(части):
                s += f'        <text class="{ключ}" data-такт="{кадр}" x="{x}" y="{y - 40 + j * 40}">{ч}</text>\n'
        else:
            s += f'        <text class="{ключ}" data-такт="{кадр}" x="{x}" y="{y + 8}">{имя}</text>\n'
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
      <!-- 18.09 (Адиль, ночь): без кликов — с пустой карты слои сами наслаиваются по очереди (~2 с шаг),
           карточки выходят синхронно, потом всё гаснет и идёт по кругу, «как гифка». data-такт — номер
           такта автопоказа, а не кадра по клику -->
      <ul class="бас_список">
{li_т('15', 'бассейнов', 'осадочных бассейнов на территории Казахстана', 1)}{li_т('6', 'бассейнов', 'малоизученные: Тенизский, Балхашский, Илийский, Зайсанский, Алакольский, Северо-Казахстанский', 2, 'мало')}{li_т('4', 'бассейна', 'с доказанной нефтегазоносностью: Прииртышский, Северо-Торгайский, Аральский, Сырдарьинский', 3, 'мнб')}{li_т('5', 'моделей', '<em>цифровые бассейновые модели</em>: Прикаспийский, Устюрт-Бозашинский, Мангышлакский, Южно-Торгайский, Шу-Сарысуский', 4, 'пять')}      </ul>
      <div class="бас_карта" id="бас_карта">
        <div class="полотно_слоёв">
          {база_карты()}
          <img class="слой пунктир" data-такт="1" src="медиа/геология/бассейны/бассейны_15_пунктир.png" alt="">
          {''.join(f'<img class="слой мало" data-такт="2" src="медиа/геология/бассейны/мало_{i}.png" alt="">' for i in range(len(слои['мало'])))}
          {''.join(f'<img class="слой мнб" data-такт="3" src="медиа/геология/бассейны/мнб_{i}.png" alt="">' for i in range(len(слои['мнб'])))}
          {''.join(f'<img class="слой пять" data-такт="4" src="медиа/геология/бассейны/пять_{i}.png" alt="">' for i in range(len(слои['пять'])))}
          <svg class="слой включён" viewBox="0 0 {слои['холст'][0]} {слои['холст'][1]}" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
{свг_группа('мало', 2)}{свг_группа('мнб', 3)}{свг_группа('пять', 4)}          </svg>
        </div>
        <div class="подпись">Карта — Департамент геологоразведки КМГ</div>
        <div class="легенда" data-такт="2">
          <div><i style="background:#FFD166"></i>цифровые бассейновые модели</div>
          <div><i style="background:var(--мята)"></i>доказанная нефтегазоносность</div>
          <div><i style="background:rgba(175,192,216,.8)"></i>малоизученные</div>
        </div>
      </div>
    </div>
  </div>
</section>
'''

# 17.09 вечер (геологи): слайд «Прикаспий в цифре» (две белые картинки — девон и очаг
# генерации) снят: «белое надо убрать, чёрное вернуть — только 3D-модель, чтобы всегда крутилась».

# --- слайд 2: живые модели ---
слайд2 = '''
<section class="слайд" id="с2" aria-label="Цифровая бассейновая модель живьём">
  <div class="бровь">Геологоразведка · цифровые бассейновые модели</div>
  <h2 class="заголовок дисплей">Бассейновое моделирование: живая цифровая модель недр</h2>
  <div class="полотно">
    <!-- 18.09 (геологи, WhatsApp): «карта миграции нужна — на одном слайде, чуть поменьше, рядом» —
         структурная поверхность девона D3 из их pptx (белый скрин Petrel как есть) справа от модели -->
    <div class="живая_сетка девон">
      <div class="живо" id="живо">
        <!-- Адиль 17.09: «главный ролик, который хотел увидеть ПП, — на 5-м слайде pptx» —
             3D-модель бассейна с очагом генерации УВ (media3). Геологи 17.09 вечер: только она,
             зациклена и ускорена (×1,5), карточки справа сняты — «просто 3D-модель бассейна». -->
        <video src="медиа/геология/petrel/модель_3d.mp4" poster="медиа/геология/petrel/модель_3d.jpg" muted playsinline preload="auto" loop class="играет"
          data-титр="3D-модель бассейна и очаг генерации УВ" data-под="Где нефть образовалась, куда мигрировала и где скопилась — литология, разрез, очаги генерации"></video>
        <div class="вуаль"></div>
        <div class="титр" id="титр"><span>3D-модель бассейна и очаг генерации УВ</span><small>Где нефть образовалась, куда мигрировала и где скопилась — литология, разрез, очаги генерации</small></div>
      </div>
      <div class="девон_карта">
        <img src="медиа/геология/кейсы/прикаспий_девон.jpg" alt="Структурная поверхность девона D3, Прикаспийский бассейн">
        <!-- 18.09 (Адиль, фото стенда): заголовок «Структурная поверхность девона» снят, подпись крупнее -->
        <div class="титр"><span>Карта миграции УВ: глубины от −4 000 до −14 000 м, контуры участков и месторождения</span></div>
      </div>
    </div>
  </div>
</section>
'''

# --- слайд 3: сейсмика ---
# 18.09 (Адиль, ночь): слайда сейсморазведки/ML в бассейнах нет — он в Geo AI (геораг.html), между
# Data Room и эффектами; ролик сейсмики (медиа/геология/petrel/сейсмика.mp4) живёт там.

# --- слайд 4: портфель поверх карты бассейнов ---
портфель = json.load(io.open(R + 'медиа/геология/бассейны/портфель.json', encoding='utf-8'))
# 18.09 (Адиль, ночь): «каша — текст на тексте, не читается». Имена с карты сняты: на участках
# только номера, имена — списком под карточками слева по классам; бассейны под участками
# приглушены. Порядок номеров — по классам, внутри класса с запада на восток.
ПОРЯДОК_КЛАССОВ = ['действующие', 'кмг', 'партнёры', 'гин_зел', 'гин_син']
КЛАСС_ИМЯ = {'действующие': 'Действующие контракты на недропользование', 'кмг': 'Планируемые к получению контракта за счёт КМГ',
             'партнёры': 'Планируемые с привлечением партнёров', 'гин_зел': 'Региональные исследования (ГИН)', 'гин_син': 'Региональные исследования (ГИН)'}
КЛАСС_ЦСС = {'действующие': 'действ', 'кмг': 'кмг', 'партнёры': 'партн', 'гин_зел': 'гин', 'гин_син': 'гин'}
# 18.09 (геологи): «все 23 перечислены в презе» — на их карте это 21 подпись + Жылыой и Жылыойская
# платформа, а Тажигали ПЗ и Сазтобе ПЗ — два участка (у нас были слиты в один полигон). Разбиваем и
# добавляем: у Сазтобе и платформы своих полигонов нет — номер ставится рядом с соседом.
проекты = []
for пр in портфель['проекты']:
    if пр['класс'] == 'жылыой':
        # 18.09 (геологи): Жылыой — в первую группу, действующие контракты, последним (№ 7); платформа остаётся
        проекты.append(dict(пр, имя='Жылыой', класс='действующие', центр=[пр['центр'][0] + 9999, пр['центр'][1]]))
        проекты.append(dict(пр, имя='Жылыойская платформа', класс='жылыой', пути=[], центр=[пр['центр'][0] - 40, пр['центр'][1] + 30]))
    elif пр['имя'] == 'Тажигали ПЗ · Сазтобе ПЗ':
        проекты.append(dict(пр, имя='Тажигали ПЗ'))
        проекты.append(dict(пр, имя='Сазтобе ПЗ', пути=[], центр=[пр['центр'][0] + 30, пр['центр'][1] + 26]))
    else: проекты.append(пр)
ПОРЯДОК_КЛАССОВ.append('жылыой'); КЛАСС_ИМЯ['жылыой'] = 'Глубокие перспективы Прикаспия'; КЛАСС_ЦСС['жылыой'] = 'жыл'
проекты.sort(key=lambda пр: (ПОРЯДОК_КЛАССОВ.index(пр['класс']), пр['центр'][0]))
for i, пр in enumerate(проекты): пр['н'] = i + 1
# номера на карте: у тесного кластера Жылыоя — сдвиг, чтобы кружки не легли друг на друга
СДВИГ_НОМЕРА = {'Каспий Северный': (-14, -18), 'Большой Жамбыл': (-12, 18), 'Каратон подсолевой': (26, 10),
                'Тажигали ПЗ · Сазтобе ПЗ': (-4, -22), 'Береке': (14, -14), 'Болашак': (18, 14), 'Тайсойган': (0, -6),
                'Озен Северный': (18, -10), 'Озен Палеозой': (-16, 12), 'Прикаспий палеозой (ГИН)': (-30, -125), 'ГИН Торгай Северный': (40, -20)}
СДВИГ_НОМЕРА.update({'Жылыой': (10, 22), 'Тажигали ПЗ': (-4, -22)})
def свг_участки():
    s = ''
    for пр in проекты:
        for д in пр['пути']: s += f'        <path class="{пр["класс"]}" data-к="1" d="{д}"/>\n'
    for пр in проекты:
        x, y = пр['центр']; x = x - 9999 if x > 5000 else x; dx, dy = СДВИГ_НОМЕРА.get(пр['имя'], (0, 0))
        s += f'        <g class="номер {КЛАСС_ЦСС[пр["класс"]]}" data-к="1" transform="translate({x + dx:.1f},{y + dy:.1f})"><circle r="13"/><text y="4.5">{пр["н"]}</text></g>\n'
    return s
def список_проектов():
    # две колонки по высоте: слева действующие + ГИН (8 строк), справа планируемые КМГ + партнёры (12)
    s = ''
    for колонка in (['действ', 'партн', 'гин'], ['кмг', 'жыл']):
        s += '        <div class="колонка">\n'
        for кл in колонка:
            группа = [пр for пр in проекты if КЛАСС_ЦСС[пр['класс']] == кл]
            if not группа: continue
            s += f'        <div class="группа {кл}"><div class="имя_группы">{КЛАСС_ИМЯ[группа[0]["класс"]]}</div>\n'
            for пр in группа: s += f'          <span><b>{пр["н"]}</b>{пр["имя"]}</span>\n'
            s += '        </div>\n'
        s += '        </div>\n'
    return s
слайд4 = f'''
<section class="слайд" id="с4" aria-label="Программа ГРР до 2030 года">
  <div class="бровь">Геологоразведка · портфель разведочных проектов на карте бассейнов</div>
  <h2 class="заголовок дисплей">Программа ГРР до 2030 года</h2>
  <div class="полотно">
    <div class="бас_сетка программа">
      <div class="левая">
        <ul class="бас_список">
{li_0('23', 'проекта', '<em>6</em> страновой значимости · <em>13</em> социальной · <em>2</em> малоизученные бассейны · <em>2</em> глубокие перспективы Прикаспия', 'действ')}{li_0('2026–30', '', 'сейсморазведка 2D <em>6 250 км</em>, 3D <em>2 542 км²</em>, региональная 2D — <em>60 тыс. км</em> · геохимия <em>22 тыс. точек</em> · бурение <em>26</em> скважин', 'партн')}{li_0('4,7', 'млрд т у.т.', 'геологический потенциал программы', 'пять')}        </ul>
        <div class="список_проектов" data-к="1">
{список_проектов()}        </div>
        <a class="к_геораг включён" href="геораг.html"><div><b>Дальше — KMG Geo AI</b><small>ИИ-ассистент геолога</small></div><span>→</span></a>
      </div>
      <div class="бас_карта портфель">
        <div class="полотно_слоёв">
          {база_карты('4')}
          {''.join(f'<img class="слой мало включён" src="медиа/геология/бассейны/мало_{i}.png" alt="">' for i in range(len(слои['мало'])))}
          {''.join(f'<img class="слой мнб включён" src="медиа/геология/бассейны/мнб_{i}.png" alt="">' for i in range(len(слои['мнб'])))}
          {''.join(f'<img class="слой пять включён" src="медиа/геология/бассейны/пять_{i}.png" alt="">' for i in range(len(слои['пять'])))}
          <svg class="слой участки включён" viewBox="0 0 {слои['холст'][0]} {слои['холст'][1]}" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
{свг_участки()}          </svg>
        </div>
        <div class="подпись">Участки — карта портфеля ГРР, Департамент геологоразведки КМГ</div>
        <div class="легенда включён">
          <div><i style="background:#3B8BEF"></i>действующие контракты</div>
          <div><i style="background:#B266F0"></i>планируемые за счёт КМГ</div>
          <div><i style="background:#F6C48F"></i>с привлечением партнёров</div>
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
  /* Слайд 2: ролик 3D-модели крутится по кругу, пока виден слайд (геологи 17.09 вечер: «только чёрный,
     чтобы всегда крутился, ускоренно»). На уходе — пауза, чтобы не жечь кадры. */
  var модель = document.getElementById("живо").querySelector("video"), секция = document.getElementById("с2");
  модель.playbackRate = 1.5;
  function состояние(){ if(секция.classList.contains("виден")){ модель.play().catch(function(){}); } else модель.pause(); }
  new MutationObserver(состояние).observe(секция, { attributes:true, attributeFilter:["class"] });
  состояние();

  /* Слайд 1 — автопоказ (Адиль 18.09 ночь): с пустой карты слои наслаиваются по очереди, карточки
     слева выходят синхронно; после последнего слоя пауза, всё гаснет и идёт по кругу, как гифка.
     Клик по слайду — сразу дальше (кадров по клику у него нет). ?к=N ставит такт сразу (снимки). */
  var с1 = document.getElementById("с1"), всеТакты = [].slice.call(с1.querySelectorAll("[data-такт]")), ВСЕГО = 4;
  /* карточки и легенда — один раз (первый круг), дальше по кругу идёт только карта (Адиль 18.09) */
  var картаТакты = всеТакты.filter(function(э){ return !э.matches("li, .легенда"); }), такты = всеТакты, первыйКруг = true;
  /* 18.09 (Адиль): наложение быстрее, после последнего слоя пауза ~5 с */
  var ШАГ = 900, ПАУЗА = 5000, ГАШЕНИЕ = 700, таймер = null;
  function такт(n){ такты.forEach(function(э){ э.classList.toggle("включён", +э.getAttribute("data-такт") <= n); }); }
  function цикл(){
    clearTimeout(таймер);
    if(!с1.classList.contains("виден")) return;
    var n = 0; такт(0);
    (function шаг(){
      n++; такт(n);
      if(n < ВСЕГО){ таймер = setTimeout(шаг, ШАГ); }
      else { таймер = setTimeout(function(){ с1.classList.add("гаснет"); таймер = setTimeout(function(){ с1.classList.remove("гаснет"); первыйКруг = false; такты = картаТакты; цикл(); }, ГАШЕНИЕ); }, ПАУЗА); }
    })();
  }
  /* наблюдатель реагирует только на смену видимости: класс «гаснет» ставит сам цикл, и без этой
     проверки он же перезапускал цикл и обрывал таймер снятия «гаснет» */
  var былВиден = с1.classList.contains("виден");
  new MutationObserver(function(){
    var виден = с1.classList.contains("виден"); if(виден === былВиден) return; былВиден = виден;
    if(виден) цикл(); else { clearTimeout(таймер); с1.classList.remove("гаснет"); }
  }).observe(с1, { attributes:true, attributeFilter:["class"] });
  var мк = /[?&]к=(\d+)/.exec(decodeURIComponent(location.search));
  if(мк){ такт(+мк[1]); } else if(с1.classList.contains("виден")) цикл();
})();
</script>
'''
страница = голова + '\n</head>\n<body>\n<div id="обёртка">\n<div id="кадр">\n' + слайд1 + слайд2 + слайд4 + низ + листание + видео + '\n</body>\n</html>\n'
io.open(R + 'бассейны.html', 'w', encoding='utf-8').write(страница)
print('ok', len(страница))
