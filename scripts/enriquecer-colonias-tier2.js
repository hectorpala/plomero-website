const fs = require('fs');
const path = require('path');

const BASE = '/Users/openclaw/Documents/Mis Apps/Sitios Web/Plomero Culiacán/servicios/plomero-colonias-culiacan';

const colonias = {
  'bugambilias': {
    faqs: [
      { q: '¿Por qué hay fugas frecuentes en las casas de Bugambilias?', a: 'Las casas de Bugambilias construidas entre 1970 y 1990 tienen instalaciones galvanizadas de 35-55 años que nunca se renovaron. El agua dura de JAPAC corroe el galvanizado internamente: reduce el diámetro útil y genera pinhole leaks en codos y uniones. La referencia de la Iglesia de Nuestra Señora de Guadalupe Bugambilias marca el corazón de una colonia con plomería que ya llegó al final de su ciclo de vida original.' },
      { q: '¿El agua con olor oxidado en Bugambilias es señal de qué?', a: 'Es la señal más clara de corrosión avanzada en la tubería galvanizada. El óxido que se desprende internamente tiñe el agua de un tono herrumbroso. No es peligroso en el corto plazo, pero indica que la tubería está fallando y las fugas son inminentes. Recomendamos no usarla para cocinar o beber hasta inspeccionar.' },
      { q: '¿Cuánto cuesta cambiar la tubería en una casa de Bugambilias?', a: 'Un baño completo en CPVC está entre $3,500 y $6,000 MXN con mano de obra. Una casa mediana de Bugambilias (2 baños + cocina) varía entre $12,000 y $22,000 MXN. Damos presupuesto gratis antes de iniciar — llama al 667 392 2273.' },
      { q: '¿Cuánto tardan en llegar a Bugambilias?', a: 'Llegamos en 25-35 minutos para emergencias. Conocemos la colonia con referencia en Avenida de las Higueras y la Iglesia de Guadalupe. Atendemos 24/7 los 365 días.' },
      { q: '¿Puedo reparar solo el tubo roto o conviene cambiar toda la tubería de Bugambilias?', a: 'Si la casa tiene más de 40 años con galvanizado original, reparar solo el tramo roto es un parche temporal — en 6-18 meses fallará otro punto. Te damos diagnóstico honesto del estado general antes de recomendar reparación parcial o cambio completo.' }
    ]
  },
  'santa-fe': {
    faqs: [
      { q: '¿Por qué hay problemas de agua en Santa Fe si es una colonia relativamente nueva?', a: 'Santa Fe tiene entre 15 y 35 años y es uno de los fraccionamientos más poblados de Sinaloa con ~9,250 habitantes. Esa alta densidad genera mayor demanda sobre la red de JAPAC, lo que provoca baja presión en horas pico. Además, el agua dura ya acumula sarro en calentadores de 10-25 años de uso sin mantenimiento.' },
      { q: '¿Por qué el tinaco de mi casa de Santa Fe no llena bien?', a: 'Las causas más comunes en Santa Fe son: flotador mal calibrado o con fugas (no abre completamente la válvula de entrada), válvula de llenado desgastada, o presión de JAPAC insuficiente en horas pico. Un diagnóstico rápido identifica cuál es el caso — llama al 667 392 2273.' },
      { q: '¿Cuánto cuesta limpiar el sarro del calentador en Santa Fe?', a: 'La limpieza de sarro (lavado ácido del intercambiador) cuesta entre $400 y $800 MXN dependiendo del tipo de calentador. Si el calentador ya tiene daño irreversible por sarro, el reemplazo está entre $3,500 y $8,000 MXN con instalación incluida.' },
      { q: '¿Cuánto tardan en llegar a Santa Fe?', a: 'Para emergencias en Santa Fe llegamos en 25-35 minutos por Boulevard Santa Fe. Cubrimos todo el fraccionamiento 24/7 los 365 días.' },
      { q: '¿Atienden también FOVISSSTE Humaya y Lomas del Humaya, vecinos de Santa Fe?', a: 'Sí, toda la zona que comparte el CP 80029 — Santa Fe, FOVISSSTE Humaya y Lomas del Humaya — está dentro de nuestra cobertura habitual. Llegamos en el mismo tiempo a todas estas colonias.' }
    ]
  },
  'las-palmas': {
    faqs: [
      { q: '¿Por qué tengo baja presión de agua en Las Palmas si el tinaco está lleno?', a: 'En Las Palmas, con casas de 35-55 años, la causa más frecuente es el galvanizado interno corroído. La tubería original de los 70-80 se obstruye con óxido y sarro hasta que el agua apenas pasa, aunque el tinaco esté lleno. El Parque Las Palmas en Blvd. Las Palmas es referencia de una colonia donde muchas casas nunca renovaron su instalación hidráulica.' },
      { q: '¿Cuándo es urgente llamar al plomero en Las Palmas?', a: 'Llama de inmediato si: el agua sale con color oxidado, hay manchas de humedad en muros sin causa aparente, la presión cayó de golpe (puede ser fuga activa), o el WC tarda más de 10 minutos en llenarse. Estos son síntomas de que la tubería ya está fallando.' },
      { q: '¿Cuánto cuesta renovar la plomería en una casa de Las Palmas?', a: 'Un baño completo en CPVC cuesta entre $3,500 y $6,000 MXN. Casa mediana (2 baños + cocina) entre $12,000 y $22,000 MXN con mano de obra. Presupuesto gratuito al 667 392 2273.' },
      { q: '¿Cuánto tardan en llegar a Las Palmas?', a: 'Para emergencias llegamos en 25-35 minutos con referencia en Blvd. Las Palmas y el Parque Las Palmas. Atendemos 24/7 los 365 días.' },
      { q: '¿Hay riesgo estructural si ignoro una fuga en una casa de 40 años en Las Palmas?', a: 'Sí. Una fuga oculta en muro de una casa de 40 años humedece el tabique de forma continua. En 3-6 meses aparecen manchas, hongos y deterioro del acabado. A largo plazo puede comprometer muros y losas. Detectar y reparar a tiempo ahorra decenas de miles de pesos en daños estructurales.' }
    ]
  },
  'bosques-del-humaya': {
    faqs: [
      { q: '¿Qué problemas de plomería son más comunes en Bosques del Humaya?', a: 'En Bosques del Humaya, con casas de 15-35 años cercanas al Río Humaya, los problemas más frecuentes son: sarro en calentadores de paso por el agua dura de JAPAC, golpes de ariete que dañan uniones de PVC por los cortes programados, y flotadores de tinaco que fallan después de 10-15 años. El Panteón Jardines del Humaya cercano es punto de referencia de una zona que combina modernidad con plomería ya en su segundo ciclo de vida.' },
      { q: '¿La humedad del Río Humaya afecta las instalaciones de plomería?', a: 'La cercanía al río no afecta directamente las tuberías internas, pero sí las instalaciones externas y cisternas subterráneas. En temporada de lluvias, las cisternas bajo nivel de piso pueden recibir filtración de agua freática si tienen grietas. Si tu cisterna huele a tierra o el agua tiene turbiedad, solicita inspección al 667 392 2273.' },
      { q: '¿Cuánto cuesta el mantenimiento preventivo en Bosques del Humaya?', a: 'Una revisión preventiva completa (calentador, tinaco, válvulas, drenajes y presión) cuesta entre $1,000 y $1,800 MXN. Limpieza de sarro en calentador por separado: $400-$800 MXN. Diagnóstico inicial gratuito.' },
      { q: '¿Cuánto tardan en llegar a Bosques del Humaya?', a: 'Para emergencias llegamos en 25-35 minutos por Boulevard Jardín de las Orquídeas. Atendemos 24/7 los 365 días al 667 392 2273.' },
      { q: '¿Puedo prevenir los daños por golpes de ariete en Bosques del Humaya?', a: 'Sí. Una válvula amortiguadora de golpes de ariete instalada en la entrada de la red de tu casa previene el daño a válvulas y uniones de PVC cuando JAPAC corta y restaura el servicio. Cuesta entre $600 y $1,200 MXN con instalación y puede evitar reparaciones de $3,000-$8,000 MXN en el futuro.' }
    ]
  },
  'amorada': {
    faqs: [
      { q: '¿Qué problemas de plomería son más frecuentes en Amorada?', a: 'Amorada es un fraccionamiento del noroeste de Culiacán con casas de 15-35 años sobre Blvd. Jesús Kumate Rodríguez. Los problemas más frecuentes son: sarro acumulado en calentadores de paso (el agua dura de JAPAC afecta toda la ciudad), válvulas de paso que no cierran completamente después de 10-15 años, y drenajes con grasa acumulada en las cocinas.' },
      { q: '¿Por qué mi calentador de paso falla si la casa de Amorada es reciente?', a: 'El agua de JAPAC tiene alta dureza independientemente de la zona. Sin mantenimiento anual, el sarro bloquea el intercambiador del calentador en 8-12 años. La limpieza anual (lavado ácido) cuesta $400-$800 MXN y puede triplicar la vida útil del equipo.' },
      { q: '¿Cuánto tardan en llegar a Amorada?', a: 'Para emergencias en Amorada llegamos en 25-35 minutos por Blvd. Jesús Kumate Rodríguez. Atendemos 24/7 los 365 días.' },
      { q: '¿Cuánto cuesta destapar un drenaje en Amorada?', a: 'El destape varía entre $500 y $1,200 MXN dependiendo del tipo de obstrucción y profundidad. El diagnóstico es gratuito. Para obstrucciones simples (grasa, cabello), el servicio dura 30-60 minutos.' },
      { q: '¿Atienden también colonias cercanas a Amorada?', a: 'Sí, cubrimos Amorada y las colonias del noroeste de Culiacán sobre Blvd. Jesús Kumate Rodríguez. Llegamos en 25-40 minutos dependiendo de la ubicación exacta.' }
    ]
  },
  'altamira': {
    faqs: [
      { q: '¿Por qué Altamira tiene más problemas de plomería que colonias nuevas?', a: 'Altamira fue desarrollada entre 1970 y 1990 como fraccionamiento de nivel medio-alto al norte de Culiacán. Con casas de 35-55 años sobre Blvd. Francisco Zarco, la mayoría conserva instalaciones galvanizadas originales de los 70-80 que nunca se renovaron integralmente. El galvanizado con el agua dura de JAPAC genera corrosión interna, baja presión progresiva y fugas ocultas en muros.' },
      { q: '¿Las secciones Barceló y Altana de Altamira tienen los mismos problemas?', a: 'Sí, las secciones Barceló y Altana comparten el mismo período de construcción y el mismo tipo de instalaciones. Las variaciones dependen más de si cada casa en particular renovó o no su tubería. El diagnóstico gratuito determina el estado específico de cada propiedad.' },
      { q: '¿Cuánto cuesta cambiar la tubería galvanizada en Altamira?', a: 'Un baño completo en CPVC cuesta entre $3,500 y $6,000 MXN. Una casa mediana de Altamira (2 baños + cocina) varía entre $12,000 y $22,000 MXN con mano de obra. Diagnóstico y presupuesto gratis al 667 392 2273.' },
      { q: '¿Cuánto tardan en llegar a Altamira?', a: 'Para emergencias en Altamira llegamos en 25-35 minutos por Blvd. Francisco Zarco. Cubrimos las tres secciones: Altamira, Barceló y Altana. Atendemos 24/7 los 365 días.' },
      { q: '¿Qué señales me dicen que la plomería de mi casa en Altamira necesita renovación?', a: 'Las señales clave: agua herrumbrosa al abrir por primera vez en la mañana, manchas de humedad en muros sin causa aparente, presión que baja progresivamente, calentador que falla antes de su tiempo, o WC que tarda más en llenarse. Si tienes 3 o más señales, la tubería galvanizada ya está al límite.' }
    ]
  },
  'colinas-de-la-rivera': {
    faqs: [
      { q: '¿Qué problemas de plomería son más comunes en Colinas de la Rivera?', a: 'Colinas de la Rivera es un fraccionamiento moderno (1990-2010) sobre Blvd. Jardín de las Orquídeas, colindante con Balcones del Humaya. Los problemas más frecuentes son sarro en calentadores de paso por el agua dura de JAPAC, golpes de ariete por cortes programados que dañan uniones de PVC, y presión irregular en horas pico por la demanda de la zona norte de Culiacán.' },
      { q: '¿El Estadio Dorados afecta el servicio de agua en Colinas de la Rivera?', a: 'En días de partido con alta concurrencia, la demanda de agua en la zona puede incrementarse y reducir la presión en las colonias aledañas como Colinas de la Rivera. Si notas caídas de presión recurrentes en esos días, el problema es externo (red JAPAC) y no interno. Podemos verificar si hay problema interno en tu casa de forma gratuita.' },
      { q: '¿Cuánto cuesta el mantenimiento preventivo en Colinas de la Rivera?', a: 'Revisión preventiva completa (calentador, tinaco, válvulas, drenajes): entre $1,000 y $1,800 MXN. Limpieza de sarro en calentador por separado: $400-$800 MXN. Diagnóstico gratuito al 667 392 2273.' },
      { q: '¿Cuánto tardan en llegar a Colinas de la Rivera?', a: 'Para emergencias llegamos en 25-35 minutos por Blvd. Jardín de las Orquídeas. Cubrimos Colinas de la Rivera y su segunda sección. Atendemos 24/7.' },
      { q: '¿Atienden también Balcones del Humaya y Bosques del Humaya, colonias vecinas?', a: 'Sí, cubrimos todo el sector norte del Humaya: Colinas de la Rivera, Balcones del Humaya, Bosques del Humaya, Praderas del Humaya y Lomas del Humaya. Llegamos en 25-35 minutos a cualquiera de estas colonias.' }
    ]
  },
  'villa-universidad': {
    faqs: [
      { q: '¿Por qué las casas de Villa Universidad tienen problemas crónicos de presión?', a: 'Villa Universidad fue desarrollada en los años 70 junto al campus de la UAS. Con más de 50 años, las instalaciones galvanizadas originales están en el último tramo de su vida útil. El galvanizado corroído internamente, combinado con la presión de la red de JAPAC en esa zona que abastece también Ciudad Universitaria, genera baja presión crónica en horas pico (7-9am, 7-9pm).' },
      { q: '¿La reactivación de la Ruta Villa Universidad en 2025 afectó el tráfico para emergencias?', a: 'La Ruta Villa Universidad que beneficia a 10,000 vecinos circula por Blvd. de las Américas y Blvd. Pedro María Anaya. Para emergencias de plomería, conocemos las rutas alternativas por las calles internas de la colonia y llegamos en 25-35 minutos independientemente del tráfico en los bulevares principales.' },
      { q: '¿Cuánto cuesta renovar la tubería en una casa de Villa Universidad?', a: 'Con más de 50 años de antigüedad, la renovación es prácticamente necesaria. Un baño completo en CPVC cuesta $3,500-$6,000 MXN. Casa mediana (2 baños + cocina): $12,000-$22,000 MXN con mano de obra. Presupuesto gratuito al 667 392 2273.' },
      { q: '¿Cuánto tardan en llegar a Villa Universidad?', a: 'Para emergencias llegamos en 20-30 minutos. Conocemos bien la zona: Jardín Botánico de Culiacán en Av. Las Américas 2131, Parque Villa Universidad en Calle Homero y Galileo, y los accesos por Blvd. de las Américas. Atendemos 24/7.' },
      { q: '¿Atienden también negocios y locales comerciales cerca de la UAS en Villa Universidad?', a: 'Sí, atendemos vivienda, comercios y edificios universitarios en la zona. Para negocios emitimos factura SAT el mismo día. Para edificios con varios departamentos o locales, ofrecemos inspección general y presupuesto global.' }
    ]
  },
  'nuevo-culiacan': {
    faqs: [
      { q: '¿Por qué las casas de Nuevo Culiacán tienen tantos problemas de plomería?', a: 'Nuevo Culiacán fue desarrollado en los años 60-75 con viviendas de 50-60 años. Sus calles con nomenclatura de bahías (Bahía de Acapulco, Bahía de Altamira) y ríos marcan un fraccionamiento planificado de los 60s cuyas instalaciones galvanizadas originales ya están muy deterioradas. A esa antigüedad, el galvanizado se corroe internamente hasta generar fugas múltiples y agua herrumbrosa.' },
      { q: '¿Cuánto cuesta renovar la plomería en Nuevo Culiacán?', a: 'Con 50-60 años de antigüedad, la renovación es necesaria. Un baño completo en CPVC: $3,500-$6,000 MXN. Casa mediana (2 baños + cocina): $12,000-$22,000 MXN. Si además se requiere renovar drenajes de barro vidriado, el costo sube $5,000-$15,000 MXN adicionales. Presupuesto gratuito al 667 392 2273.' },
      { q: '¿Por qué el agua sale tan lenta en Nuevo Culiacán aunque el tinaco esté lleno?', a: 'En casas de 50-60 años como las de Nuevo Culiacán, la tubería galvanizada se corroe internamente hasta reducir su diámetro útil en un 60-80%. Es como tratar de pasar agua por un popote. La única solución definitiva es el reemplazo de la tubería — ningún aditivo ni limpieza externa resuelve la corrosión interna del galvanizado.' },
      { q: '¿Cuánto tardan en llegar a Nuevo Culiacán?', a: 'Para emergencias llegamos en 25-35 minutos. Conocemos la zona: calles sobre Bahía de Acapulco y Av. Juan de Dios Bátiz. Atendemos 24/7 los 365 días.' },
      { q: '¿Hay riesgo de daño estructural por fugas en casas de Nuevo Culiacán?', a: 'Sí, y es importante. En casas de 50-60 años, una fuga oculta en muro puede acumular humedad durante meses sin manifestarse. Esa humedad sostenida debilita el tabique, promueve hongos y puede comprometer muros y losas. Si notas paredes frías o manchas de humedad sin causa aparente, llama de inmediato al 667 392 2273.' }
    ]
  },
  'libertad': {
    faqs: [
      { q: '¿Por qué las casas de Libertad tienen instalaciones tan complicadas?', a: 'La colonia Libertad fue fundada antes de 1960, con viviendas de 60-80 años en la zona poniente de Culiacán. Las casas se ampliaron generación tras generación mezclando galvanizado de los 50-60, cobre de los 70 y PVC de los 80-90. Esa mezcla de materiales genera corrosión galvánica en las uniones entre metales distintos — la causa más común de fugas crónicas en Libertad.' },
      { q: '¿Es seguro el agua que sale de las tuberías viejas de Libertad?', a: 'Si el agua sale con color herrumbroso u olor metálico, no es recomendable para cocinar o beber mientras no se resuelva el problema. El óxido en suspensión no es agudamente tóxico pero indica tubería fallando. Usa agua embotellada como medida preventiva y llama al 667 392 2273 para diagnóstico urgente.' },
      { q: '¿Cuánto cuesta modernizar la plomería de una casa de Libertad?', a: 'Para casas de 60-80 años recomendamos renovación completa. Red hidráulica (2 baños + cocina) en CPVC: $12,000-$22,000 MXN. Si se requiere renovar también los drenajes de barro vidriado: $5,000-$15,000 MXN adicionales. Diagnóstico y presupuesto gratuitos al 667 392 2273.' },
      { q: '¿Cuánto tardan en llegar a la colonia Libertad?', a: 'Para emergencias llegamos en 25-35 minutos. Atendemos toda la colonia Libertad sobre Av. Constituyente Ciro C. Ceballos. Servicio 24/7 los 365 días.' },
      { q: '¿Qué es la corrosión galvánica y por qué afecta tanto a Libertad?', a: 'La corrosión galvánica ocurre cuando dos metales distintos (como galvanizado y cobre) se conectan directamente con agua como electrolito. El metal más reactivo se corroe aceleradamente. En Libertad, donde conviven tuberías de tres épocas distintas conectadas entre sí, este fenómeno es la causa más frecuente de fugas en las uniones. La única solución es reemplazar los tramos de metales distintos o usar conectores dieléctricos.' }
    ]
  },
  'barrancos': {
    faqs: [
      { q: '¿Por qué hay tanta baja presión en Barrancos?', a: 'Barrancos es una colonia de vivienda social desarrollada entre 1972 y 1990, contigua al INFONAVIT Barrancos. Con casas de 35-50 años y tubería galvanizada original que nunca se renovó, más la alta densidad de la zona, la presión disponible en las llaves es baja — especialmente en horas pico. Los cortes frecuentes de JAPAC en el sector noreste agravan el problema.' },
      { q: '¿Cuánto cuesta renovar la plomería en una casa de Barrancos?', a: 'Para viviendas de interés social de Barrancos ofrecemos opciones escalonadas: solo baño principal en CPVC: $2,800-$4,500 MXN. Cocina: $1,500-$2,500 MXN. Renovación completa (baño + cocina): $6,000-$10,000 MXN con mano de obra. Aceptamos pagos en parcialidades. Presupuesto gratuito al 667 392 2273.' },
      { q: '¿Los cortes de JAPAC dañan las instalaciones de Barrancos?', a: 'Sí. Cada corte y restauración genera un golpe de ariete que desgasta válvulas, uniones y flotadores. En una zona con cortes frecuentes como Barrancos, ese desgaste acumulado puede reducir la vida útil de las válvulas a la mitad. Si después de un corte notas pérdida de agua o ruidos en tuberías, llama para revisión.' },
      { q: '¿Cuánto tardan en llegar a Barrancos?', a: 'Para emergencias en Barrancos llegamos en 25-35 minutos con referencia en Avenida General Benjamín Hill. Cubrimos Barrancos y las secciones del INFONAVIT. Atendemos 24/7.' },
      { q: '¿Qué hago si hay una fuga y necesito cortar el agua urgente en Barrancos?', a: 'La llave de paso principal está generalmente junto al medidor de agua, cerca de la banqueta. Ciérrala completamente para cortar el flujo mientras llega el plomero. Si la llave no cierra bien (problema común en casas de 40+ años), llama inmediatamente al 667 392 2273 para atención de emergencia.' }
    ]
  },
  'praderas-del-humaya': {
    faqs: [
      { q: '¿Qué problemas de plomería son más comunes en Praderas del Humaya?', a: 'Praderas del Humaya es un fraccionamiento de interés social desarrollado entre 1990 y 2010 sobre Calle Ley Humaya. Con casas de 15-35 años, los problemas más frecuentes son: sarro en calentadores de paso por el agua dura de JAPAC, válvulas de tinaco que fallan después de 10-20 años, y drenajes obstruidos por grasa acumulada en cocinas de viviendas de uso intensivo.' },
      { q: '¿Por qué hay presión irregular en Praderas del Humaya?', a: 'Praderas del Humaya está en la zona de expansión nororiente de Culiacán, al final de la red de distribución de JAPAC. Las zonas más alejadas de las plantas de tratamiento trabajan con menor presión residual. En horas pico (7-9am, 7-9pm), la presión cae notablemente. Si el problema persiste fuera de horas pico, puede ser la tubería interna o el flotador del tinaco.' },
      { q: '¿Cuánto cuesta revisar y reparar en Praderas del Humaya?', a: 'El diagnóstico es gratuito. Limpieza de sarro en calentador: $400-$800 MXN. Revisión y ajuste de tinaco + válvula: $300-$600 MXN. Destape de drenaje: $500-$1,200 MXN. Para renovación de tubería: presupuesto personalizado gratuito al 667 392 2273.' },
      { q: '¿Cuánto tardan en llegar a Praderas del Humaya?', a: 'Para emergencias llegamos en 25-40 minutos por Calle Ley Humaya. Atendemos 24/7 los 365 días.' },
      { q: '¿Atienden también colonias vecinas de Praderas del Humaya?', a: 'Sí, cubrimos Praderas del Humaya y todo el sector Humaya norte: Lomas del Humaya, Balcones del Humaya, Villas del Humaya y Bosques del Humaya. Llegamos en 25-40 minutos a cualquiera de estas colonias.' }
    ]
  },
  'culiacan-tres-rios': {
    faqs: [
      { q: '¿Por qué hay problemas de plomería en Culiacán Tres Ríos si es un fraccionamiento moderno?', a: 'Culiacán Tres Ríos fue desarrollado entre 1990 y 2010 dentro del Desarrollo Urbano creado en 1991 por decreto del gobernador Labastida Ochoa. Con 15-35 años de antigüedad, el sarro del agua dura de JAPAC ya afecta calentadores de paso y el tránsito constante en el principal distrito corporativo de Culiacán genera alta demanda de agua que reduce la presión en horas pico.' },
      { q: '¿Cuánto cuesta el mantenimiento preventivo en Culiacán Tres Ríos?', a: 'Revisión preventiva completa (calentador, tinaco, válvulas, drenajes): $1,000-$1,800 MXN. Limpieza de sarro en calentador: $400-$800 MXN. Diagnóstico gratuito al 667 392 2273.' },
      { q: '¿Cuánto tardan en llegar a Culiacán Tres Ríos?', a: 'Para emergencias llegamos en 20-30 minutos por Blvd. Pedro Infante / Avenida Tres Ríos. La cercanía al corredor corporativo hace que tengamos presencia frecuente en la zona. Atendemos 24/7.' },
      { q: '¿Atienden también locales comerciales y edificios de oficinas en Culiacán Tres Ríos?', a: 'Sí, atendemos tanto vivienda como locales comerciales, oficinas y edificios corporativos en la zona. Emitimos factura SAT el mismo día para empresas y negocios. Para edificios con varios locales, ofrecemos inspección general y presupuesto global.' },
      { q: '¿Cómo afectan los cortes de JAPAC a las instalaciones de Culiacán Tres Ríos?', a: 'Los cortes y restauraciones generan golpes de ariete que dañan válvulas y uniones de PVC en instalaciones de 15-35 años. Después de un corte programado, revisa que el tinaco llene bien y que no haya ruidos en las tuberías. Una válvula amortiguadora de golpes de ariete en la entrada previene estos daños por $600-$1,200 MXN instalada.' }
    ]
  },
  'lomas-del-humaya': {
    faqs: [
      { q: '¿Qué problemas de plomería son más frecuentes en Lomas del Humaya?', a: 'Lomas del Humaya está en la periferia nororiente de Culiacán sobre Blvd. Constelación, con casas de 15-35 años. Los problemas más frecuentes son sarro en calentadores de paso (el agua dura de JAPAC afecta toda la ciudad desde el primer año), presión irregular por ser zona de expansión lejana de las plantas de tratamiento, y válvulas de tinaco que fallan después de 10-20 años de uso.' },
      { q: '¿Por qué la presión de agua en Lomas del Humaya es baja en las mañanas?', a: 'Lomas del Humaya está en el extremo de la red de distribución de JAPAC. En horas pico (7-9am), cuando toda la zona demanda agua simultáneamente, la presión residual que llega es mínima. Si el problema ocurre también fuera de horas pico, la causa puede ser interna: tubería con sarro, válvula de paso parcialmente cerrada o flotador mal calibrado.' },
      { q: '¿Cuánto tardan en llegar a Lomas del Humaya?', a: 'Para emergencias llegamos en 30-40 minutos por Blvd. Constelación. Atendemos 24/7 los 365 días. Llama al 667 392 2273.' },
      { q: '¿Cuánto cuesta la limpieza del tinaco en Lomas del Humaya?', a: 'Limpieza y revisión de tinaco (vaciado, lavado interior, revisión de flotador y válvula de llenado): $400-$800 MXN dependiendo del tamaño. Si el flotador o la válvula están dañados, el reemplazo agrega $200-$500 MXN adicionales. Recomendamos limpieza cada 1-2 años.' },
      { q: '¿Atienden también Praderas del Humaya y Balcones del Humaya, vecinos de Lomas del Humaya?', a: 'Sí, cubrimos todo el corredor del Humaya norte: Lomas del Humaya, Praderas del Humaya, Balcones del Humaya, Villas del Humaya y Bosques del Humaya. Llegamos en 25-40 minutos a cualquiera de estas colonias.' }
    ]
  },
  'balcones-del-humaya': {
    faqs: [
      { q: '¿Qué problemas son más comunes en Balcones del Humaya?', a: 'Balcones del Humaya es un fraccionamiento moderno (1990-2010) en la ribera del Río Humaya, sector norte de Culiacán. Los problemas más frecuentes son: sarro en calentadores de paso por el agua dura de JAPAC, golpes de ariete por cortes programados de la red, y flotadores de tinaco que fallan después de 10-20 años. La cercanía a los Jardines del Humaya hace de esta una zona bien conocida y de fácil acceso para nosotros.' },
      { q: '¿La cercanía al Río Humaya afecta las cisternas en Balcones del Humaya?', a: 'En temporada de lluvias intensas, las cisternas subterráneas cercanas al río pueden recibir filtración de agua freática si tienen grietas o si el nivel freático sube. Si tu cisterna huele a tierra o el agua tiene turbiedad después de lluvias, solicita inspección antes de usarla. Revisamos y sellamos grietas en cisternas.' },
      { q: '¿Cuánto tardan en llegar a Balcones del Humaya?', a: 'Para emergencias llegamos en 25-35 minutos por Avenida del Humaya. Atendemos 24/7 los 365 días.' },
      { q: '¿Cuánto cuesta el mantenimiento preventivo en Balcones del Humaya?', a: 'Revisión preventiva completa (calentador, tinaco, válvulas, drenajes): $1,000-$1,800 MXN. Limpieza de sarro en calentador por separado: $400-$800 MXN. Diagnóstico inicial gratuito al 667 392 2273.' },
      { q: '¿Atienden también Colinas de la Rivera, colindante con Balcones del Humaya?', a: 'Sí, cubrimos Balcones del Humaya, Colinas de la Rivera, Bosques del Humaya y toda la zona del Humaya norte. Llegamos en 25-35 minutos a cualquiera de estas colonias.' }
    ]
  },
  'campestre-tres-rios': {
    faqs: [
      { q: '¿Por qué hay sarro en las instalaciones de Campestre Tres Ríos si el fraccionamiento es moderno?', a: 'Campestre Tres Ríos está desarrollado sobre Blvd. Alfonso Zaragoza Maytorena, colindante con el Desarrollo Tres Ríos. Con casas de 15-35 años, el agua dura de JAPAC (150-200 mg/L de calcio) ya ha acumulado sarro en calentadores de paso sin mantenimiento. En 10-20 años de uso sin limpieza anual, el sarro puede bloquear el intercambiador completamente.' },
      { q: '¿Cuánto cuesta el mantenimiento anual en Campestre Tres Ríos?', a: 'Revisión preventiva completa (calentador, tinaco, válvulas, drenajes y presión): $1,000-$1,800 MXN. Limpieza de sarro en calentador: $400-$800 MXN. El mantenimiento anual puede triplicar la vida útil del calentador y prevenir emergencias costosas.' },
      { q: '¿Cuánto tardan en llegar a Campestre Tres Ríos?', a: 'Para emergencias llegamos en 25-35 minutos por Blvd. Alfonso Zaragoza Maytorena. La cercanía al corredor Tres Ríos hace que tengamos presencia frecuente en la zona. Atendemos 24/7.' },
      { q: '¿Atienden fraccionamientos cerrados en Campestre Tres Ríos?', a: 'Sí. El residente coordina el acceso con la caseta antes de nuestra llegada. Para emergencias, el residente nos autoriza por WhatsApp para que seguridad permita el ingreso. También gestionamos carta de presentación digital si se requiere.' },
      { q: '¿Atienden también las colonias vecinas del corredor Tres Ríos?', a: 'Sí, cubrimos todo el corredor Tres Ríos: Campestre Tres Ríos, Culiacán Tres Ríos, Jardines Tres Ríos, Floresta Tres Ríos, Los Sabinos Tres Ríos y Lago Tres Ríos. Llegamos en 20-35 minutos a cualquiera.' }
    ]
  },
  'jardines-del-valle': {
    intro: '<strong>Jardines del Valle</strong> es una colonia residencial de Culiacán desarrollada entre <strong>1985 y 2005</strong>, ubicada en la zona poniente de la ciudad. Con viviendas de 20-40 años, la colonia tiene un perfil de clase media consolidada. Las instalaciones hidráulicas de las casas más antiguas ya presentan corrosión en galvanizado, mientras que las más recientes empiezan a mostrar sarro en calentadores de paso por el agua dura que distribuye JAPAC en toda la ciudad.',
    faqs: [
      { q: '¿Qué problemas de plomería son más frecuentes en Jardines del Valle?', a: 'En Jardines del Valle los problemas más comunes son: baja presión por galvanizado corroído en casas de más de 30 años, sarro en calentadores de paso en casas más recientes, y drenajes con grasa acumulada. El diagnóstico gratuito determina cuál es el caso en tu casa.' },
      { q: '¿Cuánto tardan en llegar a Jardines del Valle?', a: 'Para emergencias llegamos en 25-35 minutos. Atendemos toda la colonia 24/7 los 365 días. Llama al 667 392 2273.' },
      { q: '¿Cuánto cuesta cambiar la tubería galvanizada en Jardines del Valle?', a: 'Un baño completo en CPVC: $3,500-$6,000 MXN. Casa mediana (2 baños + cocina): $12,000-$22,000 MXN con mano de obra. Presupuesto gratuito antes de iniciar.' },
      { q: '¿Con qué frecuencia debo dar mantenimiento a la plomería en Jardines del Valle?', a: 'Para casas de 15-25 años: revisión preventiva cada 2 años (calentador, tinaco, válvulas). Para casas de más de 30 años con galvanizado: diagnóstico inmediato para evaluar si ya requiere renovación. El mantenimiento preventivo cuesta 5-10 veces menos que reparar una emergencia.' },
      { q: '¿Atienden también colonias vecinas de Jardines del Valle?', a: 'Sí, cubrimos Jardines del Valle y las colonias aledañas de la zona poniente de Culiacán. Llegamos en 25-40 minutos dependiendo de la ubicación exacta.' }
    ]
  },
  'lomas-de-san-isidro': {
    intro: '<strong>Lomas de San Isidro</strong> es un fraccionamiento residencial de nivel medio-alto en Culiacán, desarrollado entre <strong>1990 y 2010</strong>. Ubicado en la zona sur de la ciudad, incluye subsecciones como Cumbres del Sur y Paseo Azteca. Con viviendas de 15-35 años, la colonia combina modernidad con el reto del agua dura de JAPAC que acumula sarro en calentadores de paso y el desgaste acumulado de válvulas y flotadores de tinaco.',
    faqs: [
      { q: '¿Por qué hay sarro en el calentador si Lomas de San Isidro es un fraccionamiento moderno?', a: 'El sarro lo genera el agua de JAPAC (alta dureza por calcio y magnesio), no la antigüedad de la casa. En Lomas de San Isidro, con casas de 15-35 años, el calentador lleva entre 10 y 30 años acumulando sarro sin mantenimiento. La limpieza anual del intercambiador cuesta $400-$800 MXN y puede triplicar la vida útil del equipo.' },
      { q: '¿Cuánto tardan en llegar a Lomas de San Isidro?', a: 'Para emergencias llegamos en 25-35 minutos. Cubrimos Lomas de San Isidro y sus secciones: Cumbres del Sur y Paseo Azteca. Atendemos 24/7 los 365 días al 667 392 2273.' },
      { q: '¿Cuánto cuesta la revisión preventiva en Lomas de San Isidro?', a: 'Revisión preventiva completa (calentador, tinaco, válvulas y drenajes): $1,000-$1,800 MXN. Diagnóstico inicial gratuito. Si se detectan piezas que requieren reemplazo, cotizamos antes de proceder.' },
      { q: '¿Atienden fraccionamientos cerrados en Lomas de San Isidro?', a: 'Sí. El residente coordina el acceso con seguridad antes de nuestra llegada. Para emergencias nocturnas, el residente nos autoriza por WhatsApp. También gestionamos carta de presentación digital si el fraccionamiento la requiere.' },
      { q: '¿Atienden también las secciones Cumbres del Sur y Paseo Azteca?', a: 'Sí, cubrimos Lomas de San Isidro completo incluyendo las subsecciones Cumbres del Sur y Paseo Azteca. Llegamos en 25-35 minutos a cualquier punto de la colonia.' }
    ]
  },
  'isla-del-oeste': {
    intro: '<strong>Isla del Oeste</strong> es un fraccionamiento residencial de Culiacán desarrollado entre <strong>1990 y 2010</strong>, ubicado en la zona poniente de la ciudad rodeado por el Río Tamazula. Su posición geográfica como "isla" entre cauces fluviales le da características únicas: casas de 15-35 años que deben considerar la humedad del entorno y la posibilidad de variaciones en el nivel freático en temporada de lluvias, además del sarro por el agua dura de JAPAC.',
    faqs: [
      { q: '¿La posición entre ríos de Isla del Oeste afecta las cisternas y la plomería?', a: 'Sí. Al estar rodeada por el Río Tamazula, en temporada de lluvias intensas el nivel freático puede subir y filtrarse en cisternas subterráneas que tengan grietas o sellado deficiente. Si después de lluvias fuertes el agua de tu cisterna tiene turbiedad, olor a tierra o sedimento, solicita inspección antes de usarla.' },
      { q: '¿Qué problemas de plomería son más comunes en Isla del Oeste?', a: 'Los más frecuentes son: sarro en calentadores de paso por el agua dura de JAPAC, válvulas de paso desgastadas por los cortes programados de la red, y en casas con cisterna subterránea: revisión periódica de grietas y sellado. El diagnóstico inicial es gratuito al 667 392 2273.' },
      { q: '¿Cuánto tardan en llegar a Isla del Oeste?', a: 'Para emergencias llegamos en 25-35 minutos considerando los accesos disponibles a la zona. Atendemos 24/7 los 365 días.' },
      { q: '¿Cuánto cuesta revisar y sellar una cisterna subterránea en Isla del Oeste?', a: 'La inspección de cisterna (incluyendo revisión de grietas, sellado y sistema de flotador) está entre $600 y $1,500 MXN dependiendo del tamaño y el estado. Si requiere reparación de grietas, el costo adicional varía entre $800 y $3,000 MXN según la extensión del daño.' },
      { q: '¿Atienden también las colonias vecinas de Isla del Oeste?', a: 'Sí, cubrimos Isla del Oeste y las colonias aledañas de la zona poniente de Culiacán. Llegamos en 25-40 minutos dependiendo de la ubicación.' }
    ]
  },
  'fovissste': {
    intro: '<strong>FOVISSSTE Culiacán</strong> es un conjunto habitacional desarrollado en los años <strong>80</strong> para trabajadores al servicio del Estado, con viviendas de 35-45 años de antigüedad. Como fraccionamiento de interés social de esa época, las instalaciones hidráulicas originales en galvanizado nunca se renovaron integralmente. El agua dura de JAPAC aceleró el deterioro interno de las tuberías, generando baja presión crónica, agua herrumbrosa y calentadores con sarro acumulado.',
    faqs: [
      { q: '¿Por qué hay baja presión y agua con color en FOVISSSTE Culiacán?', a: 'Las viviendas de FOVISSSTE de los años 80 tienen tubería galvanizada de 35-45 años que nunca se renovó. El galvanizado se corroe internamente por el agua dura de JAPAC, reduciendo el diámetro útil y desprendiendo partículas de óxido que colorean el agua. Es el deterioro natural de instalaciones de esa época.' },
      { q: '¿Cuánto cuesta renovar la plomería en una vivienda de FOVISSSTE?', a: 'Para viviendas de interés social ofrecemos opciones escalonadas: baño principal en CPVC: $2,800-$4,500 MXN. Cocina: $1,500-$2,500 MXN. Renovación completa (baño + cocina): $6,000-$10,000 MXN con mano de obra. Aceptamos pagos en parcialidades. Presupuesto gratuito al 667 392 2273.' },
      { q: '¿Cuánto tardan en llegar a FOVISSSTE?', a: 'Para emergencias llegamos en 25-35 minutos. Atendemos 24/7 los 365 días. Llama al 667 392 2273.' },
      { q: '¿Qué hago si el agua sale con mucho óxido en FOVISSSTE?', a: 'Como medida inmediata, deja correr el agua durante 2-3 minutos para desalojar el óxido acumulado en el tramo más cercano. Para cocinar y beber usa agua embotellada mientras no se resuelva. El agua herrumbrosa indica que la tubería galvanizada ya está fallando — llama para diagnóstico gratuito.' },
      { q: '¿Atienden también FOVISSSTE Diamante, FOVISSSTE Abelardo y FOVISSSTE Humaya?', a: 'Sí, cubrimos todas las secciones de FOVISSSTE en Culiacán: Diamante, Abelardo de la Torre, Humaya y demás. Llegamos en 25-40 minutos dependiendo de la sección.' }
    ]
  },
  'villas-del-humaya': {
    intro: '<strong>Villas del Humaya</strong> es un fraccionamiento residencial de Culiacán desarrollado entre <strong>1995 y 2010</strong>, ubicado en la zona norte de la ciudad sobre la ribera del Río Humaya. Con viviendas de 15-30 años, la colonia combina modernidad relativa con los retos del agua dura de JAPAC: sarro en calentadores de paso y desgaste en válvulas por los cortes programados de la red.',
    faqs: [
      { q: '¿Qué problemas de plomería son más comunes en Villas del Humaya?', a: 'Los más frecuentes son: sarro en calentadores de paso por el agua dura de JAPAC (afecta toda Culiacán desde el primer año de uso), válvulas de tinaco desgastadas, y golpes de ariete por cortes de JAPAC que dañan uniones de PVC. En casas con cisterna cerca del nivel del suelo, también puede haber filtración en temporada de lluvias intensas.' },
      { q: '¿Cuánto tardan en llegar a Villas del Humaya?', a: 'Para emergencias llegamos en 25-35 minutos. Cubrimos Villas del Humaya y el resto del sector norte del Humaya. Atendemos 24/7 los 365 días al 667 392 2273.' },
      { q: '¿Cuánto cuesta la limpieza de sarro en calentador en Villas del Humaya?', a: 'Limpieza ácida del intercambiador del calentador de paso: $400-$800 MXN dependiendo del modelo. Si el calentador ya tiene daño irreversible, el reemplazo con instalación está entre $3,500 y $8,000 MXN.' },
      { q: '¿Con qué frecuencia debo hacer mantenimiento en Villas del Humaya?', a: 'Para casas de 15-30 años: revisión preventiva cada 2 años. La limpieza anual del calentador y la revisión del tinaco y válvulas previenen la mayoría de las emergencias. Una revisión completa cuesta entre $1,000 y $1,800 MXN.' },
      { q: '¿Atienden también Lomas del Humaya y Balcones del Humaya, vecinas de Villas del Humaya?', a: 'Sí, cubrimos todo el sector norte del Humaya: Villas del Humaya, Lomas del Humaya, Balcones del Humaya, Praderas del Humaya y Bosques del Humaya. Llegamos en 25-40 minutos a cualquiera.' }
    ]
  },
  'portales-del-rio': {
    intro: '<strong>Portales del Río</strong> es un fraccionamiento residencial de Culiacán desarrollado entre <strong>1995 y 2010</strong>, ubicado en la zona norponiente de la ciudad a orillas del Río Humaya. Con viviendas de 15-30 años, combina la modernidad de sus construcciones con el agua dura de JAPAC que ya acumula sarro en calentadores de paso, y la exposición fluvial que requiere atención especial en cisternas y conexiones externas.',
    faqs: [
      { q: '¿La cercanía al Río Humaya afecta la plomería en Portales del Río?', a: 'La cercanía al río no afecta las tuberías internas, pero sí las cisternas subterráneas y conexiones externas. En temporadas de lluvia intensa, el nivel freático puede subir y filtrar agua en cisternas con grietas o sellado deteriorado. Si el agua de tu cisterna tiene turbiedad u olor a tierra después de lluvias, solicita inspección al 667 392 2273.' },
      { q: '¿Qué problemas son más comunes en Portales del Río?', a: 'Los más frecuentes son: sarro en calentadores de paso por el agua dura de JAPAC, válvulas de paso desgastadas por los cortes programados de la red, y en casas con cisterna: revisión periódica de integridad. El diagnóstico es gratuito.' },
      { q: '¿Cuánto tardan en llegar a Portales del Río?', a: 'Para emergencias llegamos en 25-35 minutos. Atendemos 24/7 los 365 días al 667 392 2273.' },
      { q: '¿Cuánto cuesta el mantenimiento preventivo en Portales del Río?', a: 'Revisión completa (calentador, tinaco, válvulas y drenajes): $1,000-$1,800 MXN. Diagnóstico inicial gratuito. Si se detectan piezas que requieren cambio, cotizamos antes de proceder.' },
      { q: '¿Atienden también colonias vecinas de Portales del Río?', a: 'Sí, cubrimos Portales del Río y las colonias aledañas de la zona norponiente: Haciendas del Río, Riberas del Humaya, Jardines del Valle y Colinas del Tamazula. Llegamos en 25-40 minutos.' }
    ]
  },
  'jardines-tres-rios': {
    intro: '<strong>Jardines Tres Ríos</strong> es un fraccionamiento residencial de Culiacán desarrollado entre <strong>1995 y 2010</strong> dentro del corredor del Desarrollo Urbano Tres Ríos. Con viviendas de 15-30 años, la zona concentra el crecimiento más moderno de Culiacán pero ya enfrenta el reto del agua dura de JAPAC: sarro en calentadores y tuberías, y desgaste de válvulas por los cortes programados de la red en una zona de alta demanda.',
    faqs: [
      { q: '¿Por qué hay sarro en instalaciones tan nuevas de Jardines Tres Ríos?', a: 'El sarro lo genera la dureza del agua de JAPAC (150-200 mg/L de calcio y magnesio), no la antigüedad. En Jardines Tres Ríos, con casas de 15-30 años, el sarro lleva entre 10 y 25 años acumulándose en calentadores, tinacos y válvulas sin mantenimiento. La limpieza anual del calentador previene la mayoría de las fallas.' },
      { q: '¿Cuánto tardan en llegar a Jardines Tres Ríos?', a: 'Para emergencias llegamos en 25-35 minutos. La cercanía al corredor Tres Ríos nos permite estar en la zona con frecuencia. Atendemos 24/7 los 365 días.' },
      { q: '¿Cuánto cuesta el mantenimiento preventivo en Jardines Tres Ríos?', a: 'Revisión completa (calentador, tinaco, válvulas y drenajes): $1,000-$1,800 MXN. Limpieza de sarro en calentador por separado: $400-$800 MXN. Diagnóstico gratuito al 667 392 2273.' },
      { q: '¿Atienden fraccionamientos cerrados en Jardines Tres Ríos?', a: 'Sí. El residente coordina el acceso con seguridad antes de nuestra llegada. Para emergencias nocturnas, el residente nos autoriza por WhatsApp para que seguridad permita el ingreso.' },
      { q: '¿Atienden también Floresta Tres Ríos y Campestre Tres Ríos, vecinas de Jardines Tres Ríos?', a: 'Sí, cubrimos todo el corredor: Jardines Tres Ríos, Floresta Tres Ríos, Campestre Tres Ríos, Los Sabinos Tres Ríos, Culiacán Tres Ríos y Lago Tres Ríos. Llegamos en 20-35 minutos a cualquiera.' }
    ]
  },
  'floresta-tres-rios': {
    intro: '<strong>Floresta Tres Ríos</strong> es un fraccionamiento residencial de Culiacán desarrollado entre <strong>1995 y 2010</strong> en el corredor del Desarrollo Urbano Tres Ríos. Con viviendas de 15-30 años, es parte de la zona de mayor crecimiento y plusvalía de la ciudad. A pesar de su modernidad, el agua dura de JAPAC ya acumula sarro en calentadores de paso y los cortes programados generan desgaste en válvulas y uniones de PVC.',
    faqs: [
      { q: '¿Qué problemas son más comunes en Floresta Tres Ríos?', a: 'En Floresta Tres Ríos los problemas más frecuentes son: sarro en calentadores de paso (15-25 años acumulando sin mantenimiento), válvulas de tinaco que fallan después de 15-20 años, y golpes de ariete por cortes de JAPAC que dañan uniones de PVC. El diagnóstico gratuito determina el estado específico de tu instalación.' },
      { q: '¿Cuánto tardan en llegar a Floresta Tres Ríos?', a: 'Para emergencias llegamos en 25-35 minutos. La cercanía al corredor Tres Ríos nos permite presencia frecuente en la zona. Atendemos 24/7 los 365 días.' },
      { q: '¿Cuánto cuesta el mantenimiento anual en Floresta Tres Ríos?', a: 'Revisión completa (calentador, tinaco, válvulas y drenajes): $1,000-$1,800 MXN. Limpieza de sarro en calentador: $400-$800 MXN. El mantenimiento anual previene emergencias costosas y puede triplicar la vida útil del calentador.' },
      { q: '¿Atienden fraccionamientos cerrados en Floresta Tres Ríos?', a: 'Sí. El residente coordina el acceso con la caseta de seguridad. Para emergencias, el residente nos autoriza por WhatsApp. Gestionamos carta de presentación digital si se requiere.' },
      { q: '¿Atienden también Jardines Tres Ríos y Campestre Tres Ríos, vecinas de Floresta?', a: 'Sí, cubrimos todo el corredor Tres Ríos: Floresta, Jardines, Campestre, Los Sabinos, Culiacán Tres Ríos y Lago Tres Ríos. Llegamos en 20-35 minutos a cualquiera.' }
    ]
  },
  'los-laureles': {
    intro: '<strong>Los Laureles</strong> es una colonia residencial de Culiacán desarrollada entre <strong>1975 y 1995</strong>, con viviendas de 30-50 años de antigüedad. Ubicada en la zona poniente de la ciudad, combina casas de clase media con un ambiente consolidado. Las instalaciones más antiguas ya presentan corrosión en galvanizado, mientras que las de los 90s muestran sarro acumulado en calentadores de paso por el agua dura que distribuye JAPAC.',
    faqs: [
      { q: '¿Qué problemas son más frecuentes en Los Laureles?', a: 'En Los Laureles los problemas varían según la época de construcción: en casas de más de 35 años (1975-1990), el principal problema es el galvanizado corroído que genera baja presión y fugas ocultas. En casas de los 90s, el sarro en calentadores y válvulas desgastadas son los más frecuentes. El diagnóstico gratuito determina cuál es tu caso.' },
      { q: '¿Cuánto cuesta cambiar la tubería galvanizada en Los Laureles?', a: 'Un baño completo en CPVC cuesta $3,500-$6,000 MXN. Casa mediana (2 baños + cocina): $12,000-$22,000 MXN con mano de obra. Para casas de los 90s con tubería PVC en buen estado, a veces solo se requiere limpieza de sarro y revisión de válvulas: $800-$1,800 MXN.' },
      { q: '¿Cuánto tardan en llegar a Los Laureles?', a: 'Para emergencias llegamos en 25-35 minutos. Atendemos toda la colonia 24/7 los 365 días al 667 392 2273.' },
      { q: '¿Cuándo debo renovar la tubería en una casa de Los Laureles?', a: 'Si tu casa tiene más de 35 años con galvanizado original, ya superó su vida útil y el cambio es necesario — es cuestión de cuándo, no de si. Si tiene entre 20 y 35 años, un diagnóstico determina si la tubería está bien o ya requiere renovación. Diagnóstico gratuito al 667 392 2273.' },
      { q: '¿Atienden también colonias vecinas de Los Laureles?', a: 'Sí, cubrimos Los Laureles y las colonias aledañas de la zona poniente. Llegamos en 25-40 minutos dependiendo de la ubicación exacta.' }
    ]
  },
  'hacienda-del-valle': {
    intro: '<strong>Hacienda del Valle</strong> es un fraccionamiento residencial de nivel medio-alto en Culiacán, desarrollado entre <strong>1995 y 2010</strong>. Con viviendas de 15-30 años, la colonia combina amplias residencias con el reto del agua dura de JAPAC que ya acumula sarro en calentadores de paso, sistemas de cisterna y bombas de presión. Los sistemas hidroneumáticos más antiguos del fraccionamiento están llegando al final de su primer ciclo de vida útil.',
    faqs: [
      { q: '¿Por qué fallan los sistemas de presión en Hacienda del Valle?', a: 'Las residencias de Hacienda del Valle con más de 20 años tienen sistemas hidroneumáticos o de cisterna-bomba que están llegando al final de su primer ciclo. La membrana del hidroneumático pierde elasticidad, la bomba se desgasta y el sistema ya no mantiene presión constante. Señales: presión irregular, bomba que arranca y para en ciclos muy cortos, o agua que sale a chorros y luego débil.' },
      { q: '¿Cuánto cuesta reemplazar el sistema hidroneumático en Hacienda del Valle?', a: 'El reemplazo de un hidroneumático residencial varía entre $8,000 y $18,000 MXN dependiendo de la capacidad y la potencia requerida. Si solo necesita mantenimiento (cambio de membrana y presostato): $2,000-$5,000 MXN. Revisión y diagnóstico gratuitos al 667 392 2273.' },
      { q: '¿Cuánto tardan en llegar a Hacienda del Valle?', a: 'Para emergencias llegamos en 25-35 minutos. Atendemos 24/7 los 365 días. Si el fraccionamiento tiene caseta de seguridad, el residente coordina el acceso antes de nuestra llegada.' },
      { q: '¿Atienden albercas y sistemas de riego en Hacienda del Valle?', a: 'Sí, además de plomería hidráulica y sanitaria atendemos: bombas de alberca, sistemas de recirculación, riego automatizado (solenoides, aspersores, programadores) y sistemas de presión para jardines. También instalamos suavizadores de agua para reducir el sarro en toda la instalación.' },
      { q: '¿Cuánto cuesta el mantenimiento anual en Hacienda del Valle?', a: 'Revisión preventiva completa (calentador, cisterna, sistema de presión, válvulas y drenajes): $1,500-$3,000 MXN dependiendo del tamaño de la propiedad. El mantenimiento anual previene el 80% de las emergencias. Diagnóstico gratuito al 667 392 2273.' }
    ]
  },
  'santa-clara': {
    faqs: [
      { q: '¿Qué problemas de plomería son más frecuentes en Santa Clara?', a: 'Santa Clara es un fraccionamiento con casas de 15-35 años. Los problemas más comunes son: sarro en calentadores de paso por el agua dura de JAPAC, válvulas de tinaco desgastadas y golpes de ariete por cortes programados de la red que dañan uniones de PVC. El diagnóstico gratuito determina el estado específico de tu instalación.' },
      { q: '¿Por qué se acumula sarro en Santa Clara si las casas son relativamente nuevas?', a: 'El sarro lo genera la dureza del agua de JAPAC (alta concentración de calcio y magnesio), no la antigüedad de la casa. Con 15-35 años de uso sin mantenimiento, el intercambiador del calentador ya tiene sarro significativo. La limpieza anual cuesta $400-$800 MXN y puede triplicar la vida útil del equipo.' },
      { q: '¿Cuánto tardan en llegar a Santa Clara?', a: 'Para emergencias llegamos en 25-35 minutos. Atendemos 24/7 los 365 días. Llama al 667 392 2273.' },
      { q: '¿Cuánto cuesta el mantenimiento preventivo en Santa Clara?', a: 'Revisión completa (calentador, tinaco, válvulas y drenajes): $1,000-$1,800 MXN. Diagnóstico inicial gratuito. Limpieza de sarro en calentador por separado: $400-$800 MXN.' },
      { q: '¿Atienden también colonias cercanas a Santa Clara?', a: 'Sí, cubrimos Santa Clara y las colonias aledañas. Llegamos en 25-40 minutos dependiendo de la ubicación exacta.' }
    ]
  },
  'residencial-san-jose': {
    intro: '<strong>Residencial San José</strong> es un fraccionamiento de nivel medio-alto en Culiacán, desarrollado entre <strong>1990 y 2010</strong>. Con viviendas de 15-35 años, combina la modernidad de sus construcciones con el reto del agua dura de JAPAC que acumula sarro en calentadores y tuberías, y el desgaste acumulado en válvulas por los cortes programados de la red.',
    faqs: [
      { q: '¿Qué problemas son más comunes en Residencial San José?', a: 'Los más frecuentes son: sarro en calentadores de paso (15-35 años acumulando sin mantenimiento), válvulas de tinaco que fallan después de 15-20 años, y presión irregular en horas pico. El diagnóstico gratuito determina el estado específico de tu instalación.' },
      { q: '¿Cuánto tardan en llegar a Residencial San José?', a: 'Para emergencias llegamos en 25-35 minutos. Atendemos 24/7 los 365 días al 667 392 2273.' },
      { q: '¿Cuánto cuesta la revisión preventiva en Residencial San José?', a: 'Revisión completa (calentador, tinaco, válvulas y drenajes): $1,000-$1,800 MXN. Diagnóstico inicial gratuito. Si se detectan piezas que requieren cambio, cotizamos antes de proceder.' },
      { q: '¿Atienden fraccionamientos cerrados en Residencial San José?', a: 'Sí. El residente coordina el acceso con la caseta de seguridad antes de nuestra llegada. Para emergencias nocturnas, el residente nos autoriza por WhatsApp.' },
      { q: '¿Por qué debo hacer mantenimiento preventivo en Residencial San José si la casa es nueva?', a: 'El agua de JAPAC tiene alta dureza y afecta las instalaciones desde el primer año. Sin mantenimiento cada 2 años, el sarro puede bloquear el calentador en 10-15 años, las válvulas se calcifican y los flotadores de tinaco pierden calibración. Una revisión preventiva cuesta 5-10 veces menos que atender una emergencia.' }
    ]
  }
};

