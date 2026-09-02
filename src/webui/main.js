const ICONS = {
  translate: `<path d="M247.15,212.42l-56-112a8,8,0,0,0-14.31,0l-21.71,43.43A88,88,0,0,1,108,126.93,103.65,103.65,0,0,0,135.69,64H160a8,8,0,0,0,0-16H104V32a8,8,0,0,0-16,0V48H32a8,8,0,0,0,0,16h87.63A87.76,87.76,0,0,1,96,116.35a87.74,87.74,0,0,1-19-31,8,8,0,1,0-15.08,5.34A103.63,103.63,0,0,0,84,127a87.55,87.55,0,0,1-52,17,8,8,0,0,0,0,16,103.46,103.46,0,0,0,64-22.08,104.18,104.18,0,0,0,51.44,21.31l-26.6,53.19a8,8,0,0,0,14.31,7.16L148.94,192h70.11l13.79,27.58A8,8,0,0,0,240,224a8,8,0,0,0,7.15-11.58ZM156.94,176,184,121.89,211.05,176Z"/>`,
  waveform: `<path d="M56,96v64a8,8,0,0,1-16,0V96a8,8,0,0,1,16,0ZM88,24a8,8,0,0,0-8,8V224a8,8,0,0,0,16,0V32A8,8,0,0,0,88,24Zm40,32a8,8,0,0,0-8,8V192a8,8,0,0,0,16,0V64A8,8,0,0,0,128,56Zm40,32a8,8,0,0,0-8,8v64a8,8,0,0,0,16,0V96A8,8,0,0,0,168,88Zm40-16a8,8,0,0,0-8,8v96a8,8,0,0,0,16,0V80A8,8,0,0,0,208,72Z"/>`,
  microphone: `<path d="M168,16A72.07,72.07,0,0,0,96,88a73.29,73.29,0,0,0,.63,9.42L27.12,192.22A15.93,15.93,0,0,0,28.71,213L43,227.29a15.93,15.93,0,0,0,20.78,1.59l94.81-69.53A73.29,73.29,0,0,0,168,160a72,72,0,1,0,0-144Zm56,72a55.72,55.72,0,0,1-11.16,33.52L134.49,43.16A56,56,0,0,1,224,88ZM54.32,216,40,201.68,102.14,117A72.37,72.37,0,0,0,139,153.86ZM112,88a55.67,55.67,0,0,1,11.16-33.51l78.34,78.34A56,56,0,0,1,112,88Zm-2.35,58.34a8,8,0,0,1,0,11.31l-8,8a8,8,0,1,1-11.31-11.31l8-8A8,8,0,0,1,109.67,146.33Z"/>`,
  stack: `<path d="M12,111l112,64a8,8,0,0,0,7.94,0l112-64a8,8,0,0,0,0-13.9l-112-64a8,8,0,0,0-7.94,0l-112,64A8,8,0,0,0,12,111ZM128,49.21,223.87,104,128,158.79,32.13,104ZM246.94,140A8,8,0,0,1,244,151L132,215a8,8,0,0,1-7.94,0L12,151A8,8,0,0,1,20,137.05l108,61.74,108-61.74A8,8,0,0,1,246.94,140Z"/>`,
  broom: `<path d="M235.5,216.81c-22.56-11-35.5-34.58-35.5-64.8V134.73a15.94,15.94,0,0,0-10.09-14.87L165,110a8,8,0,0,1-4.48-10.34l21.32-53a28,28,0,0,0-16.1-37,28.14,28.14,0,0,0-35.82,16,.61.61,0,0,0,0,.12L108.9,79a8,8,0,0,1-10.37,4.49L73.11,73.14A15.89,15.89,0,0,0,55.74,76.8C34.68,98.45,24,123.75,24,152a111.45,111.45,0,0,0,31.18,77.53A8,8,0,0,0,61,232H232a8,8,0,0,0,3.5-15.19ZM67.14,88l25.41,10.3a24,24,0,0,0,31.23-13.45l21-53c2.56-6.11,9.47-9.27,15.43-7a12,12,0,0,1,6.88,15.92L145.69,93.76a24,24,0,0,0,13.43,31.14L184,134.73V152c0,.33,0,.66,0,1L55.77,101.71A108.84,108.84,0,0,1,67.14,88Zm48,128a87.53,87.53,0,0,1-24.34-42,8,8,0,0,0-15.49,4,105.16,105.16,0,0,0,18.36,38H64.44A95.54,95.54,0,0,1,40,152a85.9,85.9,0,0,1,7.73-36.29l137.8,55.12c3,18,10.56,33.48,21.89,45.16Z"/>`,
  cc: `<circle cx="6" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><circle cx="18" cy="18" r="3"/><path d="M6 9v6"/><path d="M15 18H9"/><path d="M18 15v-2a3 3 0 0 0-3-3H9"/>`,
  globe: `<path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm88,104a87.62,87.62,0,0,1-6.4,32.94l-44.7-27.49a15.92,15.92,0,0,0-6.24-2.23l-22.82-3.08a16.11,16.11,0,0,0-16,7.86h-8.72l-3.8-7.86a15.91,15.91,0,0,0-11-8.67l-8-1.73L96.14,104h16.71a16.06,16.06,0,0,0,7.73-2l12.25-6.76a16.62,16.62,0,0,0,3-2.14l26.91-24.34A15.93,15.93,0,0,0,166,49.1l-.36-.65A88.11,88.11,0,0,1,216,128ZM143.31,41.34,152,56.9,125.09,81.24,112.85,88H96.14a16,16,0,0,0-13.88,8l-8.73,15.23L63.38,84.19,74.32,58.32a87.87,87.87,0,0,1,69-17ZM40,128a87.53,87.53,0,0,1,8.54-37.8l11.34,30.27a16,16,0,0,0,11.62,10l21.43,4.61L96.74,143a16.09,16.09,0,0,0,14.4,9h1.48l-7.23,16.23a16,16,0,0,0,2.86,17.37l.14.14L128,205.94l-1.94,10A88.11,88.11,0,0,1,40,128Zm102.58,86.78,1.13-5.81a16.09,16.09,0,0,0-4-13.9,1.85,1.85,0,0,1-.14-.14L120,174.74,133.7,144l22.82,3.08,45.72,28.12A88.18,88.18,0,0,1,142.58,214.78Z"/>`,
  github: `<path d="M208.31,75.68A59.78,59.78,0,0,0,202.93,28,8,8,0,0,0,196,24a59.75,59.75,0,0,0-48,24H124A59.75,59.75,0,0,0,76,24a8,8,0,0,0-6.93,4,59.78,59.78,0,0,0-5.38,47.68A58.14,58.14,0,0,0,56,104v8a56.06,56.06,0,0,0,48.44,55.47A39.8,39.8,0,0,0,96,192v8H72a24,24,0,0,1-24-24A40,40,0,0,0,8,136a8,8,0,0,0,0,16,24,24,0,0,1,24,24,40,40,0,0,0,40,40H96v16a8,8,0,0,0,16,0V192a24,24,0,0,1,48,0v40a8,8,0,0,0,16,0V192a39.8,39.8,0,0,0-8.44-24.53A56.06,56.06,0,0,0,216,112v-8A58.14,58.14,0,0,0,208.31,75.68ZM200,112a40,40,0,0,1-40,40H112a40,40,0,0,1-40-40v-8a41.74,41.74,0,0,1,6.9-22.48A8,8,0,0,0,80,73.83a43.81,43.81,0,0,1,.79-33.58,43.88,43.88,0,0,1,32.32,20.06A8,8,0,0,0,119.82,64h32.35a8,8,0,0,0,6.74-3.69,43.87,43.87,0,0,1,32.32-20.06A43.81,43.81,0,0,1,192,73.83a8.09,8.09,0,0,0,1,7.65A41.72,41.72,0,0,1,200,104Z"/>`,
  sidebar: `<path d="M165.66,202.34a8,8,0,0,1-11.32,11.32l-80-80a8,8,0,0,1,0-11.32l80-80a8,8,0,0,1,11.32,11.32L91.31,128Z"/>`,
  caret: `<path d="M213.66,101.66l-80,80a8,8,0,0,1-11.32,0l-80-80A8,8,0,0,1,53.66,90.34L128,164.69l74.34-74.35a8,8,0,0,1,11.32,11.32Z"/>`,
  file: `<path d="M213.66,82.34l-56-56A8,8,0,0,0,152,24H56A16,16,0,0,0,40,40V216a16,16,0,0,0,16,16H200a16,16,0,0,0,16-16V88A8,8,0,0,0,213.66,82.34ZM160,51.31,188.69,80H160ZM200,216H56V40h88V88a8,8,0,0,0,8,8h48V216Z"/>`,
  folder: `<path d="M245,110.64A16,16,0,0,0,232,104H216V88a16,16,0,0,0-16-16H130.67L102.94,51.2a16.14,16.14,0,0,0-9.6-3.2H40A16,16,0,0,0,24,64V208h0a8,8,0,0,0,8,8H211.1a8,8,0,0,0,7.59-5.47l28.49-85.47A16.05,16.05,0,0,0,245,110.64ZM93.34,64,123.2,86.4A8,8,0,0,0,128,88h72v16H69.77a16,16,0,0,0-15.18,10.94L40,158.7V64Zm112,136H43.1l26.67-80H232Z"/>`,
  info: `<path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216Zm16-40a8,8,0,0,1-8,8,16,16,0,0,1-16-16V128a8,8,0,0,1,0-16,16,16,0,0,1,16,16v40A8,8,0,0,1,144,176ZM112,84a12,12,0,1,1,12,12A12,12,0,0,1,112,84Z"/>`,
  extlink: `<path d="M200,64V168a8,8,0,0,1-16,0V83.31L69.66,197.66a8,8,0,0,1-11.32-11.32L172.69,72H88a8,8,0,0,1,0-16H192A8,8,0,0,1,200,64Z"/>`,
  check: `<path d="M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z"/>`,
  dub: `<path d="M155.51,24.81a8,8,0,0,0-8.42.88L77.25,80H32A16,16,0,0,0,16,96v64a16,16,0,0,0,16,16H77.25l69.84,54.31A8,8,0,0,0,160,224V32A8,8,0,0,0,155.51,24.81ZM32,96H72v64H32ZM144,207.64,88,164.09V91.91l56-43.55Zm54-106.08a40,40,0,0,1,0,52.88,8,8,0,0,1-12-10.58,24,24,0,0,0,0-31.72,8,8,0,0,1,12-10.58ZM248,128a79.9,79.9,0,0,1-20.37,53.34,8,8,0,0,1-11.92-10.67,64,64,0,0,0,0-85.33,8,8,0,1,1,11.92-10.67A79.83,79.83,0,0,1,248,128Z"/>`,
  article: `<path d="M216,40H40A16,16,0,0,0,24,56V200a16,16,0,0,0,16,16H216a16,16,0,0,0,16-16V56A16,16,0,0,0,216,40Zm0,160H40V56H216V200ZM184,96a8,8,0,0,1-8,8H80a8,8,0,0,1,0-16h96A8,8,0,0,1,184,96Zm0,32a8,8,0,0,1-8,8H80a8,8,0,0,1,0-16h96A8,8,0,0,1,184,128Zm0,32a8,8,0,0,1-8,8H80a8,8,0,0,1,0-16h96A8,8,0,0,1,184,160Z"/>`,
  monitor: `<path d="M208,40H48A24,24,0,0,0,24,64V176a24,24,0,0,0,24,24H208a24,24,0,0,0,24-24V64A24,24,0,0,0,208,40Zm8,136a8,8,0,0,1-8,8H48a8,8,0,0,1-8-8V64a8,8,0,0,1,8-8H208a8,8,0,0,1,8,8Zm-48,48a8,8,0,0,1-8,8H96a8,8,0,0,1,0-16h64A8,8,0,0,1,168,224Zm-3.56-110.66-48-32A8,8,0,0,0,104,88v64a8,8,0,0,0,12.44,6.66l48-32a8,8,0,0,0,0-13.32ZM120,137.05V103l25.58,17Z"/>`,
  sparkle: `<path d="M197.58,129.06,146,110l-19-51.62a15.92,15.92,0,0,0-29.88,0L78,110l-51.62,19a15.92,15.92,0,0,0,0,29.88L78,178l19,51.62a15.92,15.92,0,0,0,29.88,0L146,178l51.62-19a15.92,15.92,0,0,0,0-29.88ZM137,164.22a8,8,0,0,0-4.74,4.74L112,223.85,91.78,169A8,8,0,0,0,87,164.22L32.15,144,87,123.78A8,8,0,0,0,91.78,119L112,64.15,132.22,119a8,8,0,0,0,4.74,4.74L191.85,144ZM144,40a8,8,0,0,1,8-8h16V16a8,8,0,0,1,16,0V32h16a8,8,0,0,1,0,16H184V64a8,8,0,0,1-16,0V48H152A8,8,0,0,1,144,40ZM248,88a8,8,0,0,1-8,8h-8v8a8,8,0,0,1-16,0V96h-8a8,8,0,0,1,0-16h8V72a8,8,0,0,1,16,0v8h8A8,8,0,0,1,248,88Z"/>`,
  terminal: `<path d="M216,40H40A16,16,0,0,0,24,56V200a16,16,0,0,0,16,16H216a16,16,0,0,0,16-16V56A16,16,0,0,0,216,40Zm0,160H40V56H216V200ZM104,120a8,8,0,0,1-2.34,5.66l-24,24a8,8,0,0,1-11.32-11.32L86.69,120,66.34,99.66a8,8,0,0,1,11.32-11.32l24,24A8,8,0,0,1,104,120Zm72,32a8,8,0,0,1-8,8H136a8,8,0,0,1,0-16h32A8,8,0,0,1,176,152Z"/>`
};

