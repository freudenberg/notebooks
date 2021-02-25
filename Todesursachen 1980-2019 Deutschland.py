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
