# %%
## PROYECTO FINAL MASTER NEOLAND

# %% [markdown]
# ## 1.- Importar las herramientas

# %%
from pathlib import Path
from IPython.display import display
import pandas as pd

# Guardar el cuaderno y los cuatro CSV en la misma carpeta.
carpeta_datos = Path(__file__).resolve().parent

# %% [markdown]
# ## 2.- Importar los conjuntos de datos

# %% [markdown]
# ### 2.1 Cargamos el número de transacciones por áreas geográficas

# %%
transacciones_geograficas = pd.read_csv(
    carpeta_datos / "Evolución trimestral del NUMERO transacciones del comercio electrónico por áreas geográficas.csv",
    sep=";",
    decimal=","
)
# Mostramos las primeras cinco filas
transacciones_geograficas.head()

# %% [markdown]
# ### 2.2 Cargamos el volumen de negocio por ramas de actividad

# %%
volumen_actividad = pd.read_csv(
    carpeta_datos / "Evolución trimestral del volumen de negocio del comercio electrónico por ramas de actividad.csv",
    sep=";",
    decimal=","
)

# Mostramos las primeras cinco filas
volumen_actividad.head()

# %% [markdown]
# ### 2.3 Cargamos el número de transacciones por ramas de actividad

# %%
transacciones_actividad = pd.read_csv(
    carpeta_datos / "Evolución trimestral del NUMERO de transacciones del comercio electrónico por ramas de actividad.csv",
    sep=";",
    decimal=","
)

# Mostramos las primeras cinco filas
transacciones_actividad.head()

# %% [markdown]
# ### 2.4 Cargamos el volumen de negocio por áreas geográficas

# %%
volumen_geografico = pd.read_csv(
    carpeta_datos / "Volumen de negocio del comercio electrónico por áreas geográficas.csv",
    sep=";",
    decimal=","
)

# Mostramos las primeras cinco filas
volumen_geografico.head()

# %% [markdown]
# # Paso 3.-Revisión y limpieza de datos.

# %% [markdown]
# ### 3.1.- Comprobar que se hayan pasado todos los datos completos

# %%
print("Transacciones por áreas geográficas",transacciones_geograficas.shape)
print("Volumen por rama de actividad",volumen_actividad.shape)
print("Transacciones por ramas de actividad:", transacciones_actividad.shape)
print("Volumen por áreas geográficas:", volumen_geografico.shape)

# %% [markdown]
# ## 3.2 Revisamos los tipos de datos y los valores no nulos o typeados de manera incongruente.

# %%
transacciones_geograficas.info()

# %%
volumen_actividad.info()

# %%
transacciones_actividad.info()

# %%
volumen_geografico.info()

# %%
# Se comprobaron nulos y tipo de información y todo coincide.

# %% [markdown]
# ## 3.3 Comprobación de filas duplicadas de cada uno de los datasets.

# %%
transacciones_geograficas.duplicated().sum()

# %%
volumen_actividad.duplicated().sum()

# %%
transacciones_actividad.duplicated().sum()

# %%
volumen_geografico.duplicated().sum()

# %%
# Se comprobaron las filas duplicadas en los cuatro DataFrames.
# No se encontraron filas completamente duplicadas en ninguno.

# %% [markdown]
# ## 3.4.-Revisión de valores y categorías

# %%
# Revisar si hay categorías que estén escritas diferente o que tengan diferentes formatos.

# %% [markdown]
# ### 3.4.1 -Transacciones geográficas

# %%
transacciones_geograficas["Trimestre"].unique()

# %%
transacciones_geograficas["Sentido transacción"].unique()

# %%
transacciones_geograficas["Zona geográfica"].unique()

# %%
# Por último verificar si hay alguna transacción menor a cero, que sería un dato raro pero que podría modificar nuestras curvas porque que se hayan registrado
# -10 ventas sería ilógico

(transacciones_geograficas["Evolución trimestral de las transacciones (Núm)"] < 0).sum()

# %% [markdown]
# ### 3.4.2.- Volumen por actividad

# %%
volumen_actividad["Trimestre"].unique()

# %%
volumen_actividad["Sentido transacción"].unique()

# %%
volumen_actividad["Ramas actividad"].unique()

# %%
volumen_actividad["Código (armonización según CNAE y CNPA)"].unique()

# %%
volumen_actividad["Evolución trimestral del volumen de negocio (€)"].unique()

# %%
# En general, he comprobado que en las columnas anteriores cumplían con la cantidad de datos esperada, sin embargo el volumen de actvidad arroja una cantidad de datos
# menor, lo que nos indica la duplicidad de cantidades que es un poco sospechoso, y por tanto, merece la pena investigar el motivo.

# %%
volumen_actividad["Evolución trimestral del volumen de negocio (€)"].value_counts().head(10)

# %%
# Todo parece relativamente normal; sin embargo, los 2.530 registros con un importe de cero euros merecen atención.
# En el análisis exploratorio revisaremos en qué actividades, trimestres y sentidos de transacción se concentran.
# El objetivo es comprender estos patrones y obtener información sobre los sectores, no borrar ni modificar esos registros.

# %% [markdown]
# ### 3.4.3.- Transacciones_actividad

# %%
transacciones_actividad["Trimestre"].unique()

# %%
transacciones_actividad["Sentido transacción"].unique()	

# %%
transacciones_actividad["Ramas actividad"].unique()

# %%
transacciones_actividad["Código (armonización según CNAE y CNPA)"].unique()

# %%
transacciones_actividad["Evolución trimestral de las transacciones (Núm)"].unique()

# %%
# Vemos las 10 cantidades más frecuentes en la última columna: número de transacciones.
transacciones_actividad.iloc[:, -1].value_counts().head(10)

# %%
# Aquí también aparecen 2.530 registros con cero, la misma cantidad que en volumen_actividad. Es coherente, aunque todavía no hemos comprobado que correspondan exactamente a las mismas filas.

# %% [markdown]
# ### 3.4.4.- Volumen_geografico

# %%
volumen_geografico["Trimestre"].unique()

# %%
volumen_geografico["Sentido transacción"].unique()

# %%
volumen_geografico["Zona geográfica"].unique()

# %%
volumen_geografico["Evolución trimestral del volumen de negocio (€)"].unique()

# %%
# Revisamos los 10 importes más frecuentes de la última columna.
volumen_geografico.iloc[:, -1].value_counts().head(10)		

# %% [markdown]
# ## 3.5.- Limpieza de espacios sobrantes en las columnas de texto

# %% [markdown]
# ### 3.5.1.- Transacciones geográficas

# %%
# Contamos las filas con espacios sobrantes en cada columna de texto.
for columna in transacciones_geograficas.select_dtypes(include="object").columns:
    cantidad = transacciones_geograficas[columna].str.contains(
        r"^\s|\s$|\s{2,}", regex=True, na=False
    ).sum()
    print(columna, ":", cantidad)

# %% [markdown]
# ### 3.5.2.- Volumen por actividad

# %%
for columna in volumen_actividad.select_dtypes(include="object").columns:
    cantidad = volumen_actividad[columna].str.contains(
        r"^\s|\s$|\s{2,}",regex=True, na=False
    ).sum()
    print(columna, ":", cantidad)
    

# %%
# "Ramas actividad" presenta algunos espacios, son cuatro nombres mal espaciados, pero cada uno está escrito 150 veces en la tabla lo que arroja los 600

# %%
# Mostramos los nombres únicos que tienen espacios sobrantes.
volumen_actividad.loc[
    volumen_actividad["Ramas actividad"].str.contains(
        r"^\s|\s$|\s{2,}", regex=True, na=False
    ),
    "Ramas actividad"
].unique()

# %%
# Simplificación de espacios a 1 en Ramas actividad.
volumen_actividad["Ramas actividad"] = (
    volumen_actividad["Ramas actividad"].str.replace(r"\s{2,}", " ", regex=True)
)

# %%
for columna in volumen_actividad.select_dtypes(include="object").columns:
    cantidad = volumen_actividad[columna].str.contains(
        r"^\s-|\s$|\s{2,}",regex=True, na=False
    ).sum()
    print(columna, ":", cantidad)
    

# %%
# Listo, hemos comprobado que han quedado en cero.

# %% [markdown]
#  ### 3.5.3.- Transacciones por actividad

# %%
for columna in transacciones_actividad.select_dtypes(include="object").columns:
    cantidad = transacciones_actividad[columna].str.contains(
        r"^\s|\s$|\s{2,}", regex=True, na=False
    ).sum()
    print(columna, ":", cantidad)

# %%
transacciones_actividad.loc[
    transacciones_actividad["Ramas actividad"].str.contains(
        r"^\s|\s$|\s{2,}", regex=True, na=False
    ),
    "Ramas actividad"
].unique()

# %%
# Dejamos un solo espacio entre palabras.
transacciones_actividad["Ramas actividad"] = (
    transacciones_actividad["Ramas actividad"]
    .str.replace(r"\s{2,}", " ", regex=True)
)

# %% [markdown]
# ### 3.5.4 Volumen Geográfico

# %%
for columna in volumen_geografico.select_dtypes(include="object").columns:
    cantidad = volumen_geografico[columna].str.contains(
     r"^\s|\s$|\s{2,}", regex=True, na=False
    ).sum()
    print(columna, ":", cantidad)    

# %% [markdown]
# ## 3.6.- Revisión y adecuación de los tipos de datos

# %%
# Adecuación de los tipos de datos para las columnas que lo necesiten.

# No utilizamos datetime que se utiliza para fechas de un solo día, utilizamos pd.PeriodIndex porque cada registro corresponde a un periodo de tres meses,no a una
# fecha concreta. Los datos ya están agrupados por trimestre.
# Esta conversión permite que Python reconozca Trimestre como un periodo temporal en lugar de texto.

# %% [markdown]
# ### 3.6.1.- Transacciones geográficas

# %%
# Convertimos el dato de trimestre que está en texto a tipo fecha.(Q = quarter)
transacciones_geograficas["Trimestre"] = pd.PeriodIndex(
    transacciones_geograficas["Trimestre"].str.replace("T","Q", regex=False),
    freq="Q-DEC"
)

# %%
# Comprobamos: 
transacciones_geograficas["Trimestre"].dtype

# %% [markdown]
# ### 3.6.2.- Volumen por actividad

# %%


# Convertimos Trimestre de texto a periodo trimestral.
volumen_actividad["Trimestre"] = pd.PeriodIndex(
    volumen_actividad["Trimestre"].str.replace("T", "Q", regex=False),
    freq="Q-DEC"
)

# %%
# Comprobamos el tipo de Trimestre en volumen_actividad.
volumen_actividad["Trimestre"].dtype

# %% [markdown]
# ### 3.6.3.- Transacciones por actividad

# %%
# Convertimos Trimestre de texto a periodo trimestral.
transacciones_actividad["Trimestre"] = pd.PeriodIndex(
    transacciones_actividad["Trimestre"].str.replace("T", "Q", regex=False),
    freq="Q-DEC"
)

# %%
transacciones_actividad["Trimestre"].dtype

# %% [markdown]
# ### 3.6.4.- Volumen geográfico

# %%
# Convertimos Trimestre de texto a periodo trimestral.
volumen_geografico["Trimestre"] = pd.PeriodIndex(
    volumen_geografico["Trimestre"].str.replace("T", "Q", regex=False),
    freq="Q-DEC"
)

# %%
volumen_geografico["Trimestre"].dtype

# %% [markdown]
# # 4.- Integración de los datasets

# %%
# A partir de los cuatro datasets, crearemos dos tablas integradas:
# una por áreas geográficas y otra por ramas de actividad.
# Cada tabla reunirá el volumen de negocio y el número de transacciones, emparejando los registros mediante sus columnas comunes.
# Estas dos tablas serán la base del análisis posterior.

# %% [markdown]
# ### 4.1.- Unión de volumen y transacciones por áreas geográficas

# %%
columnas_union_geograficas = ["Trimestre","Sentido transacción","Zona geográfica"]

# %%
# Revisamos si se repiten las combinaciones que usaremos para unir.
print("Volumen:", volumen_geografico.duplicated(subset=columnas_union_geograficas).sum())
print("Transacciones:", transacciones_geograficas.duplicated(subset=columnas_union_geograficas).sum())

# %%
# Unimos volumen y transacciones por sus columnas comunes.   
datos_geograficos = pd.merge(
    volumen_geografico,
    transacciones_geograficas,
    on=columnas_union_geograficas,
    how="outer",
    validate="one_to_one",
    indicator=True
)

# %%
datos_geograficos.head()

# %%
# Comprobamos si todas las filas encontraron pareja.
print(datos_geograficos["_merge"].value_counts())

# Eliminamos la columna merge de comprobación.
datos_geograficos = datos_geograficos.drop(columns="_merge")

# Mostramos las primeras filas de la tabla integrada.
datos_geograficos.head()

# %%
# Las 698 filas encontraron pareja y ninguna quedó fuera.
# La unión de volumen y transacciones por áreas geográficas está completa.

# %% [markdown]
# ### 4.2.- Unión de volumen y transacciones por actividad

# %%
columnas_union_actividad = [
    "Trimestre",
    "Sentido transacción",
    "Ramas actividad",
    "Código (armonización según CNAE y CNPA)"
]

# %%
# Comprobamos que las combinaciones de unión sean únicas.
print("Volumen:", volumen_actividad.duplicated(subset=columnas_union_actividad).sum())
print("Transacciones:", transacciones_actividad.duplicated(subset=columnas_union_actividad).sum())

# %%
# Unimos los datasets de actividad para crear uno solo.

datos_actividad= pd.merge(
    volumen_actividad,
    transacciones_actividad,
    on=columnas_union_actividad,
    how="outer",
    validate="one_to_one",
    indicator=True
)

# Comprobamos cuántas filas encontraron pareja.
datos_actividad["_merge"].value_counts()

# %%
# Las 13.950 filas encontraron pareja y ninguna quedó fuera. La unión está completa.
# Eliminamos la columna auxiliar de comprobación.
datos_actividad = datos_actividad.drop(columns="_merge")

# Mostramos las primeras filas de la tabla integrada.
datos_actividad.head()

# %%
# Vamos a revisar los registros con valores cero.
# Primero comprobaremos si cuando el volumen es cero también lo es el número de transacciones.
# Después veremos en qué actividades, sentidos de transacción y trimestres se concentran.
# Estas comprobaciones nos ayudarán a entender los datos antes de hacer predicciones.
# Por ahora no vamos a borrar ni modificar esos registros.

# %%
# Comprobamos si los ceros de volumen y transacciones coinciden en las mismas filas.

ceros_volumen = datos_actividad["Evolución trimestral del volumen de negocio (€)"] == 0
ceros_transacciones = datos_actividad["Evolución trimestral de las transacciones (Núm)"] == 0

print("Filas con ambos valores en cero:", (ceros_volumen & ceros_transacciones).sum())
print("Filas donde solo uno es cero:", (ceros_volumen != ceros_transacciones).sum())

# %%
# Contamos las filas con ambos valores en cero por rama de actividad.

datos_actividad.loc[
    ceros_volumen & ceros_transacciones
].groupby("Ramas actividad").size().sort_values(ascending=False)

# %%
# Contamos las filas con ambos valores en cero por sentido de transacción.

datos_actividad.loc[
    ceros_volumen & ceros_transacciones
].groupby("Sentido transacción").size()

# %%
# Contamos las filas con ambos valores en cero por trimestre.

datos_actividad.loc[
    ceros_volumen & ceros_transacciones
].groupby("Trimestre").size()

# %%
# Revisión de los registros con cero:

# Los 2.530 registros coinciden en volumen de negocio y número de transacciones.
# Se concentran en 34 ramas, principalmente dentro de España y en ventas al exterior.
# Aparecen durante todo el histórico, con un aumento desde 2016Q1.
# Conservamos estos registros sin modificarlos: no hemos confirmado la causa de los ceros.
# Antes de modelar, revisaremos cómo afectan a las series seleccionadas.

# %%
# Comprobamos que los totales por geografía y por actividad coincidan
# para cada trimestre y sentido de transacción.

columnas_importes = [
    "Evolución trimestral del volumen de negocio (€)",
    "Evolución trimestral de las transacciones (Núm)"
]

totales_geografia = datos_geograficos.groupby(
    ["Trimestre", "Sentido transacción"]
)[columnas_importes].sum()

totales_actividad = datos_actividad.groupby(
    ["Trimestre", "Sentido transacción"]
)[columnas_importes].sum()

# Restamos ambos totales y mostramos la mayor diferencia absoluta.
diferencias_totales = (totales_geografia - totales_actividad).abs()

diferencias_totales.max()

# %%
# Los totales por geografía y actividad coinciden en la práctica.
# El número de transacciones coincide exactamente.
# La diferencia máxima de volumen es de aproximadamente 0,000002 €,
# compatible con la precisión decimal de los cálculos y sin relevancia para el análisis.

# %% [markdown]
# # 5.- Análisis exploratorio de los datos

# %% [markdown]
# ## 5.1.- Análisis de la tabla datos_geograficos

# %% [markdown]
# ### 5.1.1.- Evolución trimestral del volumen de negocio

# %%
volumen_trimestral = datos_geograficos.groupby("Trimestre")[
    "Evolución trimestral del volumen de negocio (€)"
    ].sum()

volumen_trimestral.head()

# %%
 # Ahora graficarmos los 50 semestres juntos mostrando importes en millones de euros
import matplotlib.pyplot as plt

# %%
plt.figure(figsize=(16, 6))

plt.plot(
    volumen_trimestral.index.astype(str),
    volumen_trimestral / 1_000_000,
    marker="o"
)

plt.title("Evolución trimestral del volumen de negocio del comercio electrónico")
plt.xlabel("Trimestre")
plt.ylabel("Volumen de negocio (millones de €)")
plt.xticks(rotation=90)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
    

# %%
# Conclusiones parciales o exploratorias:

# 1.- Resumen del gráfico: evolución trimestral del volumen de negocio del comercio electrónico.
# 2.- Se observa una tendencia general de crecimiento entre 2013Q4 y 2026Q1.
# 3.- Hay caídas puntuales, pero la trayectoria global sigue siendo ascendente.
# 4.- Las bajadas del cuarto al primer trimestre desde 2021 sugieren un patrón estacional.
# 5.- El máximo se alcanza en 2025Q4.
# 6.- La caída de 2026Q1 no indica, por sí sola, un cambio de tendencia.

# %% [markdown]
# ### 5.1.2.- Evolución trimestral del número de transacciones de comercio electrónico

# %%
# Vamos a ver cuántas transacciones u operaciones se realizaron cada trimestre desde 2013 a 2026.

# %%
# Sumamos las transacciones de cada trimestre usando la tabla integrada geográfica.

num_transacciones_trimestrales = datos_geograficos.groupby("Trimestre")[
    "Evolución trimestral de las transacciones (Núm)"
].sum()

num_transacciones_trimestrales

# %%
# Gráfico de la evolución del num de las transacciones por trimestre en orden cronológico.

plt.figure(figsize=(16,6))

plt.plot(
    num_transacciones_trimestrales.index.astype(str),
    num_transacciones_trimestrales /1_000_000,
    marker="o"
)

plt.title("Evolución del número de transacciones de comercio electrónico 2013-2026")
plt.xlabel("Trimestre")
plt.ylabel("Número de transacciones(millones)")
plt.xticks(rotation=90)
plt.grid(alpha = 0.3)
plt.tight_layout()
plt.show()

# %%
# Datos relevantes del análisis exploratorio

# 1.- Las transacciones muestran una tendencia creciente, con máximos en el cuarto trimestre de cada año completo.
# 2.- Pasan de 54,5 millones en 2013Q4 a 550 millones en 2026Q1.Aumentó 909 %
# 3.- Su evolución es similar a la del volumen de negocio: aumenta tanto el número de operaciones como el dinero movido.

# %% [markdown]
# ### 5.1.3. Evolución trimestral del importe medio por transacción.

# %%
# Importe medio = volumen de negocio ÷ número de transacciones

# %%
importe_medio_trimestral = volumen_trimestral / num_transacciones_trimestrales

importe_medio_trimestral

# %%
# Graficar los importes medios de cada transaccción en cada trimestre


plt.figure(figsize=(16,6))

plt.plot(
    importe_medio_trimestral.index.astype(str),
    importe_medio_trimestral,
    marker = "o"
)

