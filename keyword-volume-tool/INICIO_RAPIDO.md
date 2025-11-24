# ⚡ INICIO RÁPIDO - Keyword Volume Tool

## 🚀 EN 3 PASOS (5 minutos)

### PASO 1: Instalar Backend

```bash
cd keyword-volume-tool/backend

# Crear entorno virtual
python3 -m venv venv

# Activar entorno (macOS/Linux)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### PASO 2: Instalar Frontend

Abre una NUEVA terminal:

```bash
cd keyword-volume-tool/frontend

# Instalar dependencias
npm install
```

### PASO 3: Iniciar Ambos Servicios

**Terminal 1 (Backend):**
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

**Terminal 2 (Frontend):**
```bash
cd keyword-volume-tool/frontend
npm start
```

El navegador abrirá automáticamente: `http://localhost:3000` 🎉

---

## ✅ VERIFICAR QUE TODO FUNCIONA

### Test 1: API Backend

Abre http://localhost:8000 en tu navegador.

Deberías ver:
```json
{
  "service": "Keyword Volume Tool",
  "version": "1.0.0",
  "cost": "100% GRATIS",
  "data_sources": ["Google Trends", "Autocomplete", "ML Estimation"]
}
```

### Test 2: Interfaz Web

Abre http://localhost:3000

1. Ingresa keyword: **plomero culiacan**
2. Selecciona ubicación: **Sinaloa**
3. Click "Analizar Keyword"

Deberías ver:
- Volumen estimado (~4,000-6,000 búsquedas/mes)
- Google Trends score
- Autocomplete ranking
- Keywords relacionadas

---

## 🎯 PRIMER ANÁLISIS

### Ejemplo 1: Keyword Local

**Input:**
- Keyword: `plomero las quintas`
- Ubicación: `Culiacán`

**Output esperado:**
- Volumen: 200-500/mes
- Confianza: Baja
- Trend: 20-40/100

### Ejemplo 2: Keyword Nacional

**Input:**
- Keyword: `plomero`
- Ubicación: `México`

**Output esperado:**
- Volumen: 50,000-100,000/mes
- Confianza: Alta
- Trend: 80-100/100

---

## 📊 ANALIZAR MÚLTIPLES KEYWORDS

### Usando Script Batch

```bash
cd keyword-volume-tool/ejemplos

# Editar lista de keywords
nano analizar_batch.py

# Ejecutar (asegúrate que backend esté corriendo)
python analizar_batch.py
```

Genera archivo CSV con resultados:
```
keyword,volumen,confianza,trend_score,peak_score,tendencia,autocomplete_rank,cached
plomero culiacan,4800,Media,65,87,rising,3,false
plomero las quintas,280,Baja,28,45,stable,8,false
...
```

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### ❌ Error: "Module not found: pytrends"

**Solución:**
```bash
cd backend
source venv/bin/activate
pip install pytrends
```

### ❌ Error: "Connection refused" en frontend

**Causa:** Backend no está corriendo

**Solución:**
```bash
# Terminal 1
cd backend
source venv/bin/activate
python main.py
```

### ❌ Error: "Rate limit exceeded"

**Causa:** Demasiados requests a Google Trends

**Solución:**
- Espera 5-10 minutos
- Reduce frecuencia de análisis
- Usa el cache (resultados válidos 7 días)

---

## 🎨 PERSONALIZACIÓN RÁPIDA

### Cambiar Ubicaciones

Edita `backend/main.py` línea 153:

```python
geo_map = {
    "México": "MX",
    "Culiacán": "MX-SIN",
    "Sinaloa": "MX-SIN",
    # Agregar más ubicaciones:
    "Monterrey": "MX-NLE",
    "Tijuana": "MX-BCN"
}
```

Edita `frontend/src/App.jsx` línea 10:

```javascript
const locations = [
  'México',
  'Culiacán',
  'Sinaloa',
  // Agregar más:
  'Monterrey',
  'Tijuana'
];
```

---

## 📖 MÁS INFORMACIÓN

- **README completo:** [README.md](README.md)
- **API Docs:** http://localhost:8000/docs
- **Ejemplos:** [ejemplos/](ejemplos/)

---

## ✨ ¡LISTO!

Ya tienes tu herramienta de keyword research **100% gratis** funcionando.

**Próximos pasos:**
1. Analiza tus keywords principales
2. Exporta resultados a CSV
3. Compara volúmenes entre keywords
4. Optimiza tu estrategia SEO

🚀 **Happy keyword research!**
