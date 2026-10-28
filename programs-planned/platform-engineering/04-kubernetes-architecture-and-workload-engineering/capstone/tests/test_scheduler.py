from atlas_kube.scheduler import Node, PodRequest, Taint, Toleration, schedule, evaluate_node


def nodes():
    return [
        Node("n1",2000,2048,{"pool":"general","zone":"a"}),
        Node("n2",2000,2048,{"pool":"general","zone":"b"}),
        Node("n3",4000,4096,{"pool":"batch","zone":"a"},[Taint("dedicated","batch")]),
    ]


def test_simple_schedule():
    selected, decisions=schedule(nodes(), PodRequest("p",100,64,{"pool":"general"}))
    assert selected == "n1" and any(d.feasible for d in decisions)


def test_impossible_joint_constraints():
    pod=PodRequest("p",1500,64,{"pool":"general"},prohibited_hostnames={"n1","n2"})
    selected, decisions=schedule(nodes(),pod)
    assert selected is None
    assert {d.node for d in decisions if not d.feasible}=={"n1","n2","n3"}


def test_toleration_does_not_override_affinity():
    pod=PodRequest("p",100,64,{"pool":"general"},[Toleration("dedicated","batch")],{"n1","n2"})
    selected, decisions=schedule(nodes(),pod)
    assert selected is None
    n3=next(d for d in decisions if d.node=="n3")
    assert "LabelMismatch:pool" in n3.reasons


def test_capacity_reason():
    node=Node("small",100,64,{})
    result=evaluate_node(node,PodRequest("p",200,128))
    assert result.reasons == ("InsufficientCPU","InsufficientMemory")


def test_topology_skew():
    node=Node("n",1000,1024,{"zone":"a"})
    pod=PodRequest("p",10,10,topology_key="zone",occupied_domains={"a":2,"b":1},max_skew=1)
    assert "TopologySkew" in evaluate_node(node,pod).reasons