function svg(name, opts = {}) {
  const cls = opts.cls ? ` class="${opts.cls}"` : '';
  const fill = opts.fill ? ` fill="${opts.fill}"` : ' fill="currentColor"';
  const stroke = opts.stroke ? ` stroke="${opts.stroke}" stroke-width="${opts.strokeWidth || 2}" stroke-linecap="round" stroke-linejoin="round"` : '';
  return `<svg viewBox="0 0 256 256"${cls}${fill}${stroke}>${ICONS[name]||''}</svg>`;
}
function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

const BRIDGE = (function() {
  const T = window.__TAURI__;
  if (T && T.core && typeof T.core.invoke === 'function') {
    const invoke = T.core.invoke;
    try {
      if (T.event && T.event.listen) {
        T.event.listen('term-line', e => termAppend(String(e.payload).replace(/\r?\n$/, '') + '\n'));
        T.event.listen('term-done', e => taskDone(e && e.payload));
      }
    } catch (_) {}
    return {
      host: 'tauri',
      winMin: () => invoke('win_minimize'),
      winMax: () => invoke('win_toggle_maximize'),
      winClose: () => invoke('win_close'),
      openUrl: (u) => invoke('open_url', { url: u }),
      pickFile: async () => (await invoke('pick_file')) || '',
      pickFolder: async () => (await invoke('pick_folder')) || '',
      getOllama: async () => { try { return (await invoke('get_ollama')) || []; } catch (_) { return []; } },
      run: (kind, args) => invoke('run_task', { kind, args }),
    };
  }
  
  // Demo fallback
  return {
    host: 'demo',
    winMin() {}, winMax() {}, winClose() {}, openUrl: (u) => window.open(u, '_blank'),
    pickFile: async () => 'C:/Users/User/Videos/sample.mkv',
    pickFolder: async () => 'C:/Users/User/Videos/Folder',
    getOllama: async () => [],
    run: (kind, args) => {
      const L_arr = I18N[lang].demo;
      let i = 0;
      (function s() {
        if (i >= L_arr.length) { taskDone({ code: 0 }); return; }
        termAppend(L_arr[i++] + '\n');
        setTimeout(s, 600);
      })();
    },
  };
})();

