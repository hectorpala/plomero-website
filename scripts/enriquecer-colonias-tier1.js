const fs = require('fs');
const path = require('path');

const BASE = '/Users/openclaw/Sitios Web/Plomero Culiacán/servicios/plomero-colonias-culiacan';

const colonias = {
  'tres-rios': {
    faqs: [
      {
        q: '¿Por qué los edificios de Tres Ríos construidos en los 90s ya tienen fugas si son "relativamente nuevos"?',
        a: 'Las torres y fraccionamientos de Tres Ríos levantados entre 1991 y 1995 tienen más de 30 años. Las tuberías de cobre y galvanizado originales ya alcanzaron su vida útil: el cobre desarrolla picaduras por el agua dura de JAPAC y el galvanizado se corroe internamente. Una fuga oculta dentro de una losa de concreto puede acumular humedad durante meses antes de manifestarse en el techo del piso inferior.'
      },
      {
        q: '¿Cómo afectan los cortes de la Planta Isleta a los edificios de Tres Ríos?',
        a: 'La Planta Isleta abastece gran parte de Tres Ríos. Cuando opera al 60% de capacidad (como ocurrió en octubre de 2023), la presión en los pisos superiores cae drásticamente. Al restaurarse el servicio, el golpe de ariete puede dañar válvulas de paso, uniones de PVC y membranas de hidroneumáticos, especialmente en edificios con sistemas de presión de 20-30 años de uso.'
      },
      {
        q: '¿Por qué tengo baja presión en los pisos altos de mi edificio de Tres Ríos?',
        a: 'En edificios de Tres Ríos de los 90s, la causa más común es el desgaste del hidroneumático: la membrana pierde elasticidad y la bomba ya no empuja el agua con suficiente fuerza hacia los pisos superiores. También puede ser por válvulas de alivio o flotadores mal calibrados en el tinaco o cisterna. Diagnosticamos sin costo antes de recomendar cambios.'
      },
      {
        q: '¿Cuánto cuesta reparar una fuga oculta en un departamento de Tres Ríos?',
        a: 'El diagnóstico con geófono es gratuito. La reparación de una fuga en losa o muro varía entre $800 y $2,500 MXN dependiendo de la accesibilidad y el tipo de tubería. Trabajamos con mínima demolición y dejamos el acabado lo más cercano al original. Llama al 667 392 2273 para cotización exacta.'
      },
      {
        q: '¿Atienden emergencias en el Forum Culiacán y edificios corporativos de Tres Ríos?',
        a: 'Sí, atendemos tanto vivienda como locales comerciales, oficinas corporativas y edificios de uso mixto en toda la zona de Tres Ríos — incluyendo el corredor del Forum Culiacán, Blvd. Enrique Sánchez Alonso y Blvd. Rotarismo. Emitimos factura SAT para negocios y administradores de edificio.'
      }
    ]
  },
  'chapultepec': {
    faqs: [
      {
        q: '¿Por qué Chapultepec tiene más problemas de plomería que colonias nuevas?',
        a: 'Chapultepec fue fundada en 1950 y muchas casas conservan sus tuberías galvanizadas originales de los años 70-80, que nunca se renovaron integralmente. Con 35-55 años de uso y el agua dura de JAPAC, el galvanizado se corroe por dentro: el diámetro útil se reduce hasta la mitad, causando baja presión crónica y fugas ocultas en muros. Es el ciclo de vida normal de esos materiales, no un defecto de construcción.'
      },
      {
        q: '¿El agua con olor o color en mi casa de Chapultepec es peligrosa?',
        a: 'El agua herrumbrosa en Chapultepec es señal de corrosión interna avanzada en la tubería galvanizada. El óxido en sí no es acutamente tóxico, pero indica que la tubería está fallando y las fugas son inminentes. Recomendamos no usar esa agua para cocinar o beber hasta reemplazar la tubería. Llama al 667 392 2273 para diagnóstico urgente.'
      },
      {
        q: '¿Cuánto cuesta renovar la tubería en una casa de Chapultepec?',
        a: 'El cambio de un baño completo (regadera, lavabo, WC) a tubería CPVC está entre $3,500 y $6,000 MXN. Una casa mediana de Chapultepec (2 baños + cocina) varía entre $12,000 y $22,000 MXN con mano de obra incluida. Damos presupuesto detallado sin costo antes de iniciar al 667 392 2273.'
      },
      {
        q: '¿Cuánto tiempo tardan en llegar a Chapultepec en una emergencia?',
        a: 'Para emergencias en Chapultepec llegamos en 25-35 minutos desde que confirmas por WhatsApp. Conocemos las calles principales sobre Blvd. Jesús Rodolfo Acedo y las internas. Atendemos 24/7 incluyendo madrugadas y días festivos.'
      },
      {
        q: '¿Puedo reparar solo la tubería que tiene fuga o debo cambiar toda la instalación?',
        a: 'Si la casa tiene más de 40 años con galvanizado original, reparar solo el tramo con fuga es un parche temporal — en 6-12 meses fallará otro punto. Te damos un diagnóstico honesto: si el resto de la tubería está en buen estado, reparamos el tramo; si el deterioro es generalizado, te recomendamos el cambio completo para evitar pagar varias veces.'
      }
    ]
  },
  'centro': {
    faqs: [
      {
        q: '¿Por qué las casas del Centro de Culiacán tienen varios tipos de tubería mezclados?',
        a: 'Las casas del Centro fueron construidas antes de 1960 y se ampliaron generación tras generación. Cada ampliación usó el material disponible en su época: galvanizado en los 50-60, cobre en los 70, PVC en los 80-90. El resultado es una instalación con tres materiales distintos conectados entre sí, lo que genera corrosión galvánica en las uniones y fugas crónicas en esos puntos de contacto.'
      },
      {
        q: '¿Qué es la corrosión galvánica y por qué es tan común en el Centro?',
        a: 'La corrosión galvánica ocurre cuando dos metales distintos (galvanizado y cobre, por ejemplo) se conectan directamente con agua como electrolito. El metal más "activo" se corroe aceleradamente. En el Centro de Culiacán, donde conviven instalaciones de tres épocas distintas, este fenómeno es la causa más frecuente de fugas en las uniones entre tramos de tubería de diferentes materiales.'
      },
      {
        q: '¿Se puede reparar un drenaje de barro vidriado o hay que reemplazarlo?',
        a: 'Los drenajes de barro vidriado originales del Centro pueden durar décadas más si están íntegros, pero cuando se fracturan o acumulan sedimento en las juntas ya no se pueden reparar con parches. La solución definitiva es reemplazarlos con tubería PVC. Realizamos la excavación, retiro del barro vidriado y reposición del drenaje minimizando daños en pisos y muros históricos.'
      },
      {
        q: '¿Atienden locales comerciales y edificios en el Centro histórico de Culiacán?',
        a: 'Sí, atendemos vivienda, locales comerciales, edificios de oficinas y propiedades históricas en toda la zona del Centro. Emitimos factura SAT el mismo día. Para intervenciones en edificios con valor histórico, trabajamos con mínima demolición y acabados compatibles con la construcción original.'
      },
      {
        q: '¿Cuánto cuesta modernizar completamente la plomería de una casa del Centro?',
        a: 'Depende del tamaño y la complejidad de la instalación existente. Como referencia: reemplazar una red hidráulica completa en una casa mediana del Centro (2 baños + cocina) con tubería CPVC nueva está entre $15,000 y $30,000 MXN, incluyendo mano de obra y materiales. Antes de cualquier trabajo, damos diagnóstico gratuito y presupuesto detallado al 667 392 2273.'
      }
    ]
  },
  'guadalupe': {
    faqs: [
      {
        q: '¿Por qué el agua sale con color herrumbroso en Guadalupe?',
        a: 'En las casas de Guadalupe — muchas construidas en los años 40-60 — el agua herrumbrosa es señal de corrosión avanzada en la tubería galvanizada o de asbesto original. El óxido que se desprende de las paredes internas de la tubería le da ese color característico. Es una señal de que la tubería ya está fallando y las fugas son inminentes. No uses esa agua para cocinar o beber.'
      },
      {
        q: '¿Es seguro seguir usando tubería de asbesto en Guadalupe?',
        a: 'Las tuberías de asbesto-cemento usadas en redes de agua potable no representan riesgo de asbesto en el agua, ya que el material está mineralizado. Sin embargo, después de 70+ años están físicamente deterioradas: presentan fracturas, filtraciones y conexiones que ya no sellan correctamente. El riesgo real es de fugas estructurales, no de salud por asbesto. Igualmente, el reemplazo es la solución definitiva.'
      },
      {
        q: '¿Cuánto cuesta renovar completamente la plomería en una casa de Guadalupe?',
        a: 'Para las casas antiguas de Guadalupe, el rango es de $15,000 a $35,000 MXN para una renovación completa (red hidráulica + drenajes) dependiendo del tamaño. Si solo se renueva la red hidráulica (sin drenajes), el costo baja a $10,000-$22,000 MXN. Damos presupuesto gratuito con visita al 667 392 2273.'
      },
      {
        q: '¿Cuánto tardan en llegar a Guadalupe desde que llamo?',
        a: 'Para emergencias en Guadalupe llegamos en 25-35 minutos. Conocemos bien la colonia — sus calles con nombres de ríos sinaloenses (Río Mocorito, Río Zuaque, Río Sinaloa) y las referencias de la Parroquia Nuestra Señora de Guadalupe y la IMSS Clínica 35. Atendemos 24/7 los 365 días.'
      },
      {
        q: '¿Hay riesgo de daño estructural si no arreglo las fugas en una casa de 70 años en Guadalupe?',
        a: 'Sí. Las fugas ocultas en muros y losas de casas de 70+ años humedecen el tabique y el concreto durante meses o años antes de hacerse visibles. Esa humedad sostenida debilita la estructura, genera hongos y, en casos extremos, puede comprometer la integridad de muros y cimientos. Si detectas manchas de humedad o el agua sube en las paredes, llama de inmediato al 667 392 2273.'
      }
    ]
  },
  'bachigualato': {
    faqs: [
      {
        q: '¿Por qué las casas de Bachigualato tienen instalaciones tan variadas y complicadas?',
        a: 'Bachigualato es uno de los barrios más antiguos de Culiacán — su ejido fue creado por decreto de Lázaro Cárdenas en 1937. Las casas se construyeron y ampliaron en distintas épocas: galvanizado en los 50-60, cobre en los 70, PVC en los 80-90. Cada ampliación usó los materiales de su momento, generando instalaciones heterogéneas donde la corrosión galvánica en las uniones es el problema más frecuente.'
      },
      {
        q: '¿Qué zonas de Bachigualato atienden?',
        a: 'Atendemos toda la colonia Bachigualato y sus alrededores: desde Calzada Aeropuerto hasta Carretera a Navolato km 4.5, incluyendo las zonas residenciales, comerciales y la zona cercana al Aeropuerto Internacional de Culiacán. Llegamos en 25-35 minutos en cualquier horario, 24/7.'
      },
      {
        q: '¿El drenaje de barro vidriado se puede limpiar o hay que reemplazarlo?',
        a: 'Si el drenaje de barro vidriado tiene más de 40 años, la limpieza con sonda es un alivio temporal — las juntas entre piezas ya no sellan correctamente y las raíces eventualmente vuelven a penetrar. La solución definitiva es reemplazar el tramo afectado con PVC. Diagnosticamos con cámara o sonda antes de recomendar limpieza o reemplazo.'
      },
      {
        q: '¿Qué riesgo tiene ignorar una fuga en una casa de 60 años en Bachigualato?',
        a: 'En casas de 60+ años, una fuga ignorada humedece el tabique y el concreto de manera continua. A los 3-6 meses aparecen manchas, hongos y eflorescencias. A largo plazo, puede comprometer la integridad de muros y losas. En Bachigualato, donde muchas casas fueron construidas con tabique artesanal, el riesgo estructural es mayor que en construcciones modernas. Una detección temprana puede ahorrarte decenas de miles de pesos.'
      },
      {
        q: '¿Atienden también las colonias cercanas a Bachigualato como Altos de Bachigualato?',
        a: 'Sí, nuestra cobertura incluye Bachigualato, Altos de Bachigualato, Nuevo Bachigualato y todas las colonias aledañas sobre la Calzada Aeropuerto y la carretera a Navolato. Llegamos en 25-35 minutos con diagnóstico gratuito.'
      }
    ]
  },
  'humaya': {
    faqs: [
      {
        q: '¿Por qué hay tanta baja presión de agua cerca de Los Jardines del Humaya?',
        a: 'Las casas de la colonia Humaya tienen entre 50 y 60 años de antigüedad con instalaciones galvanizadas que nunca se renovaron. El galvanizado se corroe internamente por el agua dura de JAPAC, reduciendo el diámetro útil de la tubería hasta en un 60%. Esto, combinado con los cortes programados de JAPAC que generan fluctuaciones de presión, causa la baja presión crónica que reportan muchos vecinos de la zona.'
      },
      {
        q: '¿Por qué mi calentador de paso falla tan seguido en Humaya?',
        a: 'El agua que distribuye JAPAC en Humaya tiene alto contenido de calcio y magnesio. Ese sarro se acumula en el intercambiador del calentador de paso, reduciendo su eficiencia y eventualmente bloqueando el paso del agua. Un calentador sin mantenimiento en Culiacán puede fallar en 5-8 años aunque sea nuevo. El mantenimiento anual (limpieza de sarro) alarga la vida útil a 12-15 años.'
      },
      {
        q: '¿Qué indica el agua con color oxidado en una casa de Humaya?',
        a: 'El agua herrumbrosa indica corrosión interna avanzada en la tubería galvanizada. Es una señal de que la tubería está desprendiéndose internamente y las fugas son inminentes. Además de ser un problema estético, ese óxido en suspensión puede dañar electrodomésticos como lavadoras y lavavajillas. Recomendamos diagnóstico urgente — llama al 667 392 2273.'
      },
      {
        q: '¿Cuánto tardan en llegar a Humaya en una emergencia?',
        a: 'Para emergencias en Humaya llegamos en 25-35 minutos. Atendemos toda la colonia con referencia en Blvd. Emilio Barragán y los accesos a Los Jardines del Humaya. Servicio 24/7 los 365 días, incluyendo madrugadas y festivos.'
      },
      {
        q: '¿Puedo usar agua herrumbrosa para bañarme mientras espero al plomero?',
        a: 'Bañarse con agua herrumbrosa no es peligroso en el corto plazo, pero puede manchar ropa y azulejos. Para cocinar y beber, usa agua embotellada hasta que se resuelva el problema. Si el agua tiene olor a tierra o sulfuro además del color, puede haber contaminación más seria — llama de inmediato al 667 392 2273.'
      }
    ]
  },
  'campestre': {
    faqs: [
      {
        q: '¿Por qué los sistemas hidroneumáticos de Campestre fallan después de 20-30 años?',
        a: 'Los hidroneumáticos instalados en los años 80-90 en Campestre tienen tres componentes que se desgastan: la membrana de hule (pierde elasticidad y no mantiene la presión de aire), la bomba (el motor y el impulsor se desgastan) y el presostato (los contactos eléctricos se oxidan). Cuando la membrana falla, el tanque trabaja "en seco" y la bomba se enciende y apaga constantemente, lo que la quema en pocas semanas si no se atiende a tiempo.'
      },
      {
        q: '¿Cuánto cuesta reemplazar un sistema hidroneumático en Campestre?',
        a: 'El reemplazo de un hidroneumático residencial en Campestre varía entre $8,000 y $18,000 MXN dependiendo de la capacidad del tanque y la potencia de la bomba requerida. Incluimos instalación, pruebas de presión y calibración. Para casas grandes con demanda alta, recomendamos sistemas de doble bomba con arranque alternado. Damos presupuesto sin costo previo al 667 392 2273.'
      },
      {
        q: '¿Por qué hay sarro en mi calentador si la casa de Campestre es relativamente nueva?',
        a: 'El agua de Culiacán tiene alta dureza (150-200 mg/L de carbonato de calcio) independientemente de la antigüedad de la instalación. En casas de Campestre de 15-30 años, el sarro se acumula en el intercambiador del calentador de paso reduciéndolo internamente. El mantenimiento preventivo anual (limpieza ácida del intercambiador) previene fallas prematuras y mantiene la eficiencia del equipo.'
      },
      {
        q: '¿Atienden sistemas de alberca y riego en Campestre?',
        a: 'Sí, además de plomería hidráulica y sanitaria, atendemos sistemas de recirculación de alberca, riego automatizado y sistemas de presión para jardines. Muchas residencias de Campestre tienen equipos de bombeo independientes para riego — revisamos, reparamos y reemplazamos esos sistemas también.'
      },
      {
        q: '¿Cuándo es el momento ideal para renovar la tubería en una casa de Campestre?',
        a: 'En casas de Campestre con 35-55 años y galvanizado original, el momento ideal para renovar ya pasó — cada año que pasa aumenta el riesgo de fuga. Si tu casa tiene más de 30 años y nunca se ha renovado la tubería, considera hacerlo de forma preventiva antes de que una fuga cause daños en acabados. Una renovación preventiva cuesta entre 30-50% menos que hacer lo mismo después de una emergencia con daños en muros y pisos.'
      }
    ]
  },
  'montebello': {
    faqs: [
      {
        q: '¿Por qué el galvanizado instalado en los 80s ya da problemas en Montebello?',
        a: 'La tubería galvanizada tiene una vida útil de 20-40 años dependiendo de la calidad del agua. En Montebello, el galvanizado instalado entre 1975 y 1985 ya supera los 40 años, y el agua dura de JAPAC aceleró su deterioro: la corrosión interna reduce el diámetro útil progresivamente. Cuando el tubo se corroe hasta el 60-70% de su sección, las fugas son inevitables. Ya no es cuestión de "si" fallará — es cuestión de cuándo.'
      },
      {
        q: '¿Cuánto cuesta detectar y reparar una fuga oculta en Montebello?',
        a: 'El diagnóstico con geófono es gratuito. La reparación de una fuga en muro varía entre $600 y $2,000 MXN dependiendo de la accesibilidad y el tipo de acabado afectado. Si la fuga está en losa de entrepiso, el costo sube a $1,500-$3,500 MXN. Damos presupuesto exacto antes de iniciar — llama al 667 392 2273.'
      },
      {
        q: '¿Por qué baja la presión del agua en horas pico en Montebello?',
        a: 'En Montebello la baja presión en horas pico (7-9am y 7-9pm) tiene dos causas simultáneas: la red de JAPAC opera a menor presión cuando todos los vecinos usan agua al mismo tiempo, y la tubería interna galvanizada tiene el diámetro útil reducido por corrosión. Cuando conviven ambos problemas, la presión cae a casi nada. El primer paso es diagnosticar si el problema es interno (tubería) o externo (JAPAC).'
      },
      {
        q: '¿Cuánto tardan en llegar a Montebello en una emergencia?',
        a: 'Para emergencias en Montebello llegamos en 25-35 minutos. Conocemos bien la zona con referencia en Blvd. Guillermo Bátiz Paredes, la Escuela Rafael Buelna y el Cerro de Montebello. Atendemos 24/7 los 365 días.'
      },
      {
        q: '¿Es mejor reemplazar el galvanizado con CPVC o con cobre en Montebello?',
        a: 'Ambos son mejores que el galvanizado. El CPVC es más económico (30-40% menos que cobre), fácil de instalar y resistente al sarro. El cobre tiene mayor vida útil (50+ años) y mejor tolerancia a temperaturas altas. Para la mayoría de las casas de Montebello recomendamos CPVC: es la mejor relación costo-beneficio. Para instalaciones de agua caliente expuesta a altas temperaturas, preferimos cobre.'
      }
    ]
  },
  'valle-alto': {
    faqs: [
      {
        q: '¿Por qué hay fugas ocultas frecuentes en Valle Alto?',
        a: 'Las casas de Valle Alto construidas entre 1970 y 1990 conservan en su mayoría las tuberías galvanizadas originales. Con 35-55 años de uso y el agua dura de JAPAC, el galvanizado se corroe desde adentro: primero pierde presión, luego empieza a filtrar en los puntos más débiles (codos, uniones, cambios de diámetro). Esas fugas ocurren dentro de muros o losas, donde pueden acumular humedad durante meses sin verse.'
      },
      {
        q: '¿Qué señales me dicen que la tubería de mi casa en Valle Alto necesita cambio?',
        a: 'Las señales más claras en Valle Alto son: agua con tono oxidado al abrir la llave por primera vez en la mañana, manchas de humedad en muros sin causa aparente, presión que baja progresivamente con el tiempo, y calentadores que fallan antes de su tiempo de vida útil. Si tienes 3 o más de estas señales, la tubería galvanizada original ya llegó al límite de su vida útil.'
      },
      {
        q: '¿Cuánto cuesta cambiar la tubería galvanizada en Valle Alto?',
        a: 'Un baño completo (regadera, lavabo, WC) en tubería CPVC cuesta entre $3,500 y $6,000 MXN con mano de obra incluida. Una casa mediana de Valle Alto (2 baños + cocina) varía entre $12,000 y $22,000 MXN. Damos presupuesto gratuito con diagnóstico previo — llama al 667 392 2273.'
      },
      {
        q: '¿Cuánto tardan en llegar a Valle Alto?',
        a: 'Para emergencias en Valle Alto llegamos en 25-35 minutos. Conocemos bien la zona — Blvd. Valle Alto, la Parroquia José María Escrivá de Balaguer y las calles internas del fraccionamiento. Atendemos 24/7 los 365 días.'
      },
      {
        q: '¿Puedo reparar solo el tramo con fuga o debo cambiar toda la tubería de Valle Alto?',
        a: 'Depende del estado general. Si la tubería tiene 40+ años, reparar el tramo con fuga es un parche: en 6-18 meses fallará otro punto. Lo más rentable a largo plazo es el cambio completo, que evita pagar varias reparaciones parciales. Te damos un diagnóstico honesto con evaluación del estado completo antes de recomendar — llama al 667 392 2273.'
      }
    ]
  },
  'zona-dorada': {
    faqs: [
      {
        q: '¿Por qué hay sarro en mi calentador si mi casa de Zona Dorada es relativamente nueva?',
        a: 'El sarro no depende de la antigüedad de la casa, sino de la calidad del agua. El agua que distribuye JAPAC en Culiacán tiene alta dureza (150-200 mg/L de calcio y magnesio) y afecta los calentadores de paso desde el primer año de uso. En Zona Dorada, con casas de 15-25 años, los calentadores empiezan a fallar precisamente ahora porque ya acumulan 10-15 años de sarro sin mantenimiento preventivo.'
      },
      {
        q: '¿Qué daños pudo causar el megacorte de JAPAC del 7 de abril de 2026 en Zona Dorada?',
        a: 'El megacorte que afectó Zona Dorada 1 y Zona Dorada 2 en abril de 2026 pudo generar: golpes de ariete al restaurarse la presión (que dañan válvulas de paso y uniones de PVC), aire atrapado en tinacos y cisternas (que causa presión irregular), y sedimento que llega a los filtros de los calentadores. Si después del corte notas presión irregular, ruidos en tuberías o agua con turbiedad, llama al 667 392 2273 para revisión.'
      },
      {
        q: '¿Cómo sé si mi válvula de paso se dañó por un golpe de ariete en Zona Dorada?',
        a: 'Señales de válvula de paso dañada: no cierra completamente el flujo aunque la gires, gotea agua por el vástago cuando está cerrada, o al cerrarla escuchas un ruido metálico seguido de golpes en la tubería. Si la válvula principal no cierra bien, una fuga o emergencia se convierte en una inundación — reemplázala preventivamente. Cuesta menos de $500 MXN con mano de obra.'
      },
      {
        q: '¿Cuánto tardan en llegar a Zona Dorada desde Blvd. del Lago?',
        a: 'Para emergencias en Zona Dorada llegamos en 25-35 minutos. Cubrimos Zona Dorada 1 y 2, las colonias sobre Blvd. del Lago y la zona cercana al Estadio Banorte. Atendemos 24/7 incluyendo días de partido o eventos.'
      },
      {
        q: '¿Con qué frecuencia debo hacer mantenimiento a la plomería de una casa de 15-20 años en Zona Dorada?',
        a: 'En Zona Dorada recomendamos revisión preventiva cada 2 años: inspección de válvulas de paso, limpieza de sarro en calentador, revisión de flotadores de tinaco y prueba de presión del sistema. Este mantenimiento cuesta entre $800 y $1,500 MXN y previene emergencias costosas. Para calentadores de paso, la limpieza anual de sarro puede triplicar su vida útil.'
      }
    ]
  },
  'country-tres-rios': {
    faqs: [
      {
        q: '¿Por qué mi calentador de paso falla si la casa de Country Tres Ríos tiene solo 10-15 años?',
        a: 'El agua de JAPAC en Culiacán tiene alta dureza: 150-200 mg/L de calcio y magnesio que se depositan como sarro en el intercambiador del calentador. Sin mantenimiento anual, ese sarro bloquea progresivamente el paso del agua hasta que el calentador deja de calentar o el sensor de flujo ya no detecta caudal suficiente. En 8-12 años de uso sin limpieza, el daño es irreversible y el calentador hay que reemplazarlo.'
      },
      {
        q: '¿Qué hace tan agresiva el agua de Culiacán para las instalaciones de Country Tres Ríos?',
        a: 'JAPAC extrae el agua principalmente del río Humaya. Esa agua arrastra minerales de la sierra — calcio, magnesio, bicarbonatos — que le dan su alta dureza. Al calentarse, esos minerales precipitan y forman sarro. Las tuberías de PVC y CPVC resisten bien el sarro, pero los calentadores, tinacos y regaderas lo acumulan. Un filtro suavizador de agua puede reducir el sarro hasta en un 80%.'
      },
      {
        q: '¿Cuánto cuesta el mantenimiento preventivo anual en Country Tres Ríos?',
        a: 'Una revisión preventiva completa en Country Tres Ríos incluye: limpieza de sarro en calentador, revisión de válvulas, revisión de flotador de tinaco, prueba de presión y revisión de drenajes. El costo total está entre $1,200 y $2,000 MXN dependiendo del tamaño de la propiedad. Puede contratarse como servicio anual. Llama al 667 392 2273.'
      },
      {
        q: '¿Cómo acceden a fraccionamientos cerrados de Country Tres Ríos?',
        a: 'El residente debe indicar el acceso y confirmar nuestra llegada con la caseta de seguridad. Para emergencias nocturnas, coordinamos con el residente por WhatsApp para que autorice el acceso antes de que lleguemos. También emitimos carta de presentación digital si el fraccionamiento la requiere para contratistas. Llama al 667 392 2273 para coordinar.'
      },
      {
        q: '¿Cuánto tardan en llegar a Country Tres Ríos?',
        a: 'Para emergencias en Country Tres Ríos llegamos en 25-35 minutos por Blvd. Alfonso G. Calderón Velarde. Atendemos 24/7 los 365 días. Para visitas programadas, coordínamos con al menos 1 hora de anticipación para gestionar el acceso al fraccionamiento.'
      }
    ]
  },
  'colinas-de-san-miguel': {
    faqs: [
      {
        q: '¿Por qué hay baja presión de agua en Colinas de San Miguel si es una colonia relativamente nueva?',
        a: 'Colinas de San Miguel está en el sector norte de Culiacán, al final de la red de distribución de JAPAC. Las zonas al final de la red trabajan con menor presión residual que las colonias más cercanas a las plantas de tratamiento. Además, en casas de 15-35 años el sarro ya empieza a acumularse en tuberías y calentadores. Diagnosticamos si el problema es de red externa (JAPAC) o interno (tubería/calentador).'
      },
      {
        q: '¿Por qué los cortes de JAPAC dañan las instalaciones de Colinas de San Miguel?',
        a: 'Cuando JAPAC corta y restaura el servicio, el agua regresa a presión alta de forma brusca. Ese "golpe de ariete" puede dañar válvulas de paso, uniones de PVC y flotadores de tinaco. En Colinas de San Miguel, donde los cortes programados son frecuentes, estos golpes se acumulan con el tiempo. Si después de un corte notas pérdida de agua, ruidos en tuberías o el tinaco ya no llena bien, solicita una revisión.'
      },
      {
        q: '¿Cuánto cuesta limpiar y revisar el tinaco en Colinas de San Miguel?',
        a: 'La limpieza y revisión de tinaco (incluye vaciado, lavado interior, revisión de flotador, válvula de llenado y conexiones) está entre $400 y $800 MXN dependiendo del tamaño. Si el flotador o la válvula están dañados, el reemplazo de esas piezas agrega $200-$500 MXN adicionales. Recomendamos limpiar el tinaco cada 1-2 años, especialmente después de cortes prolongados de agua.'
      },
      {
        q: '¿Cuánto tardan en llegar a Colinas de San Miguel?',
        a: 'Para emergencias en Colinas de San Miguel llegamos en 25-40 minutos dependiendo del tráfico en Blvd. Colinas de San Miguel y los accesos norte. Atendemos 24/7 los 365 días, incluyendo madrugadas y festivos.'
      },
      {
        q: '¿Se puede prevenir el sarro en el calentador en Colinas de San Miguel?',
        a: 'Sí. La mejor prevención es el mantenimiento anual: limpieza ácida del intercambiador del calentador que disuelve el sarro acumulado. También existen filtros suavizadores de agua que se instalan en la entrada del calentador y reducen el sarro hasta en 80%. El mantenimiento anual cuesta entre $400 y $800 MXN y puede triplicar la vida útil del calentador.'
      }
    ]
  },
  'cumbres-tres-rios': {
    faqs: [
      {
        q: '¿Por qué hay sarro en las instalaciones de Cumbres Tres Ríos si el fraccionamiento es moderno?',
        a: 'El sarro no depende de la modernidad de la construcción sino de la calidad del agua. JAPAC distribuye agua dura con 150-200 mg/L de calcio y magnesio en toda Culiacán, incluyendo Cumbres Tres Ríos. En 10-15 años de uso sin mantenimiento, ese sarro se acumula en calentadores, regaderas y válvulas hasta causar fallas. La posición del fraccionamiento sobre el río Humaya no modifica la dureza del agua de la red.'
      },
      {
        q: '¿Los golpes de ariete pueden dañar las tuberías de PVC de Cumbres Tres Ríos?',
        a: 'Sí. Los golpes de ariete (causados por cierres bruscos de válvulas o cortes de JAPAC) generan picos de presión que superan la resistencia de las uniones y codos de PVC. Los síntomas más comunes en Cumbres son: uniones que empiezan a sudar o gotear, válvulas de paso que no cierran completamente y flotadores que pierden calibración. Una válvula amortiguadora de golpes de ariete en la entrada de la red previene estos daños.'
      },
      {
        q: '¿Cómo acceden a Cumbres Tres Ríos siendo un fraccionamiento privado?',
        a: 'El residente coordina el acceso con la caseta de seguridad antes de nuestra llegada. Para emergencias, enviamos al residente los datos del técnico por WhatsApp para que autorice el ingreso. También gestionamos carta de presentación digital cuando el fraccionamiento la requiere. Llama al 667 392 2273 para coordinar.'
      },
      {
        q: '¿Cuánto tardan en llegar a Cumbres Tres Ríos por Blvd. Pedro Infante?',
        a: 'Para emergencias en Cumbres Tres Ríos llegamos en 30-40 minutos por Blvd. Pedro Infante y el acceso al fraccionamiento. El tiempo incluye la coordinación de entrada con seguridad. Atendemos 24/7 los 365 días.'
      },
      {
        q: '¿Cuánto cuesta una revisión completa del sistema hidráulico en Cumbres Tres Ríos?',
        a: 'Una revisión preventiva completa (calentador, tinaco, válvulas, drenajes y presión general) en una casa de Cumbres Tres Ríos está entre $1,200 y $2,000 MXN. Si se detectan piezas que requieren reemplazo, damos presupuesto separado antes de proceder. El diagnóstico inicial es gratuito — llama al 667 392 2273.'
      }
    ]
  },
  'infonavit-barrancos': {
    faqs: [
      {
        q: '¿Por qué hay tanta baja presión y cortes de agua en Infonavit Barrancos?',
        a: 'Infonavit Barrancos tiene una de las densidades de población más altas de Culiacán: 12,800 habitantes en 83 hectáreas. La red de JAPAC que abastece la colonia, construida originalmente para esa densidad pero ahora bajo mayor demanda, opera frecuentemente a baja presión. Combinado con tuberías galvanizadas internas de 35-50 años, la presión disponible en las llaves es mínima en horas pico.'
      },
      {
        q: '¿Qué hago si llevo días sin agua en Infonavit Barrancos y JAPAC no responde?',
        a: 'Mientras esperas la respuesta de JAPAC, puedes hacer lo siguiente: verifica que la válvula de paso principal de tu casa esté completamente abierta, revisa si el tinaco o cisterna tiene agua (puede estar vacío sin que la válvula de entrada funcione), y reporta directamente a JAPAC por Twitter/@JAPACculiacan donde suelen responder más rápido que por teléfono. Si el tinaco está vacío por falla de la válvula de llenado, podemos solucionarlo ese mismo día.'
      },
      {
        q: '¿Cuánto cuesta renovar la plomería en una casa de interés social de Infonavit Barrancos?',
        a: 'Para las viviendas de interés social de Infonavit Barrancos ofrecemos un diagnóstico gratuito y opciones escalonadas. Renovar solo el baño principal en CPVC está entre $2,800 y $4,500 MXN. La cocina por separado entre $1,500 y $2,500 MXN. La renovación completa (baño + cocina) entre $6,000 y $10,000 MXN con mano de obra incluida. Aceptamos pagos en parcialidades.'
      },
      {
        q: '¿Los cortes frecuentes de agua en Infonavit Barrancos dañan las instalaciones con el tiempo?',
        a: 'Sí. Cada corte y restauración del servicio genera un golpe de ariete que desgasta válvulas, uniones y flotadores. En una colonia con cortes frecuentes como Infonavit Barrancos, ese desgaste acumulado puede reducir la vida útil de las válvulas a la mitad. Si después de un corte notas pérdida de agua, el tinaco no llena bien o hay ruidos en las tuberías, llama para revisión.'
      },
      {
        q: '¿Cuánto tardan en llegar a Infonavit Barrancos?',
        a: 'Para emergencias en Infonavit Barrancos llegamos en 25-35 minutos con referencia en Calle General Pablo Macías Valenzuela. Cubrimos toda la colonia Barrancos y sus secciones (Barrancos II, III, IV). Atendemos 24/7 los 365 días. Para presupuesto sin visita, puedes enviarnos fotos del problema por WhatsApp al 667 392 2273.'
      }
    ]
  },
  'monaco': {
    intro: '<strong>Mónaco</strong> es un fraccionamiento residencial de Culiacán desarrollado entre <strong>1985 y 2000</strong>, ubicado en la zona poniente de la ciudad. Con viviendas de 25-40 años de antigüedad, la colonia combina casas de clase media con comercios locales. Las instalaciones hidráulicas de las casas más antiguas ya presentan el deterioro típico del galvanizado: corrosión interna, baja presión y calentadores con sarro acumulado por el agua dura de JAPAC.',
    faqs: [
      {
        q: '¿Por qué hay baja presión de agua en algunas casas de Mónaco?',
        a: 'En las casas de Mónaco con más de 25 años, la baja presión casi siempre es por la tubería galvanizada original que se corroe internamente por el agua dura de JAPAC. El diámetro útil se reduce progresivamente hasta que el flujo cae a menos de la mitad. En casas más nuevas, puede ser por la válvula de paso parcialmente cerrada o el flotador del tinaco mal calibrado.'
      },
      {
        q: '¿Cuánto tarda el plomero en llegar a Mónaco?',
        a: 'Para emergencias en Mónaco llegamos en 20-30 minutos. Atendemos toda la colonia 24/7 los 365 días, incluyendo madrugadas y fines de semana. Llama o escríbenos al WhatsApp 667 392 2273.'
      },
      {
        q: '¿Cuánto cuesta destapar un drenaje en Mónaco?',
        a: 'El destape de drenaje en Mónaco varía entre $500 y $1,200 MXN dependiendo del tipo de obstrucción y la profundidad. El diagnóstico es sin costo. Para obstrucciones simples (grasa, cabello), el servicio tarda 30-60 minutos. Para obstrucciones por raíces o tubería colapsada, primero diagnosticamos y cotizamos antes de proceder.'
      },
      {
        q: '¿Atienden tanto casas como negocios en Mónaco?',
        a: 'Sí, atendemos vivienda y locales comerciales en Mónaco. Para negocios emitimos factura SAT el mismo día del servicio. Para propiedades en renta, coordinamos directamente con el arrendador o el inquilino según se requiera.'
      },
      {
        q: '¿Por qué mi calentador de paso falla rápido en Mónaco?',
        a: 'El agua dura de JAPAC acumula sarro en el intercambiador del calentador independientemente de la colonia. En Mónaco, sin mantenimiento anual, el sarro puede bloquear el calentador en 5-8 años. El mantenimiento preventivo anual (limpieza ácida del intercambiador) cuesta entre $400 y $800 MXN y puede triplicar la vida útil del equipo.'
      }
    ]
  },
  'la-campina': {
    intro: '<strong>La Campiña</strong> es uno de los fraccionamientos residenciales más consolidados de Culiacán, desarrollado desde los años <strong>80</strong> en la zona sur-oriente de la ciudad. Con viviendas de 25-45 años de antigüedad, La Campiña es conocida por sus amplias calles arboladas y su ambiente residencial tranquilo. Las instalaciones hidráulicas de las casas más antiguas presentan el desgaste típico del galvanizado: corrosión interna, baja presión progresiva y calentadores afectados por el sarro del agua dura de JAPAC.',
    faqs: [
      {
        q: '¿Por qué hay fugas frecuentes en las casas de La Campiña?',
        a: 'Las casas de La Campiña con más de 30 años conservan en muchos casos su tubería galvanizada original. Con tres décadas de agua dura de JAPAC, el galvanizado se corroe internamente hasta generar pinhole leaks — pequeñas perforaciones que al principio se manifiestan como manchas de humedad en muros y eventualmente como fugas abiertas. No son defectos de construcción; es el ciclo de vida normal del galvanizado con agua de alta dureza.'
      },
      {
        q: '¿Cuánto tiempo tarda el plomero en llegar a La Campiña?',
        a: 'Para emergencias en La Campiña llegamos en 25-35 minutos. Cubrimos toda la colonia y las zonas aledañas. Atendemos 24/7 los 365 días — llama o escríbenos al WhatsApp 667 392 2273.'
      },
      {
        q: '¿Cuánto cuesta cambiar tubería galvanizada en La Campiña?',
        a: 'El cambio de un baño completo (regadera, lavabo, WC) a tubería CPVC está entre $3,500 y $6,000 MXN con mano de obra. Para una casa mediana (2 baños + cocina), el rango es de $12,000 a $22,000 MXN. Damos presupuesto gratuito con diagnóstico previo al 667 392 2273.'
      },
      {
        q: '¿Qué señales me indican que la plomería de mi casa en La Campiña necesita revisión?',
        a: 'Señales de alerta en La Campiña: presión que baja progresivamente con los meses, agua herrumbrosa al abrir por primera vez en la mañana, manchas de humedad en muros sin causa aparente, calentador que falla antes de su tiempo de vida útil, o el WC que tarda más en llenarse que antes. Tres o más de estas señales indican que la tubería galvanizada ya está al límite.'
      },
      {
        q: '¿Atienden también colonias cercanas a La Campiña?',
        a: 'Sí, además de La Campiña atendemos Campestre Las Fuentes, Campestre Los Laureles, Campestre San Jorge y todas las colonias de la zona sur-oriente de Culiacán. Llegamos en 25-40 minutos dependiendo de la ubicación exacta.'
      }
    ]
  },
  'lomas-del-boulevard': {
    intro: '<strong>Lomas del Boulevard</strong> es un fraccionamiento residencial de Culiacán ubicado sobre el <strong>Blvd. Universitarios</strong>, en la zona norte de la ciudad. Desarrollado entre <strong>1990 y 2010</strong>, tiene viviendas de 15-35 años de antigüedad. Aunque la construcción es relativamente moderna, el agua dura de JAPAC ya ha acumulado sarro en calentadores y tuberías, y los cortes programados generan golpes de ariete que desgastan válvulas y uniones de PVC.',
    faqs: [
      {
        q: '¿Por qué hay sarro en mi calentador en Lomas del Boulevard si es reciente?',
        a: 'El sarro lo genera la dureza del agua de JAPAC (150-200 mg/L de calcio), no la antigüedad de la casa. En Lomas del Boulevard, con casas de 15-35 años, los calentadores de paso ya acumulan entre 10 y 25 años de sarro sin mantenimiento. El mantenimiento anual (limpieza ácida del intercambiador) previene fallas y puede triplicar la vida útil del equipo.'
      },
      {
        q: '¿Cuánto tardan en llegar a Lomas del Boulevard?',
        a: 'Para emergencias en Lomas del Boulevard llegamos en 25-35 minutos por Blvd. Universitarios. Atendemos 24/7 los 365 días. Llama o escríbenos al WhatsApp 667 392 2273.'
      },
      {
        q: '¿Cómo afectan los cortes de JAPAC a las instalaciones en Lomas del Boulevard?',
        a: 'Los cortes y restauraciones del agua de JAPAC generan golpes de ariete que dañan progresivamente las válvulas de paso, las uniones de PVC y los flotadores del tinaco. En Lomas del Boulevard, si después de un corte notas pérdida de agua, ruidos en tuberías o el tinaco ya no llena bien, solicita una revisión. Una válvula amortiguadora de golpes de ariete en la entrada previene estos daños.'
      },
      {
        q: '¿Cuánto cuesta la revisión preventiva en Lomas del Boulevard?',
        a: 'Una revisión preventiva completa (calentador, tinaco, válvulas, drenajes y presión general) está entre $1,000 y $1,800 MXN. Si se detectan piezas que requieren reemplazo, damos presupuesto separado antes de proceder. El diagnóstico es gratuito — llama al 667 392 2273.'
      },
      {
        q: '¿Atienden colonias cercanas a Lomas del Boulevard?',
        a: 'Sí, cubrimos Lomas del Boulevard y las colonias aledañas sobre Blvd. Universitarios: Colinas de San Miguel, Lomas del Bosque, Lomas Verdes y toda la zona norte de Culiacán. Llegamos en 25-40 minutos dependiendo de la ubicación.'
      }
    ]
  },
  'real-del-valle': {
    intro: '<strong>Real del Valle</strong> es un fraccionamiento residencial de nivel medio-alto en Culiacán, desarrollado entre <strong>1995 y 2010</strong>. Con viviendas de 15-30 años de antigüedad, es una de las colonias más ordenadas y bien planeadas de la ciudad. A pesar de su modernidad relativa, el agua dura de JAPAC ya empieza a generar problemas de sarro en calentadores y tinacos, y las uniones de PVC de los sistemas más viejos presentan desgaste por los cortes programados de la red.',
    faqs: [
      {
        q: '¿Por qué hay problemas de plomería en Real del Valle si el fraccionamiento es moderno?',
        a: 'Real del Valle tiene 15-30 años, lo suficiente para que el sarro del agua de JAPAC haya dañado calentadores de paso y para que válvulas y uniones de PVC hayan acumulado desgaste por golpes de ariete. Las casas más antiguas del fraccionamiento (1995-2000) ya están en el rango donde el galvanizado de tuberías auxiliares puede presentar corrosión.'
      },
      {
        q: '¿Cuánto tardan en llegar a Real del Valle?',
        a: 'Para emergencias en Real del Valle llegamos en 25-35 minutos. Atendemos toda la colonia y el fraccionamiento 24/7 los 365 días. Llama o escríbenos al WhatsApp 667 392 2273.'
      },
      {
        q: '¿Cuánto cuesta revisar y dar mantenimiento en Real del Valle?',
        a: 'Una revisión preventiva completa (calentador, tinaco, válvulas y drenajes) está entre $1,000 y $1,800 MXN. El diagnóstico inicial es gratuito. Si necesitas solo limpieza de sarro en calentador, el costo es de $400 a $700 MXN. Llama al 667 392 2273.'
      },
      {
        q: '¿Atienden fraccionamientos cerrados como Real del Valle?',
        a: 'Sí. El residente coordina el acceso con la caseta de seguridad antes de nuestra llegada. Para emergencias nocturnas, el residente nos autoriza por WhatsApp y notifica a seguridad. También gestionamos carta de presentación digital si el fraccionamiento la requiere.'
      },
      {
        q: '¿Qué hago si hay una fuga y necesito cerrar el paso del agua en Real del Valle?',
        a: 'La válvula de paso principal de tu casa generalmente está en el medidor de agua, cerca de la banqueta. Para una fuga interna urgente, cierra esa válvula para detener el flujo mientras llega el plomero. Si la válvula no cierra completamente (problema común en casas de 15+ años), llama de inmediato al 667 392 2273 para atención prioritaria.'
      }
    ]
  },
  'hacienda-los-huertos': {
    intro: '<strong>Hacienda Los Huertos</strong> es uno de los fraccionamientos residenciales de mayor nivel en Culiacán, desarrollado entre <strong>1995 y 2010</strong> con amplias residencias y áreas verdes privadas. Con viviendas de 15-30 años, la colonia combina la modernidad de sus construcciones con el desafío del agua dura de JAPAC, que en ese período ha acumulado sarro en calentadores de paso, cisternas y sistemas de riego. Los sistemas de presión (hidroneumáticos o cisterna + bomba) ya están llegando al final de su primer ciclo de vida útil.',
    faqs: [
      {
        q: '¿Por qué fallan los sistemas hidroneumáticos en Hacienda Los Huertos?',
        a: 'Las residencias de Hacienda Los Huertos instaladas en 1995-2005 tienen sistemas hidroneumáticos con 20-30 años de uso. La membrana pierde elasticidad y ya no retiene la presión de aire; la bomba trabaja constantemente y eventualmente se quema. Si el agua sale a presión irregular o la bomba arranca y para en ciclos muy cortos, el hidroneumático ya está fallando. El reemplazo cuesta entre $8,000 y $18,000 MXN dependiendo de la capacidad requerida.'
      },
      {
        q: '¿Cuánto cuesta el mantenimiento de la cisterna y el sistema de presión en Hacienda Los Huertos?',
        a: 'El mantenimiento anual de cisterna (limpieza interior, revisión de válvulas de entrada y salida, revisión de flotador) está entre $800 y $1,500 MXN. La revisión del sistema hidroneumático o de bomba sumergible agrega $500-$1,000 MXN. Para residencias con alberca o sistema de riego automatizado, el mantenimiento completo está entre $2,000 y $4,000 MXN.'
      },
      {
        q: '¿Atienden sistemas de alberca y riego en Hacienda Los Huertos?',
        a: 'Sí, además de plomería hidráulica y sanitaria atendemos: sistemas de recirculación de alberca (bombas, filtros, válvulas), riego automatizado (programadores, solenoides, aspersores) y sistemas de presión para jardines. También instalamos y reparamos sistemas de ósmosis inversa y suavizadores de agua para reducir el sarro en toda la instalación.'
      },
      {
        q: '¿Cuánto tardan en llegar a Hacienda Los Huertos?',
        a: 'Para emergencias en Hacienda Los Huertos llegamos en 25-35 minutos. Para acceso al fraccionamiento, el residente coordina con la caseta antes de nuestra llegada o nos autoriza por WhatsApp para que seguridad nos permita el ingreso. Atendemos 24/7 los 365 días al 667 392 2273.'
      },
      {
        q: '¿Ofrecen contrato de mantenimiento anual para residencias de Hacienda Los Huertos?',
        a: 'Sí, ofrecemos contratos de mantenimiento preventivo anual con 2 visitas programadas al año. El contrato incluye: revisión completa del sistema hidráulico, limpieza de sarro en calentadores, revisión de cisternas, pruebas de presión y un descuento del 15% en servicios de emergencia durante la vigencia del contrato. Consulta condiciones al 667 392 2273.'
      }
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
</div></section>

`;
}

function buildFaqSchema(faqs) {
  return `,
    {
      "@type": "FAQPage",
      "mainEntity": [
${faqs.map(f => `        {
          "@type": "Question",
          "name": ${JSON.stringify(f.q)},
          "acceptedAnswer": {
            "@type": "Answer",
            "text": ${JSON.stringify(f.a)}
          }
        }`).join(',\n')}
      ]
    }`;
}

// Display names for FAQ section headers
const displayNames = {
  'tres-rios': 'Tres Ríos',
  'chapultepec': 'Chapultepec',
  'centro': 'Centro',
  'guadalupe': 'Guadalupe',
  'bachigualato': 'Bachigualato',
  'humaya': 'Humaya',
  'campestre': 'Campestre',
  'montebello': 'Montebello',
  'valle-alto': 'Valle Alto',
  'zona-dorada': 'Zona Dorada',
  'country-tres-rios': 'Country Tres Ríos',
  'colinas-de-san-miguel': 'Colinas de San Miguel',
  'cumbres-tres-rios': 'Cumbres Tres Ríos',
  'infonavit-barrancos': 'Infonavit Barrancos',
  'monaco': 'Mónaco',
  'la-campina': 'La Campiña',
  'lomas-del-boulevard': 'Lomas del Boulevard',
  'real-del-valle': 'Real del Valle',
  'hacienda-los-huertos': 'Hacienda Los Huertos'
};

let success = 0, failed = 0;

for (const [slug, data] of Object.entries(colonias)) {
  const filePath = path.join(BASE, slug, 'index.html');

  if (!fs.existsSync(filePath)) {
    console.log(`❌ No existe: ${slug}`);
    failed++;
    continue;
  }

  let html = fs.readFileSync(filePath, 'utf-8');

  // Skip if already has FAQPage
  if (html.includes('"FAQPage"')) {
    console.log(`⏭️  Ya tiene FAQ: ${slug}`);
    success++;
    continue;
  }

  const name = displayNames[slug] || slug;

  // 1. Insert intro for basic-template colonias (those with an intro property)
  if (data.intro) {
    const introHtml = `\n<section class="section section-alt"><div class="container">\n<p class="colonia-intro-unico">${data.intro}</p>\n</div></section>\n`;
    // Insert after the hero section, before the first "¿Por qué elegirnos" section
    if (!html.includes('colonia-intro-unico')) {
      html = html.replace('<section class="section">', introHtml + '<section class="section">');
    }
  }

  // 2. Insert FAQ section before contact section
  const faqHtml = buildFaqHtml(name, data.faqs);
  const contactMarker = '<section id="contacto"';
  if (html.includes(contactMarker)) {
    html = html.replace(contactMarker, faqHtml + contactMarker);
  } else {
    console.log(`⚠️  No encontró #contacto en: ${slug}`);
  }

  // 3. Add FAQPage to schema — find last ]\n} before </script>
  const faqSchema = buildFaqSchema(data.faqs);
  // Pattern: the closing of @graph array before </script>
  html = html.replace(/(\s*\]\s*\}\s*<\/script>)/, faqSchema + '\n  ]\n}\n</script>');

  fs.writeFileSync(filePath, html, 'utf-8');
  console.log(`✅ ${slug}`);
  success++;
}

console.log(`\nListo: ${success} procesadas, ${failed} con error.`);
