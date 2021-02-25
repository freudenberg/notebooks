# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.10.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import ipywidgets as widgets
import pandas as pd
import cufflinks as cf

# %%
cf.go_offline()

# %%
with open('data/12411-0007.csv', 'rb') as f:
    df = pd.read_csv(
        f,
        dtype={'Deutsche': 'Int64', 'Ausländer': 'Int64'},
        encoding='latin_1',
        header=[0, 1], index_col=[0, 1],
        na_values=['-'],
        nrows=3480,
        parse_dates=True,
        sep=';',
        skiprows=[0, 1, 2, 3, 4, 5]
    )

# %%
df.head()

# %%
df['männlich'] = df['Deutsche']['männlich'] + df['Ausländer']['männlich']

# %%
df['weiblich'] = df['Deutsche']['weiblich'] + df['Ausländer']['weiblich']

# %%
df_ = df[['männlich', 'weiblich']].unstack(level=0).reindex(df.index.get_level_values(1))

# %%
df_by_sex = df_.loc["Insgesamt"].T.unstack(level=0)
df_by_sex.index = df_by_sex.index.get_level_values(1)
df_by_sex["Insgesamt"].iplot(kind="bar", barmode="group")


# %%
@widgets.interact
def plot_by_sex(sex=df_grouped.index.get_level_values(1).drop_duplicates()):
    frames = {
        "unter 1 Jahr": df_.iloc[0],
        "1 bis unter 15 Jahre": df_.iloc[1:15].sum(),
        "15 bis unter 20 Jahre": df_.iloc[15:20].sum(),
        "20 bis unter 25 Jahre": df_.iloc[20:25].sum(), 
        "25 bis unter 30 Jahre": df_.iloc[25:30].sum(), 
        "30 bis unter 35 Jahre": df_.iloc[30:35].sum(),
        "35 bis unter 40 Jahre": df_.iloc[35:40].sum(), 
        "40 bis unter 45 Jahre": df_.iloc[40:45].sum(), 
        "45 bis unter 50 Jahre": df_.iloc[45:50].sum(), 
        "50 bis unter 55 Jahre": df_.iloc[50:55].sum(), 
        "55 bis unter 60 Jahre": df_.iloc[55:60].sum(), 
        "60 bis unter 65 Jahre": df_.iloc[60:65].sum(), 
        "65 bis unter 70 Jahre": df_.iloc[65:70].sum(), 
        "70 bis unter 75 Jahre": df_.iloc[70:75].sum(),
        "75 bis unter 80 Jahre": df_.iloc[75:80].sum(), 
        "80 bis unter 85 Jahre": df_.iloc[80:85].sum(), 
        "85 Jahre und mehr": df_.iloc[85]
    }
    df_grouped = pd.concat(frames.values(), keys=frames.keys())
    df_grouped.unstack().xs(sex, level=1).T.iplot(kind="bar", barmode="stack", orientation='h', layout_update=dict(hoverlabel=dict(namelength=-1)))

# %%