const I18N = {
  es: {
    tools: 'Herramientas', tagline: 'Kit de subtítulos', langLabel: 'ES',
    none: 'Ninguno seleccionado', fileordir: 'Archivo o carpeta…', file: 'Archivo', folder: 'Carpeta',
    engine: 'Motor IA', voice: 'Voz de doblaje', install: 'Instalar IA local', ready: 'listo. Selecciona un archivo para empezar.',
    running: 'ejecutando…', running_btn: 'Ejecutando…', done_ok: 'Tarea completada', done_err: 'Terminó con errores', note: 'demo · vista previa', missing: '[!] Faltan archivos por seleccionar.',
    term_title: 'Consola', console_idle: 'Sistema en línea. Esperando órdenes...',
    nav: { translate: 'Traducir subtítulos', sync: 'Sincronizar subtítulos', whisper: 'Generar subtítulos', mux: 'Añadir subtítulo al vídeo', cleaner: 'Convertir ASS a SRT', dubbing: 'Doblar vídeo (voz IA)', summary: 'Resumen y capítulos', hardsub: 'Incrustar subtítulos', clean_audio: 'Limpiar audio' },
    tabs: {
      translate: { title: 'Traducir subtítulos', desc: 'Traduce un archivo .srt al español (o a otro idioma). Compatible con Ollama local.', btn: 'Traducir', rows: [null] },
      sync: { title: 'Sincronizar subtítulos', desc: 'Alinea un subtítulo desfasado con el audio del vídeo (detección de voz).', btn: 'Sincronizar', rows: ['Vídeo original', 'Subtítulo desfasado'] },
      whisper: { title: 'Generar subtítulos desde el vídeo', desc: 'Escucha el audio del vídeo y crea el archivo .srt automáticamente. Ideal para vídeos que no traen subtítulos.', btn: 'Generar', rows: ['Vídeo o carpeta'] },
      mux: { title: 'Añadir subtítulo al vídeo (MKV)', desc: 'Mete el .srt como pista dentro del vídeo, sin recodificar ni perder calidad.', btn: 'Añadir', rows: ['Vídeo (.mkv)', 'Subtítulo (.srt)'] },
      cleaner: { title: 'Convertir ASS a SRT', desc: 'Convierte subtítulos .ass complejos (típicos de anime) en .srt de texto plano compatible con cualquier reproductor o TV.', btn: 'Convertir', rows: ['Archivo (.ass)'] },
      dubbing: { title: 'Doblar vídeo (voz IA)', desc: 'Genera una pista de voz a partir del subtítulo y crea un vídeo con audio dual (original + doblaje).', btn: 'Doblar', rows: ['Subtítulo (.srt)', 'Vídeo (opcional)'] },
      summary: { title: 'Resumen y capítulos', desc: 'Resume el contenido y genera capítulos con marcas de tiempo a partir del subtítulo. Requiere Ollama.', btn: 'Resumir', rows: ['Subtítulo (.srt)'] },
      hardsub: { title: 'Incrustar subtítulos (quemar)', desc: 'Graba los subtítulos de forma permanente sobre la imagen del vídeo.', btn: 'Incrustar', rows: ['Vídeo', 'Subtítulo (.srt)'] },
      clean_audio: { title: 'Limpiar audio', desc: 'Reduce el ruido de fondo y realza la voz del audio con FFmpeg.', btn: 'Limpiar', rows: ['Vídeo o audio'] },
    },
    demo: ['[*] Analizando entrada…', '[*] Extrayendo audio (ffmpeg)…', '[*] Procesando bloque 1/1523…', '[*] Procesando bloque 1523/1523…', '[✔] Tarea completada.']
  },
  en: {
    tools: 'Tools', tagline: 'Subtitle toolkit', langLabel: 'EN',
    none: 'None selected', fileordir: 'File or folder…', file: 'File', folder: 'Folder',
    engine: 'AI Engine', voice: 'Dubbing voice', install: 'Install local AI', ready: 'ready. Pick a file to start.',
    running: 'running…', running_btn: 'Running…', done_ok: 'Task completed', done_err: 'Finished with errors', note: 'demo · preview', missing: '[!] Missing input files.',
    term_title: 'Console', console_idle: 'System online. Awaiting commands...',
    nav: { translate: 'Translate subtitles', sync: 'Sync subtitles', whisper: 'Generate subtitles', mux: 'Add subtitle to video', cleaner: 'Convert ASS to SRT', dubbing: 'Dub video (AI voice)', summary: 'Summary & chapters', hardsub: 'Burn in subtitles', clean_audio: 'Clean audio' },
    tabs: {
      translate: { title: 'Translate subtitles', desc: 'Translate an .srt file to Spanish (or another language). Works with local Ollama.', btn: 'Translate', rows: [null] },
      sync: { title: 'Sync subtitles', desc: 'Align an out-of-sync subtitle to the video audio (voice detection).', btn: 'Sync', rows: ['Original video', 'Out-of-sync subtitle'] },
      whisper: { title: 'Generate subtitles from video', desc: 'Listens to the video audio and creates the .srt automatically. Ideal for videos with no subtitles.', btn: 'Generate', rows: ['Video or folder'] },
      mux: { title: 'Add subtitle to video (MKV)', desc: 'Embeds the .srt as a track inside the video — no re-encoding, no quality loss.', btn: 'Add', rows: ['Video (.mkv)', 'Subtitle (.srt)'] },
      cleaner: { title: 'Convert ASS to SRT', desc: 'Convert complex .ass subtitles (typical of anime) into plain-text .srt compatible with any player or TV.', btn: 'Convert', rows: ['File (.ass)'] },
      dubbing: { title: 'Dub video (AI voice)', desc: 'Generate a voice track from the subtitle and build a dual-audio video (original + dub).', btn: 'Dub', rows: ['Subtitle (.srt)', 'Video (optional)'] },
      summary: { title: 'Summary & chapters', desc: 'Summarize the content and generate timestamped chapters from the subtitle. Requires Ollama.', btn: 'Summarize', rows: ['Subtitle (.srt)'] },
      hardsub: { title: 'Burn in subtitles', desc: 'Permanently render the subtitles onto the video image.', btn: 'Burn in', rows: ['Video', 'Subtitle (.srt)'] },
      clean_audio: { title: 'Clean audio', desc: 'Reduce background noise and enhance the voice with FFmpeg.', btn: 'Clean', rows: ['Video or audio'] },
    },
    demo: ['[*] Analyzing input…', '[*] Extracting audio (ffmpeg)…', '[*] Processing block 1/1523…', '[*] Processing block 1523/1523…', '[✔] Task completed.']
  }
};

