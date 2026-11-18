# %% [markdown]
# # Análisis de Airbnb NYC 2019
# Integrantes: Felipe, Danny

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("datos/AB_NYC_2019.csv")

# %% [markdown]
# ## 1. Carga e inspección inicial de los datos  (Integrante A)
# ## 1. 
print("Filas y columnas:", df.shape)
print(df.dtypes)
print(df.head())
print(df.describe().round(2).T)
print(df.describe(include="object").T)
# %% [markdown]
# ## 2. Manejo de datos faltantes  (Integrante B)
# %%
sns.heatmap(df.isna(), cbar=False)
plt.title("Datos faltantes antes de la limpieza")
plt.show()

faltantes = df.isna().sum()
porcentaje = (faltantes / len(df) * 100).round(2)
pd.DataFrame({"faltantes": faltantes, "%": porcentaje})[faltantes > 0]

# %%
sin_resenas = df["number_of_reviews"] == 0
print("Alojamientos sin reseñas:", sin_resenas.sum())
print("Coinciden con los faltantes:", (df["last_review"].isna() == sin_resenas).all())

# %%
df["name"] = df["name"].fillna("Desconocido")
df["host_name"] = df["host_name"].fillna("Desconocido")
df["reviews_per_month"] = df["reviews_per_month"].fillna(0)
df["last_review"] = pd.to_datetime(df["last_review"])

sns.heatmap(df.isna(), cbar=False)
plt.title("Datos faltantes después de la limpieza")
plt.show()
# %% [markdown]
# ## 3. Identificación de outliers  (Integrante A)
import matplotlib.pyplot as plt
import seaborn as sns

cols = ["price", "minimum_nights", "number_of_reviews", "calculated_host_listings_count"]

fig, axes = plt.subplots(1, 4, figsize=(16, 4))
for ax, col in zip(axes, cols):
    sns.boxplot(y=df[col], ax=ax)
    ax.set_title(col)
plt.tight_layout()
plt.show()

for col in cols:
    q1, q3 = df[col].quantile([0.25, 0.75])
    limite = q3 + 1.5 * (q3 - q1)
    print(col, "límite superior:", limite, "outliers:", (df[col] > limite).sum(), "máximo:", df[col].max())

df_sin_out = df[(df["price"] > 0) & (df["price"] <= 1000) & (df["minimum_nights"] <= 365)].copy()
print("Registros excluidos:", len(df) - len(df_sin_out))

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
sns.boxplot(y=df_sin_out["price"], ax=axes[0])
sns.boxplot(y=df_sin_out["minimum_nights"], ax=axes[1])
plt.show()
# %% [markdown]
# ## 4. Valores inconsistentes y duplicados  (Integrante B)
# %%
print("Filas duplicadas completas:", df.duplicated().sum())
print("IDs repetidos:", df["id"].duplicated().sum())

# %%
cols_texto = ["name", "host_name", "neighbourhood_group", "neighbourhood", "room_type"]

for col in cols_texto:
    n_espacios = (df[col] != df[col].str.strip()).sum()
    print(f"{col}: {n_espacios} con espacios extra, {df[col].nunique()} valores únicos")

print(df["neighbourhood_group"].value_counts())
print(df["room_type"].value_counts())

# %%
df["name"] = df["name"].str.strip()

print("Nombres con espacios extra después:", (df["name"] != df["name"].str.strip()).sum())
print("Registros después de la limpieza:", len(df))

# %% [markdown]
# ## 5. Creación de variables  (Integrante A)
df_sin_out["tiene_resenas"] = df_sin_out["number_of_reviews"] > 0
df_sin_out["noches_ocupadas"] = 365 - df_sin_out["availability_365"]
df_sin_out["ingreso_estimado"] = df_sin_out["price"] * df_sin_out["noches_ocupadas"]
df_sin_out["categoria_precio"] = pd.cut(df_sin_out["price"], bins=[0, 75, 150, 300, 1000],
                                        labels=["Económico", "Medio", "Alto", "Lujo"])

print(df_sin_out[["price", "availability_365", "noches_ocupadas", "ingreso_estimado", "categoria_precio"]].head())
print(df_sin_out["tiene_resenas"].value_counts(normalize=True).round(3))
print(df_sin_out["categoria_precio"].value_counts())

# Conclusión: el 79,6% de las publicaciones tiene reseñas. Por precio, 18.704 son de categoría Medio,
# 15.232 Económico, 11.578 Alto y 3.117 Lujo.
# Nota: noches_ocupadas e ingreso_estimado son aproximaciones: suponen que las noches no disponibles están ocupadas.
# %% [markdown]
# ## 6. Filtrado y condiciones en pandas  (Integrante B)
# %%
# Filtro 1: alojamientos de lujo (más de 500 dólares por noche)
caros = df[df["price"] > 500]
print("Cantidad:", len(caros), "|", round(len(caros) / len(df) * 100, 2), "%")
print(caros["neighbourhood_group"].value_counts())

