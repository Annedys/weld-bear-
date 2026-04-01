import os
import re

# =============================================================================
# REFERENCE NAVIGATION AND STYLES
# =============================================================================

NAV_HTML_TEMPLATE = """
<!-- Bottom Navigation Bar -->
<nav class="fixed bottom-0 left-0 w-full z-50 flex justify-center gap-4 p-4 bg-[#131313] border-t border-[#3B4B37]/30">
<!-- Previous Button -->
<button class="flex flex-col items-center justify-center text-[#22C55E] border border-[#22C55E]/30 px-8 py-3 hover:bg-[#22C55E] hover:text-[#003A05] transition-all active:scale-95 duration-150">
<span class="material-symbols-outlined" data-icon="arrow_back">arrow_back</span>
<span class="font-['JetBrains_Mono'] text-[12px] uppercase tracking-tighter mt-1">ANTERIOR</span>
</button>
<!-- Slide Index -->
<div class="flex flex-col items-center justify-center px-8 py-3 min-w-[120px] bg-[#131313] border border-[#22C55E] text-[#22C55E]">
<span class="material-symbols-outlined" data-icon="grid_view" style="font-variation-settings: 'FILL' 1;">grid_view</span>
<span class="font-['JetBrains_Mono'] text-[12px] uppercase tracking-tighter mt-1">{INDEX}</span>
</div>
<!-- Next Button -->
<button class="flex flex-col items-center justify-center text-[#22C55E] border border-[#22C55E]/30 px-8 py-3 hover:bg-[#22C55E] hover:text-[#003A05] transition-all active:scale-95 duration-150">
<span class="material-symbols-outlined" data-icon="arrow_forward">arrow_forward</span>
<span class="font-['JetBrains_Mono'] text-[12px] uppercase tracking-tighter mt-1">SIGUIENTE</span>
</button>
</nav>
"""

NAV_RESPONSIVE_CSS = """
    /* ===== NAV BAR UNIFICATION - DO NOT EDIT ===== */
    @media (max-width: 1366px), (max-height: 850px) {
        nav.fixed { 
            height: 64px !important; 
            padding: 8px !important; 
            flex-wrap: nowrap !important; 
            justify-content: space-around !important; 
            gap: 4px !important; 
            position: fixed !important; 
            bottom: 0 !important; 
            width: 100% !important; 
            z-index: 100 !important;
            background: #1C1B1B !important;
            display: flex !important;
            border-top: 1px solid rgba(59,75,55,0.3) !important;
        }
        
        nav.fixed button, nav.fixed div { 
            flex: 1 1 auto !important; 
            min-width: 50px !important; 
            height: 48px !important;
            padding: 4px !important; 
            border: none !important;
            background: transparent !important;
            margin: 0 !important;
        }
        nav.fixed div { border: 1px solid rgba(34,197,94,0.3) !important; background: rgba(34,197,94,0.05) !important; }
        nav.fixed button span.font-['JetBrains_Mono'] { font-size: 9px !important; margin-top: 2px !important; }
        
        /* Hide decoration elements that could overlap */
        .fixed.top-24, .fixed.bottom-24 { display: none !important; }
    }
"""

SYNC_SCRIPT = """
<script id="weld-bear-sync">
    setTimeout(() => {
        const triggers = document.querySelectorAll('button, a');
        triggers.forEach(el => {
            const text = el.innerText.toUpperCase();
            const isPrev = text.includes('PREV') || text.includes('ANTERIOR') || text.includes('BACK_IOS') || text.includes('ARROW_BACK');
            const isNext = text.includes('NEXT') || text.includes('SIGUIENTE') || text.includes('SIGUE') || text.includes('CONTINUAR') || text.includes('ARROW_FORWARD');
            const isHome = text.includes('HOME') || text.includes('INICIO');
            const isFinish = text.includes('FINALIZAR') || text.includes('FINISH');

            if (isPrev || isNext || isHome || isFinish) {
                el.onclick = (e) => {
                    e.preventDefault();
                    if (isPrev) window.parent.postMessage('PREV', '*');
                    if (isNext) window.parent.postMessage('NEXT', '*');
                    if (isHome) window.parent.postMessage('HOME', '*');
                    if (isFinish) window.parent.postMessage('FINISH', '*');
                };
            }
        });
    }, 500);

    window.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {
            e.preventDefault();
            window.parent.postMessage('NEXT', '*');
        } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
            e.preventDefault();
            window.parent.postMessage('PREV', '*');
        }
    });

    window.addEventListener('load', () => {
        window.parent.postMessage('LOADED', '*');
    });
</script>
"""

