def project_list(sim):
    list = []
    for p in sim.project_list():
        list.append(p.parameter("name").value)
    return list