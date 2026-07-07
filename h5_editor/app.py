import streamlit as st
import pandas as pd
import os


def get_h5_tables(h5_path: str) -> list[str]:
    """Get all table paths from an H5 file using pandas."""
    with pd.HDFStore(h5_path, "r") as f:
        return f.keys()


def load_table(h5_path: str, table_name: str) -> pd.DataFrame:
    """Load a table from the H5 file into a DataFrame."""
    return pd.read_hdf(h5_path, key=table_name)


st.set_page_config(page_title="H5 Table Viewer", layout="wide")

st.title("H5 Table Viewer")

# File path input
default_path = "L:/base_year_2023_inputs/urbansim2_inputs/psrc_base_year_2023_alloc_py3.h5"
h5_path = st.text_input("H5 File Path", value=default_path)

if not os.path.exists(h5_path):
    st.error(f"File not found: {h5_path}")
else:
    try:
        # Load tables list
        if "tables" not in st.session_state or st.session_state.get("h5_path") != h5_path:
            st.session_state["tables"] = get_h5_tables(h5_path)
            st.session_state["h5_path"] = h5_path

        tables = st.session_state["tables"]

        if not tables:
            st.warning("No tables found in the H5 file.")
        else:
            # Sidebar for table selection
            st.sidebar.title("Tables")
            selected_table = st.sidebar.selectbox("Select a table", tables)

            # Load and display selected table
            if selected_table:
                st.subheader(selected_table)

                with st.spinner("Loading table..."):
                    df = load_table(h5_path, selected_table)

                # Display shape and info
                st.write(f"Shape: {df.shape[0]:,} rows x {df.shape[1]} columns")

                # Show data table
                st.dataframe(df, use_container_width=True)

                # Option to show dtypes
                with st.expander("Column Info"):
                    st.dataframe(
                        pd.DataFrame(
                            {"dtype": df.dtypes, "non_null": df.count(), "null": df.isnull().sum()}
                        )
                    )

    except Exception as e:
        st.error(f"Error reading H5 file: {e}")
