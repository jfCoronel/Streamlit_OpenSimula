import streamlit as st
import json
import OpenSimula as os

@st.cache_resource
def create_sim():
    return os.Simulation()

sim = create_sim()
if "count" not in st.session_state:
    st.session_state.count = 1
    
def project_list():
    list = []
    for p in sim.project_list():
        list.append(p.parameter("name").value)
    return list

def markdown_project_list():
    md = ""
    for p in project_list():
        md = md + "- " + p+ "\n"
    return md

def new_project():
    sim.new_project(st.session_state.project_name)

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
if st.button("Remove working project", type="primary"):
    sim.del_project(sim.project(actual_project))
    st.rerun()

if st.button("Create empty project"):
    sim.new_project(f"Empty project {st.session_state.count}")
    st.session_state.count += 1
#st.text_input("New project name (press enter to create)","...",on_change=new_project,key="project_name")

uploaded_file = st.file_uploader("OpenSimular project file:")
if uploaded_file is not None:
    raw_text = str(uploaded_file.read(),"utf-8")
    file_json = json.loads(raw_text)
    sim.new_project("json")
    sim.project("json").read_dict(file_json)    
    

def projects_change():
    ed_rows = st.session_state.project_edit["edited_rows"]
    print(ed_rows)
    # Pruebas
    sim.project_list()[0].parameter("time_step").value = 1

#st.write(markdown_project_list())
st.data_editor(sim.project_dataframe(), key="project_edit",on_change=projects_change, use_container_width=True)
if len(sim.message_list()) > 0:
    st.write("_Opensimula last message:_")
    st.text(sim.message_list()[-1])
st.json(st.session_state.project_edit)