plt.title("Importes medios de transacción por trimestre")
plt.xlabel("Trimestre")
plt.ylabel("Importes medios por transacción (€)")
plt.xticks(rotation=90)
plt.grid(alpha =0.3)
plt.tight_layout()
plt.show()

# %%
# Resumen exploratorio de los datos:

# El importe medio alcanza su máximo de 72,03 € en 2015Q3.
# Desciende con altibajos hasta su mínimo de 43,12 € en 2021Q1.
# Después se recupera parcialmente y termina en 53,90 € en 2026Q1.
# Se realizan más transacciones, pero su importe medio es menor que al inicio del periodo.

# %% [markdown]
# ### 5.1.4 Evolución del volumen de negocio por sentido de la transacción

# %%
volumen_trimestral_sentido = datos_geograficos.groupby(
    ["Trimestre", "Sentido transacción"]
)["Evolución trimestral del volumen de negocio (€)"].sum().unstack()

volumen_trimestral_sentido.head()

# %%
# Gráfico del volumen de negocio trimestral por sentido de la transacción

(volumen_trimestral_sentido / 1_000_000).plot(
    figsize=(16, 6),
    marker="o"
)

plt.title("Evolución del volumen de negocio por sentido de la transacción")
plt.xlabel("Trimestre")
plt.ylabel("Volumen de negocio (millones de €)")
plt.xticks(rotation=90)
plt.legend(title="Sentido de la transacción")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# %%
# Resumen del gráfico:

# Los tres sentidos de transacción crecen entre el inicio y el final del periodo.
# Las compras desde España al exterior presentan el mayor aumento en euros y lideran al final.
# Las compras dentro de España ocupan el segundo lugar al final del periodo.
# Las compras desde el exterior a España muestran una caída marcada en 2020 y una recuperación posterior.

# %% [markdown]
# ## 5.2.- Análisis de la tabla datos_actividad

# %%
datos_actividad.head()

# %% [markdown]
# ### 5.2.1.- Las 10 ramas de actividad con mayor volumen de negocio acumulado

# %%
# Las 10 ramas de actividad con mayor volumen de negocio acumulado

volumen_por_actividad = datos_actividad.groupby("Ramas actividad")[
    "Evolución trimestral del volumen de negocio (€)"
].sum().sort_values(ascending=False)

volumen_por_actividad.head(10)

# %%
# Ahora graficamos las ramas con mayor volumen de negocio en el tiempo

# %%
# Gráfico de las 10 ramas con mayor volumen de negocio acumulado

(volumen_por_actividad.head(10).sort_values() / 1_000_000).plot(
    kind="barh",
    figsize=(12, 6)
)

plt.title("Las 10 ramas con mayor volumen de negocio acumulado (2013Q4–2026Q1)")
plt.xlabel("Volumen de negocio acumulado (millones de €)")
plt.ylabel("Rama de actividad")
plt.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.show()

# %%
# Resumen del gráfico:

# "Otros" concentra el mayor volumen de negocio acumulado, aunque es una categoría agrupada.
# Entre las actividades específicas destacan las agencias de viajes, el transporte aéreo y las prendas de vestir.
# Varias actividades relacionadas con el turismo aparecen entre las diez primeras.
# El ranking recoge el dinero acumulado de todo el periodo, no qué actividades crecieron más.

# %% [markdown]
# ### 5.2.2 Las 10 ramas de actividad con mayor número de transacciones acumuladas

# %%
transacciones_por_actividad = datos_actividad.groupby("Ramas actividad")[
    "Evolución trimestral de las transacciones (Núm)"
].sum().sort_values(ascending=False)

transacciones_por_actividad.head(10)

# %%
# Ahora graficamos las 10 ramas con mayor número de transacciones acumuladas

(transacciones_por_actividad.head(10).sort_values() / 1_000_000).plot(
    kind="barh",
    figsize=(12, 6)
)

plt.title("Las 10 ramas con más transacciones acumuladas (2013Q4–2026Q1)")
plt.xlabel("Número de transacciones acumuladas (millones)")
plt.ylabel("Rama de actividad")
plt.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.show()

# %%
# Análisis exploratorio de los datos obtenidos:

# "Otros" concentra el mayor número de transacciones, aunque es una categoría agrupada.
# Entre las actividades específicas lideran juegos de azar y apuestas, con 898,1 millones de operaciones.
# Le siguen el transporte terrestre de viajeros y las prendas de vestir.
# Las actividades con más operaciones no coinciden necesariamente con las que más dinero mueven.
# Los valores corresponden al acumulado de todo el periodo y de los tres sentidos de transacción.
# Discos, libros, periódicos y papelería se sitúa entre las diez ramas con mayor número de transacciones.

# %% [markdown]
# ### 5.3. Análisis de la tabla datos_geografia

# %%
# Exploramos con qué zonas geográficas se concentra el comercio electrónico de España.

# Mostramos las primeras cinco filas del volumen de negocio por áreas geográficas.
volumen_geografico.head()

# %%
# Analizaremos cuánto compra y cuánto vende España por comercio electrónico a cada zona geográfica para hacer un "tipo balzanza comercial de comercio online"
# Lo que queremos calcular es cuánto compra y cuánto vende España a cada zona. Los datos están ahí en la tabla volumen_geográfico, pero están repartidos
# entre los distintos trimestres y sentidos.
# O sea, es como un tipo de AGRUPACIÓN POR ZONA.

# %% [markdown]
# ### 5.3.1.- Seleccionamos las compras desde España al extranjero.

# %%
compras_exterior = volumen_geografico[
    volumen_geografico["Sentido transacción"] == "Desde España con el exterior"
    ]
compras_exterior.head()    

# %% [markdown]
# ### 5.3.2. Total de compras al extranjero por zona geográfica

# %%
# Sumamos las compras que realiza España a cada zona durante todo el periodo y 
# Obtenemos el total histórico por zona y lo ordenamos de mayor a menor

compras_por_zona = compras_exterior.groupby("Zona geográfica")[
    "Evolución trimestral del volumen de negocio (€)"
    ].sum().sort_values(ascending=False)

compras_por_zona

# %% [markdown]
# ### 5.3.3. Gráfico del total histórico de compras por zona geográfica

# %%
# Ahora representaremos los totales que acabamos de calcular en un gráfico de barras, para comparar visualmente cuánto ha comprado España a cada zona
# durante todo el histórico disponible

# %%
(compras_por_zona.sort_values() / 1_000_000).plot(
    kind="barh",
    figsize=(12, 6)
)

plt.title("Compras de España al exterior por zona geográfica (2013Q4–2026Q1)")
plt.xlabel("Compras acumuladas en todo el histórico (millones de €)")
plt.ylabel("Zona geográfica")
plt.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.show()

# %%
# Resumen del gráfico:

# La Unión Europea concentra el mayor importe de compras de España al exterior.
# Reino Unido y Estados Unidos ocupan el segundo y tercer puesto del acumulado registrado.
# Los valores representan compras acumuladas en todo el histórico disponible, no crecimiento.


# %%
# Queda pendiente comprobar desde cuándo Reino Unido aparece como categoría separada
# para interpretar correctamente su comparación con la Unión Europea.

# Por tanto vamos a realizar ésta comprobación:

# Comprobamos el primer y último trimestre disponible y la cantidad
# de trimestres registrados para las compras a cada zona geográfica.

compras_exterior.groupby("Zona geográfica")["Trimestre"].agg(
    ["min", "max", "nunique"]
)

# %%
# Reino Unido aparece como categoría separada desde 2020Q2, con 24 trimestres.
# Las demás zonas tienen 50 trimestres, desde 2013Q4 hasta 2026Q1.
# Por tanto, los acumulados por zona no tienen todos la misma cobertura temporal.
# Esta comprobación no permite determinar dónde se contabilizaba Reino Unido antes de 2020Q2.

# %% [markdown]
# ### 5.3.4.- Seleccionamos las ventas de España al exterior

# %%
# Ahora vamos a seleccionar las compras que realizan desde el exterior a España

ventas_exterior = datos_geograficos[
    datos_geograficos["Sentido transacción"] == "Desde el exterior con España"
    ]

ventas_exterior.head()

# %% [markdown]
# ### 5.3.5. Total de ventas al exterior por zona geográfica

# %%
# Sumamos las ventas de España a cada zona durante todo el histórico disponible.
# Ordenamos los importes acumulados de mayor a menor.

ventas_por_zona = ventas_exterior.groupby("Zona geográfica")[
    "Evolución trimestral del volumen de negocio (€)"
].sum().sort_values(ascending=False)

ventas_por_zona

# %% [markdown]
# ### 5.3.6. Gráfico del total histórico de ventas por zona geográfica

# %%
# Graficamos:

# Representamos las ventas de España al exterior acumuladas por zona
# durante todo el histórico disponible.
(ventas_por_zona.sort_values() / 1_000_000).plot(
    kind="barh",
    figsize=(12, 6)
)

plt.title("Ventas de España al exterior por zona geográfica (2013Q4–2026Q1)")
plt.xlabel("Ventas acumuladas en todo el histórico (millones de €)")
plt.ylabel("Zona geográfica")
plt.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.show()

# %%
# Conclusiones exploratorias:
# Resumen del gráfico:
# La Unión Europea concentra el mayor importe de ventas de España al exterior,con aproximadamente 61.192 millones de euros acumulados.
# C.E.M.E.A. y América Latina ocupan el segundo y tercer puesto, respectivamente.
# El orden de las zonas es diferente al observado en las compras al exterior.
# Los valores representan ventas acumuladas en todo el histórico disponible, no crecimiento.

# %%
# Queda pendiente comprobar la cobertura temporal de cada zona en las ventas,como hicimos anteriormente con las compras.

# %%
# Comprobamos el primer y último trimestre y la cantidad de trimestres registrados para las ventas de España a cada zona geográfica.

ventas_exterior.groupby("Zona geográfica")["Trimestre"].agg(
    ["min", "max", "nunique"]
)

# %%
# Conclusiones:
# 1.- En las ventas, Reino Unido también aparece por separado desde 2020Q2,con 24 trimestres hasta 2026Q1. Las demás zonas tienen 50 desde 2013Q4.
# 2.- La cobertura temporal de cada zona coincide entre compras y ventas.
# 3.- Podemos comparar compras y ventas dentro de cada zona durante su histórico disponible,teniendo presente que Reino Unido tiene un histórico más corto que las demás.

# %% [markdown]
# ### 5.3.7. Comparación de compras y ventas por zona geográfica.

# %%
# Reunimos las compras y ventas acumuladas de cada zona.
comparacion_por_zona = pd.DataFrame({
    "Compras (€)": compras_por_zona,
    "Ventas (€)": ventas_por_zona
})

# Calculamos la diferencia: ventas menos compras.
comparacion_por_zona["Saldo (€)"] = (
    comparacion_por_zona["Ventas (€)"]
    - comparacion_por_zona["Compras (€)"]
)

comparacion_por_zona

# %%
# Ahora graficaremos la comarativa de compras/ventas de España con respeto a las demás zonas, que como he mencionado hace la vez de un tipo de
# "Balanza comercial para el comercio electrónico"

# %%
# Comparamos compras y ventas por zona geográfica y las expresamos en millones de euros.

(comparacion_por_zona[["Compras (€)", "Ventas (€)"]] / 1_000_000).plot(
    kind="barh",
    figsize=(12,7)
)

plt.title("Balanza histórica entre compras y ventas de España por zona geográfica")
plt.xlabel("Importe acumulado en millones (€)")
plt.ylabel("Zona geográfica")
plt.legend(["Compras desde España al exterior", "Ventas de España al exterior"])
plt.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.show()

# %%
# Conclusiones del gráfico exploratorio

# 1.- La Unión Europea es la zona a la que España vende más, seguida de C.E.M.E.A. y América Latina, según los importes acumulados del histórico disponible.
# 2.- La Unión Europea concentra los mayores importes tanto de compras como de ventas.
# 3.- En la Unión Europea y Reino Unido,son las únicas zonas en las que las compras de España superan a las ventas.


# %% [markdown]
# ### 5.3.8. Gráfico del saldo por zona geográfica.

# %%
# Vamos a generar un gráfico de saldos que dejenn claras las diferencas donde podamos identificar los números en concreto

# %%
saldos = comparacion_por_zona["Saldo (€)"].sort_values() / 1_000_000
# Verde: España vende más de lo que compra
# Rojo: España compra más de lo que vende
colores = ["green" if saldo >= 0 else "red" for saldo in saldos]

ax = saldos.plot(
    kind= "barh",
    figsize=(14,7),
    color = colores
)

# Escribimos el saldo en cada barra, con formato español.
    
etiquetas = [
    f"{saldo:+,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
    for saldo in saldos
]


ax.bar_label(ax.containers[0], labels=etiquetas, padding=5)
ax.margins(x=0.20)

plt.axvline(0, color="black", linewidth=1)
plt.title("Saldo del comercio electrónico de España por zona: acumulado histórico")

plt.xlabel("Ventas − compras (millones de €)")
plt.ylabel("Zona geográfica")
plt.grid(axis="x", alpha=0.3)
plt.figtext(
    0.5, 0.01,
    "Histórico: 2013Q4–2026Q1, excepto Reino Unido: 2020Q2–2026Q1.",
    ha="center"
)
plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.show()

# %%
# Ahora las conclusiones del análisis exploratorio derivadas del gráfico.

# 1.- El saldo representa las ventas menos las compras, en millones de euros.
# 2.- La Unión Europea presenta el mayor saldo negativo: -278.109,3 millones de euros.
# 3.- Reino Unido también presenta saldo negativo: -10.244,6 millones de euros.
# 4.- En ambas zonas, España compra más de lo que vende.
# 5.- América Latina presenta el mayor saldo positivo: +6.418,5 millones de euros.
# 6.- Le siguen C.E.M.E.A. (+3.105,1) y Asia Pacífico (+1.770,2 millones de euros).
# 7.- Resto y Estados Unidos presentan saldos positivos menores: +272,2 y +267,1 millones de euros.
# 8.- En estas cinco zonas, España vende más de lo que compra.

# %% [markdown]
# ### 5.4. Evolución del volumen de negocio por ramas de actividad

# %%
# Analizamos cómo evoluciona el volumen de negocio de las ramas de actividad.
# El objetivo es identificar cuáles crecen, se estancan o retroceden.
# Este será el último apartado del análisis exploratorio y servirá de base
# para el análisis predictivo.

# %% [markdown]
# ### 5.4.1. Volumen de negocio trimestral por rama de actividad

# %%
# Ahora vamos a agrupar por trimestre y rama de actuvidad.
# Sumamos el volumen de negocio para los tres sentidos de transacción: dentro de España, desde España al exterior y desde el exterior a España.

volumen_trimestral_actividad = datos_actividad.groupby(
    ["Trimestre", "Ramas actividad"]
)["Evolución trimestral del volumen de negocio (€)"].sum()

# Organizamos la tabla con una fila por trimestre y una columna por actividad para poder graficar posteriormente.

tabla_volumen_trimestral_actividad = volumen_trimestral_actividad.unstack(
    "Ramas actividad"
)

tabla_volumen_trimestral_actividad.head()

# %%
# Para comparar el crecimiento de todas las actividades sin crear decenas de gráficos, ahora sumaremos por años completos, de 2014 a 2025.
# Excluimos 2013 y 2026 de esta comparación porque solo tenemos un trimestre de cada uno.

# Entonces, la tabla anual simplifica la gráfica, no es tan específica con los trimestres porque de lo contrario se superpondrían varias líneas.

# %% [markdown]
# ### 5.4.2. Volumen de negocio anual por rama de actividad

# %%
# Obtenemos el volumen de negocio anual de cada rama de actividad
# Sumamos los cuatro trimestres y exigimos cuatro valores válidos

volumen_anual_actividad = tabla_volumen_trimestral_actividad.groupby(
    tabla_volumen_trimestral_actividad.index.year
).sum(min_count=4)

# Conservamos únicamente los años completos, de 2014 a 2025
# Excluimos 2013 y 2026 porque solo tenemos un trimestre de cada uno

volumen_anual_actividad = volumen_anual_actividad.loc[2014:2025]
volumen_anual_actividad.index.name = "Año"

# Mostramos los totales anuales de todas las ramas
# Los importes siguen expresados en euros

volumen_anual_actividad

# %%
# Graficar:

import seaborn as sns

# Conservamos las ramas específicas y excluimos "Otros".
datos_grafico = volumen_anual_actividad.drop(
    columns="Otros", errors="ignore"
)

# Obtenemos el volumen del año anterior para cada actividad.
volumen_anterior = datos_grafico.shift(1)

# Calculamos la variación porcentual respecto al año anterior.
# Si el año anterior tiene importe cero, no calculamos el porcentaje.
variacion_interanual = (
    (datos_grafico - volumen_anterior)
    / volumen_anterior.where(volumen_anterior > 0)
) * 100

# Mostramos 2015–2025: usamos 2014 para calcular la variación de 2015.
# Las actividades quedan en filas y los años en columnas.
mapa_actividad = variacion_interanual.loc[2015:2025].T.sort_index()

# Usamos una escala de color simétrica alrededor del cero.
# Limitamos los colores extremos, pero mostramos los porcentajes completos.
limite_color = max(1, mapa_actividad.abs().stack().quantile(0.95))

plt.figure(figsize=(16, max(10, len(mapa_actividad) * 0.35)))

ax = sns.heatmap(
    mapa_actividad,
    mask=mapa_actividad.isna(),
    cmap="RdYlGn",
    center=0,
    vmin=-limite_color,
    vmax=limite_color,
    annot=True,
    fmt=".1f",
    annot_kws={"size": 7},
    linewidths=0.3,
    yticklabels=True,
    cbar_kws={
        "label": "Variación respecto al año anterior (%)",
        "extend": "both"
    }
)

# Las comparaciones sin porcentaje calculable aparecen en gris.
ax.set_facecolor("lightgray")

plt.title(
    "Variación anual del volumen de negocio por rama de actividad\n"
    "Verde: crecimiento · Rojo: disminución · Gris: no calculable\n"
    "Los valores extremos comparten color; las cifras muestran el porcentaje",
    pad=15
)
plt.xlabel("Año")
plt.ylabel("Rama de actividad")
plt.xticks(rotation=0)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

# %%
# Anotación final:
# Cada celda muestra la variación porcentual respecto al año anterior.
# Verde indica crecimiento; rojo, disminución; gris, porcentaje no calculable.
# Un porcentaje positivo menor significa que sigue creciendo, pero más despacio.
# Un crecimiento elevado no implica necesariamente un gran volumen ni rentabilidad.

# %%
# Separamos el volumen de cada actividad por sentido de transacción.
# Los valores representan importes acumulados durante todo el histórico.

volumen_actividad_sentido = datos_actividad.groupby(
    ["Ramas actividad", "Sentido transacción"]
)["Evolución trimestral del volumen de negocio (€)"].sum().unstack()

volumen_actividad_sentido.head(10)

# %%
# Esta tabla separa el volumen de cada actividad por sentido de transacción.
# Permite distinguir las ventas dentro de España y al exterior de las compras al extranjero.
# Los importes son acumulados históricos: no indican crecimiento ni rentabilidad.
# Se muestran las primeras diez actividades por orden alfabético, no las de mayor volumen.

# %% [markdown]
# ## 6. Análisis predictivo

# %% [markdown]
# ### 6.1. Definición del objetivo de predicción

# %%
# Ahora pasamos al análisis predictivo donde nuestro objetivo es conocer cómo se mueve el mercado español en términos de ventas,es decir; su evolución. 
# Esto no determina por sí solo la oportunidad de invertir o no en un sector específico. Para ello sumaremos el volumen de negocio de cada actividad en dos sentidos:
# 1.-Ventas desde España hacia España
# 2.-Ventas de España hacia el extranjero.

# %%
# Primero entrenamos el modelo con los datos de 2014Q4 a 2022Q4.

# Reservamos 2023Q1–2026Q1 para comparar las predicciones con las ventas reales.
# El entrenamiento comienza en 2014Q4 porque necesitamos las ventas del año anterior.

# Hacemos dos evaluaciones:
# 1. Predecir cada trimestre utilizando las ventas reales de los trimestres anteriores.
# 2. Simular que estamos al cierre de 2022 y predecir varios trimestres seguidos,
#    utilizando nuestras propias predicciones cuando ya no haya datos históricos disponibles.
#    En esta segunda evaluación, las ventas reales desde 2023 solo sirven para medir el error.

