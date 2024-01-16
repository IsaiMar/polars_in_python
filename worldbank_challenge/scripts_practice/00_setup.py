# %%
import pyarrow as pa
import pyarrow.parquet as pq
import polars as pl
import plotly.express as px
import plotly.io as pio
import statsmodels
pio.templates.default = "simple_white"

# %%
dat = pl.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})
dat
# %%
fig = px.scatter(dat, x="first column", y="second column")
fig
