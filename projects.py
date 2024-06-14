import streamlit as st
import json
import OpenSimula as os
from utils import project_list

st.set_page_config(layout="wide")
@st.cache_resource
def create_sim():
    return os.Simulation()

st.session_state.sim = create_sim()
sim = st.session_state.sim
if "count" not in st.session_state:
    st.session_state.count = 1
if 'project_df' not in st.session_state:
    st.session_state.project_df = sim.project_dataframe(string_format=True) 
    


def update_projects(start_df,edited_df):
    p_list = sim.project_list()
    if len(p_list) > 0:
        for i in range(len(p_list)):
            for col_name, col in start_df.items():
                if start_df.loc[i,col_name] != edited_df.loc[i,col_name]:
                    p_list[i].parameter(col_name).value = edited_df.loc[i,col_name] 


# Header
col1, col2, col3= st.columns((1,9,3))
col1.image('img/icon_opensimula.svg',width=48)
col2.write('#### VisualOpenSimula')
col3.write(f"OpenSimula Version: {os.VERSION}")

st.write('##### Projects Editor')

col1, col2 = st.columns((5,5))
actual_project = col1.selectbox(
   "Select working project:",
   project_list(st.session_state.sim),
   key="actual_project",
   placeholder="Select project..",
)
uploaded_file = col2.file_uploader("OpenSimular project file:")
if uploaded_file is not None:
    raw_text = str(uploaded_file.read(),"utf-8")
    file_json = json.loads(raw_text)
    sim.new_project("json")
    sim.project("json").read_dict(file_json)
    st.session_state.project_df = sim.project_dataframe(string_format=True)

col1, col2, col3= st.columns((2,2,6))

if col1.button("Create new project"):
    sim.new_project(f"New project {st.session_state.count}")
    st.session_state.count += 1
    st.session_state.project_df = sim.project_dataframe(string_format=True)  
    st.rerun()

if col2.button("Remove working project", type="primary"):
    sim.del_project(sim.project(actual_project))
    st.session_state.project_df = sim.project_dataframe(string_format=True)
    st.rerun()

if actual_project is not None:
    col3.download_button("Download working project file", json.dumps(st.session_state.sim.project(actual_project).write_dict()), file_name=actual_project+".json")    


#def projects_change():
#    ed_rows = st.session_state.project_edit["edited_rows"]
#    print(ed_rows)
#    # Pruebas
#    sim.project_list()[0].parameter("time_step").value = 1

edited_project_df = st.data_editor(st.session_state.project_df, key="project_edit")
if not st.session_state.project_df.equals(edited_project_df):
    update_projects(st.session_state.project_df,edited_project_df)
    st.session_state.project_df = edited_project_df
    st.rerun()

    
if len(sim.message_list()) > 0:
    st.write("_Opensimula messages:_")
    for i in sim.message_list():
        st.text(i)

