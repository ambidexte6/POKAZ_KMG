# -*- coding: utf-8 -*-
"""Слайды страницы-презентации (закупки, геологи, маркетинг) — в PNG и один PDF
headless-хромом: каждый слайд показывается целиком (все кадры), снимается на
1920×1080. Нужен, чтобы отдать закупщикам PDF без наложений: печать браузера
кладёт все кадры слайда друг на друга.

python инструменты/снимок_слайдов.py закупки.html docs/закупки/закупки.pdf
Сервер «цепочка» (порт 8092) должен быть запущен."""
import sys, io, os, subprocess, urllib.parse, re
from PIL import Image
файл, куда = sys.argv[1:3]
s = io.open(файл, encoding='utf-8').read()
n = len(re.findall(r'<section class="слайд(?! скрыт)[^"]*"', s))
папка = os.path.splitext(куда)[0] + '_png'; os.makedirs(папка, exist_ok=True)
кадры = []
for i in range(n):
    # точка i — «показать целиком»; на первом слайде кадры включаем вручную
    js = ("var т=document.querySelectorAll('#точки button'); if(%d>0) т[%d].click(); else {"
          "var с=document.querySelector('.слайд.виден'); с.querySelectorAll('[data-к]').forEach(function(э){э.classList.add('включён')});}" % (i, i))
    вставка = ('<style>*,*::before,*::after{transition:none!important;animation:none!important}</style>'
               '<script>setTimeout(function(){%s},300);</script></body>' % js)
    врем = os.path.join(os.path.dirname(os.path.abspath(файл)) or '.', '_снимок_' + os.path.basename(файл))
    io.open(врем, 'w', encoding='utf-8').write(s.replace('</body>', вставка))
    адрес = 'http://localhost:8092/' + urllib.parse.quote(os.path.basename(врем))
    png = os.path.join(папка, 'слайд_%02d.png' % (i + 1))
    subprocess.run(['C:/Program Files/Google/Chrome/Application/chrome.exe', '--headless=new', '--disable-gpu',
                    '--hide-scrollbars', '--window-size=1920,1080', '--virtual-time-budget=6000',
                    '--screenshot=' + os.path.abspath(png), адрес], capture_output=True)
    os.remove(врем); кадры.append(Image.open(png).convert('RGB')); print(png)
кадры[0].save(куда, save_all=True, append_images=кадры[1:], resolution=96)
print(куда, n, 'слайдов')
