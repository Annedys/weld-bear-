import os
import re
import json

base_dir = r"c:\Users\UserPC\Downloads\stitch_weld_bear_edu_blueprint_industrial_prd"

slides = []

for root, dirs, files in os.walk(base_dir):
    if "code.html" in files:
        filepath = os.path.join(root, "code.html")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Extract title
            title_match = re.search(r"<title>(.*?)</title>", content)
            slide_num = 999
            if title_match:
                title_text = title_match.group(1)
                num_match = re.search(r"Slide\s*(\d+)", title_text, re.IGNORECASE)
                if num_match:
                    slide_num = int(num_match.group(1))
            
            rel_path = os.path.relpath(filepath, base_dir).replace("\\", "/")
            slides.append((slide_num, rel_path))
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

# sort slides by slide_num
slides.sort(key=lambda x: x[0])

# Keep only the path
slide_paths = [s[1] for s in slides]

print(f"Found {len(slide_paths)} slides.")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WELD BEAR - Presentation Viewer</title>
    <style>
        body, html {{
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            background-color: #131313;
            font-family: sans-serif;
            color: #22C55E;
        }}
        iframe {{
            width: 100%;
            height: 100%;
            border: none;
        }}
        /* Invisible overlay buttons for click navigation */
        .nav-zone {{
            position: absolute;
            top: 0;
            bottom: 80px; /* Leave bottom navbar of the slide clickable if needed */
            width: 15vw;
            z-index: 100;
            cursor: pointer;
        }}
        .nav-left {{ left: 0; }}
        .nav-right {{ right: 0; }}
        
        #controls {{
            position: absolute;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 200;
            background: rgba(0,0,0,0.5);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            pointer-events: none;
            opacity: 0.5;
            transition: opacity 0.3s;
        }}
        body:hover #controls {{ opacity: 1; }}
    </style>
</head>
<body>
    <div id="controls">Slide <span id="current">1</span> of {len(slide_paths)} (Use Left/Right Arrows)</div>
    <div class="nav-zone nav-left" onclick="prevSlide()"></div>
    <div class="nav-zone nav-right" onclick="nextSlide()"></div>
    <iframe id="presentation-frame" src=""></iframe>

    <script>
        const slides = {json.dumps(slide_paths)};
        let currentIndex = 0;
        const frame = document.getElementById('presentation-frame');
        const currentSpan = document.getElementById('current');

        function updateSlide() {{
            if (slides.length > 0) {{
                frame.src = slides[currentIndex];
                currentSpan.textContent = currentIndex + 1;
                // Try to focus the iframe so keyboard events might be captured if we want
                frame.focus(); 
            }}
        }}

        function nextSlide() {{
            if (currentIndex < slides.length - 1) {{
                currentIndex++;
                updateSlide();
            }}
        }}

        function prevSlide() {{
            if (currentIndex > 0) {{
                currentIndex--;
                updateSlide();
            }}
        }}

        window.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowRight' || e.key === ' ') {{
                nextSlide();
            }} else if (e.key === 'ArrowLeft') {{
                prevSlide();
            }}
        }});
        
        // Listen for messages from iframe if we decide to inject script into slides later
        window.addEventListener('message', (e) => {{
            if (e.data === 'NEXT') nextSlide();
            if (e.data === 'PREV') prevSlide();
        }});

        // initial load
        updateSlide();
    </script>
</body>
</html>
"""

output_path = os.path.join(base_dir, "index.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated viewer at {output_path}")
