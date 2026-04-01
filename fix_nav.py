import os
import re

# =============================================================================
# REFERENCE NAVIGATION AND STYLES (From slide_movimientos_de_oscilaci_n_nav_fix_final)
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

MARKER_SYNC_START = "<!-- Bottom Navigation Bar -->"
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

def fix_nav_in_slide(file_path):
    slide_name = os.path.basename(os.path.dirname(file_path))
    
    # We never modify slides that already have 'nav_fix' or 'nav_style_fix' in their name
    if 'nav_fix' in slide_name or 'nav_style_fix' in slide_name:
        return False
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already fixed (marker present or looks fixed)
    # Actually, we might need to re-run if index was 00
    if 'NAV BAR UNIFICATION - DO NOT EDIT' in content and '<nav class="fixed' in content and '00' not in content:
        return False

    # 1. Extract Slide Index
    index = "00"
    
    # Try to find exactly where the index might be
    # Look for the footer/nav content first
    nav_footer_match = re.search(r'<(?:footer|nav)[^>]*>(.*?)</(?:footer|nav)>', content, re.DOTALL)
    if nav_footer_match:
        nav_c = nav_footer_match.group(1)
        # Clean entities like &nbsp;
        clean_nav = re.sub(r'&nbsp;', ' ', nav_c)
        clean_nav = re.sub(r'<[^>]*>', ' ', clean_nav) # Remove tags
        
        # Find all 1-2 digit numbers
        nums = re.findall(r'\b\d{1,2}\b', clean_nav)
        if nums:
            # Usually the index is the one that is NOT 1 or 2 (if those are labels for buttons)
            # or it's just the most plausible one. 
            # In many cases it's the ONLY number.
            index = nums[-1].zfill(2) # Take the last one and pad with zero

    # Fallback: some slides have the number in the folder name
    if index == "00":
        folder_num = re.search(r'(\d{1,2})', slide_name)
        if folder_num:
            index = folder_num.group(1).zfill(2)

    # 2. Replace Navigation
    new_nav = NAV_HTML_TEMPLATE.replace('{INDEX}', index)
    
    # Replace any current fixed footer or nav
    content = re.sub(r'<(?:nav|footer)[^>]*class="[^"]*fixed[^"]*"[^>]*>.*?</(?:nav|footer)>', new_nav, content, flags=re.DOTALL)
    
    # If no fixed nav/footer was found, try relative ones or just append
    if '<nav class="fixed bottom-0' not in content:
        if '<footer' in content:
             content = re.sub(r'<footer[^>]*>.*?</footer>', new_nav, content, flags=re.DOTALL)
        elif '<nav' in content and 'fixed' not in content:
             # Be careful not to replace top nav
             # Top nav usually has 'top-0' or is at the start of body
             # Let's target the LAST nav if multiple
             navs = list(re.finditer(r'<nav[^>]*>.*?</nav>', content, re.DOTALL))
             if navs:
                 last_nav = navs[-1]
                 content = content[:last_nav.start()] + new_nav + content[last_nav.end():]
        else:
             content = content.replace('</body>', new_nav + '\n</body>')

    # Ensure it's fixed now
    if '<nav class="fixed bottom-0' not in content:
         content = content.replace('</body>', new_nav + '\n</body>')

    # 3. Inject CSS
    if 'NAV BAR UNIFICATION' not in content:
        css_block = f"\n    <style id=\"weld-bear-nav-unified\">{NAV_RESPONSIVE_CSS}    </style>"
        head_close = content.rfind('</head>')
        if head_close != -1:
            content = content[:head_close] + css_block + content[head_close:]
    else:
        # Update existing CSS block if needed
        content = re.sub(r'<style id="weld-bear-nav-unified">.*?</style>', f'<style id="weld-bear-nav-unified">{NAV_RESPONSIVE_CSS}</style>', content, flags=re.DOTALL)

    # 4. Unify Sync Script
    if '<script id="weld-bear-sync">' in content:
        content = re.sub(r'<script id="weld-bear-sync">.*?</script>', SYNC_SCRIPT, content, flags=re.DOTALL)
    else:
        content = content.replace('</body>', SYNC_SCRIPT + '\n</body>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def process_all_slides(root_dir):
    fixed_count = 0
    for root, dirs, files in os.walk(root_dir):
        if 'code.html' in files:
            file_path = os.path.join(root, 'code.html')
            slide_name = os.path.basename(root)
            
            # Skip non-slide folders
            if slide_name in ['.git', '1200.webp', 'como.jpg', 'corte.jpg', 'equipo_plasma.jpg', 'posicion1.png', 'proteccion_auditiva_2.png', 'r.jpg_1', 'r.jpg_2', 'soldador.jpg']:
                continue
                
            if fix_nav_in_slide(file_path):
                print(f"[FIXED] {slide_name}")
                fixed_count += 1
    
    print(f"\nDone! Fixed {fixed_count} slides.")

if __name__ == "__main__":
    root = r'C:\Users\UserPC\Downloads\stitch_weld_bear_edu_blueprint_industrial_prd'
    process_all_slides(root)
