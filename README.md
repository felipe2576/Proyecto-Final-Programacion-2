## Fuente de los datos
Dataset "New York City Airbnb Open Data" (AB_NYC_2019.csv) de Kaggle:
https://www.kaggle.com/datasets/dgomonov/new-york-city-airbnb-open-data
Contiene los alojamientos publicados en Airbnb en Nueva York durante 2019.

## Estructura de los datos
- **Registros:** 48.895. Cada fila es un alojamiento publicado.
- **Variables:** 16 en total.
- **Categóricas (5):** `name`, `host_name`, `neighbourhood_group`, `neighbourhood`, `room_type`.
- **Numéricas continuas (4):** `latitude`, `longitude`, `price`, `reviews_per_month`.
- **Numéricas discretas (4):** `minimum_nights`, `number_of_reviews`, `calculated_host_listings_count`, `availability_365`.
- **Identificadores (2):** `id`, `host_id`.
- **Fecha (1):** `last_review`.

## Diccionario de datos
| Variable | Tipo | Descripción | Valores / unidades |
|---|---|---|---|
| id | Identificador | Código único del alojamiento | Número entero |
| name | Categórica | Título de la publicación | Texto libre |
| host_id | Identificador | Código único del anfitrión | Número entero |
| host_name | Categórica | Nombre del anfitrión | Texto |
| neighbourhood_group | Categórica | Zona (distrito) de Nueva York | Manhattan, Brooklyn, Queens, Bronx, Staten Island |
| neighbourhood | Categórica | Barrio del alojamiento | 221 barrios |
| latitude | Numérica continua | Latitud de la ubicación | Grados |
| longitude | Numérica continua | Longitud de la ubicación | Grados |
| room_type | Categórica | Tipo de alojamiento | Entire home/apt, Private room, Shared room |
| price | Numérica continua | Precio por noche | Dólares (USD) |
| minimum_nights | Numérica discreta | Mínimo de noches por reserva | Noches |
| number_of_reviews | Numérica discreta | Total de reseñas recibidas | Cantidad |
| last_review | Fecha | Fecha de la última reseña | AAAA-MM-DD (vacía si no hay reseñas) |
| reviews_per_month | Numérica continua | Promedio de reseñas por mes | Reseñas/mes (0 si no tiene reseñas) |
| calculated_host_listings_count | Numérica discreta | Propiedades que tiene el anfitrión | Cantidad |
| availability_365 | Numérica discreta | Días disponibles al año | 0 a 365 |
