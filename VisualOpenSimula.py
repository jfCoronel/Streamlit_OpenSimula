import streamlit as st
import json
import OpenSimula as osm

def project_list(sim):
    list = []
    for p in sim.project_list():
        list.append(p.parameter("name").value)
    return list

def update_table(start_df,edited_df):
   for i in range(len(edited_df.index)):
      for col_name, col in start_df.items():
         if start_df.loc[i,col_name] != edited_df.loc[i,col_name]:
            st.session_state.actual_pro.component(start_df.loc[i,"name"]).parameter(col_name).value = edited_df.loc[i,col_name] 

st.set_page_config(layout="wide")
@st.cache_resource
def create_sim():
    return osm.Simulation()

st.session_state.sim = create_sim()
sim = st.session_state.sim
if "count" not in st.session_state:
    st.session_state.count = 1
if 'project_df' not in st.session_state:
    st.session_state.project_df = sim.project_dataframe(string_format=True) 
    

col1, col2, col3= st.columns((1,9,3))
col1.image('img/icon_opensimula.svg',width=48)
col2.write('#### VisualOpenSimula')
col3.write(f"OpenSimula Version: {osm.VERSION}")

col1, col2 = st.columns((5,5))
## Upload File Form
with st.form("my-form", clear_on_submit=True):
    uploaded_file = st.file_uploader("OpenSimular project file:",type="json")
    submitted = st.form_submit_button("Upload",type="primary")
    if submitted and uploaded_file is not None:
        raw_text = str(uploaded_file.read(),"utf-8")
        file_json = json.loads(raw_text)
        sim.new_project("json")
        sim.project("json").read_dict(file_json)
        st.session_state.project_df = sim.project_dataframe(string_format=True)
        st.rerun()
    
edited_project_df = st.data_editor(st.session_state.project_df, key="project_edit")
if not st.session_state.project_df.equals(edited_project_df):
    p_list = sim.project_list()
    for i in range(len(p_list)):
        for col_name, col in st.session_state.project_df.items():
            if st.session_state.project_df.loc[i,col_name] != edited_project_df.loc[i,col_name]:
                p_list[i].parameter(col_name).value = edited_project_df.loc[i,col_name]
    st.session_state.project_df = edited_project_df
    st.rerun()

if st.button("Create new project", type="primary"):
    sim.new_project(f"New project {st.session_state.count}")
    st.session_state.count += 1
    st.session_state.project_df = sim.project_dataframe(string_format=True)  
    st.rerun()

col1, col2, col3,col4= st.columns((2,1,1,6))

selected_project = col1.selectbox("Select project:",project_list(st.session_state.sim),key="selected_project",placeholder="Select project..")

if selected_project is not None:
    if col2.button("Remove project"):
        sim.del_project(sim.project(selected_project))
        st.session_state.project_df = sim.project_dataframe(string_format=True)
        st.rerun()
    if col3.button("Check project"):
        st.session_state.sim.project(selected_project).check()
    col4.download_button("Download project file", json.dumps(st.session_state.sim.project(selected_project).write_dict()), file_name=selected_project+".json")    

    st.session_state.actual_pro = sim.project(selected_project)
    components_types = ['all','File_data', 'File_met', 'Day_schedule', 'Week_schedule', 'Year_schedule', 'Material', 'Glazing', 'Frame', 'Construction', 'Opening_type', 'Space_type', 'Exterior_surface', 'Virtual_exterior_surface', 'Underground_surface', 'Interior_surface', 'Virtual_interior_surface', 'Opening', 'Space', 'Building']
    actual_table = col1.selectbox("Select table component:",components_types,placeholder="Select component..",)
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
            if col2.button("Remove component"):
                comp = st.session_state.actual_pro.component(selected_component)
                st.session_state.actual_pro.del_component(comp)
                st.session_state.table_df = st.session_state.actual_pro.component_dataframe(type=actual_table,string_format=True)
                st.rerun()


with st.container(height=250,border=True):
    if len(sim.message_list()) > 0:
        st.write("_Opensimula messages:_")
        for i in sim.message_list():
            st.text(i)

