from bs4 import BeautifulSoup
import re

def on_page_content(html, page, config, files):
    
    # ==========================================
    # 0. REEMPLAZOS DE TEXTO (Ej: Checkbox Catálogo)
    # ==========================================
    # Transforma los símbolos en etiquetas HTML para que el JavaScript los detecte
    html = html.replace('☑', '<abbr class="nou comun" title="Servicio declarado como compartido">☑</abbr>')
    html = html.replace('☐', '<abbr class="nou nocom" title="Servicio NO declarado como compartido">☐</abbr>')

    # Convertimos el HTML a un objeto BeautifulSoup para procesar tablas y figuras
    soup = BeautifulSoup(html, 'html.parser')
    
    # ==========================================
    # 1. LÓGICA DE TABLAS Y FUSIÓN DE CELDAS
    # ==========================================
    re_tabcaption = re.compile(r"^Tabla( \d+)?: .+")
    for table in soup.find_all("table"):
        cpt = table.find_next_sibling("p")
        if cpt is not None:
            text = cpt.get_text().strip()
            m = re_tabcaption.match(text)
            if m:
                cpt.name = "caption"
                table.insert(0, cpt)
                m_group = m.group(1)
                if m_group:
                    if not table.attrs.get("id"):
                        table.attrs["id"] = "tb" + m_group.strip()
                new_text = str(cpt).replace(m.group(0).split(":")[0] + ":", "", 1).strip()
                cpt.replace_with(BeautifulSoup(f"<caption>{new_text}</caption>", "html.parser"))

    def add_style(tag, new_style):
        current_style = tag.attrs.get("style", "")
        if new_style not in current_style:
            tag.attrs["style"] = f"{current_style} {new_style}".strip()

    for tbody in soup.find_all(["thead", "tbody"]):
        trs = list(tbody.find_all("tr"))
        
        for i, tr in reversed(list(enumerate(trs))):
            tds = tr.find_all(["td", "th"])
            
            # Fusión horizontal (Colspan)
            for c, td in reversed(list(enumerate(tds))):
                text = td.get_text().strip()
                if text == "<":
                    if c > 0:
                        prev = tds[c-1]
                        prev.attrs["colspan"] = int(prev.get("colspan", 1)) + int(td.get("colspan", 1))
                        add_style(prev, "text-align: center;")
                        td.extract()
                elif text == ">":
                    if c < len(tds) - 1:
                        post = tds[c+1]
                        post.attrs["colspan"] = int(post.get("colspan", 1)) + int(td.get("colspan", 1))
                        add_style(post, "text-align: center;")
                        td.extract()
            
            # Fusión vertical (Rowspan)
            if i > 0:
                for c, td in enumerate(tds):
                    text = td.get_text().strip()
                    if text == "^":
                        try:
                            prev = trs[i-1].find_all(["td", "th"])[c]
                            prev.attrs["rowspan"] = int(prev.get("rowspan", 1)) + int(td.get("rowspan", 1))
                            add_style(prev, "vertical-align: middle;")
                            td.extract()
                        except IndexError:
                            pass

    # ==========================================
    # 2. LÓGICA DE FIGURAS E IMÁGENES
    # ==========================================
    re_figcaption = re.compile(r"^Figura( \d+)?: .+")
    for img in soup.find_all("img"):
        p = img.find_parent("p")
        
        if p is None or len(p.get_text().strip()) > 0:
            continue
            
        cpt = p.find_next_sibling("p")
        if cpt is None:
            continue
            
        text = cpt.get_text().strip()
        m = re_figcaption.match(text)
        
        if m:
            p.name = "figure"
            cpt.name = "figcaption"
            p.append(cpt)
            
            num = m.group(1)
            if num and num.strip():
                if not p.attrs.get("id"):
                    p.attrs["id"] = "fg" + num.strip()
            
            clean_text = text.split(":", 1)[-1].strip()
            prefix = text.split(":", 1)[0] + ":"
            new_cpt_html = str(cpt).replace(prefix, "", 1)
            cpt.replace_with(BeautifulSoup(new_cpt_html, "html.parser"))
            
            if not img.attrs.get("title"):
                img.attrs["title"] = clean_text
            if not img.attrs.get("alt"):
                img.attrs["alt"] = clean_text

    return str(soup)