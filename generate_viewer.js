const fs = require('fs');
const path = require('path');

const baseDir = __dirname;
const slides = [];

const exactOrder = {
    'car_tula_principal_layout_sin_imagen_inferior': 1,
    'portada_herramientas_necesarias_limpia': 2,
    'slide_equipo_recibido_careta_actualizada': 3,
    'slide_herramientas_del_taller_1_3': 4,
    'slide_herramientas_del_taller_2_3_1': 5,
    'slide_herramientas_del_taller_2_3_2': 6,
    'slide_equipo_del_estudiante_limpio_v2': 7,
    'slide_estructura_del_curso': 8,
    'slide_seguridad_industrial_intro': 10,
    'slide_riesgos_en_soldadura': 11,
    'slide_normativa_osha_detallada': 12,
    'slide_normativa_aws_nav_style_fix': 13,
    'slide_epp_detallado_ajuste_men_lateral': 14,
    'slide_riesgos_principales_del_soldador': 15,
    'slide_extintores_ajuste_men': 16,
    'portada_corte_de_metales_sin_imagen': 17,
    'slide_corte_oxiacetileno_intro': 18,
    'slide_equipo_oxiacetileno_1_2_imagen_actualizada': 19,
    'slide_equipo_oxiacetileno_2_2_blanco_y_negro': 20,
    'slide_tipos_de_boquillas_fix_layout': 21,
    'slide_tipos_de_llama_imagen_carburante_actualizada': 22,
    'slide_psi_oxiacetileno_completo_con_referencia': 23,
    'slide_espesores_corte_oxiacetileno_sin_icono': 24,
    'slide_preparaci_n_equipo_oxiacetileno_final': 25,
    'slide_seguridad_oxiacetileno_nav_style_fix': 26,
    'slide_proceso_de_corte_v7_sin_icono': 27,
    'slide_corte_plasma_intro': 28,
    'slide_equipo_corte_plasma_imagen_limpia': 29,
    'slide_preparaci_n_equipo_plasma_imagen_actualizada': 30,
    'slide_espesor_corte_plasma_matrix': 31,
    'slide_seguridad_corte_plasma_layout_final': 32,
    'slide_procesos_smaw_y_fcaw_detalle': 33,
    'slide_proceso_smaw_nav_style_fix': 34,
    'slide_proceso_fcaw_nav_fix_final': 35,
    'slide_tipos_de_corriente_contenido_auditado': 36,
    'slide_arco_el_ctrico_solo_texto': 37,
    'slide_partes_visibles_solo_texto': 38,
    'slide_porosidad_nav_style_fix': 39,
    'slide_socavado_nav_style_fix': 40,
    'slide_cord_n_de_soldadura_nav_fix_final': 41,
    'slide_cordones_solapados_ajuste_color': 42,
    'slide_la_escoria_nav_style_fix': 43,
    'slide_limpieza_del_cord_n_ajuste_color_final': 44,
    'slide_postura_para_soldar_imagen_limpia': 45,
    'slide_movimientos_de_oscilaci_n_nav_fix_final': 46,
    'slide_uso_de_oscilaciones_ajuste_nav': 47,
    'slide_la_pulgada_ajuste_color_final': 48,
    'slide_clasificaci_n_de_electrodos': 49,
    'slide_significado_del_c_digo': 50,
    'slide_clasificaci_n_de_cada_electrodo': 51,
    'slide_corriente_por_electrodo': 52,
    'slide_tabla_ltimo_d_gito': 53,
    'slide_amperajes_teor_a_auditado': 54,
    'slide_matriz_de_amperajes_dise_o_limpio': 55,
    'slide_tipos_de_metales': 56,
    'slide_electrodo_seg_n_metal_solo_texto': 57,
    'portada_sistema_alfanum_rico_logo_fix': 58,
    'slide_sistema_alfanum_rico_nav_fix': 59,
    'slide_tipos_de_juntas_solo_texto': 60,
    'slide_posici_n_1f_nav_style_fix': 61,
    'slide_posici_n_2f_layout_limpio': 62,
    'slide_posici_n_3f_layout_limpio': 63,
    'slide_posici_n_4f_texto_simplificado': 64,
    'slide_posici_n_1g_texto_simplificado': 65,
    'slide_pases_dentro_del_bisel_ajuste_visual': 66,
    'slide_resultados_de_alumnos_doble_testimonio': 67,
    'slide_empresas_aliadas_clean_version': 68,
    'slide_ruta_para_tu_prop_sito_ajuste_est_tico_final': 69,
    'slide_redes_sociales_y_contacto_logo_final': 70
};

