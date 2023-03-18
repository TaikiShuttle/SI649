# %%
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

# %%
df1 = pd.read_csv('insurance.csv')
df2 = pd.read_csv('income.csv')
df3 = pd.read_csv('healthy.csv')

df = pd.merge(df1, df2, on='Location')
df = df[['Location', 'Estimate (%)',  'Estimate ($)']]
df.columns = ['Location', 'Insurance_rate', 'Income']
df['Disabled'] = True
# df

# %%
dff = pd.merge(df2, df3, on = 'Location')
dff = dff[['Location', 'Estimate (%)', 'Estimate ($)']]
dff.columns = ['Location', 'Insurance_rate', 'Income']
dff['Disabled'] = False
# dff

# %%
df = pd.concat([df, dff])
# df

# %%
selection = alt.selection_single(empty = 'none', on = 'mouseover', nearest = True, fields = ['Income', 'Insurance_rate'])

subgroup = alt.selection_single(name = 'subgroup', fields = ['Disabled'], init = {'Disabled': True}, bind = alt.binding_radio(options = [True, False]))

color_condition = alt.condition(selection, alt.ColorValue('red'), alt.ColorValue('steelblue'))

scatter = alt.Chart(df).transform_filter(subgroup).mark_circle(size = 100).encode(
    x= alt.X('Income', title = 'Income ($)'),
    y= alt.Y('Insurance_rate', title = 'Insurance Rate (%)'),
    color = color_condition,
    tooltip = ['Location', 'Insurance_rate', 'Income']
).properties(
    width=600,
    height=400
).add_selection(
    selection, subgroup
)
# scatter

# %%
# top histogram
top_hist = alt.Chart(df).transform_filter(subgroup).mark_bar().encode(
    x = alt.X('Income:Q', bin = alt.Bin(maxbins = 10), axis = None, scale = alt.Scale(domain = [0, 65000])),
    y = alt.Y('count()', axis = None),
).properties(
    width=600,
    height=50
).add_selection(
    subgroup
)

# density line
top_line = alt.Chart(df).transform_filter(subgroup).transform_density(
    'Income',
    as_ = ['Income', 'density'],
    extent = [0, 65000]
).mark_line().encode(
    x = alt.X('Income:Q', axis = None, scale = alt.Scale(domain = [0, 65000])),
    y = alt.Y('density:Q', axis = None),
    color = alt.value('red')
).properties(
    width=600,
    height=50
)

vlines = alt.Chart(df).transform_filter(subgroup).mark_rule(color = 'red').encode(
    x = alt.X('Income:Q', axis = None, scale = alt.Scale(domain = [0, 65000])),
    size = alt.value(4),
    opacity = alt.condition(selection, alt.value(1), alt.value(0))
).properties(
    width=600,
    height=50
).add_selection(
    selection
)

top = (top_hist + top_line + vlines).resolve_scale(y = 'independent')
# top

# %%
# right histogram
right_hist = alt.Chart(df).transform_filter(subgroup).mark_bar().encode(
    y = alt.Y('Insurance_rate:Q', bin = alt.Bin(maxbins = 10), axis = None, scale = alt.Scale(domain = [0, 26])),
    x = alt.X('count()', axis = None),
).properties(
    width=50,
    height=400
).add_selection(
    subgroup
)

# density line
right_line = alt.Chart(df).transform_filter(subgroup).transform_density(
    'Insurance_rate',
    as_ = ['Insurance_rate', 'density'],
    extent = [0, 26]
).mark_line(orient = alt.Orientation('horizontal')).encode(
    y = alt.Y('Insurance_rate:Q', axis = None, scale = alt.Scale(domain = [0, 26])),
    x = alt.X('density:Q', axis = None),
    color = alt.value('red')
).properties(
    width=50,
    height=400
)

hlines = alt.Chart(df).transform_filter(subgroup).mark_rule(color = 'red').encode(
    y = alt.Y('Insurance_rate:Q', axis = None, scale = alt.Scale(domain = [0, 26])),
    size = alt.value(4),
    opacity = alt.condition(selection, alt.value(1), alt.value(0)),
).properties(
    width=50,
    height=400
).add_selection(
    selection
)

right = (right_hist + right_line + hlines).resolve_scale(x = 'independent')
# right

# %%
output = top & (scatter| right).resolve_scale(y = 'shared')
output.properties(title = 'Insurance Rate vs. Income for Disabled People in the US')

# %%
st.title('Insurance Rate vs. Income for People in the US')
st.altair_chart(output)


