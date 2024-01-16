# %%
import polars as pl
import plotly.express as px
import plotly.graph_objects as go

# %%
patterns = pl.read_parquet("../data/patterns.parquet")
places = pl.read_parquet("../data/places.parquet")

# %%
dat = patterns\
    .unique(subset=["placekey", "date_range_start"])\
    .join(places.unique(subset="placekey"), on=["placekey"], how="left")\
    .with_columns(date_range_start=pl.col("date_range_start").str.to_datetime())\
    .select("placekey", "date_range_start", "latitude", "longitude", "raw_visit_counts", "raw_visitor_counts", "visits_by_day")\
    .with_columns(date_start=pl.col("date_range_start").dt.date())


# %%
# https://plotly.com/python-api-reference/generated/plotly.express.scatter_geo

px.scatter_geo(dat,
    lat="latitude", lon="longitude", scope="usa",
    color="raw_visit_counts",
    animation_frame="date_start")

# %%
px.histogram(dat, x="raw_visit_counts")


# %%
# https://pythonplot.com/
# https://blog.jetbrains.com/pycharm/2021/03/interactive-visualizations-in-pycharm-and-datalore/