const injectionScript = `
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
`;

function walk(dir) {
    const list = fs.readdirSync(dir);
    


    list.forEach(file => {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);
        if (stat && stat.isDirectory()) {
            walk(fullPath);
        } else {
            if (path.basename(fullPath) === 'code.html') {
                try {
                    let content = fs.readFileSync(fullPath, 'utf8');
                    
                    const folderName = path.basename(path.dirname(fullPath));
                    
                    if (exactOrder[folderName] !== undefined) {
                        const rank = exactOrder[folderName];
                        
                        if (content.includes('weld-bear-sync')) {
                            content = content.replace(/<script id="weld-bear-sync">[\s\S]*?<\/script>/g, '');
                        }
                        content = content.replace('</body>', injectionScript + '\n</body>');
                        fs.writeFileSync(fullPath, content, 'utf8');
                        
                        const relPath = path.relative(baseDir, fullPath).replace(/\\/g, '/');
                        slides.push({ rank, relPath, fullPath, folderName });
                    }
                } catch (err) {}
            }
        }
    });
}

walk(baseDir);

slides.sort((a, b) => a.rank - b.rank);

console.log("Ordered Slides:");
slides.slice(0, 12).forEach((s, idx) => console.log(`${idx + 1}. [${s.rank}] ${s.folderName}`));

const slidePaths = slides.map(s => s.relPath);

const targetWidth = 1920;
const targetHeight = 1080;

const indexHtml = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WELD BEAR - Presentation Viewer</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            background-color: #0d0d0d;
            font-family: sans-serif;
        }
        #frame-container {
            position: absolute;
            top: 50%;
            left: 50%;
            width: ${targetWidth}px;
            height: ${targetHeight}px;
            transform-origin: center center;
        }
        .slide-frame {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
            opacity: 0;
            transition: opacity 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            background-color: #131313;
        }
        .slide-frame.active {
            opacity: 1;
            z-index: 10;
        }
        .slide-frame.standby {
            z-index: 1;
        }
        #nav-indicator {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 200;
            background: rgba(0,0,0,0.8);
            border: 1px solid #22C55E;
            color: #22C55E;
            padding: 8px 20px;
            border-radius: 20px;
            font-family: monospace;
            font-size: 14px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s;
        }
        body:hover #nav-indicator { opacity: 0.8; }
    </style>
</head>
<body>
    <div id="nav-indicator">Slide <span id="current">1</span> of ${slidePaths.length}</div>
    <div id="frame-container">
        <iframe id="frame-a" class="slide-frame active" src=""></iframe>
        <iframe id="frame-b" class="slide-frame standby" src=""></iframe>
    </div>

    <script>
        const slides = ${JSON.stringify(slidePaths)};
        let currentIndex = -1;
        
        let activeFrameId = 'frame-a';
        const frameA = document.getElementById('frame-a');
        const frameB = document.getElementById('frame-b');
        const currentSpan = document.getElementById('current');
        const container = document.getElementById('frame-container');

        function scaleContainer() {
            const winW = window.innerWidth;
            const winH = window.innerHeight;
            const scale = Math.min(winW / ${targetWidth}, winH / ${targetHeight});
            container.style.transform = \`translate(-50%, -50%) scale(\${scale})\`;
        }
        window.addEventListener('resize', scaleContainer);
        scaleContainer();

        function loadSlide(index) {
            if (index < 0 || index >= slides.length || index === currentIndex) return;
            
            const nextFrameId = activeFrameId === 'frame-a' ? 'frame-b' : 'frame-a';
            const nextFrame = activeFrameId === 'frame-a' ? frameB : frameA;
            const activeFrame = activeFrameId === 'frame-a' ? frameA : frameB;
            
            nextFrame.src = slides[index];
            
            nextFrame.onload = () => {
                nextFrame.classList.remove('standby');
                nextFrame.classList.add('active');
                
                activeFrame.classList.remove('active');
                activeFrame.classList.add('standby');
                
                activeFrameId = nextFrameId;
                currentIndex = index;
                currentSpan.textContent = currentIndex + 1;
                
                nextFrame.focus();
            };
        }

        window.addEventListener('message', (e) => {
            if (e.data === 'NEXT') {
                loadSlide(currentIndex + 1);
            } else if (e.data === 'PREV') {
                loadSlide(currentIndex - 1);
            } else if (e.data === 'HOME') {
                loadSlide(0);
            }
        });

        loadSlide(0);
    </script>
</body>
</html>`;

fs.writeFileSync(path.join(baseDir, 'index.html'), indexHtml, 'utf8');
console.log('Generated index.html successfully!');
