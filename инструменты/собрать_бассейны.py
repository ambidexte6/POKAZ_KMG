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
.бас_карта img.слой,.бас_карта svg.слой{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;opacity:0;transition:opacity .9s ease}
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
.портфель{position:relative;border-radius:22px;overflow:hidden;border:1px solid var(--грань);background:var(--фон0);min-height:0;display:flex;align-items:center;justify-content:center}
.портфель img{max-width:100%;max-height:100%;object-fit:contain}
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
слайд1 = f'''
<section class="слайд виден" id="с1" aria-label="Осадочные бассейны Казахстана">
  <div class="бровь">Геологоразведка · поиск и оценка участков</div>
  <h2 class="заголовок дисплей">15 осадочных бассейнов — пять из них в цифре</h2>
  <div class="полотно">
    <div class="бас_сетка">
      <ul class="бас_список">
{li('15', 'бассейнов', 'осадочных бассейнов на территории Казахстана — контуры на карте пунктиром', 1)}{li('4', 'бассейна', 'малоперспективные: Тенизский, Балхашский, Алакольский, Зайсанский', 2, 'мало')}{li('4', 'бассейна', 'с доказанной нефтегазоносностью: Прииртышский, Северо-Торгайский, Аральский, Сырдарьинский', 3, 'мнб')}{li('5', 'моделей', '<em>цифровые бассейновые модели</em>: Прикаспийский, Устюрт-Бозашинский, Мангышлакский, Южно-Торгайский, Шу-Сарысуский — структурные карты и очаги генерации УВ', 4, 'пять')}{li('748', 'млн т ЖУ', 'остаточные извлекаемые запасы (ABC1 на 01.01.2026) — основа в этих бассейнах', 5)}      </ul>
      <div class="бас_карта">
        <div class="полотно_слоёв">
          <img class="слой включён" src="медиа/геология/бассейны/каспий.png" alt="">
          <img class="слой включён" src="медиа/геология/бассейны/контур_рк.png" alt="">
          <img class="слой пунктир" data-к="1" src="медиа/геология/бассейны/бассейны_15_пунктир.png" alt="">
          {''.join(f'<img class="слой мало" data-к="2" src="медиа/геология/бассейны/мало_{i}.png" alt="">' for i in range(len(слои['мало'])))}
          {''.join(f'<img class="слой мнб" data-к="3" src="медиа/геология/бассейны/мнб_{i}.png" alt="">' for i in range(len(слои['мнб'])))}
          {''.join(f'<img class="слой пять" data-к="4" src="медиа/геология/бассейны/пять_{i}.png" alt="">' for i in range(len(слои['пять'])))}
          <svg class="слой включён" viewBox="0 0 1984 1201" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
{свг_группа('мало', 2)}{свг_группа('мнб', 3)}{свг_группа('пять', 4)}          </svg>
        </div>
        <div class="подпись">Карта — Департамент геологоразведки КМГ</div>
        <div class="легенда" data-к="2">
          <div><i style="background:#FFD166"></i>цифровые бассейновые модели</div>
          <div><i style="background:var(--мята)"></i>доказанная нефтегазоносность</div>
          <div><i style="background:rgba(175,192,216,.8)"></i>малоперспективные</div>
        </div>
      </div>
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

# --- слайд 4: портфель ---
слайд4 = '''
<section class="слайд" id="с4" aria-label="Портфель проектов ГРР">
  <div class="бровь">Геологоразведка · программа ГРР до 2030 года</div>
  <h2 class="заголовок дисплей">Портфель разведочных проектов на карте бассейнов</h2>
  <div class="полотно">
    <div class="бас_сетка">
      <ul class="бас_список">
''' + li('23', 'проекта', 'на разных стадиях подготовки · <em>26</em> поисковых скважин, проходка 89 тыс. м', 1) + li('6', 'проектов', 'страновой значимости · <em>13</em> — социальной значимости', 2) + li('2D · 3D', '', 'сейсморазведка <em>6 250 км</em> и <em>2 540 км²</em> · региональная 2D по Прикаспию — 60 тыс. км', 3) + li('4,7', 'млрд т у.т.', 'потенциальная геологическая ресурсная база программы', 4, 'пять') + '''      </ul>
      <div class="портфель" data-к="1">
        <img src="медиа/геология/карта_портфеля_тёмная.png" alt="Карта портфеля разведочных проектов">
        <div class="подпись" style="position:absolute;right:22px;top:18px;padding:10px 14px;border-radius:12px;background:rgba(5,8,16,.78);border:1px solid var(--грань);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--кмг)">Карта портфеля — Департамент геологоразведки КМГ</div>
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
  if(с3.classList.contains("виден")) сейсм.play().catch(function(){});
  /* титры сейсмики — по отрезкам ролика (5 фрагментов по ~10 с) */
  var ТИТРЫ = [[0,"Сейсмический куб","разрезы через толщу пород"],[9.5,"Разрезы","геолог читает слои и разломы"],[19,"Интерпретация горизонтов","здесь помогут ML и нейросети — в работе"],[28.5,"Структура-ловушка","где нефть могла скопиться"],[38,"Геологическая модель","основа для точки бурения и оценки запасов"]];
  var тс = document.getElementById("титр_сейсмика");
  setInterval(function(){ if(сейсм.paused) return; var t = сейсм.currentTime, к = ТИТРЫ[0]; ТИТРЫ.forEach(function(х){ if(t >= х[0]) к = х; });
    if(тс.querySelector("span").textContent !== к[1]){ тс.querySelector("span").textContent = к[1]; тс.querySelector("small").textContent = к[2]; } }, 250);
})();
</script>
'''
страница = голова + '\n</head>\n<body>\n<div id="обёртка">\n<div id="кадр">\n' + слайд1 + слайд2 + слайд3 + слайд4 + низ + листание + видео + '\n</body>\n</html>\n'
io.open(R + 'бассейны.html', 'w', encoding='utf-8').write(страница)
print('ok', len(страница))
