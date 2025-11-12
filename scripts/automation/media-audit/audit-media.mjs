// audit-media.mjs
import puppeteer from "puppeteer";

const BASE = "https://plomeroculiacanpro.mx";
const PAGES = [
  "/", "/servicios/plomero/cerca-de-mi/", "/servicios/plomero/24-7/",
  "/servicios/plomero/a-domicilio/", "/servicios/plomero/precios/", "/contacto/"
];

// Selectores típicos de imágenes y "recuadros" (ajusta si usas otros)
const IMG_SELECTORS = [
  "img",                           // todas las <img>
  "[style*='background-image']",   // divs con bg-image inline
  ".card img, .card-picture img, .service-card img",
  ".hero img, .banner img, .gallery img",
];

// Títulos cercanos de contexto
const TITLE_SELECTORS = ["h1","h2","h3",".card-title",".section-title"];

const VIEWPORTS = [
  {name:"mobile", width:390, height:844, dpr:3},
  {name:"tablet", width:768, height:1024, dpr:2},
  {name:"desktop", width:1366, height:900, dpr:1.5}
];

function sanitize(s){ return (s||"").replace(/\s+/g," ").trim(); }

function closestTitle(el){
  // Busca el heading más cercano hacia arriba en el DOM
  let n = el;
  while(n && n.parentElement){
    for(const sel of TITLE_SELECTORS){
      const t = n.parentElement.querySelector(sel);
      if(t && t.textContent) return sanitize(t.textContent);
    }
    n = n.parentElement;
  }
  return "";
}

async function auditPage(page, url, vp){
  await page.emulateVisionDeficiency(null);
  await page.setViewport({width:vp.width, height:vp.height, deviceScaleFactor:vp.dpr});
  await page.goto(BASE+url, {waitUntil:"networkidle2", timeout:60000});

  return await page.evaluate(({IMG_SELECTORS, TITLE_SELECTORS, vpName})=>{
    const out=[];
    const sels = Array.from(new Set(IMG_SELECTORS));
    const nodes = new Set();

    // Recolecta nodos por selectores
    sels.forEach(sel=>{
      document.querySelectorAll(sel).forEach(n=>nodes.add(n));
    });

    function getBgUrl(el){
      const bg = getComputedStyle(el).backgroundImage || "";
      const m = bg.match(/url\\((['"]?)(.*?)\\1\\)/i);
      return m ? m[2] : "";
    }

    function nearestTitle(el){
      // heading en el mismo bloque/ancestro
      let n=el;
      while(n && n.parentElement){
        const candidate = n.parentElement.querySelector("h1,h2,h3,.card-title,.section-title");
        if(candidate) return candidate.textContent.trim();
        n = n.parentElement;
      }
      return "";
    }

    nodes.forEach(el=>{
      const rect = el.getBoundingClientRect();
      if(rect.width<8 || rect.height<8) return; // ignora iconos
      const isImg = el.tagName?.toLowerCase()==="img";
      const src = isImg ? (el.currentSrc || el.src || "") : getBgUrl(el);
      const natW = isImg ? (el.naturalWidth||0) : 0;
      const natH = isImg ? (el.naturalHeight||0) : 0;
      const cls = (el.className || "").toString().trim().slice(0,120);
      const titleNear = nearestTitle(el);

      const w = Math.round(rect.width);
      const h = Math.round(rect.height);
      const rec1x = `${w}x${h}`;
      const rec2x = `${w*2}x${h*2}`;

      out.push({
        page: url,
        viewport: vpName,
        tag: isImg ? "img" : "bg",
        class: cls,
        src,
        rendered_w: w,
        rendered_h: h,
        natural_w: natW,
        natural_h: natH,
        title_context: titleNear,
        recommended_export_1x: rec1x,
        recommended_export_2x: rec2x
      });
    });
    return out;
  }, {IMG_SELECTORS,TITLE_SELECTORS, vpName:vp.name});
}

(async ()=>{
  const browser = await puppeteer.launch({headless:"new", args:["--no-sandbox"]});
  const page = await browser.newPage();

  // CSV header
  console.log([
    "page","viewport","tag","class","src",
    "rendered_w","rendered_h","natural_w","natural_h",
    "title_context","recommended_export_1x","recommended_export_2x"
  ].join(","));

  for(const vp of VIEWPORTS){
    for(const url of PAGES){
      const rows = await auditPage(page, url, vp);
      rows.forEach(r=>{
        const row = [
          r.page, r.viewport, r.tag,
          `"${r.class.replace(/"/g,'""')}"`,
          `"${(r.src||"").replace(/"/g,'""')}"`,
          r.rendered_w, r.rendered_h, r.natural_w, r.natural_h,
          `"${(r.title_context||"").replace(/"/g,'""')}"`,
          r.recommended_export_1x, r.recommended_export_2x
        ].join(",");
        console.log(row);
      });
    }
  }
  await browser.close();
})();