# Según los resultados, valoraremos si el modelo permite realizar una proyección
# razonable desde 2026Q2 hasta 2028Q4, reentrenándolo con todo el histórico disponible.

# %% [markdown]
# ### 6.1.1. Suma de las ventas dentro de España y al extranjero por trimestre y actividad

# %%
# Seleccionamos las ventas dentro de España y de España hacia el extranjero.

ventas_desde_espana = datos_actividad[
    datos_actividad["Sentido transacción"].isin([
        "Dentro de España",
        "Desde el exterior con España"
    ])
    ]

# Sumamos ambos sentidos para cada trimestre y rama de actividad.

ventas_trimestrales_actividad = ventas_desde_espana.groupby(
    ["Trimestre", "Ramas actividad"]
)["Evolución trimestral del volumen de negocio (€)"].sum().reset_index()

# Mostramos un head().

ventas_trimestrales_actividad.head()

# %%
# Listo, ahora cada fila representa las ventas de cada actividad económica por trimestre detro y desde España al extranjero
# NOTA PERSONAL:
# Es obvio, ero lo voy a dejar asentado; que los datos de compra no interesan en este caso, porque lo que estoy haciendoe es tratar de predecir el comportamento de 
# las ventas para mostrar un panorama amplio del comportamiento de los mercados a futuro en ese rubro.El análisis que hicimos de las compras, únicamente nos
# sirvió para darle contexto al proyecto.

# %% [markdown]
# ### 6.1.2. Exclusión de la categoría "Otros" del análisis predictivo

# %%
# EL dato de "Otros" no ofrece infrmación precisa de los sectores que la contniene, entonces al no tener disponible la información, no nos es de utilidad para
# predecir comportamientos por sector, por eso se ha deterinado eliminarla del análisis predictivo. ES NECESARIO CREAR UNA COPIA PARA GENERAR ESTE ANÁLISIS PARA
# EVITAR COMPROMETER LOS DATOS ORIGINALES.

# %%
ventas_trimestrales_actividad = ventas_trimestrales_actividad[
    ventas_trimestrales_actividad["Ramas actividad"] != "Otros"
    ].copy()

# Comprobamos cuántas actividades quedan
ventas_trimestrales_actividad["Ramas actividad"].nunique()

# %% [markdown]
# #### 6.1.2.1. Revisión de ceros en las ventas trimestrales por actividad

# %%
# Revisamos los ceros en la tabla que vamos a utilizar para el modelo.
# Esta comprobación no elimina ni modifica las ventas.

revision_ceros = ventas_trimestrales_actividad.groupby(
    "Ramas actividad"
)["Evolución trimestral del volumen de negocio (€)"].agg(
    Trimestres="size",
    Trimestres_en_cero=lambda ventas: (ventas == 0).sum()
)

# Calculamos qué porcentaje de los trimestres tiene ventas iguales a cero.
revision_ceros["Porcentaje_en_cero"] = (
    revision_ceros["Trimestres_en_cero"]
    / revision_ceros["Trimestres"]
    * 100
).round(2)

print(
    "Total de registros con ventas en cero:",
    revision_ceros["Trimestres_en_cero"].sum()
)

print(
    "Actividades con algún trimestre en cero:",
    (revision_ceros["Trimestres_en_cero"] > 0).sum()
)

print(
    "Actividades con todos sus trimestres en cero:",
    (
        revision_ceros["Trimestres_en_cero"]
        == revision_ceros["Trimestres"]
    ).sum()
)

# Mostramos las actividades afectadas, empezando por las que tienen más ceros.
revision_ceros[
    revision_ceros["Trimestres_en_cero"] > 0
].sort_values("Trimestres_en_cero", ascending=False)

# %%
# Mostramos la actividad que tiene ventas en cero durante todo el histórico.
revision_ceros[
    revision_ceros["Trimestres_en_cero"] == revision_ceros["Trimestres"]
]

# %%
# Revisión de ceros en la tabla seleccionada para el modelo:

# Hay 1.120 registros con ventas en cero, distribuidos entre 30 actividades.
# "Otra reparación" presenta cero en sus 50 trimestres.
# Conservamos los registros porque no hemos confirmado la causa de esos ceros.
# Esta actividad no aporta variación histórica para aprender su evolución.
# Al evaluar por actividad, su WAPE no será calculable porque sus ventas reales suman cero.

# %% [markdown]
# ### 6.1.3. Comprobación de que cada actividad tiene los 50 trimestres

# %%
# Comprobamos que cada una de las 92 activ tenga los famosos 50 trimestres.

trimestres_por_actividad = ventas_trimestrales_actividad.groupby(
    "Ramas actividad"
)["Trimestre"].nunique()

print("Actividades con 50 trimestres", (trimestres_por_actividad == 50).sum())
print("Actividades con una cantidad diferente:",(trimestres_por_actividad !=50).sum())

# %% [markdown]
# ### 6.1.4. Creación de las variables de año y trimestre 

# %%
# NOTA PERSONAL: Ahora vamos a crear las columnas de año y número de trimestre, PARA QUE EL MODELO PUEDA USAR ESA INFORMACIÓN.

# %%
# Separamos los años y trimestres en dos columnas distintas:

ventas_trimestrales_actividad["Año"] = (
    ventas_trimestrales_actividad["Trimestre"].dt.year
)

ventas_trimestrales_actividad["Numero_trimestre"] = (
    ventas_trimestrales_actividad["Trimestre"].dt.quarter
)

ventas_trimestrales_actividad.head()

# %% [markdown]
# ### 6.1.5. Incorporación de las ventas del trimestre anterior por actividad

# %%
# El siguiente paso es añadir las ventas del trimestre anterior para cada actividad.
# ¿Por qué? Para que el modelo tenga una referencia de cuánto venía vendiendo ese sector. El año y el trimestre indican cuándo ocurre, pero no cuánto se vendía.

# %%
# NOTA PERSONAL: Copiamos las ventas de cada actividad en una columna nueva a la derecha,
# pero desplazadas una fila hacia abajo, sin mezclar actividades.
# Así, cada trimestre tiene al lado las ventas del trimestre anterior como referencia para el modelo.

# %%
# Ordenamos cada actividad desde el trimestre más antiguo hata el más reciente

ventas_trimestrales_actividad = ventas_trimestrales_actividad.sort_values(
    ["Ramas actividad", "Trimestre"]
).reset_index(drop=True)

# Creamos la columna (copiada) con las ventas desplazadas una fila hacia abajo, por separado para caad actividad.

ventas_trimestrales_actividad["Ventas_trimestre_anterior"] = (
    ventas_trimestrales_actividad.groupby("Ramas actividad")[
        "Evolución trimestral del volumen de negocio (€)"
        ].shift(1)
)
    
# Mostramos las primeras cinco filas para comprobar el resultado.
ventas_trimestrales_actividad.head()

# %%
# NOTA PERSONAL: Shift(1) Desplaza la fila hacia abajo y groupby que que cada actividad use sus propias ventas anteriores, sin tomar las de otro sector.

# %% [markdown]
# ### 6.1.6. Añadimos las ventas del mismo trimestre del año anterior

# %%
# Como los datos ya están ordenados por actividad y trimestre, crearemos otra columna con las ventas desplazadas cuatro filas hacia abajo dentro de cada actividad.
# Como cada fila es un trimestre, cuatro filas equivalen a un año.
# Así, junto a las ventas de 2015Q1 aparecerán las de 2014Q1.
# Esto le servirá al mmodelo a comparar la misma temporada de años distintos.

# %%

ventas_trimestrales_actividad["Ventas_mismo_trimestre_año_anterior"] = (
    ventas_trimestrales_actividad.groupby("Ramas actividad")[
        "Evolución trimestral del volumen de negocio (€)"
        ].shift(4)
)

# Mostramos seis filas para comprobar el desplazamiento.
ventas_trimestrales_actividad.head(6)

# %%
# NOTA PERSONAL:
# La columna de referencia es "Evolución trimestral del volumen de negocio (€)" que contiene las ventas del trimestre de cada fila.
# Las dos columnas nuevas salen de esa misma columna, pero con las ventas de un trimestre y de un año antes.
# Son las referencias que usará el modelo para predecir las ventas.

# %% [markdown]
# ### 6.1.7 Creamos una copia sin esos NaN para el modelo predictivo y conservamos la tabla completa.

# %%
# Así evitamos la pérdida de datos hitóricos en la tabla original y trabajamos con DATOS COMPLETOS el modelo de predicción

# %%
# Creamos una copia sin las filas que tienen NaN en las referencias de ventas.

datos_modelo = ventas_trimestrales_actividad.dropna(
    subset=[
        "Ventas_trimestre_anterior",
        "Ventas_mismo_trimestre_año_anterior"
    ]
).copy()

# Comprobamos cuántas filas quedan.
print("Filas para el modelo:", len(datos_modelo))

# %%
# Correcto: quedan 4.232 filas, correspondientes a 92 actividades × 46 trimestres con ambas referencias de ventas completas.

# %% [markdown]
# ### 6.2. Separación de los datos para entrenar y poner a prueba el modelo

# %%
# El objetivo de esta sección es dividir los datos: una parte para que el modelo aprenda
# y otra para comprobar cuánto se equivoca al predecir.

# El histórico empieza en 2013Q4, pero para el modelo empezamos en 2014Q4, porque apartamos las primeras cuatro filas de cada actividad al faltar 
# la referencia del año anterior.
# Entrenamiento: 2014Q4–2022Q4 → 33 trimestres, aproximadamente el 72 %.
# Prueba: 2023Q1–2026Q1 → 13 trimestres, aproximadamente el 28 %.

# %%
# PROCEDIMIETO:
# 1.- Los datos salen de datos_modelo, la tabla que acabamos de crear con 4.232 filas, sin los NA´S de las referencias de ventas.

# 2.- La vamos a dividir en dos tablas:
# datos_entrenamiento: las filas hasta finales de 2022, para que el modelo aprenda
# datos_prueba: las filas desde 2023, para comparar sus predicciones con las ventas reales

# %%
# Tomaremos las filas de datos_modelo hasta finales de 2022 para entrenar

datos_entrenamiento = datos_modelo[
    datos_modelo["Trimestre"] <= pd.Period("2022Q4", freq="Q")
    ].copy()

# Ahora tomamos las filas posteriores para poner a prueba el modelo

datos_prueba = datos_modelo[
    datos_modelo["Trimestre"] > pd.Period("2022Q4", freq="Q")
    ].copy()

# Mostramos cuántas filas tiene cada tabla.
print("Filas de entrenamiento:", len(datos_entrenamiento))
print("Filas de puerba:", len(datos_prueba))

# %% [markdown]
# ### 6.3. Separación de las variables que usará el modelo y las ventas que queremos predecir

# %%
# Nota personal: X contiene los datos del problema y y la respuesta correcta para aprender.

# %%
# Seleccionamos las columnas que nos van a ayudar como pistas para el modelo:

columnas_predictoras = [
    "Ramas actividad",
    "Año",
    "Numero_trimestre",
    "Ventas_trimestre_anterior",
    "Ventas_mismo_trimestre_año_anterior"
]

# Ahora definimos X y y

X_entrenamiento = datos_entrenamiento[columnas_predictoras].copy()

# La respuesta que queremos que aprenda a calcular son las ventas del trimestre.
y_entrenamiento = datos_entrenamiento[
    "Evolución trimestral del volumen de negocio (€)"
].copy()

print("Tamaño de X:", X_entrenamiento.shape)
print("Tamaño de y:", y_entrenamiento.shape)



# %%
# Correcto, entonces son:

# X (3036, 5): 3.036 filas con cinco pistas para el modelo.(O, 5 columnas que se utilizan para aprender a predecir las ventas)
# y (3036,): las 3.036 ventas reales correspondientes, una por cada fila de X.

# %% [markdown]
# ### 6.4. Conversión de los nombres de las actividades en columnas de ceros y unos (Crear variables Dummies)

# %%
# Se convierte únicamente la columna "Ramas actividad" puesto que es la única que no viene en un modo numérico, viene en str o object.

X_entrenamiento_dummies = pd.get_dummies(
    X_entrenamiento,
    columns=["Ramas actividad"],
    dtype=int
)

# Comprobamos el tamaño de la tabla.
print("Tamaño de X codificado:", X_entrenamiento_dummies.shape)

# %% [markdown]
# ### 6.5. Creación y entrenamiento del modelo de Machine Learning

# %%
# Aquí vamos a utilizar Random Forest como primer modelo. Usamos Regressor porque queremos predecir una cantidad:
# las ventas en euros

# %%
# Importamos el modelo:
from sklearn.ensemble import RandomForestRegressor

# %%
# Creamos la structura del modelo

modelo_random_forest = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

# Entrenamos con las pistas (X) y las ventas reales (y)

modelo_random_forest.fit(
    X_entrenamiento_dummies,
    y_entrenamiento
)

print("Modelo entrenado")

# %% [markdown]
# ### 6.6. Preparación de los datos de test o prueba

# %%
# Seleccionamos las mismas pistas que usamos para entrenar.
X_prueba = datos_prueba[columnas_predictoras].copy()

# Guardamos las ventas reales para comprobar las predicciones después.
y_prueba = datos_prueba[
    "Evolución trimestral del volumen de negocio (€)"
].copy()

# Comprobamos los tamaños.
print("Tamaño de X_prueba:", X_prueba.shape)
print("Tamaño de y_prueba:", y_prueba.shape)

# %%
# Ahora convertimos las actividades de X_prueba en dummies, igual que como hice en entrenamiento

# %%
# Convertimos Ramas actividad en dummies

X_prueba_dummies = pd.get_dummies(
    X_prueba,
    columns = ["Ramas actividad"],
    dtype=int
)

# Dejamos las mismas columnas y en ek mismo orden que en el entrenamiento.

X_prueba_dummies = X_prueba_dummies.reindex(
    columns=X_entrenamiento_dummies.columns,
    fill_value=0
)

# Comprobamos el tamaño
print("Tamaño de X_prueba_codificado:", X_prueba_dummies.shape)

# %% [markdown]
# ### 6.7. Predicción de las ventas sobre los datos de prueba

# %%
# El modelo calcula las ventas usando las pistas de prueba

predicciones_prueba = modelo_random_forest.predict(
    X_prueba_dummies
)

# %%
# Mostrar las primeras 5 predicciones en euros.
print(predicciones_prueba)

# %% [markdown]
# ### 6.8. Comparación de las ventas reales y predichas

# %%
# Ahora vamos a juntarlas con as ventas reales para poder compararlas.

comparacion_prueba = datos_prueba[
    ["Trimestre", "Ramas actividad"]
    ].copy()

comparacion_prueba["Ventas reales"] = y_prueba
comparacion_prueba["Ventas predichas"] = predicciones_prueba

# Mostramos las primeras cinco filas.
comparacion_prueba.head()

# %%
# Ahora añadimos la diferencia para cada fila

# %%
# Positivo: predijo de más. Negativo: predijo de menos.

comparacion_prueba["Diferencia"] = (
    comparacion_prueba["Ventas predichas"]
    - comparacion_prueba["Ventas reales"]
)

# Mostramos los importes con dos decimales.
comparacion_prueba.head().round(2)

# %%
# Se hizo la comparativa para obtener la diferencia establecida en euros, sin embargo, lo que ahora es tarea es medir el error.
# Ahora calculamos el MAE Mean Absolute Error, en español Error Absoluto Medio: cuánto se equivoca el modelo en euros, de media, 
# sin que los errores positivos y negativos se cancelen.

# NOTA PERSONAL:
# mae: el valor que calculamos.
# ,: separa los miles con comas.
# .2f: muestra el número con dos decimales.

# %% [markdown]
# ### 6.9. Cálculo del error absoluto medio (MAE)

# %%
# Calculamos el error absoluto medio de las 1196 predicciones.
mae = comparacion_prueba["Diferencia"].abs().mean()

print(f"Error absoluto medio (MAE): {mae:,.2f} €")

# %%
# Es la media de todos los errores, tomados sin signo, de los datos de prueba: desde 2023Q1 hasta 2026Q1. Incluye 92 actividades × 13 trimestres = 1.196 predicciones.
# En promedio, el modelo se equivoca 16,7 millones de euros por actividad y trimestre.

# %% [markdown]
# ### 6.10. Cálculo del error porcentual global (WAPE)

# %%
# Ahora calculamos qué porcentaje representa la suma de los errores absolutos respecto al total de ventas reales de prueba.

# %%
# NOTA PERSONAL
# WAPE significa Weighted Absolute Percentage Error, en español error porcentual absoluto ponderado.
# Cómo se hace? sumamos todos los errores sin signo, los dividimos entre las ventas reales totales y multiplicamos por 100.

# %%
wape = (
    comparacion_prueba["Diferencia"].abs().sum()
    / y_prueba.sum()
) * 100

print(f"Error porcentual global (WAPE): {wape:.2f}%")

# %%
# Conclusiones:
# El WAPE es del 14,85 % en el periodo de prueba (2023Q1–2026Q1).
# Por cada 100 € de ventas reales, se acumulan 14,85 € de error absoluto.
# Es un resultado global: algunas actividades pueden tener más error que otras.
# No significa que el modelo tenga un 85,15 % de aciertos. PORQUE ESTAMOS MIDIENDO CUÁNTO DINERO SE EQUIVOCA, NO CUÁNTAS PREDICCIONES ACIERTA.

# %% [markdown]
# ### 6.11.-Comparar Random Forest con una predicción sencilla. Modelo ingenuo estacional

# %%
# La idea es predecir las mismas ventas que hubo en el mismo trimestre del año anterior de manera sencilla.
# No entrenamos otro modelo: usamos esa regla como referencia y comprobamos cuál de los dos tiene menos error

# %%
# Predice las mismas ventas que en el mismo trimestre del año anterior.

predicciones_referencia = X_prueba[
    "Ventas_mismo_trimestre_año_anterior"
]

# Calculamos el WAPE de esta referencia.
wape_referencia = (
    (predicciones_referencia - y_prueba).abs().sum()
    / y_prueba.sum()
) * 100

# Comparamos los dos métodos sobre los mismos datos de prueba.
# El que tenga menor WAPE tendrá menor error global.
print(f"WAPE del modelo ingenuo estacional: {wape_referencia:.2f}%")
print(f"WAPE de Random Forest: {wape:.2f}%") 

# %%
# Random Forest obtiene un WAPE del 14,85 %, frente al 18,33 % del modelo ingenuo estacional.
# Reduce el error global en 3,48 puntos porcentuales.

# %% [markdown]
# ### 6.12. Evaluación de predicciones de varios trimestres seguidos

# %%
# En concreto,ahora queremos predecir el primer trimestre QUE NO EXISTE usando los datos reales. y para el siguiente usaremos el primero que predijo QUE CREÓ EL MOD.

# %%
# SIMULAMOS QUE ESTAMOS A FINALES DE 2022 Y PREDECIMOS DESDE 2023Q1.
# EMPEZAMOS CON LOS DATOS REALES DISPONIBLES HASTA 2022Q4.
# DESPUÉS USAMOS NUESTRAS PROPIAS PREDICCIONES PARA AVANZAR TRIMESTRE A TRIMESTRE.
# LAS VENTAS REALES DE 2023 EN ADELANTE SOLO SE USARÁN AL FINAL
# PARA COMPARAR Y MEDIR CUÁNTO NOS EQUIVOCAMOS.

# %%
# Guardamos únicamente las ventas reales conocidas hasta finales de 2022
# Esta tabla se irá ampliando con nuestras predicciones.

historial_prediccion = ventas_trimestrales_actividad.loc[
    ventas_trimestrales_actividad["Trimestre"] <= pd.Period("2022Q4", freq="Q"),
    [
        "Trimestre",
        "Ramas actividad",
        "Evolución trimestral del volumen de negocio (€)"]
    ].copy()

# Definimos los trimestrs que vamos a predecir en orden:

trimestres_prediccion = pd.period_range(
    start="2023Q1",
    end="2026Q1",
    freq="Q"
)

# Comprobamos el punto de partida
print("Último trimestre real:", historial_prediccion["Trimestre"].max())
print("Filas del histórico:", len(historial_prediccion))
print("Trimestres que predeciremos:", len(trimestres_prediccion))
                      