function buildFaqHtml(coloniaName, faqs) {
  const items = faqs.map(f => `
  <details style="background:#fff;border-radius:12px;padding:1.25rem 1.5rem;box-shadow:0 2px 8px rgba(0,0,0,0.07);cursor:pointer;">
    <summary style="font-weight:700;font-size:1rem;color:#0c4a6e;list-style:none;">${f.q}</summary>
    <p style="margin-top:0.75rem;color:#475569;">${f.a}</p>
  </details>`).join('\n');
  return `<section class="section"><div class="container">
<h2>Preguntas Frecuentes — Plomero en ${coloniaName}</h2>
<div style="margin-top:1.5rem;display:grid;gap:1rem;">${items}
</div>
</div></section>\n\n`;
}

function buildFaqSchema(faqs) {
  return `,\n    {\n      "@type": "FAQPage",\n      "mainEntity": [\n${faqs.map(f =>
    `        {\n          "@type": "Question",\n          "name": ${JSON.stringify(f.q)},\n          "acceptedAnswer": {\n            "@type": "Answer",\n            "text": ${JSON.stringify(f.a)}\n          }\n        }`
  ).join(',\n')}\n      ]\n    }`;
}

const displayNames = {
  'bugambilias': 'Bugambilias', 'santa-fe': 'Santa Fe', 'las-palmas': 'Las Palmas',
  'bosques-del-humaya': 'Bosques del Humaya', 'amorada': 'Amorada', 'altamira': 'Altamira',
  'colinas-de-la-rivera': 'Colinas de la Rivera', 'villa-universidad': 'Villa Universidad',
  'nuevo-culiacan': 'Nuevo Culiacán', 'libertad': 'Libertad', 'barrancos': 'Barrancos',
  'praderas-del-humaya': 'Praderas del Humaya', 'culiacan-tres-rios': 'Culiacán Tres Ríos',
  'lomas-del-humaya': 'Lomas del Humaya', 'balcones-del-humaya': 'Balcones del Humaya',
  'campestre-tres-rios': 'Campestre Tres Ríos', 'jardines-del-valle': 'Jardines del Valle',
  'lomas-de-san-isidro': 'Lomas de San Isidro', 'isla-del-oeste': 'Isla del Oeste',
  'fovissste': 'FOVISSSTE', 'villas-del-humaya': 'Villas del Humaya',
  'portales-del-rio': 'Portales del Río', 'jardines-tres-rios': 'Jardines Tres Ríos',
  'floresta-tres-rios': 'Floresta Tres Ríos', 'los-laureles': 'Los Laureles',
  'hacienda-del-valle': 'Hacienda del Valle', 'santa-clara': 'Santa Clara',
  'residencial-san-jose': 'Residencial San José'
};

