// audit-media-simple.mjs - Simplified version without puppeteer
import https from 'https';

const BASE = "https://plomeroculiacanpro.mx";
const PAGES = [
  "/", "/servicios/plomero/cerca-de-mi/", "/servicios/plomero/24-7/",
  "/servicios/plomero/a-domicilio/", "/servicios/plomero/precios/", "/contacto/"
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

function extractImages(html, page) {
  const imgRegex = /<img[^>]+src\s*=\s*["']([^"']+)["'][^>]*>/gi;
  const images = [];
  let match;
  
  while ((match = imgRegex.exec(html)) !== null) {
    const imgTag = match[0];
    const src = match[1];
    
    // Extract width/height attributes if present
    const widthMatch = imgTag.match(/width\s*=\s*["']?(\d+)["']?/i);
    const heightMatch = imgTag.match(/height\s*=\s*["']?(\d+)["']?/i);
    const altMatch = imgTag.match(/alt\s*=\s*["']([^"']*)["']/i);
    
    const width = widthMatch ? parseInt(widthMatch[1]) : 0;
    const height = heightMatch ? parseInt(heightMatch[1]) : 0;
    const alt = altMatch ? altMatch[1] : '';
    
    images.push({
      page,
      src: src.startsWith('http') ? src : BASE + (src.startsWith('/') ? src : '/' + src),
      declared_width: width,
      declared_height: height,
      alt_text: alt,
      full_tag: imgTag.slice(0, 100) + '...'
    });
  }
  
  return images;
}

(async () => {
  console.log("page,src,declared_width,declared_height,alt_text,full_tag");
  
  for (const page of PAGES) {
    try {
      console.error(`Fetching ${BASE}${page}...`);
      const html = await fetchPage(BASE + page);
      const images = extractImages(html, page);
      
      images.forEach(img => {
        const row = [
          img.page,
          `"${img.src}"`,
          img.declared_width,
          img.declared_height, 
          `"${img.alt_text.replace(/"/g, '""')}"`,
          `"${img.full_tag.replace(/"/g, '""')}"`
        ].join(',');
        console.log(row);
      });
    } catch (err) {
      console.error(`Error fetching ${page}: ${err.message}`);
    }
  }
})();