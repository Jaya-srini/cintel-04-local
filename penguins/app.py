import faicons as fa  # For using font awesome in cards
import palmerpenguins  # This package provides the Palmer Penguins dataset
import pandas as pd  # Pandas for data manipulation, required by plotly.express
import plotly.express as px  # Plotly Express for making Plotly plots
import seaborn as sns  # Seaborn for making Seaborn plots
from shinywidgets import render_plotly  # For rendering Plotly plots
from shiny import reactive, render, req  # To define reactive calculations
from shiny.express import input, ui  # To define the user interface

# Load the dataset into a pandas DataFrame.
penguins_df = palmerpenguins.load_penguins()

# Define the Shiny UI Page layout
ui.page_opts(
    title="Jaya: Palmer Penguins Example", 
    fillable=True
    )

with ui.sidebar(open="open"):

    ui.h2("Sidebar")

    ui.input_selectize(
        "selected_attribute",
        "Select Plotly Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g", "year"],
    )

    ui.input_numeric("plotly_bin_count", "Number of Plotly bins", 30)

    ui.input_slider("seaborn_bin_count", "Number of Seaborn bins", 1, 100, 20)

    ui.hr()

    ui.input_checkbox_group(
        "selected_species",
        "Species in Scatterplot",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=True,
    )

    ui.hr()
    ui.h6("Links:")
    ui.a(
        "GitHub Source",
        href="https://github.com/Jaya-srini/cintel-04-local.git",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/pyshiny-penguins-dashboard-express/",
        target="_blank",
    )
    

with ui.layout_columns():

    with ui.card(full_screen=True):
        ui.card_header("Plotly Histogram")

        @render_plotly
        def plotly_histogram():
            # Return the histogram created by the px.histogram() function
            return px.histogram(
                penguins_df, x=input.selected_attribute(), nbins=input.plotly_bin_count()
            )


    with ui.card(full_screen=True):
        ui.card_header("Seaborn Histogram")

        @render.plot(alt="A Seaborn histogram on penguin body mass in grams.")
        def seaborn_histogram():
            # Return the histplot object we created and customized
            histplot = sns.histplot(
                data=penguins_df, x="body_mass_g", bins=input.seaborn_bin_count()
            )
            histplot.set_title("Palmer Penguins")
            histplot.set_xlabel("Mass (g)")
            histplot.set_ylabel("Count")
            return histplot


with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Species")

    @render_plotly
    def plotly_scatterplot():
        # Return the scatterplot created by the px.scatter() function
        return px.scatter(
            filtered_data(),
            x="bill_length_mm",
            y="body_mass_g",
            color="species",
            title="Penguins Plot (Plotly Express)",
            labels={
                "bill_length_mm": "Bill Length (mm)",
                "body_mass_g": "Body Mass (g)",
            },
            size_max=8, # set the maximum marker size
        )

# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
@reactive.calc
def filtered_data():

    # The required function req() is used to ensure that
    # the input.selected_species() function is not empty.
    req(input.selected_species())

    # Use the isin() method to filter the DataFrame
    isSpeciesMatch = penguins_df["species"].isin(input.selected_species())

    return penguins_df[isSpeciesMatch]
