import pycountry
import pandas as pd
import plotly.express as px

"""Code to generate a worlmap with countries of co-authors
Shows affilation counts (not accounting multiple affiliations per person)

It is not optimized at ALL
"""

if __name__ == "__main__":

    # affiliations file
    # See README for creation instruction
    fname = "examples/my_papers_affilations.txt"

    # read all the affiliations
    with open(fname) as f:
        lines = f.readlines()

    # create list of countries
    # to be improved
    list_countries = []
    for lin in lines:
        for country in pycountry.countries:
            if country.name in lin:
                list_countries.append(country.name)
        if "UK" in lin:
            list_countries.append("United Kingdom")
        if "USA" in lin:
            list_countries.append("United States")

    # counting countries
    uni = list(set(list_countries))
    arr_countries = []
    arr_count = []
    for u in uni:
        arr_countries.append(u)
        arr_count.append(list_countries.count(u))

    # create df for plot
    df = pd.DataFrame()
    df["country"] = arr_countries
    df["publication #"] = arr_count

    gapminder = px.data.gapminder().query("year==2007")
    df = pd.merge(gapminder, df, how="left", on="country")

    # plot
    fig = px.choropleth(
        df,
        locations="iso_alpha",
        color="publication #",
        # hover_name="country",  # column to add to hover information
        color_continuous_scale=px.colors.sequential.Plasma,
    )
    # fig.show()
    fig.write_image("images/worldmap.png")
