"""Plotting referendum results in pandas.

In short, we want to make beautiful map to report results of a referendum. In
some way, we would like to depict results with something similar to the maps
that you can find here:
https://github.com/x-datascience-datacamp/datacamp-assignment-pandas/blob/main/example_map.png

To do that, you will load the data as pandas.DataFrame, merge the info and
aggregate them by regions and finally plot them on a map using `geopandas`.
"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


def load_data():
    """Load data from the CSV files referundum/regions/departments."""
    referendum = pd.DataFrame({})
    regions = pd.DataFrame({})
    departments = pd.DataFrame({})

    return referendum, regions, departments


def merge_regions_and_departments(regions, departments):
    merged_df = pd.merge(departments, regions, left_on='common_column_in_departments', right_on='common_column_in_regions')
    return merged_df[['code_reg', 'name_reg', 'code_dep', 'name_dep']]


def merge_referendum_and_areas(referendum, regions_and_departments):
    merged_df = pd.merge(referendum, regions_and_departments, on='code_dep')
    return merged_df[~merged_df['code_dep'].isin(excluded_departments)]



def compute_referendum_result_by_regions(referendum_and_areas):
    result_by_regions = referendum_and_areas.groupby('code_reg').agg({
        'name_reg': 'first', 
        'Registered': 'sum', 
        'Abstentions': 'sum', 
        'Null': 'sum', 
        'Choice A': 'sum', 
        'Choice B': 'sum'
    }).reset_index()
    return result_by_regions
def plot_referendum_map(referendum_result_by_regions):
    gdf = gpd.read_file('regions.geojson')
    merged_gdf = gdf.merge(referendum_result_by_regions, on='code_reg')
    merged_gdf['ratio'] = merged_gdf['Choice A'] / (merged_gdf['Choice A'] + merged_gdf['Choice B'])
    ax = merged_gdf.plot(column='ratio', legend=True, cmap='viridis')
    plt.show()
    return merged_gdf


if __name__ == "__main__":

    referendum, df_reg, df_dep = load_data()
    regions_and_departments = merge_regions_and_departments(
        df_reg, df_dep
    )
    referendum_and_areas = merge_referendum_and_areas(
        referendum, regions_and_departments
    )
    referendum_results = compute_referendum_result_by_regions(
        referendum_and_areas
    )
    print(referendum_results)

    plot_referendum_map(referendum_results)
    plt.show()
