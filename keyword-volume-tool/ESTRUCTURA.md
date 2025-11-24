# 📁 ESTRUCTURA DEL PROYECTO

## Árbol de Directorios

```
keyword-volume-tool/
│
├── backend/                          # Backend FastAPI (Python)
│   ├── main.py                       # ⭐ API principal
│   ├── requirements.txt              # Dependencias Python
│   ├── venv/                         # Virtual environment (auto-generado)
│   └── keyword_cache.db              # SQLite cache (auto-generado)
│
├── frontend/                         # Frontend React
│   ├── src/
│   │   ├── App.jsx                   # ⭐ Componente principal
│   │   ├── App.css                   # Estilos
│   │   └── index.js                  # Entry point React
│   ├── public/
│   │   └── index.html                # HTML template
│   ├── package.json                  # Dependencias npm
│   ├── node_modules/                 # Módulos npm (auto-generado)
│   └── build/                        # Build producción (auto-generado)
│
├── ejemplos/                         # Scripts de ejemplo
│   ├── analizar_batch.py             # Analizar múltiples keywords → CSV
│   └── exportar_google_sheets.py     # Exportar a Google Sheets
│
├── README.md                         # 📖 Documentación completa
├── INICIO_RAPIDO.md                  # ⚡ Guía en 3 pasos
├── ESTRUCTURA.md                     # 📁 Este archivo
│
├── install.sh                        # 🚀 Instalación automática
├── start-backend.sh                  # Script para iniciar backend (auto-generado)
├── start-frontend.sh                 # Script para iniciar frontend (auto-generado)
└── start-all.sh                      # Script para iniciar todo (auto-generado)
```

---

## 📄 DESCRIPCIÓN DE ARCHIVOS PRINCIPALES

### Backend

#### `backend/main.py` (500 líneas)

**Funcionalidad principal:**
- API REST con FastAPI
- 3 endpoints principales
- Integración con Google Trends
- Google Autocomplete scraping
- Algoritmo ML de estimación
- Sistema de cache SQLite

**Endpoints:**

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Health check y metadata |
| `/api/keyword-volume` | POST | Analizar keyword |
| `/api/cache-stats` | GET | Estadísticas del cache |

**Funciones clave:**

```python
get_google_trends(keyword, location)
# → Obtiene tendencia de Google Trends
# Returns: {'interest_score': int, 'peak_score': int, 'trend': str, 'related_queries': list}

get_autocomplete_rank(keyword)
# → Scraping de Google Autocomplete
# Returns: int (ranking 1-10)

estimate_volume(trend_score, autocomplete_rank, keyword_length)
# → Algoritmo ML de estimación
# Returns: (volume_estimate, confidence)
```

**Modelos Pydantic:**

```python
class KeywordRequest(BaseModel):
    keyword: str
    location: str = "México"

class KeywordResponse(BaseModel):
    keyword: str
    location: str
    volume_estimate: int
    confidence: str  # "Alta", "Media", "Baja"
    trend_data: Dict
    autocomplete_rank: Optional[int]
    cached: bool
```

---

#### `backend/requirements.txt`

**Dependencias:**
- `fastapi==0.104.1` - Framework web
- `uvicorn[standard]==0.24.0` - ASGI server
- `pydantic==2.5.0` - Validación de datos
- `pytrends==4.9.2` - Google Trends API (gratis)
- `requests==2.31.0` - HTTP client
- `beautifulsoup4==4.12.2` - Web scraping

**Tamaño total:** ~50 MB instalado

---

### Frontend

#### `frontend/src/App.jsx` (250 líneas)

**Componentes:**
- Formulario de búsqueda (keyword + ubicación)
- Display de resultados (volumen, confianza, métricas)
- Grid de métricas (Trends, Peak, Autocomplete, Tendencia)
- Lista de keywords relacionadas
- Info section (cómo funciona)

**Estado React:**

```javascript
const [keyword, setKeyword] = useState('');
const [location, setLocation] = useState('México');
const [loading, setLoading] = useState(false);
const [result, setResult] = useState(null);
const [error, setError] = useState(null);
```

**API Call:**

```javascript
const response = await fetch('http://localhost:8000/api/keyword-volume', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    keyword: keyword.trim(),
    location: location
  })
});
```

