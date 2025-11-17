# 🚀 IMPORTAR CONFIGURACIÓN GTM EN 1 CLIC

**Tiempo total: 3 minutos**

---

## ⚠️ ANTES DE EMPEZAR (30 segundos)

### **Obtener tu ID de Medición GA4:**

1. Ve a: https://analytics.google.com
2. Haz clic en **"Administrar"** (⚙️ esquina inferior izquierda)
3. En la columna "Propiedad", haz clic en **"Flujos de datos"**
4. Haz clic en tu flujo de datos web (plomeroculiacanpro.mx)
5. **Copia el "ID de medición"** (formato: `G-XXXXXXXXXX`)

**✅ ANOTA TU ID AQUÍ:** `G-___________________`

---

## 📥 PASO 1: EDITAR EL ARCHIVO JSON (1 minuto)

1. Abre el archivo: **`gtm-config-import.json`** con un editor de texto
2. Presiona `Ctrl+F` (o `Cmd+F` en Mac)
3. Busca: `G-XXXXXXXXXX`
4. Reemplaza con: **TU ID de medición** que copiaste arriba
5. **Guarda el archivo** (`Ctrl+S` o `Cmd+S`)

**Ejemplo:**
```json
"value": "G-XXXXXXXXXX"     ← ANTES
"value": "G-ABC123XYZ789"   ← DESPUÉS (con tu ID real)
```

---

## 📤 PASO 2: IMPORTAR A GOOGLE TAG MANAGER (1 minuto)

### **2.1 Abrir GTM:**
1. Ve a: https://tagmanager.google.com
2. Busca el contenedor: **GTM-W75CRTX5**
3. Haz clic para abrirlo

### **2.2 Importar Archivo:**
1. En el menú superior, haz clic en **"Administrar"**
2. En la sección "Contenedor", haz clic en **"Importar contenedor"**
3. Haz clic en **"Elegir archivo del contenedor"**
4. Selecciona el archivo: **`gtm-config-import.json`** (el que editaste)
5. Haz clic en **"Continuar"**

### **2.3 Configurar Importación:**
1. En "Elegir espacio de trabajo":
   - Selecciona: **"Nuevo"**
   - Nombre: `Tracking SEO Cards`
2. En "Elegir una opción de importación":
   - Selecciona: **"Combinar"** (segundo radio button)
   - Marca: ☑️ **"Sobrescribir etiquetas, activadores y variables conflictivos"**
3. Haz clic en **"Confirmar"**

**✅ RESULTADO:** Verás un mensaje de éxito con el resumen de importación

---

## ✅ PASO 3: VERIFICAR IMPORTACIÓN (30 segundos)

En GTM, verifica que se crearon:

### **Variables (debería haber 5):**
- ✅ DL - Card Name
- ✅ DL - Card Position
- ✅ DL - Card URL
- ✅ DL - Scroll Percentage
- ✅ GA4 Measurement ID

**Cómo verificar:**
1. Menú izquierdo: **"Variables"**
2. Desplázate a "Variables definidas por el usuario"
3. Deberías ver las 5 variables listadas

### **Activadores (debería haber 2):**
- ✅ Click - SEO Card
- ✅ Scroll - Depth Milestone

**Cómo verificar:**
1. Menú izquierdo: **"Activadores"**
2. Deberías ver los 2 activadores

### **Etiquetas (debería haber 2):**
- ✅ GA4 - Event - Click SEO Card
- ✅ GA4 - Event - Scroll Depth

**Cómo verificar:**
1. Menú izquierdo: **"Etiquetas"**
2. Deberías ver las 2 etiquetas

---

## 🧪 PASO 4: PROBAR (30 segundos)

1. En GTM, esquina superior derecha: haz clic en **"Vista previa"**
2. En "Your website's URL" escribe: `https://plomeroculiacanpro.mx`
3. Haz clic en **"Connect"**
4. Se abrirá una nueva pestaña con tu sitio

**En la nueva pestaña del sitio:**
5. Desplázate hasta "Más opciones de plomería"
6. Haz clic en cualquier tarjeta

**En la ventana de GTM Tag Assistant:**
7. Verifica que aparece el evento: **"click_seo_card"**
8. Verifica que la etiqueta **"GA4 - Event - Click SEO Card"** muestra "Tags Fired" ✅

**Si ves ✅ en "Tags Fired", está funcionando correctamente.**

---

## 📢 PASO 5: PUBLICAR (30 segundos)

1. Cierra la Vista Previa
2. En GTM, haz clic en **"Enviar"** (esquina superior derecha)
3. En "Nombre de la versión" escribe: `Tracking tarjetas SEO`
4. Haz clic en **"Publicar"**

**✅ ¡LISTO! La configuración está en producción.**

---

## 🔍 VERIFICACIÓN FINAL EN GA4 (1 minuto)

### **Ver eventos en tiempo real:**

1. Ve a: https://analytics.google.com
2. Menú izquierdo: **"Informes" → "Tiempo real"**
3. Abre en otra pestaña: https://plomeroculiacanpro.mx
4. Haz clic en una tarjeta "Más opciones"

**En GA4 Tiempo real:**
5. En la sección "Evento por nombre de evento"
6. Deberías ver: **`click_seo_card`**

**Si ves el evento, ¡TODO ESTÁ FUNCIONANDO! 🎉**

---

## ⏱️ RESUMEN TOTAL

| Paso | Tiempo | Acción |
|------|--------|--------|
| 1 | 30s | Obtener ID de GA4 |
| 2 | 1min | Editar JSON con tu ID |
| 3 | 1min | Importar a GTM |
| 4 | 30s | Verificar importación |
| 5 | 30s | Probar en Preview |
| 6 | 30s | Publicar |
| 7 | 1min | Verificar en GA4 |
| **TOTAL** | **~5 min** | **¡COMPLETADO!** |

---

## 🆘 ¿PROBLEMAS?

### **Error: "El archivo no es válido"**
**Solución:**
- Asegúrate de haber guardado el archivo JSON después de editarlo
- Verifica que reemplazaste `G-XXXXXXXXXX` con tu ID real
- El ID debe tener formato: `G-` seguido de 10 caracteres

### **Error: "No se puede importar"**
**Solución:**
- Asegúrate de seleccionar "Combinar" (no "Sobrescribir")
- Marca la casilla "Sobrescribir etiquetas, activadores y variables conflictivos"

### **No veo eventos en GA4 Tiempo real**
**Solución:**
- Espera 1-2 minutos (puede haber delay)
- Verifica en GTM Preview que las etiquetas se disparan (Tags Fired)
- Confirma que el ID de medición en la variable "GA4 Measurement ID" es correcto

---

## 📊 PRÓXIMOS PASOS

Una vez que verifiques que los eventos funcionan:

1. **Esta semana:** Documenta métricas baseline (ver `CONFIGURACION_ANALYTICS.md`)
2. **Semanas 2-4:** Monitorea qué tarjeta es más popular
3. **Mes 2:** Analiza resultados y optimiza

---

## 📞 ¿NECESITAS AYUDA?

Si algo no funciona:
1. Revisa que el ID de GA4 esté correcto en el JSON
2. Verifica en GTM Preview que los eventos se disparan
3. Consulta la sección "Problemas Comunes" en `CONFIGURACION_ANALYTICS.md`

---

**¡Ahora tu sitio está trackeando automáticamente cada clic en las tarjetas SEO! 🎉**
