// audit-frames.mjs — Mide contenedores de imagen ("recuadros") por página y viewport
import puppeteer from "puppeteer";

const BASE = "https://plomeroculiacanpro.mx";
const PAGES = [
  "/", "/servicios/plomero/cerca-de-mi/", "/servicios/plomero/24-7/",
  "/servicios/plomero/a-domicilio/", "/servicios/plomero/precios/", "/contacto/"
];

// Ajusta/añade selectores de tus recuadros aquí (clases de cards, hero, banners, galerías)
const FRAME_SELECTORS = [
  ".hero", ".hero-media", ".banner", ".section-media",
  ".service-card", ".service-media",
  ".card", ".card-media", ".card .media",
  ".gallery", ".gallery-item", ".grid .card", "[data-media]"
];

const TITLE_SELECTORS = ["h1","h2","h3",".card-title",".section-title",".hero-title"];

const VIEWPORTS = [
  {name:"mobile",  width:390,  height:844,  dpr:3},
  {name:"tablet",  width:768,  height:1024, dpr:2},
  {name:"desktop", width:1366, height:900,  dpr:1.5},
];

function gcd(a,b){ return b ? gcd(b, a % b) : a; }
function ratioStr(w, h){
  w = Math.round(w); h = Math.round(h);
  if (w<=0 || h<=0) return "";
  const g = gcd(w,h);
  return `${w/g}:${h/g}`;
}

async function measurePage(page, url, vp){
  await page.setViewport({width:vp.width, height:vp.height, deviceScaleFactor:vp.dpr});
  await page.goto(BASE+url, {waitUntil:"networkidle2", timeout:60000});

  return await page.evaluate(({FRAME_SELECTORS, TITLE_SELECTORS, vp})=>{
    const out=[];
    const sels = Array.from(new Set(FRAME_SELECTORS));
    const nodes = new Set();
    const isVisible = el=>{
      const r = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return r.width>30 && r.height>30 && style.visibility!=="hidden" && style.display!=="none";
    };

    function nearestTitle(el){
      // Busca título en ancestros o hermanos cercanos
      let n = el;
      for(let i=0; i<6 && n; i++, n=n.parentElement){
        for(const s of TITLE_SELECTORS){
          const cand = n.querySelector(s);
          if (cand && cand.textContent?.trim()) return cand.textContent.trim().replace(/\s+/g," ");
        }
      }
      // fallback: título del documento
      const h1 = document.querySelector("h1");
      return h1?.textContent?.trim() || "";
    }

    sels.forEach(sel=>{ document.querySelectorAll(sel).forEach(n=>nodes.add(n)); });

    nodes.forEach(el=>{
      if(!isVisible(el)) return;
      const r = el.getBoundingClientRect();
      const w = Math.round(r.width);
      const h = Math.round(r.height);
      const cl = (el.className||"").toString().replace(/\s+/g," ").trim();
      const id = el.id || "";
      const selectorHit = FRAME_SELECTORS.find(s=>el.matches?.(s)) || "";

      const oneX = `${w}x${h}`;
      const twoX = `${w*2}x${h*2}`;
      const ratio = (w>0 && h>0) ? (()=>{ const g=(a,b)=>b?g(b,a%b):a; const G=g(w,h); return `${w/G}:${h/G}`; })() : "";

      // safe area sugerida (márgenes para texto/sellos en la imagen)
      const safe = Math.round(Math.min(w,h) * 0.08); // 8% del lado menor

      out.push({
        page: url,
        viewport: vp.name,
        selector: selectorHit || "custom",
        id,
        class: cl,
        title_context: nearestTitle(el),
        rendered_w: w,
        rendered_h: h,
        aspect_ratio: ratio,
        recommended_export_1x: oneX,
        recommended_export_2x: twoX,
        recommended_safe_margin_px: safe
      });
    });
    return out;
  }, {FRAME_SELECTORS, TITLE_SELECTORS, vp});
}

(async ()=>{
  const browser = await puppeteer.launch({headless:"new", args:["--no-sandbox"]});
  const page = await browser.newPage();

  // CSV header
  console.log([
    "page","viewport","selector","id","class","title_context",
    "rendered_w","rendered_h","aspect_ratio",
    "recommended_export_1x","recommended_export_2x","recommended_safe_margin_px"
  ].join(","));

  for(const vp of VIEWPORTS){
    for(const url of PAGES){
      const rows = await measurePage(page, url, vp);
      for(const r of rows){
        const row = [
          r.page, r.viewport,
          `"${r.selector}"`,
          `"${(r.id||"").replace(/"/g,'""')}"`,
          `"${(r.class||"").replace(/"/g,'""')}"`,
          `"${(r.title_context||"").replace(/"/g,'""')}"`,
          r.rendered_w, r.rendered_h, r.aspect_ratio,
          r.recommended_export_1x, r.recommended_export_2x, r.recommended_safe_margin_px
        ].join(",");
        console.log(row);
      }
    }
  }
  await browser.close();
})();