# %%
# Tenemos los datos reales de 2023, pero simulamos que todavía no los conocemos.
# Los reservamos para comparar después y medir cuánto se equivoca el modelo.

# Para predecir las ventas de 2023Q1 de cada actividad, usamos dos referencias:
# 1. Las ventas del trimestre inmediatamente anterior: 2022Q4.
# 2. Las ventas del mismo trimestre del año anterior: 2022Q1.

# Son las mismas referencias que creamos con shift(1) y shift(4) al entrenar.

# %%
# Seleccionaos el primer trimestre que vamos a predecir
trimestre = trimestres_prediccion[0]

# Recuperamos las ventas del trimestre anterior: 2022Q4
datos_trimestre = historial_prediccion.loc[
    historial_prediccion["Trimestre"] == trimestre -1,
    ["Ramas actividad", "Evolución trimestral del volumen de negocio (€)"]
    ].rename(columns={
        "Evolución trimestral del volumen de negocio (€)": "Ventas_trimestre_anterior"
        })

# Recuperamos las ventas del mismo trimestre del año anterior: 2022Q1.
datos_año_anterior = historial_prediccion.loc[
    historial_prediccion["Trimestre"] == trimestre - 4,
    ["Ramas actividad", "Evolución trimestral del volumen de negocio (€)"]
].rename(columns={
    "Evolución trimestral del volumen de negocio (€)": "Ventas_mismo_trimestre_año_anterior"
})

# Juntamos ambas referencias, emparejando por actividad
datos_trimestre = datos_trimestre.merge(
    datos_año_anterior,
    on="Ramas actividad",
    how="left",
    validate="one_to_one"
)

# Añadimos el año y el número del trimestre que queremos predecir
datos_trimestre["Año"] = trimestre.year
datos_trimestre["Numero_trimestre"] = trimestre.quarter

# Colocamos las cinco variales en el mismo orden utilizado al entrenar.
datos_trimestre = datos_trimestre[columnas_predictoras]

print("Trimestre que vamos a predecir:", trimestre)
print("Tamaño de la tabla:", datos_trimestre.shape)
print("Valores nulos:", datos_trimestre.isna().sum().sum())

datos_trimestre.head()


# %%
# Convertimos los nombres de las actividades en columnas de ceros y unos.
X_trimestre = pd.get_dummies(
    datos_trimestre,
    columns=["Ramas actividad"],
    dtype=int
)

# Usamos las mismas columnas y el mismo orden que en el entrenamiento.
X_trimestre = X_trimestre.reindex(
    columns=X_entrenamiento_dummies.columns,
    fill_value=0
)

# Calculamos las ventas previstas para 2023Q1 con el modelo ya entrenado.
predicciones_trimestre = modelo_random_forest.predict(X_trimestre)

# Guardamos las predicciones junto a su actividad y trimestre.
resultado_trimestre = datos_trimestre[["Ramas actividad"]].copy()
resultado_trimestre["Trimestre"] = trimestre
resultado_trimestre["Ventas predichas"] = predicciones_trimestre

# Mostramos las primeras cinco predicciones.
resultado_trimestre[
    ["Trimestre", "Ramas actividad", "Ventas predichas"]
].head()

# %%
# Ya tenemos las predicciones de 2023Q1. Ahora las añadimos al histórico para que, al predecir 2023Q2, el modelo utilice estas 
# ventas predichas como referencia del trimestre anterior.

# %%
# Preparamos las predicciones con las mismas columnas que tiene el histórico.
filas_predichas = resultado_trimestre.rename(columns={
    "Ventas predichas": "Evolución trimestral del volumen de negocio (€)"
})[
    ["Trimestre", "Ramas actividad", "Evolución trimestral del volumen de negocio (€)"]
].copy()

# Añadimos las ventas predichas de 2023Q1 al histórico.
historial_prediccion = pd.concat(
    [historial_prediccion, filas_predichas],
    ignore_index=True
)

# Evitamos duplicar registros si ejecutamos esta celda más de una vez.
historial_prediccion = historial_prediccion.drop_duplicates(
    subset=["Trimestre", "Ramas actividad"],
    keep="last",
    ignore_index=True
)

# Comprobamos que se añadieron las 92 predicciones.
print("Último trimestre del histórico:", historial_prediccion["Trimestre"].max())
print("Filas del histórico:", len(historial_prediccion))

# %%
# YA comprobamos el proceso con un trimestre. Ahora lo repetimos automáticamente para los 13, hasta 2026Q1

# %%
# Empezamos únicamente con las ventas reales hasta finales de 2022.
historial_prediccion = ventas_trimestrales_actividad.loc[
    ventas_trimestrales_actividad["Trimestre"] <= pd.Period("2022Q4", freq="Q"),
    ["Trimestre", "Ramas actividad", "Evolución trimestral del volumen de negocio (€)"]
].copy()

# Aquí guardaremos los resultados de todos los trimestres.
resultados_recursivos = []

# Repetimos el proceso para cada trimestre, en orden.
for trimestre in trimestres_prediccion:

    # Recuperamos las ventas del trimestre anterior.
    datos_trimestre = historial_prediccion.loc[
        historial_prediccion["Trimestre"] == trimestre - 1,
        ["Ramas actividad", "Evolución trimestral del volumen de negocio (€)"]
    ].rename(columns={
        "Evolución trimestral del volumen de negocio (€)": "Ventas_trimestre_anterior"
    })

    # Recuperamos las ventas del mismo trimestre del año anterior.
    datos_año_anterior = historial_prediccion.loc[
        historial_prediccion["Trimestre"] == trimestre - 4,
        ["Ramas actividad", "Evolución trimestral del volumen de negocio (€)"]
    ].rename(columns={
        "Evolución trimestral del volumen de negocio (€)": "Ventas_mismo_trimestre_año_anterior"
    })

    # Juntamos las referencias de cada actividad.
    datos_trimestre = datos_trimestre.merge(
        datos_año_anterior,
        on="Ramas actividad",
        how="left",
        validate="one_to_one"
    )

    # Añadimos el año y el número de trimestre.
    datos_trimestre["Año"] = trimestre.year
    datos_trimestre["Numero_trimestre"] = trimestre.quarter
    datos_trimestre = datos_trimestre[columnas_predictoras]

    # Convertimos las actividades en dummies y alineamos las columnas.
    X_trimestre = pd.get_dummies(
        datos_trimestre,
        columns=["Ramas actividad"],
        dtype=int
    ).reindex(
        columns=X_entrenamiento_dummies.columns,
        fill_value=0
    )

    # Predecimos las ventas del trimestre.
    predicciones_trimestre = modelo_random_forest.predict(X_trimestre)

    # Guardamos las predicciones junto a su actividad y trimestre.
    resultado_trimestre = datos_trimestre[["Ramas actividad"]].copy()
    resultado_trimestre["Trimestre"] = trimestre
    resultado_trimestre["Ventas predichas"] = predicciones_trimestre

    resultados_recursivos.append(resultado_trimestre)

    # Incorporamos estas predicciones al histórico para los siguientes trimestres.
    filas_predichas = resultado_trimestre.rename(columns={
        "Ventas predichas": "Evolución trimestral del volumen de negocio (€)"
    })

    historial_prediccion = pd.concat(
        [historial_prediccion, filas_predichas],
        ignore_index=True
    )

# Unimos los resultados de los 13 trimestres en una sola tabla.
predicciones_recursivas = pd.concat(
    resultados_recursivos,
    ignore_index=True
)

print("Primer trimestre predicho:", predicciones_recursivas["Trimestre"].min())
print("Último trimestre predicho:", predicciones_recursivas["Trimestre"].max())
print("Total de predicciones:", len(predicciones_recursivas))

# %%
# Ahora las comparamos con las ventas reales para medir el error

# %%
# Recuperamos las ventas reales del periodo de prueba.
ventas_reales_prueba = datos_prueba[
    ["Trimestre", "Ramas actividad", "Evolución trimestral del volumen de negocio (€)"]
].rename(columns={
    "Evolución trimestral del volumen de negocio (€)": "Ventas reales"
})

# Emparejamos cada predicción con su venta real por trimestre y actividad.
comparacion_recursiva = predicciones_recursivas.merge(
    ventas_reales_prueba,
    on=["Trimestre", "Ramas actividad"],
    how="left",
    validate="one_to_one"
)

# Comprobamos que todas las predicciones encontraron su venta real.
assert comparacion_recursiva["Ventas reales"].notna().all(), (
    "Hay predicciones sin ventas reales asociadas."
)

# Calculamos la diferencia: positivo si predijo de más, negativo si predijo de menos.
comparacion_recursiva["Diferencia"] = (
    comparacion_recursiva["Ventas predichas"]
    - comparacion_recursiva["Ventas reales"]
)

# Calculamos el error absoluto medio en euros.
mae_recursivo = comparacion_recursiva["Diferencia"].abs().mean()

# Calculamos el error porcentual global.
wape_recursivo = (
    comparacion_recursiva["Diferencia"].abs().sum()
    / comparacion_recursiva["Ventas reales"].sum()
) * 100

print(f"MAE de las predicciones encadenadas: {mae_recursivo:,.2f} €")
print(f"WAPE de las predicciones encadenadas: {wape_recursivo:.2f}%")

# %%
# Conclusiones: 
# En la evaluación encadenada, Random Forest obtiene:
# MAE: 31.903.598,85 € por actividad y trimestre.
# WAPE: 28,36 %.
# El WAPE aumenta 13,51 puntos porcentuales respecto a la evaluación que utilizaba ventas reales anteriores.
# Esto muestra un peor resultado al predecir varios trimestres sin nuevos datos reales.
# Falta compararlo con una referencia estacional bajo las mismas condiciones y revisar cómo varía el error según el plazo y la actividad.

# %%
# Calculamos el error absoluto de cada predicción.
comparacion_recursiva["Error absoluto"] = (
    comparacion_recursiva["Diferencia"].abs()
)

# Sumamos los errores y las ventas reales por trimestre.
error_por_trimestre = comparacion_recursiva.groupby("Trimestre")[
    ["Error absoluto", "Ventas reales"]
].sum()

# Calculamos qué porcentaje representan los errores respecto a las ventas reales.
error_por_trimestre["WAPE (%)"] = (
    error_por_trimestre["Error absoluto"]
    / error_por_trimestre["Ventas reales"]
) * 100

# Mostramos el error de cada trimestre por separado.
error_por_trimestre[["WAPE (%)"]].round(2)

# %%
# Conclusiones:

# El WAPE trimestral presenta una tendencia general ascendente:
# Pasa del 13,26 % en 2023Q1 al 39,02 % en 2026Q1.
# El aumento no es continuo: hay descensos puntuales, como en los cuartos trimestres.
# En esta prueba, las predicciones más lejanas presentan mayor error relativo.
# El resultado muestra limitaciones para proyectar varios años sin nuevos datos reales.
# Por ahora, no consideramos validado este modelo para proyectar hasta 2028Q4.

# %%
# Con esto queda analizada la evolución del error del modelo inicial. El siguiente paso es calcular la referencia estacional encadenada para comprobar si Random Forest aporta una mejora en las mismas condiciones.

# %% [markdown]
# ### 6.3. Predicción con el modelo Ingenuo Estacional y comparación con Random Forest

# %%
# No necesita entrenamiento, predice repitiendo las ventas del mismo trimestre del año anterior.

# Seleccionamos las ventas reales de 2022 para cada actividad.
# Son los últimos cuatro trimestres conocidos al comenzar la prueba.

referencia_2022 = ventas_trimestrales_actividad.loc[
    ventas_trimestrales_actividad["Trimestre"].dt.year == 2022,
    [
        "Ramas actividad",
        "Numero_trimestre",
        "Evolución trimestral del volumen de negocio (€)"
    ]
    ].copy()

# Estas ventas sarán las predicciones del modelo ingenuo estacional

referencia_2022 = referencia_2022.rename(columns={
    "Evolución trimestral del volumen de negocio (€)": "Predicción estacional"
})

# Comprobamos el tamaño: 92 actividades x 4 trimestres = 368 filas.

print("Filas de referencia:", len(referencia_2022))

referencia_2022.head()

# %%
# Recuperamos los trimestres, las actividades y las ventas reales de prueba.
comparacion_estacional = datos_prueba[
    [
        "Trimestre",
        "Ramas actividad",
        "Numero_trimestre",
        "Evolución trimestral del volumen de negocio (€)"
    ]
].copy()

# Renombramos las ventas reales para facilitar la comparación.
comparacion_estacional = comparacion_estacional.rename(columns={
    "Evolución trimestral del volumen de negocio (€)": "Ventas reales"
})

# Asignamos la predicción de 2022 que corresponde a cada actividad y trimestre.
# Por ejemplo: todos los primeros trimestres recibirán las ventas de 2022Q1.
comparacion_estacional = comparacion_estacional.merge(
    referencia_2022,
    on=["Ramas actividad", "Numero_trimestre"],
    how="left",
    validate="many_to_one"
)

# Comprobamos que todas las filas tengan una predicción.
print("Filas de prueba:", len(comparacion_estacional))
print(
    "Predicciones sin asignar:",
    comparacion_estacional["Predicción estacional"].isna().sum()
)

comparacion_estacional.head()

# %%
# Calculamos cuánto se equivoca cada predicción, sin signo.
comparacion_estacional["Error absoluto"] = (
    comparacion_estacional["Predicción estacional"]
    - comparacion_estacional["Ventas reales"]
).abs()

# Calculamos el error medio en euros.
mae_estacional = comparacion_estacional["Error absoluto"].mean()

# Calculamos el error porcentual global.
wape_estacional = (
    comparacion_estacional["Error absoluto"].sum()
    / comparacion_estacional["Ventas reales"].sum()
) * 100

# Comparamos ambos modelos para los mismos 13 trimestres de prueba.
print(f"MAE del modelo ingenuo estacional: {mae_estacional:,.2f} €")
print(f"MAE de Random Forest encadenado: {mae_recursivo:,.2f} €")

print(f"\nWAPE del modelo ingenuo estacional: {wape_estacional:.2f}%")
print(f"WAPE de Random Forest encadenado: {wape_recursivo:.2f}%")




# %%
# Comparando ambos modelos en las mismas condiciones durante 13 trimestres:
# Random Forest encadenado obtiene un WAPE del 28,36 %.
# El modelo ingenuo estacional obtiene un WAPE del 30,63 %.
# Random Forest reduce el error global en 2,27 puntos porcentuales.Supera la referencia sencilla, pero esto no garantiza que su error sea
# aceptable para el objetivo del proyecto ni que funcione bien en todas las actividades.

# %% [markdown]
# ### 6.4. Comparación de los modelos en un horizonte de 11 trimestres

# %%
# Seleccionamos los primeros 11 trimestres de la prueba de ambos modelos.
comparacion_rf_11 = comparacion_recursiva.loc[
    comparacion_recursiva["Trimestre"] <= pd.Period("2025Q3", freq="Q")
].copy()

comparacion_estacional_11 = comparacion_estacional.loc[
    comparacion_estacional["Trimestre"] <= pd.Period("2025Q3", freq="Q")
].copy()

# Calculamos el WAPE de Random Forest para esos 11 trimestres.
wape_rf_11 = (
    comparacion_rf_11["Diferencia"].abs().sum()
    / comparacion_rf_11["Ventas reales"].sum()
) * 100

# Calculamos el WAPE del modelo ingenuo estacional para el mismo periodo.
wape_estacional_11 = (
    comparacion_estacional_11["Error absoluto"].sum()
    / comparacion_estacional_11["Ventas reales"].sum()
) * 100

# Mostramos los resultados.
print("Trimestres evaluados:", comparacion_rf_11["Trimestre"].nunique())
print(f"WAPE de Random Forest: {wape_rf_11:.2f}%")
print(f"WAPE del modelo ingenuo estacional: {wape_estacional_11:.2f}%")

# %%
# Conclusiones:
# En realidad y como podemos observar, ambos modelos presentan errores casi idénticos, solo con una diferencia a favor de random fores con un 0.51
# lo que nos hace pensar que no hemos encontrado todavía los modelos que nos puedan aportar una proyección que sea confiable.

# %%
# En este punto, y al conocer los resultados de las predicciones del modelo ingenuo estacional y de Random Forest, he decidido
# buscar otros modelos que puedan ser más adecuados para predecir la evolución de las ventas trimestrales.
# Probaremos con Holt-Winters, un método de suavizado exponencial que combina el nivel de ventas, la tendencia
# y la estacionalidad: cuánto se vende, cómo crecen o disminuyen las ventas y qué patrones se repiten cada año.
# Da más peso a las observaciones recientes y utiliza estos componentes para proyectar las ventas futuras.

# %% [markdown]
# ### 6.5. Predicción de ventas con Holt-Winters

# %% [markdown]
# #### 6.5.1. Preparación de las series de entrenamiento

# %%
# Importación de Holt Winters

from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Organizamos las ventas de entrenamiento
# Cada Fila es un trimestre y cada columna es una actividad

series_entrenamiento_hw = datos_entrenamiento.pivot(
    index="Trimestre",
    columns="Ramas actividad",
    values="Evolución trimestral del volumen de negocio (€)"
).sort_index()

# Comprobamos el periodo, etl tamaño y los valores ausentes.

print("Primer trimestre:", series_entrenamiento_hw.index.min())
print("Último trimestre:", series_entrenamiento_hw.index.max())
print("Tamaño de la tabla:", series_entrenamiento_hw.shape)
print("Valores nulos:", series_entrenamiento_hw.isna().sum().sum())

series_entrenamiento_hw.head()

# %% [markdown]
# #### 6.5.2. Entrenamiento de Holt-Winters por actividad

# %%
# Guardaremos los modelos entrenados por actividad

modelos_hw = {}

# Si una actividad tiene siempre las mismas ventas durante el entrenamiento,
# conservaremos ese valor como predicción constante
actividades_constantes_hw = {}

for actividad in series_entrenamiento_hw.columns:

# Recuperamos las ventas de esta actividad
    
    ventas = series_entrenamiento_hw[actividad]

    if ventas.nunique() == 1:
        actividades_constantes_hw[actividad] = ventas.iloc[0]

    else:
# Expresamos las ventas en millones de euros para facilitar el ajuste
        
        ventas_millones = ventas.to_numpy() / 1_000_000

# Creamos y entrenamos el modelo
        
        modelo = ExponentialSmoothing(
            ventas_millones,
            trend="add",
            damped_trend=True,
            seasonal="add",
            seasonal_periods=4,
            initialization_method="estimated"
        ).fit(optimized=True)

        modelos_hw[actividad] = modelo

print("Modelos Holt-Winters entrenados:", len(modelos_hw))
print("Actividades con ventas constantes:", len(actividades_constantes_hw))

# %% [markdown]
# #### 6.5.3. Predicción de las ventas con Holt-Winters

# %%
# Definimos los mismos 13 trimestres de prueba utilizados anteriormente.

trimestres_prueba_hw = pd.period_range(
    start="2023Q1",
    end="2026Q1",
    freq="Q"
)

resultados_hw = []

for actividad in series_entrenamiento_hw.columns:

    if actividad in actividades_constantes_hw:
        # Para las actividades constantes, repetimos su valor.
        predicciones = [
            actividades_constantes_hw[actividad]
        ] * len(trimestres_prueba_hw)

    else:
        # Predecimos los 13 trimestres y convertimos de millones a euros.
        predicciones = (
            modelos_hw[actividad].forecast(len(trimestres_prueba_hw))
            * 1_000_000
        )

    # Guardamos las predicciones con su actividad y trimestre.
    resultado = pd.DataFrame({
        "Trimestre": trimestres_prueba_hw,
        "Ramas actividad": actividad,
        "Ventas predichas HW": predicciones
    })

    resultados_hw.append(resultado)

# Unimos las predicciones de todas las actividades.
predicciones_hw = pd.concat(resultados_hw, ignore_index=True)

# Comprobamos el resultado antes de evaluar.
print("Total de predicciones:", len(predicciones_hw))
print("Predicciones nulas:", predicciones_hw["Ventas predichas HW"].isna().sum())
print("Predicciones negativas:", (predicciones_hw["Ventas predichas HW"] < 0).sum())

predicciones_hw.head()

# %%
# Vamos a ubicar los registros negativos que encontramos en las ventas que el sistema ha predicho negativamente. (Algo imposible o totalmente incoherente), 
# porque no se pueden vender -50000 € por ejemplo. El objetivo de el proyecto es conocer las VENTAS FUTURAS, no considera pérdidas.

