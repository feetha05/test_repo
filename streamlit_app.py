import altair as alt
import pandas as pd
import streamlit as st

### P1.2 ###

# Move this code into `load_data` function {{
cancer_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/cancer_ICD10.csv").melt(  # type: ignore
    id_vars=["Country", "Year", "Cancer", "Sex"],
    var_name="Age",
    value_name="Deaths",
)

pop_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/population.csv").melt(  # type: ignore
    id_vars=["Country", "Year", "Sex"],
    var_name="Age",
    value_name="Pop",
)

df = pd.merge(left=cancer_df, right=pop_df, how="left")
df["Pop"] = df.groupby(["Country", "Sex", "Age"])["Pop"].fillna(method="bfill")
df.dropna(inplace=True)

df = df.groupby(["Country", "Year", "Cancer", "Age", "Sex"]).sum().reset_index()
df["Rate"] = df["Deaths"] / df["Pop"] * 100_000

# }}


@st.cache
def load_data():
    ## {{ CODE HERE }} ##
    path = "https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/cancer_ICD10.csv"
    path_2 = "https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/population.csv"
    cancer_df = pd.read_csv(path).melt(id_vars=["Country", "Year", "Cancer", "Sex"],var_name="Age",value_name="Deaths",)
    pop_df = pd.read_csv(path_2).melt(id_vars=["Country", "Year", "Sex"],var_name="Age",value_name="Pop",)
    df = pd.merge(left=cancer_df, right=pop_df, how="left")
    df["Pop"] = df.groupby(["Country", "Sex", "Age"])["Pop"].fillna(method="bfill")
    df.dropna(inplace=True)
    df = df.groupby(["Country", "Year", "Cancer", "Age", "Sex"]).sum().reset_index()
    df["Rate"] = df["Deaths"] / df["Pop"] * 100_000
    return df


# Uncomment the next line when finished
# df = load_data()

### P1.2 ###


st.write("## Age-specific cancer mortality rates")

### P2.1 ###
# replace with st.slider
#year = 2012
#subset = df[df["Year"] == year]
### P2.1 ###
st.slider('Select a Year', min_value=int(df["Year"].min()), max_value=int(df["Year"].max()), step=1)

### P2.2 ###
# replace with st.radio
#sex = "M"
#subset = subset[subset["Sex"] == sex]
### P2.2 ###
st.radio('Select Sex',df["Sex"].unique())

### P2.3 ###
# replace with st.multiselect
# (hint: can use current hard-coded values below as as `default` for selector)
countries = [
    "Austria",
    "Germany",
    "Iceland",
    "Spain",
    "Sweden",
    "Thailand",
    "Turkey",
]
#subset = subset[subset["Country"].isin(countries)]
### P2.3 ###

#unique_countries = df[df['Country'].isin(countries)]

unique_countries = df["Country"].unique()

st.multiselect('Select Country',unique_countries)

### P2.4 ###
# replace with st.selectbox
#cancer = "Malignant neoplasm of stomach"
#subset = subset[subset["Cancer"] == cancer]
### P2.4 ###
st.selectbox('Select Cancer',df["Cancer"].unique())
#st.selectbox('Select Cancer',df["Cancer"].unique())
### P2.5 ###
ages = [
    "Age <5",
    "Age 5-14",
    "Age 15-24",
    "Age 25-34",
    "Age 35-44",
    "Age 45-54",
    "Age 55-64",
    "Age >64",
]

chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("Age", sort=ages),
    y=alt.Y("Rate", title="Mortality rate per 100k"),
    color="Country",
    tooltip=["Rate"],
).properties(
    #title=f"{cancer} mortality rates for {'males' if sex == 'M' else 'females'} in {year}",
)
### P2.5 ###

st.altair_chart(chart, use_container_width=True)

countries_in_subset = df["Country"].unique()
if len(countries_in_subset) != len(countries):
    if len(countries_in_subset) == 0:
        st.write("No data avaiable for given subset.")
    else:
        missing = set(countries) - set(countries_in_subset)
        st.write("No data available for " + ", ".join(missing) + ".")