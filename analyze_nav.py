import os
import re

def analyze_slides(root_dir):
    slides_to_fix = []
    
    for root, dirs, files in os.walk(root_dir):
        if 'code.html' in files:
            file_path = os.path.join(root, 'code.html')
            slide_name = os.path.basename(root)
            
            # Skip folders that aren't actually slides or are reference ones
            if slide_name in ['.git', '1200.webp', 'como.jpg', 'corte.jpg', 'equipo_plasma.jpg', 'posicion1.png', 'proteccion_auditiva_2.png', 'r.jpg_1', 'r.jpg_2', 'soldador.jpg']:
                continue
                
            if 'nav_fix' in slide_name or 'nav_style_fix' in slide_name:
                continue
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            issues = []
            
            # Find nav or footer
            nav_match = re.search(r'<nav[^>]*class="[^"]*fixed[^"]*"[^>]*>(.*?)</nav>', content, re.DOTALL)
            footer_match = re.search(r'<footer[^>]*class="[^"]*fixed[^"]*"[^>]*>(.*?)</footer>', content, re.DOTALL)
            
            if not nav_match:
                if footer_match:
                    issues.append("Uses <footer> instead of <nav>")
                else:
                    issues.append("No common fixed nav/footer found")
            
            nav_content = (nav_match.group(1) if nav_match else "") + (footer_match.group(1) if footer_match else "")
            
            if nav_content:
                text = nav_content.upper()
                if 'PREVIOUS' in text or 'NEXT' in text:
                    issues.append("Uses English labels (PREVIOUS/NEXT)")
                
                if 'arrow_back_ios' in text or 'arrow_forward_ios' in text:
                    issues.append("Uses _ios icons")
                
                # Check for z-index in the HTML (inline or classes)
                if 'z-50' not in content and 'z-100' not in content:
                    issues.append("Missing z-50/z-100 (potential visibility issue)")

            if issues:
                slides_to_fix.append({
                    'path': file_path,
                    'name': slide_name,
                    'issues': issues
                })
                
    return slides_to_fix

if __name__ == "__main__":
    root = r'C:\Users\UserPC\Downloads\stitch_weld_bear_edu_blueprint_industrial_prd'
    bad_slides = analyze_slides(root)
    print(f"Found {len(bad_slides)} slides to fix.")
    for slide in bad_slides:
        print(f"- {slide['name']}: {', '.join(slide['issues'])}")