# %%
# Revisamos dónde se encuentran y de qué tamaño son:

# Seleccionamos las predicciones negativas de Holt-Winters.

negativos_hw = predicciones_hw.loc[
predicciones_hw["Ventas predichas HW"] < 0
]

# Contamos los negativos por actividad y mostramos el valor más negativo

resumen_negativos_hw = negativos_hw.groupby("Ramas actividad").agg(
    Trimestres_negativos=("Ventas predichas HW", "size"),
    Prediccion_minima_euros=("Ventas predichas HW","min")
).sort_values("Prediccion_minima_euros")

print("Acrividades con predicciones negativas:", len(resumen_negativos_hw))

display(resumen_negativos_hw.round(2))

# %%
# Ahora sabemos que el modelo escupe 27 actividades con negativos, que a su vez tienen bastantes negativos y de una cantidad considerable de dinero.

# %%
# Utilizareos merge que une cada predicción con su venta real, usando el trimestre y la actividad para emparejarlas

# Unimos las predicciones con las ventas reales de prueba.
comparacion_hw = predicciones_hw.merge(
    ventas_reales_prueba,
    on=["Trimestre", "Ramas actividad"],
    how="left",
    validate="one_to_one"
)

# Comprobamos que todas las predicciones tengan su venta real.
assert comparacion_hw["Ventas reales"].notna().all()

# Calculamos el error de cada predicción sin signo.
comparacion_hw["Error absoluto"] = (
    comparacion_hw["Ventas predichas HW"]
    - comparacion_hw["Ventas reales"]
).abs()

# MAE: cuánto se equivoca, en euros, por actividad y trimestre de media.
mae_hw = comparacion_hw["Error absoluto"].mean()

# WAPE: qué porcentaje representan los errores sobre las ventas reales totales.
wape_hw = (
    comparacion_hw["Error absoluto"].sum()
    / comparacion_hw["Ventas reales"].sum()
) * 100

print(f"MAE de Holt-Winters: {mae_hw:,.2f} €")
print(f"WAPE de Holt-Winters: {wape_hw:.2f}%")

# %%
# Holt‑Winters tiene menos error global que Random Forest en los mismos 13 trimestres:

# %%
# Holt-Winters obtiene un WAPE del 24,13 %, frente al 28,36 % de Random Forest encadenado.
# Reduce el error global en 4,23 puntos porcentuales, incluyendo las predicciones negativas.
# Sin embargo, genera 276 predicciones negativas repartidas entre 27 actividades.
# Por tanto, mejora el resultado global, pero todavía produce valores incoherentes para las ventas.
# Evaluaremos el ajuste comparándolo con este WAPE del 24,13 % y los 276 valores negativos.
# Eliminar los negativos, por sí solo, no demuestra una mejora en la precisión.

# %%
# Desde el análisis exploratorio, vimos que el coportamiento de el mercado tenía comportamiento estacional en los trimestres de año con año, 
# o sea como que las subidas y bajadas se producían en la misma temporada de un año tras otro, por ello:
# Vamos a probar una versión sin tendencia, manteniendo el PATRÓN ESTACIONAL de cuatro trimestres.

# %%
# Guardamos los nuevos modelos por separado para conservar la versión original.
modelos_hw_sin_tendencia = {}

for actividad in series_entrenamiento_hw.columns:

    # Las actividades constantes mantienen la predicción que ya definimos.
    if actividad in actividades_constantes_hw:
        continue

    # Recuperamos las ventas y las expresamos en millones de euros.
    ventas_millones = (
        series_entrenamiento_hw[actividad].to_numpy() / 1_000_000
    )

    # Entrenamos sin tendencia, conservando la estacionalidad anual.
    modelo = ExponentialSmoothing(
        ventas_millones,
        trend=None,
        seasonal="add",
        seasonal_periods=4,
        initialization_method="estimated"
    ).fit(optimized=True)

    modelos_hw_sin_tendencia[actividad] = modelo

print("Modelos entrenados:", len(modelos_hw_sin_tendencia))

# %%
# Perfeto, Ahora vamos a predecir los mismos 13 trimestres y contar los negativos. forecast genera las predicciones

# %%
resultados_hw_sin_tendencia = []

for actividad in series_entrenamiento_hw.columns:

    if actividad in actividades_constantes_hw:
        predicciones = [
            actividades_constantes_hw[actividad]
        ] * len(trimestres_prueba_hw)

    else:
# Predecimos y convertimos de millones a euros
        predicciones = (
            modelos_hw_sin_tendencia[actividad]
            .forecast(len(trimestres_prueba_hw))
            * 1_000_000
        )

    resultado = pd.DataFrame({
        "Trimestre": trimestres_prueba_hw,
        "Ramas actividad": actividad,
        "Ventas predichas HW": predicciones
    })

    resultados_hw_sin_tendencia.append(resultado)

# Reunimos los resultados de todas las actividades en una tabla
predicciones_hw_sin_tendencia = pd.concat(
    resultados_hw_sin_tendencia,
    ignore_index=True
)

print("Total de predicciones:", len(predicciones_hw_sin_tendencia))
print(
    "Predicciones nulas:",
    predicciones_hw_sin_tendencia["Ventas predichas HW"].isna().sum()
)
print(
    "Predicciones negativas:",
    (predicciones_hw_sin_tendencia["Ventas predichas HW"] < 0).sum()
)

# %%
# Pero falta comprobar si también disminuyó el error.
# Vamos a repetir el cálculo de MAE y WAPE, ahora con las nuevas predicciones:

# %%
# Emparejamos las nuevas predicciones con las mismas ventas reales

comparacion_hw_sin_tendencia = predicciones_hw_sin_tendencia.merge(
    ventas_reales_prueba,
    on=["Trimestre", "Ramas actividad"],
    how="left",
    validate="one_to_one"
)

# Comprobamos que todas las predicciones tengan su venta real

assert comparacion_hw_sin_tendencia["Ventas reales"].notna().all()

# Calculamos los errores sin signo.

comparacion_hw_sin_tendencia["Error absoluto"] = (
    comparacion_hw_sin_tendencia["Ventas predichas HW"]
    - comparacion_hw_sin_tendencia["Ventas reales"]
).abs()

# Calculamos el error medio en euros y el error porcentual global

mae_hw_sin_tendencia = (
    comparacion_hw_sin_tendencia["Error absoluto"].mean()
)

wape_hw_sin_tendencia = (
    comparacion_hw_sin_tendencia["Error absoluto"].sum()
    / comparacion_hw_sin_tendencia["Ventas reales"].sum()
) * 100

print(f"MAE sin tendencia: {mae_hw_sin_tendencia:,.2f} €")
print(f"WAPE sin tendencia: {wape_hw_sin_tendencia:.2f}%")

# %%
# # Al eliminar la tendencia, las predicciones negativas disminuyen de 276 a 215,sin embargo, el WAPE aumenta del 24,13 % al 27,79 %.
# Este ajuste reduce los negativos, pero empeora la precisión global.
# Conservamos la configuración original pero queda pendiente resolver los registros en negativo

# %%
# La prueba sin tendencia ya terminó y empeoró el error.Ahora probaremos una adaptación por actividadd,para algunas usaremos un método más sencillo de la misma familia.

# %% [markdown]
# ### 6.5.4. Ajuste del método Holt-Winters según el comportamiento de cada actividad

# %%
# Quitar la tendencia redujo los negativos, pero empeoró el WAPE.
# Por ello, retomamos Holt-Winters original y adaptamos el método únicamente en las actividades donde produjo predicciones negativas.

# 1.- Si sus ventas de entrenamiento son siempre positivas, probaremos Holt-Winters con una transformación logarítmica.
# 2.-Si contienen ceros, probaremos suavizado exponencial simple.
# 3.-Las demás actividades conservarán su modelo original.

# Después evaluaremos el conjunto para comprobar si reduce el error y elimina los negativos, sin modificar las ventas reales.

#  lo que estamos haciendo es combinar ajustes y modelos al mismo tiempo.

# %%
# 1.- Identificamos los negativos en el original

actividades_a_ajustar = predicciones_hw.loc[
    predicciones_hw["Ventas predichas HW"] < 0,
    "Ramas actividad"
    ].unique()

# 2.- Creamos  las listas para separar los ajustes que probaremos.
actividades_log = []
actividades_suavizado_simple =[]

for actividad in actividades_a_ajustar:

    ventas = series_entrenamiento_hw[actividad]

# 3.- Si todas las ventas son positivas aplicaremos logaritmos

    if (ventas > 0).all():
        actividades_log.append(actividad)
    
# 4.- Si hay ceros, probaremos suavizado exponencial simple.
    else:
        actividades_suavizado_simple.append(actividad)

# Comprobamos cuántas actividades quedan en cada grupo.
print("Actividades para logaritmos:", len(actividades_log))
print("Actividades para suavizado simple:", len(actividades_suavizado_simple))
print(
    "Actividades que conservan el modelo original:",
    len(series_entrenamiento_hw.columns) - len(actividades_a_ajustar)
)

# %%
# Listo, ahora podeos entender cuántas actividades existen para aplicar un ajuste distinto.
# Ahora entrenaremos las 3 con ventas siempre positivas usando logaritmos. np.log()transforma las ventas para entrenar.
# después usaremos np.exp() para convertir las predicciones de vuelta a euros.
# La tabla original permanece intacta.

# %%
# Entrenamos Holt-Winters con LOGARITMOs para las 3 actividades.

import numpy as np

modelos_hw_log = {}

for actividad in actividades_log:

    # Transformamos las ventas a escala logarítmica.
    ventas_log = np.log(
        series_entrenamiento_hw[actividad].to_numpy()
    )

    # Entrenamos el modelo con las ventas transformadas.
    modelo = ExponentialSmoothing(
        ventas_log,
        trend="add",
        damped_trend=True,
        seasonal="add",
        seasonal_periods=4,
        initialization_method="estimated"
    ).fit(optimized=True)

    # Guardamos el modelo de cada actividad.
    modelos_hw_log[actividad] = modelo

print("Modelos entrenados con logaritmos:", len(modelos_hw_log))

# %%
 # Ahora entrenamos las 24 actividades con ceros mediante SUAVIZADO EXPONENCIAL SIMPLE
# Entrenamos las 24 actividades con suavizado exponencial simple.

modelos_suavizado_simple = {}

for actividad in actividades_suavizado_simple:

    # Expresamos las ventas en millones de euros.
    ventas_millones = (
        series_entrenamiento_hw[actividad].to_numpy() / 1_000_000
    )

    # Entrenamos sin tendencia ni estacionalidad.
    modelo = ExponentialSmoothing(
        ventas_millones,
        trend=None,
        seasonal=None,
        initialization_method="known",
        initial_level=ventas_millones[0],
        bounds={"smoothing_level": (0, 1)}
    ).fit(optimized=True)

    # Guardamos el modelo de cada actividad.
    modelos_suavizado_simple[actividad] = modelo

print("Modelos de suavizado simple entrenados:", len(modelos_suavizado_simple))

# %%
# Ahora generamos sus predicciones y las incorporamos a una copia de las originales, conservando las otras 65 actividades.

# %%

# Copiamos las predicciones originales para conservarlas.
predicciones_hw_ajustadas = predicciones_hw.copy()

# Sustituimos las predicciones de las 3 actividades con logaritmos.
for actividad in actividades_log:

    predicciones = np.exp(
        modelos_hw_log[actividad].forecast(len(trimestres_prueba_hw))
    )

    filas = predicciones_hw_ajustadas["Ramas actividad"] == actividad

    predicciones_hw_ajustadas.loc[
        filas, "Ventas predichas HW"
    ] = predicciones

# Sustituimos las predicciones de las 24 actividades con suavizado simple.
for actividad in actividades_suavizado_simple:

    # Convertimos las predicciones de millones a euros.
    predicciones = (
        modelos_suavizado_simple[actividad]
        .forecast(len(trimestres_prueba_hw)) * 1_000_000
    )

    filas = predicciones_hw_ajustadas["Ramas actividad"] == actividad

    predicciones_hw_ajustadas.loc[
        filas, "Ventas predichas HW"
    ] = predicciones

# Indicamos qué método se utilizó en cada actividad.
predicciones_hw_ajustadas["Método"] = "Holt-Winters original"

predicciones_hw_ajustadas.loc[
    predicciones_hw_ajustadas["Ramas actividad"].isin(actividades_log),
    "Método"
] = "Holt-Winters con logaritmos"

predicciones_hw_ajustadas.loc[
    predicciones_hw_ajustadas["Ramas actividad"].isin(
        actividades_suavizado_simple
    ),
    "Método"
] = "Suavizado exponencial simple"

# Comprobamos las predicciones del conjunto.
print("Total de predicciones:", len(predicciones_hw_ajustadas))

print(
    "Predicciones nulas:",
    predicciones_hw_ajustadas["Ventas predichas HW"].isna().sum()
)

print(
    "Predicciones negativas:",
    (predicciones_hw_ajustadas["Ventas predichas HW"] < 0).sum()
)

# %%
# Unimos las predicciones ajustadas con las ventas reales
comparacion_hw_ajustadas = predicciones_hw_ajustadas.merge(
    ventas_reales_prueba,
    on=["Trimestre", "Ramas actividad"],
    how="left",
    validate="one_to_one"
)

# Comprobamos que cada predicción tenga su venta real
assert comparacion_hw_ajustadas["Ventas reales"].notna().all()

# Calculamos el error absoluto de cada predicción
comparacion_hw_ajustadas["Error absoluto"] = (
    comparacion_hw_ajustadas["Ventas predichas HW"]
    - comparacion_hw_ajustadas["Ventas reales"]
).abs()

# MAE: error medio en euros.
mae_hw_ajustadas = comparacion_hw_ajustadas["Error absoluto"].mean()

# WAPE: suma de errores absolutos respecto al total de ventas reales.
wape_hw_ajustadas = (
    comparacion_hw_ajustadas["Error absoluto"].sum()
    / comparacion_hw_ajustadas["Ventas reales"].sum()
) * 100

print(f"MAE ajustado: {mae_hw_ajustadas:,.2f} €")
print(f"WAPE ajustado: {wape_hw_ajustadas:.2f}%")

# %%
# Ya resolvimos el problema de los negativos. Todavía falta saber si las nuevas predicciones se acercan más a las ventas reales,
# eso es lo que comprobaremos con el MAE y el WAPE.

# %%
# Unimos cada predicción ajustada con su venta real.
comparacion_hw_ajustadas = predicciones_hw_ajustadas.merge(
    ventas_reales_prueba,
    on=["Trimestre", "Ramas actividad"],
    how="left",
    validate="one_to_one"
)

# Comprobamos que cada predicción tenga su venta real.
assert comparacion_hw_ajustadas["Ventas reales"].notna().all()

# Calculamos cuánto se alejó cada predicción, sin importar el signo.
comparacion_hw_ajustadas["Error absoluto"] = (
    comparacion_hw_ajustadas["Ventas predichas HW"]
    - comparacion_hw_ajustadas["Ventas reales"]
).abs()

# Calculamos el error medio en euros.
mae_hw_ajustadas = comparacion_hw_ajustadas["Error absoluto"].mean()

# Calculamos el error global respecto al total de ventas reales.
wape_hw_ajustadas = (
    comparacion_hw_ajustadas["Error absoluto"].sum()
    / comparacion_hw_ajustadas["Ventas reales"].sum()
) * 100

print(f"MAE ajustado: {mae_hw_ajustadas:,.2f} €")
print(f"WAPE ajustado: {wape_hw_ajustadas:.2f}%")

# %%
# La mejora del WAPE es pequeña: 0,21 puntos porcentuales. Lo más relevante es que conseguimos eliminar los negativos sin empeorar el error global,
#incluso lo redujimos un poco este ajuste mejora al Holt-Winters original en esta prueba, pero todavía no basta para afirmar que sea adecuado para
# proyectar hasta 2028

# %%
# Vamos a comparar los mismos 11 trimestres para los tres modelos.

# Seleccionamos de 2023Q1 a 2025Q3 entre las predicciones que ya calculamos. Así evaluamos una distancia de 11 trimestres, igual a la que queremos proyectar
# después hasta 2028Q4.

# %%
# Seleccionamos los primeros 11 trimestres de la prueba.
comparacion_hw_ajustadas_11 = comparacion_hw_ajustadas.loc[
    comparacion_hw_ajustadas["Trimestre"] <= pd.Period("2025Q3", freq="Q")
].copy()

# Calculamos el WAPE para esos 11 trimestres.
wape_hw_ajustadas_11 = (
    comparacion_hw_ajustadas_11["Error absoluto"].sum()
    / comparacion_hw_ajustadas_11["Ventas reales"].sum()
) * 100

# Comparamos los tres modelos durante el mismo periodo.
print(
    "Trimestres evaluados:",
    comparacion_hw_ajustadas_11["Trimestre"].nunique()
)
print(f"WAPE de Holt-Winters ajustado: {wape_hw_ajustadas_11:.2f}%")
print(f"WAPE de Random Forest: {wape_rf_11:.2f}%")
print(f"WAPE del ingenuo estacional: {wape_estacional_11:.2f}%")

# %%
# Holt-Winters ajustado es el que obtiene menor error de los tres en esta prueba de 11 trimestres, esto CONVIERTE A HOLT WINTERS como nuestro mejor modelo
# hasta ahora, sin embargo todavía no hemos alcanzado la disminución de erores que nos permita generar una proyección de confianza.

# %%
# Sumamos las ventas reales y los errores de cada activiadd
error_por_actividad_hw = comparacion_hw_ajustadas_11.groupby(
    "Ramas actividad"
).agg(
    Ventas_reales_total=("Ventas reales","sum"),
    Error_absoluto_total=("Error absoluto", "sum"),
)

# Calculalmos el WAPE por cada actividad.

# Si sus ventas reales suman cero, el WAPE no se puede calcular.
error_por_actividad_hw["WAPE (%)"] = (
    error_por_actividad_hw["Error_absoluto_total"]
    / error_por_actividad_hw["Ventas_reales_total"].replace(0, np.nan)
) * 100

# Si sus ventas relaes suman cero, el WAPE no se puede calcular.

error_por__actividad_hw = error_por_actividad_hw.sort_values(
    "Error_absoluto_total",
    ascending=False
)

# Mostramos las 15 actividades que más dan por culo

display(error_por_actividad_hw.head(15).round(2))

# %%
# Esta tabla se encuentra en orden alfabético, así que vamos a ordenarla por "mayor error"

display(
    error_por_actividad_hw
    .sort_values("Error_absoluto_total", ascending=False)
    .head(15)
    .style.format({
        "Ventas_reales_total": "{:,.2f}",
        "Error_absoluto_total": "{:,.2f}",
        "WAPE (%)": "{:.2f}"
    }, na_rep="No calculable")
)

# %%
# El modelo ajustado obtiene un WAPE global del 21,70 % en los 11 trimestres,
# pero el error varía considerablemente entre actividades.

# Transporte aéreo y Hoteles acumulan los mayores errores EN EUROS, con WAPE del 35,46 % y 39,29 %, respectivamente.
# Sin embargo, entre las actividades mostradas destacan errores relativos mayores en Muebles(100.21 %), iluminación y hogar (100,21 %) y Servicios auxiliares
# a la intermediación financiera (294,91 %).

# Como el objetivo es comparar las perspectivas de distintos sectores,
# ordenaremos todas las actividades por WAPE para identificar aquellas
# con mayor error relativo y estudiar sus fallos antes de probar nuevos ajustes.

# %%
# Ordenamos todas las actividades por su porcentaje de error.
error_por_actividad_hw = error_por_actividad_hw.sort_values(
    "WAPE (%)",
    ascending=False,
    na_position="last"
)

# Mostramos las 15 actividades con mayor WAPE.
display(
    error_por_actividad_hw.head(15).style.format({
        "Ventas_reales_total": "{:,.2f}",
        "Error_absoluto_total": "{:,.2f}",
        "WAPE (%)": "{:.2f}"
    }, na_rep="No calculable")
)

# %%
# Ahora tenemos identificadas las actividades con mayor error relativo. Destacan:
# 1.-Construcción: WAPE del 431,50 %. Por cada 100 € de ventas reales,cumula 431,50 € de error absoluto.
# 2.-Servicios auxiliares a la intermediación financiera: WAPE del 294,91 %.
# 3.- Actividades cinematográficas y de vídeo: WAPE del 212,80 %.

