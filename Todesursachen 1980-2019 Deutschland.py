# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
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
import numpy as np
import cufflinks as cf

# %%
cf.go_offline()

# %%
icd = ["Bestimmte infektiöse und parasitäre Krankheiten", "Neubildungen", "Krankheiten des Blutes u. der blutbildenden Organe", "Endokrine, Ernährungs- u. Stoffwechselkrankheiten", "Krankheiten des Kreislaufsystems", "Psychische und Verhaltensstörungen", "Krankheiten d. Nervensystems u. d. Sinnesorgane", "Krankheiten des Atmungssystems", "Krankheiten des Verdauungssystems", "Krankheiten der Haut und der Unterhaut", "Krankh. des Muskel-Skelett-Systems u. Bindegewebes", "Krankheiten des Urogenitalsystems", "Schwangerschaft, Geburt und Wochenbett", "Best.Zustände mit Ursprung in der Perinatalperiode", "Angeb. Fehlbildungen,Deformitäten,Chromosomenanom.", "Symptome und abnorme klinische und Laborbefunde", "Äußere Ursachen von Morbidität und Mortalität"]


# %%
def load_demographics(file):
    with open(file, 'rb') as f:
        df_ = pd.read_csv(
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
    df_['männlich'] = df_['Deutsche']['männlich'] + df_['Ausländer']['männlich']
    df_['weiblich'] = df_['Deutsche']['weiblich'] + df_['Ausländer']['weiblich']
    df_ = df_[['männlich', 'weiblich']].unstack(level=0).reindex(df_.index.get_level_values(1))
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
    df_ = pd.concat(frames.values(), keys=frames.keys()).unstack().T
    df_.index = df_.index.year
    return df_


# %%
def load_2020(file):
    with open(file, 'rb') as f:
        df_ = pd.read_csv(
            f,
            header=[0], index_col=[0, 1, 2],
            nrows=34,
            sep=';',
            skiprows=[0, 1, 2, 3, 4, 5, 6, 7]
        ).fillna(0)
    df_2020 = df_[18:34]["Unnamed: 15"].reset_index().iloc[:, 1:4]
    df_2020.columns = ["Jahr", "AG", "Anzahl"]
    return df_2020.set_index(["Jahr", "AG"]).unstack().astype('Int64')


# %%
with open('data/23211-0004.csv', 'rb') as f:
    df = pd.read_csv(
        f,
        dtype={'männlich': 'Int64', 'weiblich': 'Int64'},
        encoding='latin_1',
        header=[0, 1], index_col=[0, 1],
        na_values=['-'],
        nrows=3200,
        sep=';',
        skiprows=[0, 1, 2, 3, 4, 5, 6, 8]
    ).fillna(0)

# %%
df.head()


# %%
@widgets.interact
def show_total_by_year_and_cause(year=(1980, 2019, 1), cause=df.index.get_level_values(1).drop_duplicates()):
    df_t = df.loc[year, cause].unstack().T
    index = df_t.index.to_list()
    return df_t.reindex([index.pop()] + index)


# %%
@widgets.interact
def plot_by_year_and_cause(year=(1980, 2019, 1), cause=df.index.get_level_values(1).drop_duplicates()):
    df_t = df.loc[year, cause].unstack().T
    index = df_t.index.to_list()
    return df_t.reindex([index.pop()] + index).iplot(kind="bar", subplots=False)


# %%
@widgets.interact
def sum_by_sex(cause=df.index.get_level_values(1).drop_duplicates()):
    return df.xs(cause, level=1).T.groupby(level=0).sum().T.head()


# %%
@widgets.interact
def plot_by_sex(cause=df.index.get_level_values(1).drop_duplicates()):
    return df.xs(cause, level=1).T.groupby(level=0).sum().T.iplot(kind="bar")


# %%
df.loc[(slice(None), icd + ["Insgesamt"]), :].T.sum().unstack().iplot(kind="bar", barmode="overlay", layout_update=dict(hoverlabel=dict(namelength=-1)), colorscale='dark2')


# %%
@widgets.interact(variables=widgets.SelectMultiple(description="Ursachen", options=df.index.get_level_values(1).drop_duplicates(), value=icd, disabled=False))
def series(variables):
    df_t = df.T.sum().unstack()
    return df_t.div(df_t["Insgesamt"], axis="index")[list(variables)].iplot(layout_update=dict(hoverlabel=dict(namelength=-1)))


# %%
df_by_age_group = df.T.groupby(level=1).sum()
index = df_by_age_group.index.to_list()
df_by_age_group = df_by_age_group.reindex([index.pop()] + index)
df_by_age_group.head()


# %%
def custom_age_groups(frame):
    return pd.concat([frame.iloc[0:13].sum(), frame.iloc[13:16].sum(), frame.iloc[16:17].sum()], keys=["Unter 70 Jahre", "70 bis unter 85 Jahre", "85 Jahre und mehr"])


# %%
population = load_demographics('data/12411-0007.csv')


# %%
@widgets.interact
def relative_deaths_by_age_group(cause=df.index.get_level_values(1).drop_duplicates()):
    deaths = custom_age_groups(df_by_age_group).unstack(level=0).xs(cause, level=1)
    population_grouped = custom_age_groups(population.T.groupby(level=0).sum()).unstack(level=0)
    df_ = deaths / (population_grouped + deaths)
    df_.loc[1990:].iplot(kind="bar", barmode="group")


# %%
@widgets.interact
def absolute_deaths_by_age_group(cause=df.index.get_level_values(1).drop_duplicates()):
    df_ = custom_age_groups(df_by_age_group).unstack(level=0).xs(cause, level=1)
    df_.loc[1990:].iplot(kind="bar", barmode="group")


# %%
@widgets.interact
def absolute_death_by_age_group_including_2020():
    df_ = custom_age_groups(df_by_age_group).unstack(level=0).xs("Insgesamt", level=1)
    df_2020 = load_2020('data/sonderauswertung-sterbefaelle/D_2016-2021_Monate_AG_Ins-Tabelle 1.csv')
    return df_.loc[1990:].append([pd.Series([df_2020.iloc[0, 0:10].sum(), df_2020.iloc[0, 10:13].sum(), df_2020.iloc[0, 13:].sum()], index=["Unter 70 Jahre", "70 bis unter 85 Jahre", "85 Jahre und mehr"], name=2020)]).iplot(kind="bar", barmode="group")


# %%
@widgets.interact(age_group=widgets.Dropdown(options=custom_age_groups(df_by_age_group).index.get_level_values(0).unique(), description="Altersgruppe"))
def plot_percentage_of_cause(age_group):
    df_ = custom_age_groups(df_by_age_group).xs(age_group).unstack()
    return df_.div(df_["Insgesamt"], axis="index")[icd].iplot(kind="bar", barmode="stack", layout_update=dict(hoverlabel=dict(namelength=-1), legend=dict(orientation="h",), yaxis=dict(tickformat=",.0%")))


# %%
def regroup_ages(frame):
    df_by_age_group = frame.T.unstack(level=0)
    index = df_by_age_group.index.to_list()
    return custom_age_groups(df_by_age_group.reindex([index.pop()] + index)).unstack(level=3).unstack(level=0)



# %%
df_pct_change = regroup_ages(df).pct_change(df.index.get_level_values(1).nunique()).loc[1981:]

# %%
more_than_hundred_percent = list()

for row in df_pct_change.iterrows():
    for k, v in dict(row[1]).items():
        if v != float("inf") and (v >= 2.0 or v<= -2.0):
            more_than_hundred_percent.append((row[0], k, v))
            print(row[0], k, v)

# %%
