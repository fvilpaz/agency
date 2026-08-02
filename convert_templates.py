import os
import re

DOWNLOAD_DIR = "/home/fvilpaz/Downloads/web-qreas-agency"
TEMPLATES_DIR = "/home/fvilpaz/code/github/agency/templates"

# Mapping of original files to new routes
routes_map = {
    "index.html": "/",
    "servicios.html": "/servicios",
    "metodo.html": "/metodo",
    "tecnologia-hosteleria.html": "/tecnologia-hosteleria",
    "contacto.html": "/contacto",
    "politica-de-privacidad.html": "/politica-de-privacidad",
    "aviso-legal.html": "/aviso-legal",
    "politica-de-cookies.html": "/politica-de-cookies"
}

# Mapping of original files to new template filenames
templates_map = {
    "index.html": "index.html",
    "servicios.html": "servicios.html",
    "metodo.html": "metodo.html",
    "tecnologia-hosteleria.html": "tecnologia.html",
    "contacto.html": "contacto.html",
    "politica-de-privacidad.html": "legal/privacidad.html",
    "aviso-legal.html": "legal/aviso_legal.html",
    "politica-de-cookies.html": "legal/cookies.html"
}

def clean_html(content):
    # Replace assets path
    content = content.replace('href="assets/', 'href="/static/')
    content = content.replace('src="assets/', 'src="/static/')
    content = content.replace('content="assets/', 'content="/static/')
    content = content.replace('url("assets/', 'url("/static/')
    content = content.replace("url('assets/", "url('/static/")
    
    # Replace routes
    for file, route in routes_map.items():
        # Match href="file" or href="file#something"
        content = re.sub(rf'href="{file}(#[^"]*)?"', lambda m: f'href="{route}{m.group(1) or ""}"', content)
        
    return content

def main():
    # Ensure legal dir exists
    os.makedirs(os.path.join(TEMPLATES_DIR, "legal"), exist_ok=True)
    
    # 1. Create base.html from index.html
    with open(os.path.join(DOWNLOAD_DIR, "index.html"), "r", encoding="utf-8") as f:
        index_html = clean_html(f.read())
        
    parts = index_html.split('<main id="main">')
    head_header = parts[0]
    # To fix SEO meta title/description dynamically we can add Jinja blocks
    head_header = head_header.replace(
        "<title>QREA'S Agency | Consultoría 360º para hostelería</title>",
        "<title>{% block title %}QREA'S Agency | Consultoría 360º para hostelería{% endblock %}</title>"
    )
    head_header = re.sub(
        r'<meta name="description" content="([^"]+)">',
        '{% block meta_description %}\\g<0>{% endblock %}',
        head_header
    )
    
    main_and_footer = parts[1].split('</main>')
    footer = main_and_footer[1]
    
    base_html = head_header + '<main id="main">\n{% block content %}\n{% endblock %}\n</main>' + footer
    with open(os.path.join(TEMPLATES_DIR, "base.html"), "w", encoding="utf-8") as f:
        f.write(base_html)

    # 2. Convert all pages
    for file, tmpl in templates_map.items():
        with open(os.path.join(DOWNLOAD_DIR, file), "r", encoding="utf-8") as f:
            content = clean_html(f.read())
        
        # Extract main content
        main_content = ""
        if '<main id="main">' in content and '</main>' in content:
            main_content = content.split('<main id="main">')[1].split('</main>')[0]
        elif '<main' in content: # Just in case it has different classes
            main_content = re.search(r'<main[^>]*>(.*?)</main>', content, re.DOTALL).group(1)
        
        # Get custom title if not index
        title_block = ""
        meta_desc_block = ""
        if file != "index.html":
            title_match = re.search(r'<title>(.*?)</title>', content)
            if title_match:
                title_block = f'{{% block title %}}{title_match.group(1)}{{% endblock %}}\n'
            
            desc_match = re.search(r'<meta name="description" content="([^"]+)">', content)
            if desc_match:
                meta_desc_block = f'{{% block meta_description %}}<meta name="description" content="{desc_match.group(1)}">{{% endblock %}}\n'

        jinja_template = f'{{% extends "base.html" %}}\n{title_block}{meta_desc_block}{{% block content %}}\n{main_content}\n{{% endblock %}}\n'
        
        with open(os.path.join(TEMPLATES_DIR, tmpl), "w", encoding="utf-8") as f:
            f.write(jinja_template)
            
    print("Templates successfully converted and saved.")

if __name__ == "__main__":
    main()
