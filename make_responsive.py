"""
make_responsive.py
Hace que todos los slides HTML de la presentación Weld Bear IEDU sean completamente responsive.
Estrategia:
  1. El index.html ya escala los slides via CSS transform (scale) - eso está bien.
  2. Para cada slide individual, inyectamos un <style> responsive que:
     - Garantiza que el contenido llene exactamente la pantalla sin scroll
     - Escala tipografía y espaciados con clamp() y vw/vh
     - Ajusta grids y layouts para mobile/tablet/desktop
     - Mantiene el estilo Blueprint Industrial intacto
"""

import os
import re
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))

# CSS responsivo universal que se inyecta en cada slide
RESPONSIVE_CSS = """
    /* =============================================
       WELD BEAR IEDU - RESPONSIVE SYSTEM v2.0
       Inyectado automáticamente - no editar
       ============================================= */
    
    /* Viewport base - asegura que todo quepa en pantalla */
    html, body {
        width: 100% !important;
        height: 100% !important;
        overflow: hidden !important;
        -webkit-text-size-adjust: 100%;
    }
    
    /* El body siempre en columna de pantalla completa */
    body {
        display: flex !important;
        flex-direction: column !important;
        min-height: 100vh !important;
        max-height: 100vh !important;
    }
    
    /* Header fijo - reduce en pantallas pequeñas */
    header {
        flex-shrink: 0 !important;
        padding-top: clamp(0.4rem, 1vh, 1rem) !important;
        padding-bottom: clamp(0.4rem, 1vh, 1rem) !important;
    }
    
    /* Footer/nav fijo */
    footer, nav[class*="fixed bottom"] {
        flex-shrink: 0 !important;
    }
    
    /* Main content - ocupa el espacio disponible */
    main {
        flex: 1 1 auto !important;
        overflow: hidden !important;
        min-height: 0 !important;
        display: flex !important;
        flex-direction: column !important;
    }
    
    /* Títulos principales - escalan con la pantalla */
    h1.font-headline, h1[class*="font-headline"] {
        font-size: clamp(1.8rem, 5vw, 7rem) !important;
        line-height: 1 !important;
    }
    
    h2.font-headline, h2[class*="font-headline"],
    h3.font-headline, h3[class*="font-headline"] {
        font-size: clamp(1rem, 2.5vw, 2.5rem) !important;
    }
    
    /* Texto de párrafos - legible en cualquier tamaño */
    p, li {
        font-size: clamp(0.75rem, 1.5vw, 1.3rem) !important;
        line-height: 1.4 !important;
    }
    
    /* Grids adaptativos */
    .grid-cols-12 {
        grid-template-columns: repeat(12, minmax(0, 1fr)) !important;
    }
    
    /* Espaciado adaptativo */
    .p-8 { padding: clamp(0.5rem, 1.5vw, 2rem) !important; }
    .p-6 { padding: clamp(0.4rem, 1.2vw, 1.5rem) !important; }
    .p-4 { padding: clamp(0.3rem, 1vw, 1rem) !important; }
    .mb-8 { margin-bottom: clamp(0.4rem, 1.5vh, 2rem) !important; }
    .mb-6 { margin-bottom: clamp(0.3rem, 1vh, 1.5rem) !important; }
    .mb-4 { margin-bottom: clamp(0.2rem, 0.8vh, 1rem) !important; }
    .gap-8 { gap: clamp(0.5rem, 1.5vw, 2rem) !important; }
    .gap-6 { gap: clamp(0.4rem, 1.2vw, 1.5rem) !important; }
    .gap-4 { gap: clamp(0.3rem, 1vw, 1rem) !important; }
    
    /* Imágenes responsive */
    img {
        max-width: 100% !important;
        height: auto !important;
    }
    
    /* Alturas fijas de contenedores - hacerlas flexibles */
    [class*="h-64"] { height: clamp(8rem, 20vh, 16rem) !important; }
    [class*="h-48"] { height: clamp(6rem, 15vh, 12rem) !important; }
    [class*="h-32"] { height: clamp(4rem, 10vh, 8rem) !important; }
    [class*="min-h-\\[400px\\]"] { min-height: clamp(200px, 35vh, 400px) !important; }
    
    /* Padding-top de main quando hay header fixed */
    .pt-24 { padding-top: clamp(3rem, 8vh, 6rem) !important; }
    .pt-16 { padding-top: clamp(2rem, 6vh, 4rem) !important; }
    
    /* Márgenes negativos problemáticos */
    .-mt-4 { margin-top: 0 !important; }
    .-ml-10 { margin-left: 0 !important; }
    
    /* Pantallas muy pequeñas (< 768px) */
    @media (max-width: 768px) {
        h1.font-headline, h1[class*="font-headline"] {
            font-size: clamp(1.5rem, 6vw, 3rem) !important;
        }
        
        .grid-cols-12 {
            grid-template-columns: 1fr !important;
        }
        
        [class*="col-span"] {
            grid-column: span 12 !important;
        }
        
        [class*="md:col-span"] {
            grid-column: span 12 !important;
        }
        
        [class*="lg:col-span"] {
            grid-column: span 12 !important;
        }
        
        /* Ocultar elementos decorativos en móvil para ganar espacio */
        [class*="fixed bottom-20 right"] { display: none !important; }
        [class*="absolute bottom-16"] { display: none !important; }
        [class*="absolute top-0 left-1/2"] { display: none !important; }
        
        /* Nav header links se ocultan en móvil */
        .hidden.md\\:flex { display: none !important; }
        nav.hidden.md\\:flex { display: none !important; }
        
        /* Ajustar padding horizontal */
        .px-6 { padding-left: 0.75rem !important; padding-right: 0.75rem !important; }
        .px-8 { padding-left: 1rem !important; padding-right: 1rem !important; }
        .px-12 { padding-left: 1rem !important; padding-right: 1rem !important; }
    }
    
    /* Pantallas medianas (768px - 1024px) */
    @media (min-width: 768px) and (max-width: 1024px) {
        h1.font-headline, h1[class*="font-headline"] {
            font-size: clamp(2rem, 5vw, 5rem) !important;
        }
    }
    
    /* Pantallas grandes - diseño original preservado */
    @media (min-width: 1280px) {
        h1.font-headline, h1[class*="font-headline"] {
            font-size: clamp(3rem, 6vw, 8rem) !important;
        }
    }
    
    /* Touch targets mínimos para botones de navegación */
    footer button, nav button {
        min-height: 44px !important;
        min-width: 44px !important;
    }

    /* Hacer que el main con overflow-hidden sea scrollable solo si necesita */
    main.overflow-hidden {
        overflow: hidden !important;
    }
    
    /* Clamp para calcular la altura del main correctamente */
    main[class*="h-\\[calc"] {
        height: auto !important;
        flex: 1 1 auto !important;
        min-height: 0 !important;
    }
"""