let ok = 0, skip = 0, err = 0;

for (const [slug, data] of Object.entries(colonias)) {
  const filePath = path.join(BASE, slug, 'index.html');
  if (!fs.existsSync(filePath)) { console.log(`❌ No existe: ${slug}`); err++; continue; }
  let html = fs.readFileSync(filePath, 'utf-8');
  if (html.includes('"FAQPage"')) { console.log(`⏭️  Ya tiene FAQ: ${slug}`); skip++; continue; }

  const name = displayNames[slug] || slug;

  if (data.intro && !html.includes('colonia-intro-unico')) {
    const introHtml = `\n<section class="section section-alt"><div class="container">\n<p class="colonia-intro-unico">${data.intro}</p>\n</div></section>\n`;
    html = html.replace('<section class="section">', introHtml + '<section class="section">');
  }

  html = html.replace('<section id="contacto"', buildFaqHtml(name, data.faqs) + '<section id="contacto"');
  html = html.replace(/(\s*\]\s*\}\s*<\/script>)/, buildFaqSchema(data.faqs) + '\n  ]\n}\n</script>');

  fs.writeFileSync(filePath, html, 'utf-8');
  console.log(`✅ ${slug}`);
  ok++;
}

console.log(`\nResultado: ${ok} enriquecidas · ${skip} ya tenían FAQ · ${err} errores`);
