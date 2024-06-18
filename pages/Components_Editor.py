import streamlit as st
import OpenSimula as osm
from utils import project_list

def update_table(start_df,edited_df):
   for i in range(len(edited_df.index)):
      for col_name, col in start_df.items():
         if start_df.loc[i,col_name] != edited_df.loc[i,col_name]:
            st.session_state.actual_pro.component(start_df.loc[i,"name"]).parameter(col_name).value = edited_df.loc[i,col_name] 
        
@st.cache_resource
def create_sim():
    return osm.Simulation()
st.session_state.sim = create_sim()    
# Header
col1, col2, col3= st.columns((1,9,3))
col1.image('img/icon_opensimula.svg',width=48)
col2.write('#### VisualOpenSimula')
col3.write(f"OpenSimula Version: {osm.VERSION}")

col1, col2= st.columns((5,5))
actual_project = col1.selectbox(
   "Select working project:",
   project_list(st.session_state.sim),
   key="actual_project",
   placeholder="Select project..",
)
st.session_state.actual_pro = st.session_state.sim.project(actual_project)
components_types = ['all','File_data', 'File_met', 'Day_schedule', 'Week_schedule', 'Year_schedule', 'Material', 'Glazing', 'Frame', 'Construction', 'Opening_type', 'Space_type', 'Exterior_surface', 'Virtual_exterior_surface', 'Underground_surface', 'Interior_surface', 'Virtual_interior_surface', 'Opening', 'Space', 'Building']
actual_table = col2.selectbox(
   "Select table component:",
   components_types,
   key="actual_table",
   placeholder="Select component..",
)
st.session_state.table_df = st.session_state.actual_pro.component_dataframe(type=actual_table,string_format=True)

edited_table_df = st.data_editor(st.session_state.table_df, key="table_edit")
if not st.session_state.table_df.equals(edited_table_df):
    update_table(st.session_state.table_df,edited_table_df)
    st.session_state.table_df = edited_table_df
    st.rerun()

if actual_table != "all":
   if st.button("Create new component", type="primary"):
      st.session_state.actual_pro.new_component(actual_table,"New_"+actual_table)
      st.session_state.table_df = st.session_state.actual_pro.component_dataframe(type=actual_table,string_format=True)
      st.rerun()

col1, col2= st.columns((2,8))
if len(st.session_state.table_df.index) > 0:
   selected_component = col1.selectbox("Select component:",st.session_state.table_df["name"].to_list(),placeholder="Select component..")
   if selected_component is not None:
      if col2.button("Remove"):
         comp = st.session_state.actual_pro.component(selected_component)
         st.session_state.actual_pro.del_component(comp)
         st.session_state.table_df = st.session_state.actual_pro.component_dataframe(type=actual_table,string_format=True)
         st.rerun()

with st.container(height=250,border=True):
    if len(st.session_state.sim.message_list()) > 0:
        st.write("_Opensimula messages:_")
        for i in st.session_state.sim.message_list():
            st.text(i)
