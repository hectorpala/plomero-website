# 🔧 CONFIGURACIÓN MANUAL GTM (10 MINUTOS)

**Como la importación da errores de formato, vamos a configurarlo manualmente.**
**Es muy simple, solo copy-paste de valores.**

---

## 📋 **LO QUE VAMOS A CREAR**

- ✅ 4 Variables
- ✅ 2 Activadores
- ✅ 2 Etiquetas GA4

**Total: ~10 minutos**

---

# PARTE 1: VARIABLES (3 minutos)

## **Variable 1: Card Name**

1. En GTM, ve a: **Variables** (menú izquierdo)
2. Haz clic en: **Nueva** (en "Variables definidas por el usuario")
3. Haz clic en el cuadro de "Configuración de la variable"
4. Selecciona: **Variable de capa de datos**
5. En "Nombre de la variable de la capa de datos" escribe:
   ```
   card_name
   ```
6. Arriba, en "Nombre" escribe:
   ```
   DL - Card Name
   ```
7. Haz clic en: **Guardar**

---

## **Variable 2: Card Position**

1. Haz clic en: **Nueva**
2. Configuración: **Variable de capa de datos**
3. Nombre de la variable: `card_position`
4. Nombre: `DL - Card Position`
5. **Guardar**

---

## **Variable 3: Card URL**

1. Haz clic en: **Nueva**
2. Configuración: **Variable de capa de datos**
3. Nombre de la variable: `card_url`
4. Nombre: `DL - Card URL`
5. **Guardar**

---

## **Variable 4: Scroll Percentage**

1. Haz clic en: **Nueva**
2. Configuración: **Variable de capa de datos**
3. Nombre de la variable: `scroll_percentage`
4. Nombre: `DL - Scroll Percentage`
5. **Guardar**

---

# PARTE 2: ACTIVADORES (2 minutos)

## **Activador 1: Click SEO Card**

1. En GTM, ve a: **Activadores** (menú izquierdo)
2. Haz clic en: **Nuevo**
3. Haz clic en "Configuración del activador"
4. Selecciona: **Evento personalizado**
5. En "Nombre del evento" escribe:
   ```
   click_seo_card
   ```
6. Deja marcado: "Todos los eventos personalizados"
7. Arriba, en "Nombre" escribe:
   ```
   Click - SEO Card
   ```
8. **Guardar**

---

## **Activador 2: Scroll Depth**

1. Haz clic en: **Nuevo**
2. Configuración: **Evento personalizado**
3. Nombre del evento: `scroll_depth`
4. Deja marcado: "Todos los eventos personalizados"
5. Nombre: `Scroll - Depth Milestone`
6. **Guardar**

---

# PARTE 3: ETIQUETAS GA4 (5 minutos)

## **Etiqueta 1: Click SEO Card**

1. En GTM, ve a: **Etiquetas** (menú izquierdo)
2. Haz clic en: **Nueva**
3. Haz clic en "Configuración de la etiqueta"
4. Selecciona: **Google Analytics: Evento GA4**

### **Configurar:**

**ID de medición:**
```
G-NSV2K9N2ZD
```

**Nombre del evento:**
```
click_seo_card
```

**Parámetros del evento:** (Haz clic en "Agregar fila" 3 veces)

| Nombre del parámetro | Valor |
|---------------------|-------|
| `card_name` | `{{DL - Card Name}}` |
| `card_position` | `{{DL - Card Position}}` |
| `card_url` | `{{DL - Card URL}}` |

**Cómo agregar el valor `{{DL - Card Name}}`:**
- Haz clic en el ícono de **cuadrado con +** junto al campo "Valor"
- Busca y selecciona: **DL - Card Name**
- Repite para los otros 2 parámetros

### **Activación:**

1. Haz clic en "Activación"
2. Selecciona: **Click - SEO Card**

### **Nombre de la etiqueta:**
```
GA4 - Event - Click SEO Card
```

**Guardar**

---

## **Etiqueta 2: Scroll Depth**

1. Haz clic en: **Nueva**
2. Configuración: **Google Analytics: Evento GA4**

### **Configurar:**

**ID de medición:**
```
G-NSV2K9N2ZD
```

**Nombre del evento:**
```
scroll_depth
```

**Parámetros del evento:** (Agregar 1 fila)

| Nombre del parámetro | Valor |
|---------------------|-------|
| `scroll_percentage` | `{{DL - Scroll Percentage}}` |

### **Activación:**

1. Haz clic en "Activación"
2. Selecciona: **Scroll - Depth Milestone**

### **Nombre de la etiqueta:**
```
GA4 - Event - Scroll Depth
```

**Guardar**

---

# ✅ VERIFICAR Y PUBLICAR

## **1. Verificar que creaste todo:**

**Variables (4):**
- ✅ DL - Card Name
- ✅ DL - Card Position
- ✅ DL - Card URL
- ✅ DL - Scroll Percentage

**Activadores (2):**
- ✅ Click - SEO Card
- ✅ Scroll - Depth Milestone

**Etiquetas (2):**
- ✅ GA4 - Event - Click SEO Card
- ✅ GA4 - Event - Scroll Depth

---

## **2. Probar (IMPORTANTE):**

1. En GTM, haz clic en: **Vista previa** (esquina superior derecha)
2. En "Your website's URL" escribe: `https://plomeroculiacanpro.mx`
3. Haz clic en: **Connect**
4. Se abrirá tu sitio en una nueva pestaña

**En tu sitio:**
- Haz clic en una tarjeta de "Más opciones"
- Haz scroll hasta el 50%

**En la ventana de GTM Tag Assistant:**
- Verifica que aparece: `click_seo_card`
- Verifica que aparece: `scroll_depth`
- Verifica que las etiquetas muestran "Tags Fired" ✅

---

## **3. Publicar:**

1. Si todo funciona en Preview, cierra la vista previa
2. Haz clic en: **Enviar** (esquina superior derecha)
3. Nombre: `Tracking tarjetas SEO`
4. Haz clic en: **Publicar**

---

## **4. Verificar en GA4:**

1. Ve a: https://analytics.google.com
2. **Informes → Tiempo real**
3. Abre: https://plomeroculiacanpro.mx
4. Haz clic en una tarjeta
5. Deberías ver: `click_seo_card` en eventos

---

# 🎯 RESUMEN DE COPY-PASTE

Para facilitarte, aquí están todos los valores que necesitas copiar y pegar:

**Variables (nombre de capa de datos):**
```
card_name
card_position
card_url
scroll_percentage
```

**Activadores (nombre de evento):**
```
click_seo_card
scroll_depth
```

**Etiquetas (ID de medición):**
```
G-NSV2K9N2ZD
```

**Etiquetas (nombre de evento):**
```
click_seo_card
scroll_depth
```

**Parámetros:**
```
card_name
card_position
card_url
scroll_percentage
```

---

**¡Listo! Con esto tendrás tracking completo funcionando.** 🎉