# %%
# Filtro 2: habitaciones privadas baratas en Manhattan (menos de 100 dólares)
baratas = df[(df["room_type"] == "Private room")
             & (df["neighbourhood_group"] == "Manhattan")
             & (df["price"] < 100)]
print("Cantidad:", len(baratas))
print("Precio promedio:", round(baratas["price"].mean(), 2))

# %%
# Filtro 3: muy populares (más de 100 reseñas) y con alta disponibilidad
populares = df[(df["number_of_reviews"] > 100) & (df["availability_365"] > 300)]
print("Cantidad:", len(populares))
print(populares["room_type"].value_counts())
# %%
# Filtro 4: estadías largas (30 noches o más)
largas = df[df["minimum_nights"] >= 30]
print("Cantidad:", len(largas), "|", round(len(largas) / len(df) * 100, 2), "%")
print("Precio promedio estadías largas:", round(largas["price"].mean(), 2))
print("Precio promedio general:", round(df["price"].mean(), 2))
# %%
# Filtro 5: anfitriones con más de 10 propiedades
grandes = df[df["calculated_host_listings_count"] > 10]
print("Cantidad:", len(grandes), "|", round(len(grandes) / len(df) * 100, 2), "%")
print(grandes["neighbourhood_group"].value_counts())
# %% [markdown]
# ## 7. Agrupación con groupby  (Integrante A)
# 1. Precio promedio y mediano por zona
print(df_sin_out.groupby("neighbourhood_group")["price"].agg(["count", "mean", "median"]).round(1).sort_values("mean", ascending=False))
# 2. Precio mediano por tipo de habitación
print(df_sin_out.groupby("room_type")["price"].agg(["count", "median"]))

# 3. Tipo de habitación por zona (porcentaje)
print((df_sin_out.groupby("neighbourhood_group")["room_type"].value_counts(normalize=True) * 100).round(1).unstack())
# 4. Barrios más caros (mínimo 50 publicaciones)
barrios = df_sin_out.groupby("neighbourhood")["price"].agg(["count", "mean"])
print(barrios[barrios["count"] >= 50].sort_values("mean", ascending=False).head(10).round(1))

# 5. Disponibilidad e ingreso estimado por zona
print(df_sin_out.groupby("neighbourhood_group")[["availability_365", "ingreso_estimado"]].mean().round(1))
# %% [markdown]
# ## 8. Visualizaciones  (Integrante B)
# %%
# Gráfico 1: alojamientos por zona
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="neighbourhood_group",
              order=df["neighbourhood_group"].value_counts().index)
plt.title("Cantidad de alojamientos por zona")
plt.xlabel("Zona")
plt.ylabel("Cantidad")
plt.show()

# %%
# Gráfico 2: distribución del precio (hasta 500 dólares)
plt.figure(figsize=(8, 5))
sns.histplot(df[df["price"] <= 500]["price"], bins=40, kde=True)
plt.title("Distribución del precio por noche (hasta 500 USD)")
plt.xlabel("Precio (USD)")
plt.ylabel("Cantidad")
plt.show()

# %%
# Gráfico 3: precio por tipo de habitación (hasta 500 dólares)
plt.figure(figsize=(8, 5))
sns.boxplot(data=df[df["price"] <= 500], x="room_type", y="price")
plt.title("Precio por tipo de habitación (hasta 500 USD)")
plt.xlabel("Tipo de habitación")
plt.ylabel("Precio (USD)")
plt.show()

# %%
# Gráfico 4: precio promedio por zona
plt.figure(figsize=(8, 5))
promedio_zona = df.groupby("neighbourhood_group")["price"].mean().sort_values(ascending=False)
sns.barplot(x=promedio_zona.index, y=promedio_zona.values)
plt.title("Precio promedio por zona")
plt.xlabel("Zona")
plt.ylabel("Precio promedio (USD)")
plt.show()
print(promedio_zona.round(2))

# %%
# Gráfico 5: correlación entre variables numéricas
plt.figure(figsize=(9, 6))
numericas = ["price", "minimum_nights", "number_of_reviews",
             "reviews_per_month", "calculated_host_listings_count", "availability_365"]
sns.heatmap(df[numericas].corr(), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlación entre variables numéricas")
plt.show()
# %% [markdown]
# ## 9. Conclusiones finales  (Integrante A)
## Conclusiones
#1. **Concentración:** Manhattan y Brooklyn reúnen el 85,4% de las 48.895 publicaciones.
#2. **Precio por zona:** Manhattan es la zona más cara (mediana de 149 dólares) y el Bronx la más barata (65). Los 10 barrios más caros son de Manhattan, con Tribeca a la cabeza.
#3. **Tipo de habitación:** es lo que más pesa en el precio: el apartamento completo (mediana de 160 dólares) cuesta más del doble que la habitación privada (70).
#4. **Valores extremos:** hay precios de hasta 10.000 dólares y estadías mínimas de hasta 1.250 noches. Se excluyó el 0,5% de los registros para no distorsionar los promedios.
#5. **Reseñas e ingreso:** el 79,6% de las publicaciones tiene reseñas y el ingreso estimado es más alto en Manhattan que en el Bronx, aunque es solo una aproximación.