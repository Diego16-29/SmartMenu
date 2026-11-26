from pathlib import Path
import base64, json, re
from playwright.sync_api import sync_playwright
base=Path(__file__).resolve().parents[1]
out=base/'evidencias'
assets=base/'app/src/main/assets'
photos={x.stem:'data:image/jpeg;base64,'+base64.b64encode(x.read_bytes()).decode() for x in (assets/'img').glob('*.jpg')}
html=(assets/'index.html').read_text()
html=re.sub(r'<meta http-equiv="Content-Security-Policy"[^>]*>','',html)
html=html.replace('<link rel="stylesheet" href="style.css">','<style>'+(assets/'style.css').read_text()+'</style>').replace('<script src="app.js"></script>','').replace('img/logo.jpg',photos['logo'])
js=(assets/'app.js').read_text().replace('img/${p.id}.jpg','${photos[p.id]}')
# In-memory harness: no URL navigation, equivalent storage API backed by a test object.
def load(page, state=None):
    page.set_content(html)
    page.evaluate("s=>{window.testStorage=s;Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>window.testStorage[k]??null,setItem:(k,v)=>window.testStorage[k]=String(v),clear:()=>window.testStorage={}}});}",state or {})
    page.add_script_tag(content='(()=>{const photos='+json.dumps(photos)+';'+js+'})();')
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1280,'height':720},device_scale_factor=1)
    errors=[];page.on('pageerror',lambda error: errors.append(str(error)))
    load(page)
    page.wait_for_function("document.querySelectorAll('.food').length===6")
    
    assert page.locator('.food').count()==6
    assert page.evaluate("[...document.images].every(x=>x.complete&&x.naturalWidth>0)")
    page.keyboard.press('ArrowDown'); assert page.locator(':focus').get_attribute('id').startswith('cat')
    page.keyboard.press('ArrowDown'); assert page.locator(':focus').get_attribute('id').startswith('food-')
    page.locator('#food-burger').focus();page.screenshot(path=str(out/'01_menu.png'))
    page.keyboard.press('Enter');assert page.locator('#panel h2').inner_text()=='Combo Burger';page.screenshot(path=str(out/'02_detalle.png'))
    page.keyboard.press('Enter');assert page.locator('#cartCount').inner_text()=='1'
    page.locator('#cat2').click();assert page.locator('.food').count()==3
    page.locator('#food-tacos').click();page.locator('#add').click();assert page.locator('#cartCount').inner_text()=='2'
    page.locator('#cartNav').click();assert '$248' in page.locator('.total').inner_text()
    page.locator('#plus-burger').click();assert '$397' in page.locator('.total').inner_text()
    page.locator('#minus-burger').click();assert '$248' in page.locator('.total').inner_text();page.wait_for_timeout(2300);page.screenshot(path=str(out/'03_pedido.png'))
    page.keyboard.press('Escape');state=page.evaluate('window.testStorage');page=browser.new_page(viewport={'width':1280,'height':720});page.on('pageerror',lambda error: errors.append(str(error)));load(page,state);assert page.locator('#cartCount').inner_text()=='2'
    page.locator('#cartNav').click();page.locator('#checkout').click();assert 'SM-0001' in page.locator('#panel').inner_text();assert page.locator('#cartCount').inner_text()=='0';page.screenshot(path=str(out/'04_confirmacion.png'))
    page.locator('#close').click();page.locator('#promoNav').click();assert page.locator('.food').count()==2;page.locator('#food-burger').focus();page.screenshot(path=str(out/'05_promociones.png'))
    page.locator('#displayNav').click();assert page.locator('#signage h2').inner_text()=='Combo Burger';page.screenshot(path=str(out/'06_modo_pantalla.png'));page.locator('#nextSlide').click();assert page.locator('#signage h2').inner_text()=='Pizza Supreme';page.wait_for_timeout(8300);assert page.locator('#signage h2').inner_text()=='Tacos al pastor';page.keyboard.press('Escape');assert page.locator('#signage').is_hidden()
    page.keyboard.press('Escape');assert page.locator('.food').count()==6
    page.locator('#food-cake').click();page.locator('#add').click();page.locator('#cartNav').click();page.locator('#clear').click();assert 'vacío' in page.locator('#panel').inner_text();assert page.locator('#cartCount').inner_text()=='0'
    assert not errors,errors
    page.locator('#close').click();page.set_viewport_size({'width':960,'height':540});page.wait_for_timeout(2300);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');page.screenshot(path=str(out/'07_resolucion_960.png'))
    browser.close()
    print('PASS: catálogo, imágenes, D-pad, detalle, filtros, cantidades, total, restauración con almacenamiento simulado, confirmación, promociones, rotación, vaciado y resolución 960x540. Sin errores JavaScript.')