# También hay actividades con ventas muy pequeñas: Descargas suma solo 140 €. Su WAPE supera el 100 %,
# PERO EL ERROR EN EUROS ES PEQUEÑO. Por eso debemos interpretar ambas columnas juntas.

# %%
# Seleccionamos la actividad con mayor WAPE.
actividad_revisar = error_por_actividad_hw.index[0]

# Recuperamos sus ventas reales y predichas durante los 11 trimestres.
revision_actividad = comparacion_hw_ajustadas_11.loc[
    comparacion_hw_ajustadas_11["Ramas actividad"] == actividad_revisar,
    ["Trimestre", "Ventas reales", "Ventas predichas HW"]
].sort_values("Trimestre").copy()

# Calculamos la diferencia conservando el signo.
revision_actividad["Diferencia"] = (
    revision_actividad["Ventas predichas HW"]
    - revision_actividad["Ventas reales"]
)

print("Actividad:", actividad_revisar)

display(
    revision_actividad.style.format({
        "Ventas reales": "{:,.2f}",
        "Ventas predichas HW": "{:,.2f}",
        "Diferencia": "{:,.2f}"
    })
)

# %% [markdown]
# #### Construcción

# %%
# En Construcción, el modelo sobreestima las ventas en todos los trimestres evaluados.
# Las ventas reales se mantienen relativamente estables hasta 2025Q2,
# mientras las predicciones presentan una subida continuada.
# El cero registrado en 2025Q3 aumenta el error, pero no explica por sí solo
# el mal resultado: la sobreestimación ya venía creciendo desde 2023.

# %%
print(series_entrenamiento_hw[actividad_revisar].tail(12))

# %%
#   Esto nos da una pista importante sobre la subida que predice el modelo.
#   En los últimos tres años del entrenamiento aparecen:
# .-11 trimestres seguidos con ventas registradas en cero.
# .- Un último trimestre, 2022Q4, con ventas de 112.242,50 €.

# %%
# Revisamos la prueba sin tendencia para Construcción,
# para comprobar si reduce la sobreestimación de las ventas.


# Seleccionamos Construcción en la evaluación del modelo sin tendencia.
revision_sin_tendencia = comparacion_hw_sin_tendencia.loc[
    comparacion_hw_sin_tendencia["Ramas actividad"] == actividad_revisar
].copy()

# %%
# Ahora seleccionamos los mismos 11 trimestres y mostramos las ventas:

# Conservamos los mismos 11 trimestres que estamos evaluando.
revision_sin_tendencia = revision_sin_tendencia.loc[
    revision_sin_tendencia["Trimestre"] <= pd.Period("2025Q3", freq="Q")
].copy()

# Mostramos las ventas reales y las predicciones sin tendencia.
display(
    revision_sin_tendencia[
        ["Trimestre", "Ventas reales", "Ventas predichas HW"]
    ]
)

# %%
# No estaría de más cacñcular la estacionalidad y entrenar Construcción sin tendencia ni estacionalidad.
# Ver qué importe predice.
# Evaluar esa nueva versión para decidir si sustituye a la original.

# %%
# Seleccionamos Construcción.
actividad_revisar = "Construcción de inmuebles y obras de ingeniería civil"

# Expresamos sus ventas de entrenamiento en millones de euros.
ventas_construccion = (
    series_entrenamiento_hw[actividad_revisar] / 1_000_000
)

# Entrenamos suavizado exponencial simple.
modelo_construccion_simple = ExponentialSmoothing(
    ventas_construccion.to_numpy(),
    trend=None,
    seasonal=None,
    initialization_method="known",
    initial_level=ventas_construccion.iloc[0],
    bounds={"smoothing_level": (0, 1)}
).fit(optimized=True)

# Generamos 11 predicciones y las convertimos a euros.
predicciones_construccion_simple = (
    modelo_construccion_simple.forecast(11) * 1_000_000
)

print("Predicciones en euros:", predicciones_construccion_simple)

# %%
# Pues tampoco es que estos cambios hayan influido mucho en la recuperación del error, así que al parecer, lo recomadado sería DEJAR ESTÁTICA LA CIFRA
# en todos los trimestres para que el error ni crezca ni disminuya, sino que se congele, no estamos sacrificando precisión en Construcción para mejorar  
# el resultado general.Estamos intentando mejorar la predicción de Construcción y, si lo conseguimos, también reduciremos el error global.

# %%
# Recuperamos la última venta del entrenamiento, en euros.
# .iloc[-1] selecciona el último valor.

ultima_venta_construccion = (
    series_entrenamiento_hw[actividad_revisar].iloc[-1]
)

# Repetimos esa cifra en los 11 trimestres.
predicciones_construccion_ingenua = np.repeat(
    ultima_venta_construccion,
    11
)

print("Predicciones en euros:", predicciones_construccion_ingenua)

# %%
# Ahora corresponde medir el error de esta nueva prueba para compararlo con el 431,50 % original de Construcción.
# Usaremos revision_actividad, que contiene sus ventas reales ordenadas por trimestre:

# %%
# Copiamos la tabla para evaluar esta prueba por separado.
revision_construccion_ingenua = revision_actividad.copy()

# Añadimos las 11 predicciones que acabamos de generar.
revision_construccion_ingenua["Predicción ingenua"] = (
    predicciones_construccion_ingenua
)

# Calculamos el error de cada trimestre, sin signo.
revision_construccion_ingenua["Error absoluto ingenuo"] = (
    revision_construccion_ingenua["Predicción ingenua"]
    - revision_construccion_ingenua["Ventas reales"]
).abs()

# Calculamos el WAPE de Construcción con esta nueva predicción.
wape_construccion_ingenua = (
    revision_construccion_ingenua["Error absoluto ingenuo"].sum()
    / revision_construccion_ingenua["Ventas reales"].sum()
) * 100

print(f"WAPE de Construcción con método ingenuo: {wape_construccion_ingenua:.2f}%")

# %%
# Esto significa que, por cada 100 € de ventas reales, ahora acumulamos 33,76 € de error absoluto, frente a los 431,50 € anteriores.

# %%
# En Construcción, repetir la última venta conocida reduce el WAPE
# del 431,50 % al 33,76 % durante los 11 trimestres evaluados.
# Esta alternativa mejora claramente el resultado de Holt-Winters,
# aunque todavía presenta error y no garantiza la misma precisión futura.
# Las predicciones de las demás actividades permanecen sin cambios.

# %%
# Lo siguiente que tenemos que hacer es introducir este cambio al conjunto y medirlo todo de nuevo.

# %%
# Copiamos la evaluación de los 11 trimestres.
comparacion_hw_ajustadas_11_v2 = comparacion_hw_ajustadas_11.copy()

# Identificamos las filas de Construcción.
filas_construccion = (
    comparacion_hw_ajustadas_11_v2["Ramas actividad"]
    == "Construcción de inmuebles y obras de ingeniería civil"
)

# Sustituimos sus predicciones por la última venta del entrenamiento.
comparacion_hw_ajustadas_11_v2.loc[
    filas_construccion, "Ventas predichas HW"
] = ultima_venta_construccion

# Actualizamos el nombre del método para esta actividad.
comparacion_hw_ajustadas_11_v2.loc[
    filas_construccion, "Método"
] = "Ingenuo no estacional"

# Recalculamos los errores con las predicciones actualizadas.
comparacion_hw_ajustadas_11_v2["Error absoluto"] = (
    comparacion_hw_ajustadas_11_v2["Ventas predichas HW"]
    - comparacion_hw_ajustadas_11_v2["Ventas reales"]
).abs()

# Calculamos el nuevo WAPE global.
wape_hw_ajustadas_11_v2 = (
    comparacion_hw_ajustadas_11_v2["Error absoluto"].sum()
    / comparacion_hw_ajustadas_11_v2["Ventas reales"].sum()
) * 100

print("Predicciones sustituidas:", filas_construccion.sum())
print(f"WAPE global anterior: {wape_hw_ajustadas_11:.4f}%")
print(f"WAPE global actualizado: {wape_hw_ajustadas_11_v2:.4f}%")

# %%
# Sustituimos las 11 predicciones de Construcción por la última venta conocida.
# Su WAPE baja del 431,50 % al 33,76 %, mientras que el WAPE global
# disminuye del 21,7014 % al 21,6959 %.
# La mejora global es pequeña porque esta actividad tiene poco volumen
# de ventas respecto al conjunto.

# %% [markdown]
# #### Servicios auxiliares a la intermediación financiera

# %%
# La siguiente actividad a revisar es Servicios auxiliares a la intermediación financiera, con un WAPE del 294,91 %. Primero compararemos sus ventas reales y predichas,
# sin asumir que necesita el mismo ajuste.

# %%
# Seleccionamos la siguiente actividad que vamos a revisar

actividad_revisar = "Servicios auxiliares a la intermediación financiera"

# Recuperamos sus ventas reales y predichas en los 11 trimestres

revision_actividad = comparacion_hw_ajustadas_11_v2.loc[
    comparacion_hw_ajustadas_11_v2["Ramas actividad"] == actividad_revisar,
    ["Trimestre", "Ventas reales", "Ventas predichas HW"]
].sort_values("Trimestre").copy()

# Un resultado positivo indica que predijimos de más
# uno negativo indica que predijimos de menos

revision_actividad["Diferencia"] = (
    revision_actividad["Ventas predichas HW"]
    - revision_actividad["Ventas reales"]
)

display(
    revision_actividad.style.format({
        "Ventas reales": "{:,.2f}",
        "Ventas predichas HW": "{:,.2f}",
        "Diferencia": "{:,.2f}"
    })
)

# %%
# Como podemos ver, ésta extracción nos muestra que el modelo calculó subidas progresivas en las ventas, mientras que las ventas reales indican lo contrario,
# de ahí que se pueda explicar el aumeto del error. LO MÁS RECOMENDABLE ES VER SI ÉSTA CAÍDA COMIENZA CON EL ENTRENAMIENTO.
# El entrenamiento termina en 2022Q4 y esta tabla empieza en 2023Q1. Nos falta ver lo que ocurrió justo antes.

# %%
# Revisamos los últimos 12 trimestres del entrenamiento.
print(series_entrenamiento_hw[actividad_revisar].tail(12))

# %%
# Ahora vamos a comprobar si la versión sin tendencia, entrenada con esas mismas ventas reales hasta 2022, predijo cifras más cercanas a lo que ocurrió.

# %%
# Seleccionamos la activodad y los 11 trimestre de prueba

revision_intermediacion_sin_tendencia = comparacion_hw_sin_tendencia.loc[
    (comparacion_hw_sin_tendencia["Ramas actividad"] == actividad_revisar)
    & (comparacion_hw_sin_tendencia["Trimestre"] <= pd.Period("2025Q3", freq="Q")),
    ["Trimestre", "Ventas reales", "Ventas predichas HW"]
].sort_values("Trimestre").copy()

# Mostramos las ventas reales y las predicciones sin tendencia

display(
    revision_intermediacion_sin_tendencia.style.format({
        "Ventas reales": "{:,.2f}",
        "Ventas predichas HW": "{:,.2f}"
    })
)


# %%
# Ahroa como podemos observar, tenemos que a partir de 2023 las ventas reales se desploman drásticamente progresivamente entre el 2023 y 2024, teniendo después
# registros neutrales a la baja, mientras que las predichas siguen una tendencia bastante equilibrada, pero con registros mucho más altos que los reales.

# %%
# Calculamos el WAPE de Intermediación con el modelo sin tendencia.
wape_intermediacion_sin_tendencia = (
    (
        revision_intermediacion_sin_tendencia["Ventas predichas HW"]
        - revision_intermediacion_sin_tendencia["Ventas reales"]
    ).abs().sum()
    / revision_intermediacion_sin_tendencia["Ventas reales"].sum()
) * 100

print(f"WAPE sin tendencia: {wape_intermediacion_sin_tendencia:.2f}%")

# %%
# El WAPE disminuyó muy poquito y sigue siendo muy alto, por tanto la otra alternativa que se me ocurre es revisar los wapes de la misma actividad en los modelos
# que utiliamos previamente para ver si es aplicable una mejora. Esta mejora la voy a considerar como provisional.
# AQUÍ EL PROBLEMA REAL ES QUE ESA CAÍDA QUE SE TUVO EN LA ACTIVIDAD DE 50 A 7, ES UN EVENTO MUY DIFÍCIL DE PRONOSTICAR PARA CUALQUIER MODELO, ASÍ QUE SOSPOCHO QUE 
# DIFICILMENTE TENGAMOS UN AJUSTE QUE VAYA A DISMINUIR EL ERROR,Y EN CONSECUENCIA, QUIZÁ TENGAMOS QUE INDICAR QUE NO HEMOS CONSEGUIDO FIABILIDAD PARA ESTA ACTIVIDAD.

# %%
# Copiamos el conjunto que ya incluye el ajuste de Construcción.
comparacion_hw_ajustadas_11_v3 = comparacion_hw_ajustadas_11_v2.copy()

# Identificamos las filas de Intermediación.
filas_intermediacion = (
    comparacion_hw_ajustadas_11_v3["Ramas actividad"]
    == "Servicios auxiliares a la intermediación financiera"
)

# Sustituimos sus predicciones, emparejándolas por trimestre.
comparacion_hw_ajustadas_11_v3.loc[
    filas_intermediacion, "Ventas predichas HW"
] = comparacion_hw_ajustadas_11_v3.loc[
    filas_intermediacion, "Trimestre"
].map(
    revision_intermediacion_sin_tendencia.set_index("Trimestre")[
        "Ventas predichas HW"
    ]
)

# Actualizamos el método utilizado.
comparacion_hw_ajustadas_11_v3.loc[
    filas_intermediacion, "Método"
] = "Holt-Winters sin tendencia"

# Recalculamos los errores.
comparacion_hw_ajustadas_11_v3["Error absoluto"] = (
    comparacion_hw_ajustadas_11_v3["Ventas predichas HW"]
    - comparacion_hw_ajustadas_11_v3["Ventas reales"]
).abs()

# Calculamos el WAPE global actualizado.
wape_hw_ajustadas_11_v3 = (
    comparacion_hw_ajustadas_11_v3["Error absoluto"].sum()
    / comparacion_hw_ajustadas_11_v3["Ventas reales"].sum()
) * 100

print(f"WAPE global anterior: {wape_hw_ajustadas_11_v2:.4f}%")
print(f"WAPE global actualizado: {wape_hw_ajustadas_11_v3:.4f}%")

# %%
# Bien, El WAPE global baja de 21,6959 % a 21,6039 %: una mejora de 0,092 puntos porcentuales.

# %% [markdown]
# #### Actividades cinematográficas y de vídeo

# %%
# Seleccionamos la actividad que vamos a revisar.
actividad_revision_cine = "Actividades cinematográficas y de vídeo"

# Recuperamos sus ventas reales y predichas en los 11 trimestres de prueba.
revision_cine = comparacion_hw_ajustadas_11_v3.loc[
    comparacion_hw_ajustadas_11_v3["Ramas actividad"] == actividad_revision_cine,
    ["Trimestre", "Ventas reales", "Ventas predichas HW"]
].sort_values("Trimestre").copy()

# Calculamos la diferencia conservando el signo.
revision_cine["Diferencia"] = (
    revision_cine["Ventas predichas HW"]
    - revision_cine["Ventas reales"]
)

display(
    revision_cine.style.format({
        "Ventas reales": "{:,.2f}",
        "Ventas predichas HW": "{:,.2f}",
        "Diferencia": "{:,.2f}"
    })
)

# %%
# Lo mismo que anteriormente, el modelo en realidad predice con cierta lógica, pues sigue una línea de tendencia coherente, sin emabrgo, las ventas reales caen
# drásticamente desde 2024 y se mantieneen así el resto de los trimestres registrados. Lo que evidentemente resta certeza a la predicción de esa actividad.

# %%
# Recuperamos la versión sin tendencia para Cine en los mismos 11 trimestres.
revision_cine_sin_tendencia = comparacion_hw_sin_tendencia.loc[
    (comparacion_hw_sin_tendencia["Ramas actividad"] == actividad_revision_cine)
    & (comparacion_hw_sin_tendencia["Trimestre"] <= pd.Period("2025Q3", freq="Q")),
    ["Trimestre", "Ventas reales", "Ventas predichas HW"]
].sort_values("Trimestre").copy()

# Mostramos las ventas reales frente a las predicciones sin tendencia.
display(
    revision_cine_sin_tendencia.style.format({
        "Ventas reales": "{:,.2f}",
        "Ventas predichas HW": "{:,.2f}"
    })
)

# %%
# Calculamos el WAPE de Cine con las predicciones sin tendencia.
wape_cine_sin_tendencia = (
    (
        revision_cine_sin_tendencia["Ventas predichas HW"]
        - revision_cine_sin_tendencia["Ventas reales"]
    ).abs().sum()
    / revision_cine_sin_tendencia["Ventas reales"].sum()
) * 100

print(f"WAPE de Cine sin tendencia: {wape_cine_sin_tendencia:.2f}%")

# %%
# Sucede lo mismo, era de esperar que el error se mantuviera alto, puesto que que las caídas reales de ventas fueron inesperadas y muy drásticas.
# El WAPE de Cine baja del 212,80 % al 201,22 %, una mejora de 11,58 puntos porcentuales. Sigue siendo muy alto. Quitar la tendencia mejora esta prueba, 
# pero no resuelve el fallo ante el desplome de las ventas.

# %%
# Copiamos el conjunto con los ajustes anteriores

comparacion_hw_ajustadas_11_v4 = comparacion_hw_ajustadas_11_v3.copy()

# Identificamos las filas de Cine

filas_cine = (
    comparacion_hw_ajustadas_11_v4["Ramas actividad"]
    == actividad_revision_cine
)

# Sustituimos sus predicciones, emparejándolas por trimestre

comparacion_hw_ajustadas_11_v4.loc[
    filas_cine, "Ventas predichas HW"
] = comparacion_hw_ajustadas_11_v4.loc[
    filas_cine, "Trimestre"
].map(
    revision_cine_sin_tendencia.set_index("Trimestre")[
        "Ventas predichas HW"
    ]
)

# Actualizamos el método utilizado

comparacion_hw_ajustadas_11_v4.loc[
    filas_cine, "Método"
] = "Holt-Winters sin tendencia"

# Recalculamos los errores

comparacion_hw_ajustadas_11_v4["Error absoluto"] = (
    comparacion_hw_ajustadas_11_v4["Ventas predichas HW"]
    - comparacion_hw_ajustadas_11_v4["Ventas reales"]
).abs()

# Calculamos el WAPE global actualizado

wape_hw_ajustadas_11_v4 = (
    comparacion_hw_ajustadas_11_v4["Error absoluto"].sum()
    / comparacion_hw_ajustadas_11_v4["Ventas reales"].sum()
) * 100

print(f"WAPE global anterior: {wape_hw_ajustadas_11_v3:.4f}%")
print(f"WAPE global actualizado: {wape_hw_ajustadas_11_v4:.4f}%")

# %% [markdown]
# ### Revisión de actividades con mayor variación en EUROS

# %%
# En actividades con pocas ventas, un error pequeño en euros puede representar un porcentaje de error muy alto, aunque tenga poco peso en el WAPE global.
# Por eso, ahora revisaremos las actividades con mayor error acumulado en euros,para identificar dónde una mejora podría reducir más el error global.

# Este pretendo que sea el último paso para realizar los ajustes correspondientes.Hemos tratado de disminuir el error hasta un 20%, sin embargo las mismas
# variabciones drásticas en las ventas reales limitan y entorpecen el trabajo de predicción, por ello cerraremos este módulo con la revisión de 2 o 3 actividades
# más pero con el enfoque en los EUROS.
# Después cerraremos la evaluación, generaremos los pronósticos hasta 2028 y prepararemos las tablas para crear las visualizaciones en Power BI.

# %%
# Sumamos el error absoluto actualizado de cada actividad.
error_total_euros_por_actividad = (
    comparacion_hw_ajustadas_11_v4
    .groupby("Ramas actividad")["Error absoluto"]
    .sum()
    .sort_values(ascending=False)
)

# Mostramos las diez actividades con mayor error acumulado en euros.
display(
    error_total_euros_por_actividad.head(10)
    .to_frame("Error absoluto total")
    .style.format({"Error absoluto total": "{:,.2f}"})
)