def get_slide_mapping(index_html_path):
    with open(index_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple regex to extract the array content
    array_match = re.search(r'const slides = \[(.*?)\];', content, re.DOTALL)
    if not array_match:
        return {}
        
    slides_str = array_match.group(1)
    # Extract folder names from strings like "folder/code.html"
    slides_list = re.findall(r'"([^/"]+)/code\.html"', slides_str)
    
    mapping = {folder: str(idx + 1).zfill(2) for idx, folder in enumerate(slides_list)}
    return mapping

def fix_nav_in_slide(file_path, mapping):
    slide_name = os.path.basename(os.path.dirname(file_path))
    
    # Reference slides should not be touched
    if 'nav_fix' in slide_name or 'nav_style_fix' in slide_name:
        return False
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Get True Index from mapping
    index = mapping.get(slide_name, "00")
    
    # 2. Perform Replacement
    new_nav = NAV_HTML_TEMPLATE.replace('{INDEX}', index)
    
    # Clean possible duplicate markers or multiple nav bars
    if '<!-- Bottom Navigation Bar -->' in content:
        content = re.sub(r'<!-- Bottom Navigation Bar -->.*?<(?:nav|footer).*?</(?:nav|footer)>', '', content, flags=re.DOTALL)

    # Replace any current fixed/bottom/absolute nav or footer
    has_fixed = False
    if re.search(r'<(?:nav|footer)[^>]*class="[^"]*(?:fixed|bottom|absolute|Shadow)[^"]*"[^>]*>.*?</(?:nav|footer)>', content, re.DOTALL):
        content = re.sub(r'<(?:nav|footer)[^>]*class="[^"]*(?:fixed|bottom|absolute|Shadow)[^"]*"[^>]*>.*?</(?:nav|footer)>', new_nav, content, flags=re.DOTALL, count=1)
        has_fixed = True
    
    if not has_fixed:
        if '<footer' in content:
             content = re.sub(r'<footer[^>]*>.*?</footer>', new_nav, content, flags=re.DOTALL, count=1)
        else:
             if '<script id="weld-bear-sync">' in content:
                 content = content.replace('<script id="weld-bear-sync">', new_nav + '\n<script id="weld-bear-sync">')
             else:
                 content = content.replace('</body>', new_nav + '\n</body>')

    # 3. Inject CSS
    content = re.sub(r'<style id="weld-bear-nav-unified">.*?</style>', '', content, flags=re.DOTALL)
    css_block = f"\n    <style id=\"weld-bear-nav-unified\">{NAV_RESPONSIVE_CSS}    </style>"
    head_close = content.rfind('</head>')
    if head_close != -1:
        content = content[:head_close] + css_block + content[head_close:]

    # 4. Unify Sync Script
    content = re.sub(r'<script id="weld-bear-sync">.*?</script>', SYNC_SCRIPT, content, flags=re.DOTALL)
    if SYNC_SCRIPT not in content:
        content = content.replace('</body>', SYNC_SCRIPT + '\n</body>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def process_all_slides(root_dir):
    mapping = get_slide_mapping(os.path.join(root_dir, 'index.html'))
    print(f"Loaded {len(mapping)} slide mappings.")
    
    fixed_count = 0
    for root, dirs, files in os.walk(root_dir):
        if 'code.html' in files:
            file_path = os.path.join(root, 'code.html')
            slide_name = os.path.basename(root)
            
            if slide_name in ['.git', '1200.webp', 'como.jpg', 'corte.jpg', 'equipo_plasma.jpg', 'posicion1.png', 'proteccion_auditiva_2.png', 'r.jpg_1', 'r.jpg_2', 'soldador.jpg']:
                continue
                
            if fix_nav_in_slide(file_path, mapping):
                print(f"[UNIFIED] {slide_name} -> Index: {mapping.get(slide_name, '??')}")
                fixed_count += 1
    
    print(f"\nDone! Unified {fixed_count} slides.")

if __name__ == "__main__":
    root = r'C:\Users\UserPC\Downloads\stitch_weld_bear_edu_blueprint_industrial_prd'
    process_all_slides(root)
