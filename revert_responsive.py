import os
import glob
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

MARKER_START = "<!-- RESPONSIVE_INJECT_START -->"
MARKER_END = "<!-- RESPONSIVE_INJECT_END -->"

def revert_slides():
    pattern = os.path.join(ROOT, '**', 'code.html')
    slide_files = glob.glob(pattern, recursive=True)
    slide_files = [f for f in slide_files if os.path.dirname(f) != ROOT]
    
    reverted = 0
    errors = 0
    
    for filepath in slide_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if MARKER_START in content:
                # Remove the block including leading newlines
                regex = re.compile(r'\n?[ \t]*' + re.escape(MARKER_START) + r'.*?' + re.escape(MARKER_END) + r'\n?', re.DOTALL)
                new_content = regex.sub('', content)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                reverted += 1
        except Exception as e:
            print(f"ERROR: {filepath} -> {e}")
            errors += 1
            
    print(f"Reverted {reverted} slides successfully. Errors: {errors}")

if __name__ == '__main__':
    revert_slides()