# %%
# Transporte aéreo es la actividad que acumula más error: 2.902 millones de euros durante los 11 trimestres. Le siguen Hoteles y Agencias de viajes.
# Estas serán las tres actividades de nuestra última revisión.
# Empezamos por Transporte aéreo, comparando ventas reales y predichas para ver dónde falla:

# %% [markdown]
# ####  Transporte aereo

# %%
# Seleccionamos las ventas reales y las predichas de TRansporte aereo.

revision_transporte_aereo = comparacion_hw_ajustadas_11_v4.loc[
    comparacion_hw_ajustadas_11_v4["Ramas actividad"] == "Transporte aéreo",
    ["Trimestre","Ventas reales","Ventas predichas HW"]
].sort_values("Trimestre").copy()

# Positivo: Se predijo de más.
# Negativo: Se predjo de menos

revision_transporte_aereo["Diferencia"] =(
    revision_transporte_aereo["Ventas predichas HW"]
    - revision_transporte_aereo["Ventas reales"]
)

# Mostramos la comparación en euros:

display(
    revision_transporte_aereo.style.format({
        "Ventas reales": "{:,.2f}",
        "Ventas predichas HW": "{:,.2f}",
        "Diferencia": "{:,.2f}"
    })
)

# %%
# Lo que hicimos fue: Creamos un nuevo objeto llamado revision_transporte_aereo a partir de la tabla comparacion_hw_ajustadas_11_v4.
# Seleccionamos las filas donde “Ramas actividad” sea “Transporte aéreo” y conservamos únicamente las columnas “Trimestre”, “Ventas reales” y 
# “Ventas predichas HW”. Después ordenamos esas filas por trimestre y hacemos una copia para trabajar con ella sin modificar la tabla original.

# %%
# Ahora revisando el resultado, nos damos cuenta que l sventas reales crecieron mucho más de lo que se pronosticó, por ello vamos a aplicar a ajustes
# a este conjunto de datos, pero no sin antes comprobar si ese crecimiento ya aparecía al final del entrenamiento.

# %%
# REvisamos los últimos 12 trimestres del entrenamiento de Transporte aéreo.

display(
    series_entrenamiento_hw["Transporte aéreo"]
    .tail(12)
    .to_frame("Ventas reales")
    .style.format({"Ventas reales": "{:,.2f}"})
)

# %%
# El Holt-Winters que utilizamos tiene tendencia amortiguada: hace que el crecimiento previsto pierda fuerza conforme avanzamos hacia el futuro.#
# Eso podría estar contribuyendo a que las predicciones se queden cortas.

# La siguiente prueba es mantener la tendencia y la estacionalidad, pero quitar la amortiguación. Así comprobaremos si prolongar el crecimiento detectado durante
# el entrenamiento mejora las predicciones. Es una prueba con fundamento, aunque todavía no sabemos si reducirá el error.

# %%
# Entrenamos solo Transporte aéreo, cambiando damped_trend=True por False, y generamos las 11 predicciones:

# damped_trend=False Indica una tendencia aditiva: el modelo estima cuánto aumentan o disminuyen las ventas en euros por trimestre, no en porcentaje.

# Expresamos las ventas de entrenamiento en millones de euros.
ventas_transporte_aereo = (
    series_entrenamiento_hw["Transporte aéreo"].to_numpy() / 1_000_000
)

# Entrenamos manteniendo tendencia y estacionalidad, pero sin amortiguación.
modelo_transporte_aereo_sin_amortiguacion = ExponentialSmoothing(
    ventas_transporte_aereo,
    trend="add",
    damped_trend=False,
    seasonal="add",
    seasonal_periods=4,
    initialization_method="estimated"
).fit(optimized=True)

# Generamos las 11 predicciones y las convertimos a euros.
predicciones_transporte_aereo_sin_amortiguacion = (
    modelo_transporte_aereo_sin_amortiguacion.forecast(11) * 1_000_000
)

# Copiamos la tabla para comparar esta prueba con el modelo anterior.
revision_transporte_aereo_sin_amortiguacion = revision_transporte_aereo.copy()

revision_transporte_aereo_sin_amortiguacion["Predicción sin amortiguación"] = (
    predicciones_transporte_aereo_sin_amortiguacion
)

display(
    revision_transporte_aereo_sin_amortiguacion[
        ["Trimestre", "Ventas reales", "Ventas predichas HW",
         "Predicción sin amortiguación"]
    ].style.format({
        "Ventas reales": "{:,.2f}",
        "Ventas predichas HW": "{:,.2f}",
        "Predicción sin amortiguación": "{:,.2f}"
    })
)

# %%
# En realidad cambia muy poco, solo pronostica un poco más de ventas, dejando claro que este ajuste se queda corto.

# Calculamos el WAPE para ver cuánto afecta al modelo en lo que corresponde a transporte aereo..
# Calculamos el WAPE de Transporte aéreo sin amortiguación

wape_transporte_aereo_sin_amortiguacion = (
    (
        revision_transporte_aereo_sin_amortiguacion["Predicción sin amortiguación"]
        - revision_transporte_aereo_sin_amortiguacion["Ventas reales"]
    ).abs().sum()
    / revision_transporte_aereo_sin_amortiguacion["Ventas reales"].sum()
) * 100

print(
    f"WAPE de Transporte aéreo sin amortiguación: "
    f"{wape_transporte_aereo_sin_amortiguacion:.2f}%"
)

# %%
# Guardamos la actualización del ajuste para aplicarlo al final al modelo

# %%
# Identificamos las filas de Transporte aéreo.
filas_transporte_aereo = (
    comparacion_hw_ajustadas_11_v4["Ramas actividad"] == "Transporte aéreo"
)

# Incorporamos las nuevas predicciones, emparejándolas por trimestre.
comparacion_hw_ajustadas_11_v4.loc[
    filas_transporte_aereo, "Ventas predichas HW"
] = comparacion_hw_ajustadas_11_v4.loc[
    filas_transporte_aereo, "Trimestre"
].map(
    revision_transporte_aereo_sin_amortiguacion.set_index("Trimestre")[
        "Predicción sin amortiguación"
    ]
)

# Actualizamos el método utilizado.
comparacion_hw_ajustadas_11_v4.loc[
    filas_transporte_aereo, "Método"
] = "Holt-Winters sin amortiguación"

# Actualizamos los errores con las predicciones incorporadas.
comparacion_hw_ajustadas_11_v4["Error absoluto"] = (
    comparacion_hw_ajustadas_11_v4["Ventas predichas HW"]
    - comparacion_hw_ajustadas_11_v4["Ventas reales"]
).abs()

print("Predicciones de Transporte aéreo actualizadas:", filas_transporte_aereo.sum())

# %% [markdown]
# #### Hoteles y alojamientos similares

# %%
# Seleccionamos las ventas reales y predichas de Hoteles

revision_hoteles = comparacion_hw_ajustadas_11_v4.loc[
    comparacion_hw_ajustadas_11_v4["Ramas actividad"]
    == "Hoteles y alojamientos similares",
    ["Trimestre", "Ventas reales", "Ventas predichas HW"]
].sort_values("Trimestre").copy()

# Positivo: se predijo de más.
# Negativo: se predijo de menos.

revision_hoteles["Diferencia"] = (
    revision_hoteles["Ventas predichas HW"]
    - revision_hoteles["Ventas reales"]
)
# Mostramos la comparación en euros
display(
    revision_hoteles.style.format({
        "Ventas reales": "{:,.2f}",
        "Ventas predichas HW": "{:,.2f}",
        "Diferencia": "{:,.2f}"
    })
)
    

# %%
# Como podemos observar, existen diferencias significativas pronosticadas a la baja.
# Las predicciones reflejan los picos del segundo y tercer trimestre, pero el crecimiento previsto es demasiado pequeño.
# Antes de elegir el ajuste, revisamos cómo terminaba el entrenamiento:

# %%
# Revisamos los últimos 12 trimestres del entrenamiento de Hoteles.
display(
    series_entrenamiento_hw["Hoteles y alojamientos similares"]
    .tail(12)
    .to_frame("Ventas reales")
    .style.format({"Ventas reales": "{:,.2f}"})
)

# %%
# La recuperación ya era visible en el entrenamiento: todos los trimestres,de 2022 superan a los de 2021. Además, se repite el pico de ventas
# en el tercer trimestre.
# Vamos a probar Holt-Winters sin amortiguación, manteniendo la estacionalidad, para comprobar si mejora el crecimiento previsto. 

# %%
# Expresamos las ventas de entrenamiento en milloes de euros

ventas_hoteles = (
    series_entrenamiento_hw["Hoteles y alojamientos similares"]
    .to_numpy() / 1_000_000
)

# Entrenamos con tendencia y estacionalidad, pero sin la amortiguación.
modelo_hoteles_sin_amortiguacion = ExponentialSmoothing(
    ventas_hoteles,
    trend="add",
    damped_trend=False,
    seasonal="add",
    seasonal_periods=4,
    initialization_method="estimated"
).fit(optimized=True)

# Generamos las  11 predicciones y las convertimos en euros
predicciones_hoteles_sin_amortiguacion = (
    modelo_hoteles_sin_amortiguacion.forecast(11) * 1_000_000)

# Guardamos la prueba por separado para compararla.
revision_hoteles_sin_amortiguacion = revision_hoteles.copy()

revision_hoteles_sin_amortiguacion["Predicción sin amortiguación"] = (
    predicciones_hoteles_sin_amortiguacion
)

display(
    revision_hoteles_sin_amortiguacion[
        ["Trimestre", "Ventas reales", "Ventas predichas HW",
         "Predicción sin amortiguación"]
    ].style.format({
        "Ventas reales": "{:,.2f}",
        "Ventas predichas HW": "{:,.2f}",
        "Predicción sin amortiguación": "{:,.2f}"
    })
)

# %%
# Nos seguimos quedando cortos sin amortiguación, no mejora mucho el pronóstico.
# Vamos a rebelar el wape de la actividad sin amortiguación

# Calculamos el WAPE de Hoteles sin amortiguación.
wape_hoteles_sin_amortiguacion = (
    (
        revision_hoteles_sin_amortiguacion["Predicción sin amortiguación"]
        - revision_hoteles_sin_amortiguacion["Ventas reales"]
    ).abs().sum()
    / revision_hoteles_sin_amortiguacion["Ventas reales"].sum()
) * 100

print(f"WAPE de Hoteles sin amortiguación: {wape_hoteles_sin_amortiguacion:.2f}%")



# %%
# El WAPE de Hoteles baja del 39,29 % al 38,08 %: mejora 1,21 puntos porcentuales, aunque sigue siendo elevado.

# %%
# Ahora toca de nuevo incorporar el ajuste para aplicarlo al final como hicimos anteriormente.

# Identificamos las filas de Hoteles.
filas_hoteles = (
    comparacion_hw_ajustadas_11_v4["Ramas actividad"]
    == "Hoteles y alojamientos similares"
)

# Incorporamos las nuevas predicciones, emparejándolas por trimestre.
comparacion_hw_ajustadas_11_v4.loc[
    filas_hoteles, "Ventas predichas HW"
] = comparacion_hw_ajustadas_11_v4.loc[
    filas_hoteles, "Trimestre"
].map(
    revision_hoteles_sin_amortiguacion.set_index("Trimestre")[
        "Predicción sin amortiguación"
    ]
)

# Actualizamos el método utilizado.
comparacion_hw_ajustadas_11_v4.loc[
    filas_hoteles, "Método"
] = "Holt-Winters sin amortiguación"

# Actualizamos los errores.
comparacion_hw_ajustadas_11_v4["Error absoluto"] = (
    comparacion_hw_ajustadas_11_v4["Ventas predichas HW"]
    - comparacion_hw_ajustadas_11_v4["Ventas reales"]
).abs()

print("Predicciones de Hoteles actualizadas:", filas_hoteles.sum())

# %% [markdown]
# ### Agencias de viajes y operadores turísticos

# %%
# Seleccionamos las ventas reales y predichas de Agencias de viajes

revision_agencias = comparacion_hw_ajustadas_11_v4.loc[
    comparacion_hw_ajustadas_11_v4["Ramas actividad"]
    == "Agencias de viajes y operadores turísticos",
    ["Trimestre", "Ventas reales", "Ventas predichas HW"]
].sort_values("Trimestre").copy()

# Positivo: se predijo de más. Negativo: se predijo de menos

revision_agencias["Diferencia"] = (
    revision_agencias["Ventas predichas HW"]
    - revision_agencias["Ventas reales"]
)

# Mostramos la comparación en euros

display(
    revision_agencias.style.format({
        "Ventas reales": "{:,.2f}",
        "Ventas predichas HW": "{:,.2f}",
        "Diferencia": "{:,.2f}"
    })
)

# %%
# Como podemos observar el modelo se queda corto también a la baja.

# %%
# Revisamos los últimos 12 trimestres del entrenamiento de Agencias de viajes.
display(
    series_entrenamiento_hw["Agencias de viajes y operadores turísticos"]
    .tail(12)
    .to_frame("Ventas reales")
    .style.format({"Ventas reales": "{:,.2f}"})
)

# %%
# Ahora probamos quitar la amortiguación y comprobamos el resultado, como en las otras dos actividades

# Expresamos las ventas de entrenamiento en millones de euros.
ventas_agencias = (
    series_entrenamiento_hw["Agencias de viajes y operadores turísticos"]
    .to_numpy() / 1_000_000
)

# Entrenamos con tendencia y estacionalidad, pero sin amortiguación.
modelo_agencias_sin_amortiguacion = ExponentialSmoothing(
    ventas_agencias,
    trend="add",
    damped_trend=False,
    seasonal="add",
    seasonal_periods=4,
    initialization_method="estimated"
).fit(optimized=True)

# Generamos las 11 predicciones y las convertimos a euros.
predicciones_agencias_sin_amortiguacion = (
    modelo_agencias_sin_amortiguacion.forecast(11) * 1_000_000
)

# Guardamos la prueba por separado para compararla.
revision_agencias_sin_amortiguacion = revision_agencias.copy()

revision_agencias_sin_amortiguacion["Predicción sin amortiguación"] = (
    predicciones_agencias_sin_amortiguacion
)

display(
    revision_agencias_sin_amortiguacion[
        ["Trimestre", "Ventas reales", "Ventas predichas HW",
         "Predicción sin amortiguación"]
    ].style.format({
        "Ventas reales": "{:,.2f}",
        "Ventas predichas HW": "{:,.2f}",
        "Predicción sin amortiguación": "{:,.2f}"
    })
)

# %%
# Lo mismo, se elevan un poco pero se siguen quedando cortas no influyendo mucho en el WAPE de agencias de viajes que vamos a calcular a continuación para demostrarle.

# Calculamos el WAPE de Agencias de viajes sin amortiguación
wape_agencias_sin_amortiguacion = (
    (
        revision_agencias_sin_amortiguacion["Predicción sin amortiguación"]
        - revision_agencias_sin_amortiguacion["Ventas reales"]
    ).abs().sum()
    / revision_agencias_sin_amortiguacion["Ventas reales"].sum()
) * 100

print(
    f"WAPE de Agencias de viajes sin amortiguación: "
    f"{wape_agencias_sin_amortiguacion:.2f}%"
)

# %%
# El WAPE baja del 15,90 % al 13,31 %: una mejora de 2,59 puntos porcentuales. Incorporamos el ajuste de Agencias de viajes

# %%
# Incorporamos el ajuste para aplicar después.

# Identificamos las filas de Agencias de viajes.
filas_agencias = (
    comparacion_hw_ajustadas_11_v4["Ramas actividad"]
    == "Agencias de viajes y operadores turísticos"
)

# Incorporamos las nuevas predicciones, emparejándolas por trimestre.
comparacion_hw_ajustadas_11_v4.loc[
    filas_agencias, "Ventas predichas HW"
] = comparacion_hw_ajustadas_11_v4.loc[
    filas_agencias, "Trimestre"
].map(
    revision_agencias_sin_amortiguacion.set_index("Trimestre")[
        "Predicción sin amortiguación"
    ]
)

# Actualizamos el método utilizado.
comparacion_hw_ajustadas_11_v4.loc[
    filas_agencias, "Método"
] = "Holt-Winters sin amortiguación"

# Actualizamos los errores.
comparacion_hw_ajustadas_11_v4["Error absoluto"] = (
    comparacion_hw_ajustadas_11_v4["Ventas predichas HW"]
    - comparacion_hw_ajustadas_11_v4["Ventas reales"]
).abs()

print("Predicciones de Agencias de viajes actualizadas:", filas_agencias.sum())

# %%
# NOTA PERSONAl IMPORTANTE:

# comparacion_hw_ajustadas_11_v4 reúne todos los ajustes de predicciones que decidimos conservar, heredados de las versiones anteriores e 
# incorporados después en esta misma tabla, y permite calcular el WAPE global final.

# Explicación de la secuencia del objeto que acumula los ajustes:
# 1. comparacion_hw_ajustadas_11: contiene los ajustes iniciales por grupos.
# 2. comparacion_hw_ajustadas_11_v2: copia lo anterior e incorpora el ajuste de Construcción.
# 3. comparacion_hw_ajustadas_11_v3: copia lo anterior e incorpora el ajuste de Intermediación financiera.
# 4. comparacion_hw_ajustadas_11_v4: copia lo anterior e incorpora el ajuste de Cine.
# 5. Actualizamos esa misma v4 con los ajustes de Transporte aéreo, Hoteles y Agencias de viajes.
# Por tanto, v4 reúne todos los ajustes conservados y se utiliza para calcular el WAPE global final.

# %%
# Calculamos el WAPE global final de los 11 trimestres evaluados.
wape_global_final = (
    comparacion_hw_ajustadas_11_v4["Error absoluto"].sum()
    / comparacion_hw_ajustadas_11_v4["Ventas reales"].sum()
) * 100

print(f"WAPE global final: {wape_global_final:.4f}%")

# %%
# CONCLUSIONES:
# Tras incorporar todos los ajustes conservados, el WAPE global es del 21,0889 %.
# Esto equivale a unos 21,09 € de error absoluto acumulado por cada 100 € de ventas reales.
# Las tres últimas revisiones redujeron el WAPE en 0,4901 puntos porcentuales.
# No alcanzamos el objetivo del 20 % y algunas actividades mantienen errores elevados.
# Como seleccionamos ajustes utilizando este mismo período, el resultado corresponde
# a la evaluación utilizada para ajustar los modelos y no garantiza el error futuro.

# %%
# AHORA VIENE LA PARTE IMPORTANTE QUE ES LA DE REENTRENAR AL MODELO CON VISTAS A PRONOSTICAR LAS VENTAS QUE TENEMOS COMO OBJETIVO.
# OBJETIVO: 
# Ahora reentrenaremos los modelos de cada actividad con todos los datos disponibles
# hasta 2026Q1, manteniendo los métodos y ajustes seleccionados, para pronosticar
# las ventas desde 2026Q2 hasta 2028Q4.

# %% [markdown]
# ## 6.6. Reentrenamiento y pronóstico hasta 2028

# %%
# Unimos los datos de entrenamiento y prueba para el reentrenamiento final.
datos_reentrenamiento = pd.concat(
    [datos_entrenamiento, datos_prueba],
    ignore_index=True
)

# Organizamos las ventas: una fila por trimestre y una columna por actividad.
series_reentrenamiento = datos_reentrenamiento.pivot(
    index="Trimestre",
    columns="Ramas actividad",
    values="Evolución trimestral del volumen de negocio (€)"
).sort_index()

# Definimos los trimestres futuros que queremos pronosticar.
trimestres_futuros = pd.period_range(
    start=series_reentrenamiento.index.max() + 1,
    end="2028Q4",
    freq="Q"
)

# Comprobamos el período, las actividades y los valores ausentes.
print("Primer trimestre:", series_reentrenamiento.index.min())
print("Último trimestre:", series_reentrenamiento.index.max())
print("Tamaño de la tabla:", series_reentrenamiento.shape)
print("Valores nulos:", series_reentrenamiento.isna().sum().sum())
print("Trimestres que pronosticaremos:", len(trimestres_futuros))

# %%
# Ahora recuperamos el método que dejamos seleccionado para cada actividad, para que el reentrenamiento respete todos los ajustes.

