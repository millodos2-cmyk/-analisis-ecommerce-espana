# Análisis del comercio electrónico en España

¿Qué actividades del comercio electrónico en España muestran mayor potencial de crecimiento hasta 2028? En este proyecto analicé datos trimestrales de la CNMC y elaboré pronósticos para 92 actividades. El objetivo es ayudar a emprendedores a identificar qué sectores merece la pena estudiar con más detalle.

## Datos y alcance

Utilicé cuatro conjuntos de datos de la Comisión Nacional de los Mercados y la Competencia (CNMC). Recogen el volumen de negocio en euros y el número de transacciones, tanto por actividad económica como por zona geográfica.

El histórico abarca desde el cuarto trimestre de 2013 hasta el primero de 2026. Para los pronósticos por actividad, agrupé las compras realizadas desde España, tanto dentro del país como en el exterior. Excluí la categoría «Otros» porque reúne actividades que no se pueden identificar por separado.

## Cómo hice el análisis

1. Integré las tablas de volumen de negocio y número de transacciones para estudiar la evolución de las compras, el importe medio por operación y las diferencias entre actividades.
2. Comparé varios métodos de pronóstico, entre ellos Random Forest, Holt-Winters y un modelo de referencia que repite el valor del mismo trimestre del año anterior.
3. Evalué los pronósticos frente a ventas reales y seleccioné el método por actividad. Después reentrené los modelos para proyectar los 11 trimestres comprendidos entre abril de 2026 y diciembre de 2028.

## Principales resultados

- **Más operaciones y menor importe medio.** Entre el cuarto trimestre de 2013 y el primero de 2026, el número de transacciones trimestrales pasó de 54,5 millones a unos 550 millones. En ese mismo periodo, el importe medio por operación bajó de 62,95 € a 44,61 €.
- **El error varía según la actividad.** En la evaluación histórica de 11 trimestres, el error absoluto agregado equivalió al 21,09 % de las ventas reales (WAPE). El dashboard muestra también el error de cada actividad para poder valorar sus previsiones por separado.
- **Grandes almacenes destaca en la proyección.** Para esta actividad, el modelo estima que las compras online en 2028 serán un 154,52 % superiores a las registradas en 2025. La comparación utiliza un año completo de ventas observadas y un año completo de ventas pronosticadas.

## Cómo explorar el proyecto

- **Power BI (.pbix)** — Dashboard interactivo para explorar la evolución trimestral y comparar las ventas, el crecimiento previsto y el error histórico por actividad.
- **Notebook de Python (.ipynb)** — Desarrollo del análisis, comparación de modelos y generación de pronósticos.
- **Memoria final (.pdf)** — Contexto, metodología, resultados y conclusiones del proyecto.

**Herramientas utilizadas:** Excel, SQL, Python y Power BI.

**Autor:** Emilio Ahued Salas · Proyecto final del Máster en Análisis de Datos de NEOLAND.
