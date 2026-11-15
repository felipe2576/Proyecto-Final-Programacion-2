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
# ## 1. 
df = pd.read_csv("../datos/AB_NYC_2019.csv")
print("Filas y columnas:", df.shape)
print(df.dtypes)
print(df.head())
print(df.describe().round(2).T)
print(df.describe(include="object").T)
# %% [markdown]
# ## 2. Manejo de datos faltantes  (Integrante B)

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

# %% [markdown]
# ## 7. Agrupación con groupby  (Integrante A)

# %% [markdown]
# ## 8. Visualizaciones  (Integrante B)

# %% [markdown]
# ## 9. Conclusiones finales  (Integrante A)