# Comprobamos que cada actividad tenga un único método seleccionado.
assert (
    comparacion_hw_ajustadas_11_v4
    .groupby("Ramas actividad")["Método"]
    .nunique()
    .eq(1)
    .all()
), "Hay actividades con métodos inconsistentes."

# Recuperamos el método final de cada actividad.
metodos_por_actividad = (
    comparacion_hw_ajustadas_11_v4
    .groupby("Ramas actividad")["Método"]
    .first()
    .reindex(series_reentrenamiento.columns)
)

# Comprobamos que todas las actividades tengan un método asignado.
print("Actividades:", len(metodos_por_actividad))
print("Actividades sin método:", metodos_por_actividad.isna().sum())

# Mostramos cuántas actividades utilizarán cada método.
display(metodos_por_actividad.value_counts())

# %%
# Listo,las 92 actividades tienen su método asignado. Ahora sí, reentrenamos con los datos hasta 2026Q1, respetando esas configuraciones.

# %%
# Guardamos los modelos finales y los valores que se repetirán como constantes.
modelos_finales = {}
valores_constantes_finales = {}

for actividad in series_reentrenamiento.columns:

    ventas = series_reentrenamiento[actividad]
    metodo = metodos_por_actividad[actividad]

    # Para el método ingenuo o una serie constante, conservamos la última venta.
    if metodo == "Ingenuo no estacional" or ventas.nunique() == 1:
        valores_constantes_finales[actividad] = ventas.iloc[-1]
        continue

    # Entrenamos las actividades que utilizan logaritmos.
    if metodo == "Holt-Winters con logaritmos":

        # Los logaritmos requieren ventas estrictamente positivas.
        assert (ventas > 0).all(), (
            f"Hay ventas no positivas en {actividad}; debemos revisar su método."
        )

        modelo = ExponentialSmoothing(
            np.log(ventas.to_numpy()),
            trend="add",
            damped_trend=True,
            seasonal="add",
            seasonal_periods=4,
            initialization_method="estimated"
        ).fit(optimized=True)

    # Entrenamos las actividades con suavizado exponencial simple.
    elif metodo == "Suavizado exponencial simple":

        ventas_millones = ventas.to_numpy() / 1_000_000

        modelo = ExponentialSmoothing(
            ventas_millones,
            trend=None,
            seasonal=None,
            initialization_method="known",
            initial_level=ventas_millones[0],
            bounds={"smoothing_level": (0, 1)}
        ).fit(optimized=True)

    # Entrenamos las tres variantes restantes de Holt-Winters.
    elif metodo in [
        "Holt-Winters original",
        "Holt-Winters sin amortiguación",
        "Holt-Winters sin tendencia"
    ]:

        ventas_millones = ventas.to_numpy() / 1_000_000

        modelo = ExponentialSmoothing(
            ventas_millones,
            trend=None if metodo == "Holt-Winters sin tendencia" else "add",
            damped_trend=(metodo == "Holt-Winters original"),
            seasonal="add",
            seasonal_periods=4,
            initialization_method="estimated"
        ).fit(optimized=True)

    else:
        raise ValueError(f"Método no reconocido: {metodo}")

    # Guardamos el modelo entrenado de esta actividad.
    modelos_finales[actividad] = modelo

print("Modelos reentrenados:", len(modelos_finales))
print("Actividades con predicción constante:", len(valores_constantes_finales))
print("Total de actividades:", len(modelos_finales) + len(valores_constantes_finales))

# %%
# Ahora generamos los 11 trimestres futuros y comprobamos si aparecen valores nulos, infinitos o negativos:

# Guardamos los pronósticos de todas las actividades.
resultados_pronostico = []

for actividad in series_reentrenamiento.columns:

    metodo = metodos_por_actividad[actividad]

    # Repetimos el valor guardado para las predicciones constantes.
    if actividad in valores_constantes_finales:
        predicciones = np.repeat(
            valores_constantes_finales[actividad],
            len(trimestres_futuros)
        )

    else:
        predicciones = modelos_finales[actividad].forecast(
            len(trimestres_futuros)
        )

        # Convertimos las predicciones a euros según la transformación utilizada.
        if metodo == "Holt-Winters con logaritmos":
            predicciones = np.exp(predicciones)
        else:
            predicciones = predicciones * 1_000_000

    # Identificamos las series constantes que no necesitaron entrenamiento.
    metodo_pronostico = metodo
    if (
        actividad in valores_constantes_finales
        and metodo != "Ingenuo no estacional"
    ):
        metodo_pronostico = "Valor constante"

    # Creamos la tabla de pronósticos de esta actividad.
    resultados_pronostico.append(
        pd.DataFrame({
            "Trimestre": trimestres_futuros,
            "Ramas actividad": actividad,
            "Ventas pronosticadas": predicciones,
            "Método": metodo_pronostico
        })
    )

# Unimos los pronósticos en una sola tabla.
pronosticos_2028 = pd.concat(resultados_pronostico, ignore_index=True)

# Comprobamos los resultados sin modificar las predicciones.
print("Total de pronósticos:", len(pronosticos_2028))
print("Primer trimestre:", pronosticos_2028["Trimestre"].min())
print("Último trimestre:", pronosticos_2028["Trimestre"].max())
print("Valores nulos:", pronosticos_2028["Ventas pronosticadas"].isna().sum())
print("Valores infinitos:", np.isinf(pronosticos_2028["Ventas pronosticadas"]).sum())
print("Valores negativos:", (pronosticos_2028["Ventas pronosticadas"] < 0).sum())

# %%
# Compararemos las ventas reales de 2025 con las pronosticadas para 2028, ambos años completos:

# Sumamos las ventas reales de 2025 por actividad.
ventas_reales_2025 = series_reentrenamiento.loc[
    series_reentrenamiento.index.year == 2025
].sum()

# Sumamos las ventas pronosticadas de 2028 por actividad.
ventas_pronosticadas_2028 = (
    pronosticos_2028.loc[
        pronosticos_2028["Trimestre"].dt.year == 2028
    ]
    .groupby("Ramas actividad")["Ventas pronosticadas"]
    .sum()
)

# Unimos los resultados para revisar el crecimiento previsto.
revision_pronosticos = pd.DataFrame({
    "Ventas reales 2025": ventas_reales_2025,
    "Ventas pronosticadas 2028": ventas_pronosticadas_2028
})

# Calculamos el crecimiento acumulado entre ambos años.
# Si las ventas de 2025 fueron cero, el porcentaje queda sin calcular.
revision_pronosticos["Crecimiento 2025-2028 (%)"] = (
    (
        revision_pronosticos["Ventas pronosticadas 2028"]
        / revision_pronosticos["Ventas reales 2025"].replace(0, np.nan)
    ) - 1
) * 100

# Revisamos las diez actividades con mayor crecimiento porcentual previsto.
display(
    revision_pronosticos.sort_values(
        "Crecimiento 2025-2028 (%)", ascending=False
    ).head(10).style.format({
        "Ventas reales 2025": "{:,.2f}",
        "Ventas pronosticadas 2028": "{:,.2f}",
        "Crecimiento 2025-2028 (%)": "{:,.2f}"
    }, na_rep="No calculable")
)

# %%
# El caso que más debemos revisar es Peluquería y tratamientos de belleza: pasa de 185,6 millones en 2025 a 856,5 millones en 2028, unas 4,61 veces más.
# Ese 361,35 % es crecimiento acumulado entre ambos años, no anual. Para valorar si la proyección tiene fundamento, necesitamos comprobar si las ventas
# recientes ya mostraban una subida fuerte y qué método utilizamos.

# %% [markdown]
# ### Peluquería y tratamientos de belleza

# %%
 # Comprobar si las ventas recientes ya mostraban una subida fuerte y qué método utilizamos.

# Identificamos la actividad con mayor crecimiento previsto.
actividad_revision = "Peluquería y tratamientos de belleza"

# Consultamos el método utilizado.
print("Método:", metodos_por_actividad[actividad_revision])

# Revisamos los últimos 12 trimestres de ventas reales.
display(
    series_reentrenamiento[actividad_revision]
    .tail(12)
    .to_frame("Ventas reales")
    .style.format({"Ventas reales": "{:,.2f}"})
)

# %%
# Lo siguiente sería cambiar el método de Holt winters atendencia aditiva amortiguada y estacionalidad. El crecimiento se proyecta en euros y pierde fuerza progresivamente.
# no estamos aplicando crecimiento exponencial mediante logaritmos.

# Revisión:
# Revisamos la trayectoria trimestral prevista para Peluquería.
display(
    pronosticos_2028.loc[
        pronosticos_2028["Ramas actividad"]
        == "Peluquería y tratamientos de belleza",
        ["Trimestre", "Ventas pronosticadas"]
    ]
    .sort_values("Trimestre")
    .style.format({"Ventas pronosticadas": "{:,.2f}"})
)

# %%
# # Finalmete, he decidido dejar esta predicción tal cual, pero voy a indicar que genera incertidumbre debido a una proyección de elevada 
# especialmente porque la aceleración más fuerte solo aparece en los dos últimos trimestres observados.

# %% [markdown]
# ### Grandes almacenes

# %%
# Bueno, pues ahora pasamos a grandes almacenes, tratando de hacer lo que creo que debería ser ya el último ajuste del modelo, para posteriormente dar paso a la
# construcción de la entrega y conclusiones el Power BI.

# %%
# Identificaos la actividad que vamos a revisar

actividad_revision_grandes_almacenes = "Grandes almacenes"

# Mostramos el método seleccionado para esta activiad.

print(
    "Método:",
    metodos_por_actividad[actividad_revision_grandes_almacenes]
)


# %%
# Revisamos los últimos 12 trimestres de ventas reales.

display(
    series_reentrenamiento[actividad_revision_grandes_almacenes]
    .tail(12)
    .to_frame("Ventas reales")
    .style.format({"Ventas reales": "{:,.2f}"})
)

# %%
# Hemos revisado las ventas reales recientes de Grandes almacenes y el método utilizado.
# Ahora examinaremos sus pronósticos hasta 2028 para comprobar si la trayectoria prevista resulta coherente con el comportamiento observado.
# Esta revisión no permite medir el error futuro, porque todavía no disponemos de las ventas reales de esos trimestres en nuestro conjunto de datos.
# que abarcan (2026Q2 hasta 2028Q4)

# %%
# Primero vamos a comparar las ventas reales y las predicciones de los 11 trimestres de evaluación, para ver dónde falla el modelo.
# Compararemos ventas reales históricas con las predicciones que hicimos para esos mismos trimestres.(Los que están antes del testing)

# %%
# Seleccionamos las ventas reales y predichas de Grandes almacenes.

revision_grandes_almacenes = comparacion_hw_ajustadas_11_v4.loc[
    comparacion_hw_ajustadas_11_v4["Ramas actividad"] == "Grandes almacenes",
    ["Trimestre","Ventas reales", "Ventas predichas HW"]
    ].sort_values("Trimestre").copy()

# Calculamos la diferencia entre la predicción y la venta real

revision_grandes_almacenes["Diferencia"] = (
     revision_grandes_almacenes["Ventas predichas HW"]
    - revision_grandes_almacenes["Ventas reales"]
)

# Mostramos la comparacion con separadores de miles y los típicos dos decimales

print("Revisión histórica de Grandes almacenes")

display(
    revision_grandes_almacenes.style.format({
        "Ventas reales": "{:,.2f}",
        "Ventas predichas HW":"{:,.2f}",
        "Diferencia": "{:,.2f}"
    })
)  

# %%
# Pues como se puede observar se tiene una subida de las ventas súbita después de los trimestres de 2025Q1 en adelante, lo que a todas luces no estaba previsto
# en el modelo de pronóstico, por lo tanto se puede entender que el error no es propio del modelo, sino que el origen del error del modelo yace en la info original.

# Los tres trimestres de 2025 concentran el 88,71 % del error absoluto total. Por tanto, el problema se concentra claramente en ese salto durante 2023–2024 
# las predicciones estuvieron mucho más cerca de las ventas reales.

# %%
# Antes de cambiar la tendencia, revisaremos cómo terminaban las ventas utilizadas para entrenar
# Aquí .tail(12) selecciona los últimos 12 trimestres del entrenamiento, que termina en 2022Q4:

print("Grandes almacenes: últimos 12 trimestres del entrenamiento")

display(
    series_entrenamiento_hw["Grandes almacenes"]
    .tail(12)
    .to_frame("Ventas reales")
    .style.format({"Ventas reales": "{:,.2f}"})
)

# %%
# Revisamos el pronóstico final de Grandes almacenes hasta 2028.

print("Grandes almacenes: ventas pronosticadas hasta 2028")

display(
    pronosticos_2028.loc[
        pronosticos_2028["Ramas actividad"] == "Grandes almacenes",
        ["Trimestre", "Ventas pronosticadas"]
    ]
    .sort_values("Trimestre")
    .style.format({"Ventas pronosticadas": "{:,.2f}"})
)

# %%
# Después de concretar el análisis, la convicción será mantener el pronóstico tal cual, puesto que no podemos afirmar que estás subidas estrepistosas se deban a
# una reacción del mercado que pueda ser duradera.

# El modelo reentrenado incorpora la aceleración reciente de Grandes almacenes, las ventas anuales pasan de 1.669,27 millones de euros reales en 2025
# a 4.248,59 millones pronosticados en 2028.
# Esto representa un crecimiento acumulado del 154,52 %, no anual.
# El WAPE de la evaluación histórica de esta actividad fue del 26,85 %

# %%
# OJO CON ESTO:
# Reentrenamos el modelo con datos más recientes que incluían esas subidas,no cambiamos su configuración,
# mantuvimos Holt-Winters original y volvimos a calcular sus parámetros utilizando datos hasta 2026Q1, incluyendo la subida de 2025.

# %%
# Comprobamos WAPE global final:

# Calculamos el WAPE global con todas las predicciones históricas finales.
wape_global_final = (
    comparacion_hw_ajustadas_11_v4["Error absoluto"].sum()
    / comparacion_hw_ajustadas_11_v4["Ventas reales"].sum()
) * 100

print(f"WAPE global final: {wape_global_final:.4f}%")

# %% [markdown]
# ## 7. Preparación de resultados para Power BI

# %%
# Reunimos los resultados del análisis y las predicciones en tablas que
# permitan comparar las actividades, su crecimiento previsto y su error histórico.

# %% [markdown]
# ### 7.1. Tabla resumen final por actividad

# %%
# Prepararemos una tabla con las ventas reales de 2025, las ventas pronosticadas DE 2028, el crecimiento previsto, el método utilizado y el error histórico.
# Comparar 2025 con 2028 sirve para resumir cuánto crecería o disminuiría cada actividad entre el último año completo observado y el final del pronóstico.
# No sirve para medir el error.

#Por ejemplo, en Grandes almacenes:

# 1.669 millones en 2025 → 4.249 millones previstos en 2028.

# Supone un crecimiento acumulado previsto del 154,52 %. Esta medida permite comparar las perspectivas de crecimiento de las actividades,
# teniendo en cuenta también su tamaño y su error histórico.

# %%
# La comparación 2025–2028 es un indicador de resumen, no sustituye al resto del pronóstico. 
# En Power BI tendremos tanto ese resumen como la trayectoria completa.

# %%
# Agrupamos por actividad y sumamos las ventas y los errores de la evaluación

errores_finales_por_actividad = (
    comparacion_hw_ajustadas_11_v4
    .groupby("Ramas actividad")[["Ventas reales", "Error absoluto"]]
    .sum()
)

# Calculamos el WAPE histórico por actividad
# Si las ventas suman cero, dejamos el porcentaje sin calcular.
errores_finales_por_actividad["WAPE histórico (%)"] = (
    errores_finales_por_actividad["Error absoluto"]
    / errores_finales_por_actividad["Ventas reales"].replace(0, np.nan)
) * 100

# Comprobamos cuántas actividades tenemos
print("Actividades:", len(errores_finales_por_actividad))

# Mostramos las primeras cinco actividades.
display(
    errores_finales_por_actividad.head().style.format({
        "Ventas reales": "{:,.2f}",
        "Error absoluto": "{:,.2f}",
        "WAPE histórico (%)": "{:.2f}"
    }, na_rep="No calculable")
)

# %%
# Añadimos el error histórico a la tabla de ventas y crecimiento.
resumen_final_actividades = revision_pronosticos.join(
    errores_finales_por_actividad[["WAPE histórico (%)"]],
    how="left",
    validate="one_to_one"
)

# Mostramos las primeras cinco filas alfabéticamente
display(resumen_final_actividades.head())

# %%
# Siguiente paso es añadir el método utilizado para pronosticar cada actividad.

# Recuperamos el método utilizado en los pronósticos de cada actividad.
metodos_finales_por_actividad = (
    pronosticos_2028
    .groupby("Ramas actividad")["Método"]
    .first()
)

# Añadimos el método a nuestra tabla resumen.
resumen_final_actividades["Método"] = metodos_finales_por_actividad

# Mostramos cinco filas con un formato más legible.
display(
    resumen_final_actividades.head().style.format({
        "Ventas reales 2025": "{:,.2f}",
        "Ventas pronosticadas 2028": "{:,.2f}",
        "Crecimiento 2025-2028 (%)": "{:.2f}",
        "WAPE histórico (%)": "{:.2f}"
    }, na_rep="No calculable")
)

# %%
# Ahora vamos con la tabla que alimentará el gráfico de evolución, conservando todo el histórico y los pronósticos hasta 2028.

# %% [markdown]
# ### 7.2. Evolución trimestral de ventas reales y pronosticadas

# %%
# Prepararemos una tabla que permita visualizar la evolución de cada actividad,
# distinguiendo las ventas reales de las pronosticadas.

# %%
# 1.- Preparar únicamente las ventas reales

# Seleccionamos el histórico completo de ventas de las 92 actividades.
ventas_reales_powerbi = ventas_trimestrales_actividad[
    [
        "Trimestre",
        "Ramas actividad",
        "Evolución trimestral del volumen de negocio (€)"
    ]
].copy()

# Simplificamos el nombre de la columna de importes.
ventas_reales_powerbi = ventas_reales_powerbi.rename(
    columns={
        "Evolución trimestral del volumen de negocio (€)": "Volumen de negocio (€)"
    }
)

# Identificamos estos registros como datos reales.
ventas_reales_powerbi["Tipo"] = "Real"

print("Filas de ventas reales:", len(ventas_reales_powerbi))
display(ventas_reales_powerbi.head())

# %%
# 2.-Comprobar los tipos de datos

ventas_reales_powerbi.dtypes

# %%
# 3.-Preparar los pronósticos para Power BI

print("Filas de pronósticos:", len(pronosticos_2028))
display(pronosticos_2028.head())
print(pronosticos_2028.dtypes)

# %%
# 4.- Preparar los nombres de las columnas
pronosticos_powerbi = pronosticos_2028.rename(
    columns={
        "Ventas pronosticadas": "Volumen de negocio (€)"
    }
).copy()

pronosticos_powerbi["Tipo"] = "Pronosticado"

display(pronosticos_powerbi.head())

# %%
# 5.- Unir datos reales y pronosticados:

ventas_powerbi = pd.concat(
    [ventas_reales_powerbi, pronosticos_powerbi],
    ignore_index=True
)

print("Total de filas:", len(ventas_powerbi))
print(ventas_powerbi.columns.tolist())

# %%
# 6.-Paso 6. Comprobar que no existen duplicados:

duplicados = ventas_powerbi.duplicated(
    subset=["Trimestre", "Ramas actividad", "Tipo"]
).sum()

print("Duplicados encontrados:", duplicados)

# %%
# 7.- 7. Comprobar valores nulos:

ventas_powerbi.isnull().sum()

# %%
# 8.- Preparar el trimestre para Power BI

ventas_powerbi["Fecha"] = ventas_powerbi["Trimestre"].dt.to_timestamp()

display(ventas_powerbi[["Trimestre", "Fecha"]].head())

# %%
# 9. Crear columnas de año y trimestre

ventas_powerbi["Año"] = ventas_powerbi["Fecha"].dt.year

ventas_powerbi["Trimestre_num"] = ventas_powerbi["Fecha"].dt.quarter

display(ventas_powerbi[
    ["Trimestre", "Fecha", "Año", "Trimestre_num"]
].head())

# %%
# 10.- Comprobar los registros por tipo

print(ventas_powerbi["Tipo"].value_counts())

print("Actividades únicas:",
      ventas_powerbi["Ramas actividad"].nunique())
