import streamlit as st
import json
import OpenSimula as osm
from utils import project_list

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
    if col2.button("Remove"):
        sim.del_project(sim.project(selected_project))
        st.session_state.project_df = sim.project_dataframe(string_format=True)
        st.rerun()
    if col3.button("Check"):
        st.session_state.sim.project(selected_project).check()
    col4.download_button("Download project file", json.dumps(st.session_state.sim.project(selected_project).write_dict()), file_name=selected_project+".json")    

with st.container(height=250,border=True):
    if len(sim.message_list()) > 0:
        st.write("_Opensimula messages:_")
        for i in sim.message_list():
            st.text(i)