---

#### `frontend/src/App.css` (300 líneas)

**Estilos:**
- Gradient background (purple/blue)
- Card-based UI
- Responsive grid layout
- Conditional formatting (badges para confianza)
- Animaciones (hover, transform)
- Mobile-first design (breakpoint 768px)

**Paleta de colores:**

```css
Primary: #667eea (Purple)
Secondary: #764ba2 (Darker purple)
Success: #d1fae5 (Green)
Warning: #fef3c7 (Yellow)
Error: #fee2e2 (Red)
Background: Linear gradient 135deg
```

---

### Ejemplos

#### `ejemplos/analizar_batch.py` (200 líneas)

**Funcionalidad:**
- Analizar lista de keywords
- Generar reporte CSV
- Mostrar top 5 keywords
- Estadísticas agregadas
- Control de rate limits

**Output:**

```csv
keyword,volumen,confianza,trend_score,peak_score,tendencia,autocomplete_rank,cached
plomero culiacan,4800,Media,65,87,rising,3,false
```

**Uso:**

```bash
python analizar_batch.py
# Genera: keyword_analysis_20241123_143022.csv
```

---

#### `ejemplos/exportar_google_sheets.py` (180 líneas)

**Funcionalidad:**
- Conexión a Google Sheets API
- Creación automática de worksheet
- Formato condicional
- Auto-resize de columnas
- Timestamp

**Requisitos adicionales:**

```bash
pip install gspread oauth2client
```

**Setup:**
1. Google Cloud Console → Create Service Account
2. Descargar JSON de credenciales
3. Guardar como `google-credentials.json`
4. Habilitar Google Sheets API

---

### Scripts de Instalación

#### `install.sh` (180 líneas)

**Flujo:**
1. Verificar Python 3.8+
2. Verificar Node.js 16+
3. Crear venv para backend
4. Instalar dependencias Python
5. Instalar dependencias npm
6. Crear scripts de inicio
7. Mostrar resumen

**Uso:**

```bash
chmod +x install.sh
./install.sh
```

---

## 🗄️ BASE DE DATOS (SQLite)

### Schema: `keyword_cache`

```sql
CREATE TABLE keyword_cache (
    keyword TEXT PRIMARY KEY,
    location TEXT,
    volume_estimate INTEGER,
    trend_score REAL,
    autocomplete_score REAL,
    timestamp DATETIME,
    raw_data TEXT  -- JSON serializado
);
```

**Índices:**
- PRIMARY KEY en `keyword`
- Composite index en `(keyword, location)`

**Tamaño estimado:**
- ~1 KB por keyword
- 1000 keywords = ~1 MB
- 10,000 keywords = ~10 MB

---

## 📊 FLUJO DE DATOS

```
┌─────────────────────────────────────────────────────────┐
│  1. USER INPUT                                          │
│  - Keyword: "plomero culiacan"                          │
│  - Location: "Sinaloa"                                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  2. FRONTEND (React)                                    │
│  - Validación                                           │
│  - POST request a API                                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  3. BACKEND (FastAPI)                                   │
│  a) Verificar cache SQLite (7 días)                     │
│     → Si existe: retornar cached                        │
│     → Si no: continuar                                  │
│                                                          │
│  b) Google Trends API                                   │
│     → interest_score: 0-100                             │
│     → peak_score: 0-100                                 │
│     → related_queries: []                               │
│                                                          │
│  c) Google Autocomplete Scraping                        │
│     → autocomplete_rank: 1-10                           │
│                                                          │
│  d) ML Estimation Algorithm                             │
│     → Combinar señales                                  │
│     → Calcular volumen estimado                         │
│     → Determinar confianza                              │
│                                                          │
│  e) Guardar en cache SQLite                             │
│                                                          │
│  f) Retornar JSON response                              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  4. FRONTEND DISPLAY                                    │
│  - Volumen estimado (formato numérico)                  │
│  - Badge de confianza (color-coded)                     │
│  - Métricas grid (Trends, Peak, Autocomplete)           │
│  - Keywords relacionadas                                │
│  - Cache notice (si aplica)                             │
└─────────────────────────────────────────────────────────┘
```

---

## 🔌 ARQUITECTURA DE RED