const TABS = {
  translate: { icon: 'translate', engine: true, rows: [{ v: 'path', dir: false }] },
  sync: { icon: 'waveform', rows: [{ v: 'vid' }, { v: 'sub' }] },
  whisper: { icon: 'microphone', rows: [{ v: 'src', dir: true }] },
  mux: { icon: 'stack', rows: [{ v: 'vid' }, { v: 'sub' }] },
  cleaner: { icon: 'broom', rows: [{ v: 'file' }] },
  dubbing: { icon: 'dub', voice: true, rows: [{ v: 'srt' }, { v: 'vid' }] },
  summary: { icon: 'article', engine: true, rows: [{ v: 'srt' }] },
  hardsub: { icon: 'monitor', rows: [{ v: 'vid' }, { v: 'sub' }] },
  clean_audio: { icon: 'sparkle', rows: [{ v: 'vid' }] },
};
const ORDER = ['translate', 'sync', 'whisper', 'mux', 'cleaner', 'dubbing', 'summary', 'hardsub', 'clean_audio'];

let lang = localStorage.getItem('subsforge_lang') || 'es';
let active = 'translate';
let engine = 'google';
let models = ['google'];
const paths = {};
let running = false;   // hay una tarea en curso
let taskErr = false;   // se detectó [ERROR] en la tarea actual