MARKER_START = "<!-- RESPONSIVE_INJECT_START -->"
MARKER_END = "<!-- RESPONSIVE_INJECT_END -->"

def inject_responsive(html_content: str) -> tuple[str, bool]:
    """Inyecta o actualiza el bloque responsive en el HTML."""
    
    # Si ya tiene el bloque, actualizarlo
    if MARKER_START in html_content:
        pattern = re.compile(
            re.escape(MARKER_START) + r'.*?' + re.escape(MARKER_END),
            re.DOTALL
        )
        new_block = f"{MARKER_START}\n    <style id=\"weld-bear-responsive\">{RESPONSIVE_CSS}    </style>\n    {MARKER_END}"
        new_content = pattern.sub(new_block, html_content)
        return new_content, True
    
    # Buscar </head> para insertar antes
    head_close = html_content.rfind('</head>')
    if head_close == -1:
        # Buscar </style> como alternativa
        style_close = html_content.rfind('</style>')
        if style_close == -1:
            return html_content, False
        insert_pos = style_close + len('</style>')
    else:
        insert_pos = head_close
    
    block = f"\n    {MARKER_START}\n    <style id=\"weld-bear-responsive\">{RESPONSIVE_CSS}    </style>\n    {MARKER_END}\n"
    
    new_content = html_content[:insert_pos] + block + html_content[insert_pos:]
    return new_content, True


def process_slides():
    """Procesa todos los slides del proyecto."""
    
    # Encontrar todos los code.html en subdirectorios
    pattern = os.path.join(ROOT, '**', 'code.html')
    slide_files = glob.glob(pattern, recursive=True)
    
    # Excluir archivos en el directorio raíz (no son slides)  
    slide_files = [f for f in slide_files if os.path.dirname(f) != ROOT]
    
    print(f"[*] Encontrados {len(slide_files)} slides para procesar...\n")
    
    processed = 0
    skipped = 0
    errors = 0
    
    for filepath in sorted(slide_files):
        slide_name = os.path.basename(os.path.dirname(filepath))
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content, success = inject_responsive(content)
            
            if not success:
                print(f"  [!] SKIP: {slide_name} (no se encontro </head>)")
                skipped += 1
                continue
            
            if new_content == content:
                print(f"  [--] Sin cambios: {slide_name}")
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  [OK] Procesado: {slide_name}")
                processed += 1
                
        except Exception as e:
            print(f"  [ERR] ERROR: {slide_name} -> {e}")
            errors += 1
    
    print(f"\n{'='*50}")
    print(f"[OK]  Procesados:    {processed}")
    print(f"[--]  Sin cambios:   {skipped}")
    print(f"[ERR] Errores:       {errors}")
    print(f"{'='*50}")
    print(f"\n[DONE] Todos los slides son ahora completamente responsive!")


if __name__ == '__main__':
    process_slides()