```
┌──────────────────┐
│  Browser         │
│  localhost:3000  │
└────────┬─────────┘
         │ HTTP
         │
         ▼
┌──────────────────────────┐
│  React Dev Server        │
│  Port: 3000              │
│  CORS: Allow localhost   │
└────────┬─────────────────┘
         │ Fetch API
         │
         ▼
┌──────────────────────────┐
│  FastAPI Backend         │
│  Port: 8000              │
│  CORS: localhost:3000    │
└────────┬─────────────────┘
         │
         ├─────────────────────────┐
         │                         │
         ▼                         ▼
┌─────────────────┐   ┌────────────────────┐
│ Google Trends   │   │ Google Autocomplete│
│ (pytrends)      │   │ (requests)         │
│ API Pública     │   │ Endpoint Público   │
└─────────────────┘   └────────────────────┘
         │
         ▼
┌─────────────────┐
│ SQLite Cache    │
│ keyword_cache.db│
└─────────────────┘
```

---

## 🎯 PERFORMANCE

### Benchmarks

| Operación | Primera vez | Cached |
|-----------|-------------|--------|
| Analizar keyword | ~3-5s | ~50ms |
| Batch 10 keywords | ~30-50s | ~500ms |
| Batch 100 keywords | ~5-8min | ~5s |

### Rate Limits

**Google Trends:**
- ~100 requests/hora (no documentado oficialmente)
- Mitigación: Cache de 7 días

**Google Autocomplete:**
- ~1000 requests/hora (estimado)
- Sin restricciones fuertes

### Optimizaciones

1. **Cache SQLite** → 99% faster en hits
2. **Batch con delay** → Evita rate limits
3. **Async/await** → Mejor UX
4. **Indexed DB** (futuro) → Cache en browser

---

## 🔒 SEGURIDAD

### Backend

✅ **Implementado:**
- CORS restringido a localhost:3000
- Validación de inputs con Pydantic
- Rate limiting natural (Google APIs)
- No credentials expuestas

⚠️ **Producción requiere:**
- HTTPS
- API key authentication
- Rate limiting explícito (slowapi)
- Input sanitization adicional
- CORS restringido a dominio producción

### Frontend

✅ **Implementado:**
- CSP headers (React por defecto)
- Input sanitization
- Error handling

---

## 📦 TAMAÑOS

### Backend

```
venv/                  ~50 MB
*.py                   ~15 KB
keyword_cache.db       Variable (10 KB - 100 MB)
Total instalado:       ~50 MB
```

### Frontend

```
node_modules/          ~300 MB
src/                   ~20 KB
build/ (producción)    ~500 KB (comprimido)
Total instalado:       ~300 MB
Total en producción:   ~500 KB
```

---

## 🚀 DEPLOY

### Backend

**Opciones gratis:**
- Railway.app (500h/mes gratis)
- Render.com (750h/mes gratis)
- Fly.io (3 VMs gratis)

**Requirements:**
- Python 3.8+
- SQLite (incluido)
- 512 MB RAM mínimo

### Frontend

**Opciones gratis:**
- Vercel (100 GB bandwidth/mes)
- Netlify (100 GB bandwidth/mes)
- GitHub Pages (1 GB storage)

**Build:**

```bash
cd frontend
npm run build
# Deploy carpeta build/
```

---

## 🎓 LEARNING PATH

### Nivel Principiante

1. Leer `INICIO_RAPIDO.md`
2. Instalar con `install.sh`
3. Probar interfaz web
4. Modificar lista de ubicaciones

### Nivel Intermedio

5. Leer `backend/main.py`
6. Entender algoritmo de estimación
7. Modificar fórmula de volumen
8. Crear script batch personalizado

### Nivel Avanzado

9. Implementar nuevas fuentes de datos
10. Agregar ML model (scikit-learn)
11. Deploy en producción
12. Integrar con Search Console API

---

## 📞 SOPORTE

**Issues comunes:**
- Ver `README.md` → Troubleshooting
- Ver `INICIO_RAPIDO.md` → Solución problemas

**Contacto:**
- Email: contacto@plomeroculiacanpro.mx
- GitHub Issues (si aplica)

---

**Última actualización:** Noviembre 2025
**Versión:** 1.0.0
**Autor:** Héctor Palazuelos