const VOICES = [
  { group: 'Español', items: [
      { id: 'es-ES-AlvaroNeural', label: 'España · Álvaro (H)' },
      { id: 'es-ES-ElviraNeural', label: 'España · Elvira (M)' },
      { id: 'es-MX-JorgeNeural', label: 'México · Jorge (H)' },
      { id: 'es-MX-DaliaNeural', label: 'México · Dalia (M)' }
    ] },
  { group: 'English', items: [
      { id: 'en-US-GuyNeural', label: 'US · Guy (M)' },
      { id: 'en-US-JennyNeural', label: 'US · Jenny (F)' },
      { id: 'en-GB-RyanNeural', label: 'UK · Ryan (M)' },
      { id: 'en-GB-SoniaNeural', label: 'UK · Sonia (F)' }
    ] }
];
let voice = 'es-ES-AlvaroNeural';
function voiceLabel(id) { for (const g of VOICES) { for (const v of g.items) { if (v.id === id) return v.label; } } return id; }
function L() { return I18N[lang]; }

function renderNav() {
  const nav = document.getElementById('nav');
  if (!nav) return;
  nav.innerHTML = '';
  ORDER.forEach(id => {
    const el = document.createElement('div');
    el.className = 'nav-item' + (id === active ? ' active' : '');
    el.innerHTML = svg(TABS[id].icon) + `<span class="lbl">${L().nav[id]}</span>`;
    el.title = L().nav[id];
    el.onclick = () => { active = id; renderNav(); renderContent(); };
    nav.appendChild(el);
  });
}

function fieldHtml(row, i) {
  const tl = L().tabs[active].rows[i];
  const val = (paths[active] && paths[active][row.v]) || '';
  const ph = row.dir ? L().fileordir : L().none;
  const lab = tl ? `<div class="flabel">${tl}</div>` : '';
  
  const browseBtn = row.dir
    ? `<button class="btn-browse" data-pick="${row.v}" data-dir="0">${svg('file')} ${L().file}</button>
       <button class="btn-browse" data-pick="${row.v}" data-dir="1">${svg('folder')} ${L().folder}</button>`
    : `<button class="btn-browse" data-pick="${row.v}" data-dir="0">${svg('file')} ${L().file}</button>`;
    
  return `<div class="field-row">${lab}
    <div class="field ${val ? 'set' : ''}" data-pickfield="${row.v}" title="${esc(val)}">${val ? esc(val) : ph}</div>
    ${browseBtn}
  </div>`;
}

