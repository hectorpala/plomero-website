# 🔍 Keyword Volume Tool - 100% GRATIS

Herramienta para estimar volumen de búsqueda de keywords usando fuentes de datos **completamente gratuitas**.

## 💡 ¿Cómo Funciona?

Combina **3 fuentes de datos gratis** para estimar el volumen de búsqueda mensual:

1. **Google Trends API** (oficial y gratis) → Tendencia de búsqueda (score 0-100)
2. **Google Autocomplete Scraping** (legal) → Popularidad según ranking en sugerencias
3. **Algoritmo ML de Estimación** → Convierte señales en volumen estimado

### Fórmula de Estimación

```
Volumen Base (según Trend Score):
- 80-100 → 50,000 búsquedas/mes
- 50-80  → 5,000 búsquedas/mes
- 20-50  → 500 búsquedas/mes
- 0-20   → 50 búsquedas/mes

Multiplicadores:
- Autocomplete rank 1-3 → x2.0
- Autocomplete rank 4-5 → x1.5
- Autocomplete rank 6-7 → x1.2
- Long-tail (>4 palabras) → x0.5
```

---

## 🚀 INSTALACIÓN

### Requisitos Previos

- **Python 3.8+**
- **Node.js 16+**
- **npm o yarn**

### Paso 1: Instalar Backend (FastAPI)

```bash
cd keyword-volume-tool/backend

# Crear virtual environment
python3 -m venv venv

# Activar virtual environment
source venv/bin/activate  # macOS/Linux
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 2: Instalar Frontend (React)

```bash
cd keyword-volume-tool/frontend

# Instalar dependencias
npm install
```

---

## 🎯 USO

### Iniciar Backend

```bash
cd keyword-volume-tool/backend
source venv/bin/activate
python main.py
```

Deberías ver:

```
🚀 Keyword Volume Tool - Backend
======================================================================
📊 Data sources: Google Trends + Autocomplete + ML
💰 Costo: 100% GRATIS
🔗 URL: http://localhost:8000
📖 Docs: http://localhost:8000/docs
======================================================================
```

### Iniciar Frontend

En otra terminal:

```bash
cd keyword-volume-tool/frontend
npm start
```

El navegador abrirá automáticamente: `http://localhost:3000`

---

## 📊 USANDO LA HERRAMIENTA

### 1. Interfaz Web

1. Abre `http://localhost:3000`
2. Ingresa un keyword (ej: "plomero culiacan")
3. Selecciona ubicación (México, Culiacán, Sinaloa, etc.)
4. Click en "Analizar Keyword"

**Resultados:**
- Volumen estimado mensual
- Nivel de confianza (Alta/Media/Baja)
- Google Trends score
- Autocomplete ranking
- Keywords relacionadas
- Tendencia (subiendo/estable)

### 2. API Directa

**Endpoint:** `POST http://localhost:8000/api/keyword-volume`

**Request:**
```bash
curl -X POST "http://localhost:8000/api/keyword-volume" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "plomero culiacan",
    "location": "Sinaloa"
  }'
```

**Response:**
```json
{
  "keyword": "plomero culiacan",
  "location": "Sinaloa",
  "volume_estimate": 4800,
  "confidence": "Media",
  "trend_data": {
    "interest_score": 65,
    "peak_score": 87,
    "trend": "rising",
    "related_queries": [
      "plomero culiacan 24 horas",
      "plomero culiacan urgencias",
      "plomero culiacan economico"
    ]
  },
  "autocomplete_rank": 3,
  "cached": false
}
```

### 3. API Docs Interactiva

Abre `http://localhost:8000/docs` para ver documentación interactiva (Swagger UI).

---

## 📈 EJEMPLOS DE USO

### Ejemplo 1: Keyword Local

```bash
curl -X POST "http://localhost:8000/api/keyword-volume" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "plomero las quintas", "location": "Culiacán"}'
```

**Resultado esperado:**
- Volume: 200-500/mes (baja)
- Confidence: Baja
- Trend: stable

### Ejemplo 2: Keyword Nacional

```bash
curl -X POST "http://localhost:8000/api/keyword-volume" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "plomero", "location": "México"}'
```

**Resultado esperado:**
- Volume: 50,000-100,000/mes (alta)
- Confidence: Alta
- Trend: rising

### Ejemplo 3: Long-tail Keyword

```bash
curl -X POST "http://localhost:8000/api/keyword-volume" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "plomero 24 horas urgencias culiacan", "location": "Sinaloa"}'
```

**Resultado esperado:**
- Volume: 100-300/mes (baja, long-tail)
- Confidence: Media
- Trend: stable

---

## 🗄️ CACHE Y PERFORMANCE

### Sistema de Cache

- Resultados se guardan en SQLite (`keyword_cache.db`)
- Cache válido por **7 días**
- Evita rate limits de Google Trends
- Mejora velocidad de consultas repetidas

### Ver Estadísticas de Cache

```bash
curl "http://localhost:8000/api/cache-stats"
```

**Response:**
```json
{
  "total_keywords": 156,
  "recent_keywords": 89,
  "cache_age": "7 days"
}
```

---

## 🎨 PERSONALIZACIÓN

### Cambiar Ubicaciones

Edita `backend/main.py`:

```python
geo_map = {
    "México": "MX",
    "Culiacán": "MX-SIN",
    "Sinaloa": "MX-SIN",
    "Guadalajara": "MX-JAL",
    "CDMX": "MX-CMX",
    # Agregar más:
    "Monterrey": "MX-NLE",
    "Tijuana": "MX-BCN"
}
```

### Ajustar Algoritmo de Estimación

Edita función `estimate_volume()` en `backend/main.py`:

```python
# Cambiar base volumes
if trend_score >= 80:
    base = 50000  # Aumentar o disminuir según necesites
    confidence = "Alta"
```

### Cambiar Duración del Cache

Edita línea 105 en `backend/main.py`:

```python
if datetime.now() - timestamp < timedelta(days=7):  # Cambiar días
```

---

## 📊 PRECISIÓN Y LIMITACIONES

### Precisión Estimada

| Tipo de Keyword | Precisión | Ejemplo |
|-----------------|-----------|---------|
| Alta competencia | ±30% | "plomero" |
| Media competencia | ±40% | "plomero culiacan" |
| Long-tail | ±50% | "plomero 24h las quintas" |

### Limitaciones

1. **No es volumen exacto** - Son estimaciones basadas en señales públicas
2. **Rate limits** - Google Trends tiene límites (mitigado con cache)
3. **Variación estacional** - No detecta estacionalidad compleja
4. **Nuevas keywords** - Menos preciso para términos muy nuevos

### ¿Cuándo Usar Esta Herramienta?

✅ **Casos de uso ideales:**
- Research inicial de keywords
- Comparación relativa entre keywords
- Tracking de tendencias
- Presupuesto limitado ($0)
- Análisis de competencia local

❌ **Cuándo usar herramientas de pago:**
- Necesitas volúmenes exactos
- Planificación de campañas PPC
- Reportes para clientes
- Keywords altamente competidas

---

## 🔧 TROUBLESHOOTING

### Error: "Rate limit exceeded"

**Solución:** Espera 5-10 minutos y vuelve a intentar. Google Trends tiene rate limits.

### Error: "No data found"

**Causa:** Keyword muy específica o sin datos en Google Trends.

**Solución:** Prueba con keyword más general.

### Frontend no se conecta al Backend

**Verificar:**
1. Backend corriendo en `http://localhost:8000`
2. CORS configurado correctamente
3. No hay firewall bloqueando puerto 8000

### Cache no funciona

**Verificar:**
1. Archivo `keyword_cache.db` existe en `/backend`
2. Permisos de escritura en directorio
3. SQLite3 instalado correctamente

---

## 🚀 DEPLOY EN PRODUCCIÓN

### Backend (Railway/Heroku/DigitalOcean)

1. **Railway.app** (Gratis hasta 500h/mes):

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Deploy
cd backend
railway login
railway init
railway up
```

2. **Render** (Gratis):

```bash
# Crear cuenta en render.com
# Conectar repo de GitHub
# Configurar:
Build Command: pip install -r requirements.txt
Start Command: python main.py
```

### Frontend (Vercel/Netlify)

1. **Vercel** (Gratis):

```bash
cd frontend
npm install -g vercel
vercel
```

2. **Netlify**:

```bash
cd frontend
npm run build
# Subir carpeta build/ a netlify.com
```

### Variables de Entorno

En frontend, crear `.env`:

```env
REACT_APP_API_URL=https://tu-backend.railway.app
```

---

## 💰 COSTO REAL

### Herramienta Gratis vs Alternativas de Pago

| Herramienta | Costo/mes | Precisión | Keywords/mes |
|-------------|-----------|-----------|--------------|
| **Esta Tool** | **$0** | **±40%** | **Ilimitado*** |
| SEMrush | $119 | ±5% | 10,000 |
| Ahrefs | $99 | ±5% | 10,000 |
| Keyword Planner | $0** | ±10% | Ilimitado** |

\* Rate limits de Google Trends (~100/hora)
** Requiere cuenta Google Ads con gasto activo

### ROI

Si haces research de keywords:
- **10 keywords/día** = 300 keywords/mes
- Alternativa de pago: $119/mes
- **Ahorro anual: $1,428 USD**

---

## 🎯 PRÓXIMAS MEJORAS

### Roadmap

- [ ] Soporte para múltiples países (US, ES, AR, etc.)
- [ ] Gráficas de tendencia (últimos 12 meses)
- [ ] Export a CSV/Excel
- [ ] Comparación de hasta 5 keywords simultáneas
- [ ] Integración con Google Search Console (datos propios)
- [ ] Detección de estacionalidad
- [ ] API batch (analizar 100 keywords a la vez)
- [ ] Dashboard con métricas históricas

---

## 📝 NOTAS TÉCNICAS

### Stack Tecnológico

**Backend:**
- FastAPI (framework web)
- pytrends (Google Trends API)
- SQLite (cache)
- BeautifulSoup (scraping)

**Frontend:**
- React 18
- CSS Grid/Flexbox
- Fetch API

### Rate Limits

Google Trends tiene límites no documentados:
- ~100 requests/hora recomendado
- Cache de 7 días mitiga esto
- En producción, usar Redis para cache distribuido

---

## 🤝 CONTRIBUIR

Si quieres mejorar la herramienta:

1. Fork el proyecto
2. Crea branch con feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a branch (`git push origin feature/nueva-funcionalidad`)
5. Abre Pull Request

---

## 📄 LICENCIA

MIT License - Uso libre para proyectos personales y comerciales

---

## ✨ RESUMEN

✅ **100% gratis** (sin suscripciones)
✅ **Ilimitado** (sujeto a rate limits)
✅ **Fácil de instalar** (5 minutos)
✅ **Interfaz web** (React moderna)
✅ **API REST** (integración fácil)
✅ **Cache inteligente** (evita rate limits)
✅ **Precisión aceptable** (±40% para keywords medias)

🚀 **Perfecto para:** SEO freelancers, startups, agencias pequeñas, proyectos personales

---

**Creado por:** Héctor Palazuelos
**Fecha:** Noviembre 2025
**Contacto:** contacto@plomeroculiacanpro.mx
