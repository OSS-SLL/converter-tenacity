import streamlit as st
import math
import pandas as pd
from PIL import Image

favicon = Image.open('sci-lume-fav_BW.png')

st.set_page_config(page_title="SLL Tenacity Conversion", page_icon=favicon)

def convert_units(value, from_unit, to_unit, density):
    if from_unit == to_unit:
        return value
    
    units = {
        'g/den': {
            'cN/tex': lambda x: (x * 9 * 100 / 102),
            'cN/dtex': lambda x: (x * 9 / 10 * 100 / 102),
            'cN/den': lambda x: (x * 100 / 102),
            'MPa': lambda x: x * 9000 * density / 102,
            'kg/mm^2': lambda x: x * 9 * density,
            # 'N': lambda x: x / 10,
            # 'Pound': lambda x: x / 0.0022046,
            # 'kilogram': lambda x: x / 1000
        },
        'cN/tex': {
            'g/den': lambda x: x * 1.02 / 9,
            'cN/dtex': lambda x: x / 10,
            'cN/den': lambda x: x / 9,
            'MPa': lambda x: x * 1000 * density / 100,
            'kg/mm^2': lambda x: x * 1.02 * density,
            # 'N': lambda x: x / 1000,
            # 'Pound': lambda x: x / 0.00044092,
            # 'kilogram': lambda x: x / 100000
        },
        'cN/dtex': {
            'g/den': lambda x: x * 1.02 * 0.9,
            'cN/tex': lambda x: x * 10,
            'cN/den': lambda x: x * 0.9,
            'MPa': lambda x: x * 10000 * density / 100,
            'kg/mm^2': lambda x: x * 10.2 * density,
            # 'N': lambda x: x / 10000,
            # 'Pound': lambda x: x / 0.0000044092,
            # 'kilogram': lambda x: x / 1000000
        },
        'cN/den': {
            'g/den': lambda x: x * 1.02,
            'cN/tex': lambda x: x * 9,
            'cN/dtex': lambda x: x * 9 / 10,
            'MPa': lambda x: x * 9000 * density / 100,
            'kg/mm^2': lambda x: x * 1.02 * 9 * density,
            # 'N': lambda x: x / 100000,
            # 'Pound': lambda x: x / 0.00000044092,
            # 'kilogram': lambda x: x / 10000000
        },
        'MPa': {
            'g/den': lambda x: x * 102 / (density * 9000),
            'cN/tex': lambda x: x * 100 / (density * 1000),
            'cN/dtex': lambda x: x * 100 / (density * 10000),
            'cN/den': lambda x: x * 100 / (density * 9000),
            'kg/mm^2': lambda x: x * 102 / 1000,
            # 'N': lambda x: x * 10,
            # 'Pound': lambda x: x * 0.224809,
            # 'kilogram': lambda x: x * 101.9716
        },
        'kg/mm^2': {
            'g/den': lambda x: x / (density * 9),
            'cN/tex': lambda x: x / (1.02 * density * 1),
            'cN/dtex': lambda x: x / (1.02 * density * 10),
            'cN/den': lambda x: x / (1.02 * density * 9),
            'MPa': lambda x: x * 1000 / 102,
            # 'N': lambda x: x * 10,
            # 'Pound': lambda x: x * 0.224809,
            # 'kilogram': lambda x: x * 101.9716
        },
        # 'N': {
        #     'g/den': lambda x: x * 10,
        #     'cN/tex': lambda x: x * 1000,
        #     'cN/dtex': lambda x: x * 10000,
        #     'cN/den': lambda x: x * 100000,
        #     'MPa': lambda x: x * 0.1,
        #     'kg/mm^2': lambda x: x * 0.1,
        #     'Pound': lambda x: x * 0.224809,
        #     'kilogram': lambda x: x * 101.9716
        # },
        # 'Pound': {
        #     'g/den': lambda x: x * 0.0022046,
        #     'cN/tex': lambda x: x * 0.00044092,
        #     'cN/dtex': lambda x: x * 0.0000044092,
        #     'cN/den': lambda x: x * 0.00000044092,
        #     'MPa': lambda x: x * 0.0044482,
        #     'kg/mm^2': lambda x: x * 0.0044482,
        #     'N': lambda x: x * 0.0044482,
        #     'kilogram': lambda x: x * 0.453592
        # },
        # 'kilogram': {
        #     'g/den': lambda x: x * 1000,
        #     'cN/tex': lambda x: x * 100000,
        #     'cN/dtex': lambda x: x * 1000000,
        #     'cN/den': lambda x: x * 10000000,
        #     'MPa': lambda x: x * 0.00980665,
        #     'kg/mm^2': lambda x: x * 0.00980665,
        #     'N': lambda x: x * 0.00980665,
        #     'Pound': lambda x: x * 2.20462
        # }
    }
    
    if from_unit in units and to_unit in units[from_unit]:
        conversion_func = units[from_unit][to_unit]
        return conversion_func(value)
    else:
        return math.nan  # Return NaN if conversion is not supported
    
# Stress/Tenacity Part
# st.title("Tenacity Conversion") commented out per streamlit recommendation for SEO
st.header("Tenacity Conversion")
st.text("A simple app to convert between different yarn tenacity and stress measurements")

# col1, col2, col3 = st.columns(3)
mmcol1, mmcol2 = st.columns([1, 2])

# Define the units for conversion
units_tenacity = ['g/den', 'cN/tex', 'cN/dtex', 'cN/den', 'MPa', 'kg/mm^2']

# Add number input field
with mmcol1:
    tenacity = st.number_input("Enter a Stress/Tenacity:", value=1.00)

    # Add unit selection dropdown
    from_tenacity = st.selectbox("Unit:", units_tenacity)

    # Density of the material
    density_tenacity = st.number_input("Density (g/mL) of the material:", value=1.00)

# Calculate and display the converted stress/tenacity
with mmcol2: 
    converted_list_tenacity = []
    for to_unit in units_tenacity:
        converted_list_tenacity.append(convert_units(tenacity, from_tenacity, to_unit, density_tenacity))

    data_tenacity = {
        'Units': units_tenacity,
        'Value': converted_list_tenacity
    }

    df_tenacity = pd.DataFrame(data_tenacity)

    # formatted_df_tenacity = df_tenacity.style.format({"Value": "{:.2f}"})  # Format other indices with 2 decimal places

    # st.table(formatted_df_tenacity)
    st.data_editor(
    df_tenacity,
    column_config={
        "Unit": st.column_config.TextColumn(
            "Unit",
            disabled=True,
        ),
        "Value": st.column_config.NumberColumn(
            "Value",
            format="%.2f",
            disabled=True,
        )
    },
    hide_index=True,
    )