function engineRow() {
  const opts = models.map(m => `<div class="opt ${m === engine ? 'sel' : ''}" data-opt="${esc(m)}">${esc(m)}<span class="chk">${svg('check')}</span></div>`).join('');
  const help = models.length > 1 ? '' : `<button class="cta warn" id="ollama-help" style="margin-left: 10px">${svg('info')} ${L().install}</button>`;
  
  return `<div class="field-row" style="margin-top:16px">
    <div class="flabel">${L().engine}</div>
    <div class="select">
      <div class="sel-btn" id="sel-btn"><span class="val">${esc(engine)}</span>${svg('caret')}</div>
      <div class="sel-menu" id="sel-menu">${opts}</div>
    </div>
    ${help}
  </div>`;
}

function voiceRow() {
  const opts = VOICES.map(g =>
    `<div class="sel-group">${esc(g.group)}</div>` +
    g.items.map(v => `<div class="opt ${v.id === voice ? 'sel' : ''}" data-vopt="${esc(v.id)}">${esc(v.label)}<span class="chk">${svg('check')}</span></div>`).join('')
  ).join('');
  
  return `<div class="field-row" style="margin-top:16px">
    <div class="flabel">${L().voice}</div>
    <div class="select">
      <div class="sel-btn" id="voice-btn"><span class="val">${esc(voiceLabel(voice))}</span>${svg('caret')}</div>
      <div class="sel-menu" id="voice-menu">${opts}</div>
    </div>
  </div>`;
}

function renderContent() {
  const t = TABS[active], ti = L().tabs[active];
  const c = document.getElementById('tab-content-container');
  if (!c) return;
  
  const rows = t.rows.map((r, i) => fieldHtml(r, i)).join('');
  
  c.innerHTML = `
    <h1>${ti.title}</h1>
    <div class="desc">${ti.desc}</div>
    <div class="card" style="margin-top:20px;">
      ${rows}
      ${t.engine ? engineRow() : ''}
      ${t.voice ? voiceRow() : ''}
    </div>
    <div class="run-row">
      <button class="cta ${t.danger ? 'danger' : ''}" id="btn-run">${ti.btn}</button>
    </div>
  `;
  
  // Handlers for dynamic content
  c.querySelectorAll('[data-pick]').forEach(b => b.onclick = () => pick(b.getAttribute('data-pick'), b.getAttribute('data-dir') === '1'));
  c.querySelectorAll('[data-pickfield]').forEach(f => f.onclick = () => pick(f.getAttribute('data-pickfield'), false));
  
  const sb = document.getElementById('sel-btn'), sm = document.getElementById('sel-menu');
  if (sb) {
    sb.onclick = e => { e.stopPropagation(); sm.classList.toggle('open'); };
    c.querySelectorAll('[data-opt]').forEach(o => o.onclick = () => { engine = o.getAttribute('data-opt'); renderContent(); });
  }
  
  const vb = document.getElementById('voice-btn'), vm = document.getElementById('voice-menu');
  if (vb) {
    vb.onclick = e => { e.stopPropagation(); vm.classList.toggle('open'); };
    c.querySelectorAll('[data-vopt]').forEach(o => o.onclick = () => { voice = o.getAttribute('data-vopt'); renderContent(); });
  }
  
  const oh = document.getElementById('ollama-help');
  if (oh) oh.onclick = ollamaGuide;
  
  document.getElementById('btn-run').onclick = runTab;
}

document.addEventListener('click', () => {
  ['sel-menu', 'voice-menu'].forEach(id => {
    const m = document.getElementById(id);
    if (m) m.classList.remove('open');
  });
});

async function pick(v, dir) {
  const p = dir ? await BRIDGE.pickFolder() : await BRIDGE.pickFile();
  if (!p) return;
  paths[active] = paths[active] || {};
  paths[active][v] = p;
  renderContent();
}

function termAppend(text) {
  const t = document.getElementById('logs');
  if (!t) return;
  if (running && /\[ERROR\]/i.test(text)) taskErr = true;
  t.append(document.createTextNode(text));
  t.scrollTop = t.scrollHeight;
  const term = document.getElementById('console-drawer');
  if (term && term.classList.contains('collapsed')) {
    term.classList.add('has-unread');
  }
}
window.termAppend = termAppend;

// Aviso de finalización: un único evento (term-done) dispara esto. Sin bucles
// ni sondeos -> coste de rendimiento nulo. Muestra un toast y restaura el botón.
function showToast(ok) {
  let el = document.getElementById('toast');
  if (!el) {
    el = document.createElement('div');
    el.id = 'toast';
    document.body.appendChild(el);
  }
  el.className = 'toast ' + (ok ? 'ok' : 'err');
  el.innerHTML = svg(ok ? 'check' : 'info') + '<span>' + (ok ? L().done_ok : L().done_err) + '</span>';
  void el.offsetWidth;            // reflow para reiniciar la transición
  el.classList.add('show');
  clearTimeout(el._t);
  el._t = setTimeout(() => el.classList.remove('show'), 3800);
}

function taskDone(payload) {
  if (!running) return;          // ignora eventos duplicados o fuera de tarea
  running = false;
  let code = 0;
  try { if (payload && typeof payload === 'object' && payload.code != null) code = payload.code; } catch (_) {}
  const ok = (code === 0) && !taskErr;

  const btn = document.getElementById('btn-run');
  if (btn) {
    btn.disabled = false;
    btn.classList.remove('running');
    if (btn.dataset.label) { btn.textContent = btn.dataset.label; delete btn.dataset.label; }
  }
  termAppend((ok ? '\n[✔] ' + L().done_ok : '\n[✗] ' + L().done_err) + '\n');
  showToast(ok);

  const term = document.getElementById('console-drawer');
  if (term && term.classList.contains('collapsed')) term.classList.add('has-unread');
}
window.taskDone = taskDone;

