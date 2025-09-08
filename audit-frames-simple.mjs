// audit-frames-simple.mjs — Análisis estático de CSS para estimar contenedores
import https from 'https';
import { readFileSync } from 'fs';

const BASE = "https://plomeroculiacanpro.mx";
const PAGES = [
  "/", "/servicios/plomero/cerca-de-mi/", "/servicios/plomero/24-7/",
  "/servicios/plomero/a-domicilio/", "/servicios/plomero/precios/", "/contacto/"
];

// Selectores comunes de contenedores de media/imágenes
const FRAME_SELECTORS = [
  ".hero", ".hero-media", ".banner", ".section-media",
  ".service-card", ".service-media",
  ".card", ".card-media", ".card .media", ".media-box",
  ".gallery", ".gallery-item", ".grid .card", "[data-media]"
];

const VIEWPORTS = [
  {name:"mobile",  width:390,  height:844},
  {name:"tablet",  width:768,  height:1024},
  {name:"desktop", width:1366, height:900},
];

function fetchPage(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

function gcd(a,b){ return b ? gcd(b, a % b) : a; }

function analyzeHTML(html, page) {
  const containers = [];
  
  // Extract CSS classes and IDs used in the page
  const classRegex = /class\s*=\s*["']([^"']+)["']/gi;
  const idRegex = /id\s*=\s*["']([^"']+)["']/gi;
  
  let match;
  const foundClasses = new Set();
  const foundIds = new Set();
  
  while ((match = classRegex.exec(html)) !== null) {
    match[1].split(/\s+/).forEach(cls => foundClasses.add('.' + cls));
  }
  
  while ((match = idRegex.exec(html)) !== null) {
    foundIds.add('#' + match[1]);
  }
  
  // Check which frame selectors are actually used in the HTML
  const usedSelectors = FRAME_SELECTORS.filter(selector => {
    if (selector.startsWith('.')) {
      return foundClasses.has(selector);
    } else if (selector.startsWith('#')) {
      return foundIds.has(selector);
    } else {
      return html.includes('<' + selector.replace(/[\[\]]/g, ''));
    }
  });

  // Extract context titles near containers
  const titleRegex = /<(h[1-3]|[^>]*class\s*=\s*["'][^"']*(?:title|heading)[^"']*["'][^>]*)>([^<]+)<\/[^>]*>/gi;
  const titles = [];
  while ((match = titleRegex.exec(html)) !== null) {
    titles.push(match[2].trim());
  }

  // Generate estimates for different viewports
  for (const vp of VIEWPORTS) {
    for (const selector of usedSelectors) {
      let estimatedDimensions;
      
      // Estimate dimensions based on viewport and selector type
      if (selector.includes('hero')) {
        estimatedDimensions = {
          mobile: {w: 390, h: 200},
          tablet: {w: 768, h: 300}, 
          desktop: {w: 1366, h: 400}
        };
      } else if (selector.includes('card') || selector.includes('service')) {
        estimatedDimensions = {
          mobile: {w: 350, h: 200},
          tablet: {w: 350, h: 200},
          desktop: {w: 420, h: 280}
        };
      } else if (selector.includes('media') || selector.includes('gallery')) {
        estimatedDimensions = {
          mobile: {w: 300, h: 200},
          tablet: {w: 400, h: 300},
          desktop: {w: 500, h: 350}
        };
      } else {
        // Default container size
        estimatedDimensions = {
          mobile: {w: 320, h: 180},
          tablet: {w: 400, h: 225},
          desktop: {w: 500, h: 280}
        };
      }
      
      const dims = estimatedDimensions[vp.name] || estimatedDimensions.desktop;
      const ratio = gcd(dims.w, dims.h);
      const aspectRatio = `${dims.w/ratio}:${dims.h/ratio}`;
      const safeMargin = Math.round(Math.min(dims.w, dims.h) * 0.08);
      
      containers.push({
        page,
        viewport: vp.name,
        selector: selector,
        class: selector.replace(/^\./, ''),
        title_context: titles[0] || 'No title found',
        estimated_w: dims.w,
        estimated_h: dims.h,
        aspect_ratio: aspectRatio,
        recommended_export_1x: `${dims.w}x${dims.h}`,
        recommended_export_2x: `${dims.w*2}x${dims.h*2}`,
        recommended_safe_margin_px: safeMargin,
        note: 'Estimated from static analysis'
      });
    }
  }
  
  return containers;
}

(async () => {
  console.log([
    "page","viewport","selector","class","title_context",
    "estimated_w","estimated_h","aspect_ratio",
    "recommended_export_1x","recommended_export_2x","recommended_safe_margin_px","note"
  ].join(","));
  
  for (const page of PAGES) {
    try {
      console.error(`Analyzing ${BASE}${page}...`);
      const html = await fetchPage(BASE + page);
      const containers = analyzeHTML(html, page);
      
      containers.forEach(container => {
        const row = [
          container.page,
          container.viewport,
          `"${container.selector}"`,
          `"${container.class}"`,
          `"${container.title_context.replace(/"/g, '""')}"`,
          container.estimated_w,
          container.estimated_h,
          container.aspect_ratio,
          container.recommended_export_1x,
          container.recommended_export_2x,
          container.recommended_safe_margin_px,
          `"${container.note}"`
        ].join(',');
        console.log(row);
      });
    } catch (err) {
      console.error(`Error analyzing ${page}: ${err.message}`);
    }
  }
})();