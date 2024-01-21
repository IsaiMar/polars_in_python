# %%
import polars as pl
import pyarrow as pa
from pyarrow import csv
from pyarrow import dataset as ds
import pyarrow.parquet as pq

# Now we can explore the relationships using unnest and explode

dcsv_parsed = pl.read_parquet("../data/chipotle_core_poi_and_patterns.parquet")
# %%
# explore the brands
day_brand = dcsv_parsed\
    .select("placekey", "related_same_month_brand")\
    .unnest("related_same_month_brand")\
    .melt(id_vars="placekey")\
    .drop_nulls()

month_brand = dcsv_parsed\
    .select("placekey", "related_same_month_brand")\
    .unnest("related_same_month_brand")\
    .melt(id_vars="placekey")\
    .drop_nulls()

# %%
# explore the home cbgs
dcsv_parsed.select("placekey", "visitor_home_cbgs")\
    .unnest("visitor_home_cbgs")\
    .melt(id_vars="placekey")\
    .drop_nulls()
# %%
# Popularity by hour
# https://docs.pola.rs/py-polars/html/reference/expressions/api/polars.Expr.cum_count.html
dcsv_parsed\
    .select("placekey", "popularity_by_hour")\
    .explode("popularity_by_hour")\
    .with_columns(hour=pl.col("popularity_by_hour")\
        .cum_count()\
        .over("placekey") - 1)
# %%
# explore the day of the month
# Are Fridays at the end of the month more attended than Friday at the beginning of the month?
# `explode()`, `with_columns()`, `.cum_counts()`, `.over()`, `pl.duration()`, `.dt.weekday()`, `.replace()`, `.filter()`
dcsv_parsed\
    .select("placekey", "date_range_start", "visits_by_day")\
    .explode("visits_by_day")\
    .with_columns(
        pl.col("visits_by_day").cum_count().over(["placekey","date_range_start"]) -1
    )
 # let's create the code.  First, try writing out the structure in English...


# %%