function termReset() {
  const t = document.getElementById('logs');
  if (t) t.innerHTML = `<span class="prompt">$ </span>${L().running}\n`;
}

// Validación de tipo de archivo por herramienta: evita crashes crípticos
// (p. ej. dar un vídeo al Traductor, que espera un .srt). key = campo a revisar.
const REQUIRE = {
  translate: { key: 'path', exts: ['.srt'] },
  summary:   { key: 'srt',  exts: ['.srt'] },
  dubbing:   { key: 'srt',  exts: ['.srt'] },
  cleaner:   { key: 'file', exts: ['.ass'] },
};
function openConsole() {
  const term = document.getElementById('console-drawer');
  if (term && term.classList.contains('collapsed')) {
    term.classList.remove('collapsed');
    term.classList.remove('has-unread');
  }
}
function validateInput() {
  const req = REQUIRE[active];
  if (!req) return true;
  const val = (paths[active] && paths[active][req.key]) || '';
  if (!val) return true; // sin archivo: el núcleo ya avisa de que faltan
  const low = val.toLowerCase();
  if (req.exts.some(e => low.endsWith(e))) return true;
  const es = lang === 'es';
  const need = req.exts.join(' / ');
  let msg = es
    ? `[!] Esta herramienta necesita un archivo ${need}. Seleccionaste: ${val.split(/[\\/]/).pop()}`
    : `[!] This tool needs a ${need} file. You selected: ${val.split(/[\\/]/).pop()}`;
  if (active === 'translate' && req.exts.includes('.srt')) {
    msg += es
      ? '\n[i] Si el vídeo no tiene subtítulos, genera el .srt primero con "Transcripción Whisper".'
      : '\n[i] If the video has no subtitles, generate the .srt first with "Whisper Transcription".';
  }
  return msg;
}

async function runTab() {
  const p = Object.assign({}, paths[active] || {});
  p.engine = engine;
  if (TABS[active].voice) p.voice = voice;

  termReset();
  openConsole();

  const check = validateInput();
  if (check !== true) {
    termAppend(check + '\n');
    return;
  }

  // Estado "en ejecución": botón bloqueado con spinner hasta term-done.
  running = true;
  taskErr = false;
  const btn = document.getElementById('btn-run');
  if (btn) {
    btn.dataset.label = btn.textContent;
    btn.textContent = L().running_btn;
    btn.classList.add('running');
    btn.disabled = true;
  }

  BRIDGE.run(active, p);
}

function showModal(title, html) {
  let ov = document.getElementById('modal-ov');
  if (!ov) {
    ov = document.createElement('div');
    ov.id = 'modal-ov';
    ov.className = 'modal-ov';
    ov.innerHTML = `
      <div class="modal" role="dialog" aria-modal="true">
        <div class="modal-h">
          <span class="modal-t"></span>
          <button class="modal-x" aria-label="cerrar">&times;</button>
        </div>
        <div class="modal-b"></div>
      </div>
    `;
    document.body.appendChild(ov);
    ov.addEventListener('click', e => { if (e.target === ov) hideModal(); });
    ov.querySelector('.modal-x').onclick = hideModal;
    document.addEventListener('keydown', e => { if (e.key === 'Escape') hideModal(); });
  }
  ov.querySelector('.modal-t').textContent = title;
  ov.querySelector('.modal-b').innerHTML = html;
  ov.classList.add('open');
}

function hideModal() {
  const ov = document.getElementById('modal-ov');
  if (ov) ov.classList.remove('open');
}

function ollamaGuide() {
  const es = lang === 'es';
  const body = es
    ? '<p>Para traducir y resumir con IA local necesitas <b>Ollama</b>, gratuito y de código abierto.</p><ol><li>Descarga Ollama e instálalo.</li><li>Abre una terminal y ejecuta <code>ollama run llama3</code> para descargar el modelo.</li><li>Reinicia SubsForge: el modelo aparecerá en el menú <b>Motor IA</b>.</li></ol><div class="modal-actions"><button class="cta" data-ext="https://ollama.com">Abrir ollama.com</button></div>'
    : '<p>To translate and summarize with local AI you need <b>Ollama</b>, free and open source.</p><ol><li>Download and install Ollama.</li><li>Open a terminal and run <code>ollama run llama3</code> to pull the model.</li><li>Restart SubsForge: the model appears in the <b>AI Engine</b> menu.</li></ol><div class="modal-actions"><button class="cta" data-ext="https://ollama.com">Open ollama.com</button></div>';
  showModal(es ? 'Instalar IA local (Ollama)' : 'Install local AI (Ollama)', body);
  document.querySelectorAll('#modal-ov [data-ext]').forEach(el => el.onclick = e => { e.preventDefault(); BRIDGE.openUrl(el.getAttribute('data-ext')); });
}

function applyStatic() {
  const t = L();
  const setEl = (id, text) => { const e = document.getElementById(id); if (e) e.textContent = text; };
  setEl('term-title', t.term_title);
  
  const lbtn = document.getElementById('btn-lang');
  if (lbtn) lbtn.textContent = t.langLabel;
  
  document.querySelectorAll('[data-i18n="sec_tools"]').forEach(el => el.textContent = t.tools);
}

