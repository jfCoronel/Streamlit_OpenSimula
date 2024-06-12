import streamlit as st
import json
import OpenSimula as os

@st.cache_resource
def create_sim():
    return os.Simulation()

sim = create_sim()
if "count" not in st.session_state:
    st.session_state.count = 1
if 'project_df' not in st.session_state:
    st.session_state.project_df = sim.project_dataframe(string_format=True) 
    
def project_list():
    list = []
    for p in sim.project_list():
        list.append(p.parameter("name").value)
    return list

def update_projects(start_df,edited_df):
    p_list = sim.project_list()
    if len(p_list) > 0:
        for i in range(len(p_list)):
            for col_name, col in start_df.items():
                if start_df.loc[i,col_name] != edited_df.loc[i,col_name]:
                    p_list[i].parameter(col_name).value = edited_df.loc[i,col_name] 

#def new_project():
#    sim.new_project(st.session_state.project_name)
    
col1, col2, col3= st.columns((1,10,2))
col1.image('img/icon_opensimula.svg',width=48)
col2.write('#### VisualOpenSimula')
col3.write(f"Version: {os.VERSION}")

st.write('##### Projects Editor')
actual_project = st.selectbox(
   "Select working project:",
   project_list()
   ,
   index=None,
   placeholder="Select project..",
)

#if st.button("Remove working project", type="primary"):
#    sim.del_project(sim.project(actual_project))
#    st.rerun()

if st.button("Create empty project"):
    sim.new_project(f"Empty project {st.session_state.count}")
    st.session_state.count += 1
    st.session_state.project_df = sim.project_dataframe(string_format=True)  

uploaded_file = st.file_uploader("OpenSimular project file:")
if uploaded_file is not None:
    raw_text = str(uploaded_file.read(),"utf-8")
    file_json = json.loads(raw_text)
    sim.new_project("json")
    sim.project("json").read_dict(file_json)
    st.session_state.project_df = sim.project_dataframe(string_format=True)  
        
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
#st.json(st.session_state.project_edit)
