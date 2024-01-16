# %%
import polars as pl
from lets_plot import *
LetsPlot.setup_html()

# %%
patterns = pl.read_parquet("../data/patterns.parquet")
places = pl.read_parquet("../data/places.parquet")

dat = patterns\
    .unique(subset=["placekey", "date_range_start"])\
    .join(places.unique(subset="placekey"), on=["placekey"], how="left")\
    .with_columns(date_range_start=pl.col("date_range_start").str.to_datetime())\
    .select("placekey", "city", "date_range_start", "latitude", "longitude", "raw_visit_counts", "raw_visitor_counts", "visits_by_day")\
    .with_columns(date_start=pl.col("date_range_start").dt.date())


# %%
map = ggplot(dat) + \
    geom_livemap() + \
    geom_point(aes(x="longitude", y="latitude", color="raw_visit_counts"), size=.05)


# %%
histogram = ggplot(dat, aes(x="raw_visit_counts")) + geom_histogram()

# %%
bunch = GGBunch()
bunch.add_plot(map, 0, 0)
bunch.add_plot(histogram, 600, 0)
bunch.show()
# %%
# https://lets-plot.org/pages/no_js_and_offline_mode.html#no-js-and-offline-mode
# 
ggsave(bunch, "plot.html")

# %%