function toggleLang() {
  lang = lang === 'es' ? 'en' : 'es';
  localStorage.setItem('subsforge_lang', lang);
  applyStatic();
  renderNav();
  renderContent();
}

const ICON_SUN = `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="5" fill="currentColor"/><path style="fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round" d="M12 1v3M12 20v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M1 12h3M20 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/></svg>`;
const ICON_MOON = `<svg viewBox="0 0 24 24"><path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z" fill="currentColor"/></svg>`;

function applyTheme(theme) {
  if (theme === 'light') document.documentElement.setAttribute('data-theme', 'light');
  else document.documentElement.removeAttribute('data-theme');
  const btn = document.getElementById('btn-theme');
  if (btn) btn.innerHTML = theme === 'light' ? ICON_MOON : ICON_SUN;
}

function toggleTheme() {
  const current = localStorage.getItem('subsforge_theme') || 'dark';
  const next = current === 'light' ? 'dark' : 'light';
  localStorage.setItem('subsforge_theme', next);
  applyTheme(next);
}

function initUI() {
  // Configuración de Sidebar (persistencia en localStorage)
  const sidebar = document.querySelector('.sidebar');
  const btnToggleSidebar = document.getElementById('btn-toggle-sidebar');
  
  if (sidebar && btnToggleSidebar) {
    const isCollapsed = localStorage.getItem('subsforge_sidebar') === 'true';
    if (isCollapsed) {
      sidebar.classList.add('collapsed');
      btnToggleSidebar.classList.add('collapsed');
    }
    
    btnToggleSidebar.onclick = () => {
      sidebar.classList.toggle('collapsed');
      const collapsed = sidebar.classList.contains('collapsed');
      btnToggleSidebar.classList.toggle('collapsed', collapsed);
      localStorage.setItem('subsforge_sidebar', collapsed.toString());
    };
  }
  
  // Tema
  applyTheme(localStorage.getItem('subsforge_theme') || 'dark');
  document.getElementById('btn-theme').onclick = toggleTheme;

  // Controles de ventana y otros
  document.getElementById('btn-lang').onclick = toggleLang;
  document.getElementById('link-portfolio').onclick = () => BRIDGE.openUrl('https://ivanjonasfc.dev');
  document.getElementById('link-github').onclick = () => BRIDGE.openUrl('https://github.com/IvanjonasFC');
  
  const winMin = document.getElementById('win-min');
  if(winMin) winMin.onclick = () => BRIDGE.winMin();
  const winMax = document.getElementById('win-max');
  if(winMax) winMax.onclick = () => BRIDGE.winMax();
  const winClose = document.getElementById('win-close');
  if(winClose) winClose.onclick = () => BRIDGE.winClose();
  
  // La consola colapsable la gestiona el bloque de arrastre (más abajo), que
  // distingue clic de arrastre. No añadimos aquí otro onclick para no
  // provocar un doble toggle que dejaba la consola sin responder.

  // Cargar modelos y renderizar
  BRIDGE.getOllama().then(m => {
    if (m && m.length) {
      models = ['google', ...m.map(x => 'ollama:' + x)];
      renderContent();
    }
  });

  applyStatic();
  renderNav();
  renderContent();
}

// Inicialización cuando carga el DOM
document.addEventListener('DOMContentLoaded', initUI);

  // --- Floating Console Logic ---
  const term = document.getElementById('console-drawer');
  const termHead = document.getElementById('console-toggle');
  if (term && termHead) {
    let isDragging = false;
    let didDrag = false;
    let startX, startY, initialX = 0, initialY = 0;

    termHead.addEventListener('pointerdown', (e) => {
      if (term.classList.contains('collapsed')) return;
      isDragging = true;
      didDrag = false;
      startX = e.clientX;
      startY = e.clientY;
      term.style.transition = 'none';
      termHead.setPointerCapture(e.pointerId);
    });

    termHead.addEventListener('pointermove', (e) => {
      if (!isDragging) return;
      const dx = e.clientX - startX;
      const dy = e.clientY - startY;
      if (Math.abs(dx) > 3 || Math.abs(dy) > 3) didDrag = true;
      if (didDrag) {
        e.preventDefault();
        term.style.transform = `translate3d(${initialX + dx}px, ${initialY + dy}px, 0)`;
      }
    });

    termHead.addEventListener('pointerup', (e) => {
      if (isDragging) {
        isDragging = false;
        termHead.releasePointerCapture(e.pointerId);
        term.style.transition = '';
        if (didDrag) {
          initialX += e.clientX - startX;
          initialY += e.clientY - startY;
        }
      }
    });

    termHead.addEventListener('click', (e) => {
      if (didDrag) {
        e.preventDefault();
        e.stopPropagation();
        return;
      }
      term.classList.toggle('collapsed');
      if (!term.classList.contains('collapsed')) {
        term.classList.remove('has-unread');
      }
    });
  }



// Background Blob Pointer Tracking
(function() {
  const blob = document.getElementById('blob');
  if (blob) {
    let _bx = innerWidth * 0.6, _by = innerHeight * 0.4, _bq = false;
    function paintBlob() {
      _bq = false;
      blob.style.transform = "translate3d(" + _bx + "px, " + _by + "px, 0) translate(-50%, -50%)";
    }
    window.addEventListener('pointermove', (e) => {
      _bx = e.clientX; _by = e.clientY;
      if (!_bq) { _bq = true; requestAnimationFrame(paintBlob); }
    }, { passive: true });
    paintBlob();
  }
})();

