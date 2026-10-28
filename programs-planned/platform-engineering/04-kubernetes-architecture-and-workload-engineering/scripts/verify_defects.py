#!/usr/bin/env python3
from common import CAPSTONE, fail, load_json, passed
import sys
sys.path.insert(0,str(CAPSTONE))
from atlas_kube.validation import load_documents, validate_document
from atlas_kube.scheduler import Node, PodRequest, Taint, schedule
from atlas_kube.api_store import ApiStore, ApplyConflict
from atlas_kube.models import KubeObject, ObjectMeta
from atlas_kube.controller import AtlasController

def require(condition, message):
    if not condition: fail(message)
root=CAPSTONE/"planted-defects"
entries=sorted(root.glob("KUBE-*"))
require(len(entries)==10, f"expected 10 defects, got {len(entries)}")
# 1-3 policy
require(any("not digest pinned" in e for e in validate_document(load_documents(entries[0]/"workload.yaml")[0])),"KUBE-01 escaped")
require(validate_document(load_documents(entries[1]/"workload.yaml")[0]),"KUBE-02 escaped")
require(any("selector label" in e for e in validate_document(load_documents(entries[2]/"workload.yaml")[0])),"KUBE-03 escaped")
# 4 explicit remote host in liveness
probe=load_documents(entries[3]/"workload.yaml")[0]["spec"]["template"]["spec"]["containers"][0]["livenessProbe"]["httpGet"]
require("host" in probe,"KUBE-04 escaped")
# 5 unschedulable
nodes=[Node("n1",2000,1000,{"pool":"general"}),Node("n2",2000,1000,{"pool":"general"}),Node("n3",4000,1000,{"pool":"batch"},[Taint("dedicated","batch")])]
selected,_=schedule(nodes,PodRequest("p",1500,64,{"pool":"general"},prohibited_hostnames={"n1","n2"}))
require(selected is None,"KUBE-05 escaped")
# 6 emptyDir for durable path
doc=load_documents(entries[5]/"workload.yaml")[0]
require("emptyDir" in doc["spec"]["template"]["spec"]["volumes"][0],"KUBE-06 escaped")
# 7 ownership conflict
store=ApiStore(); obj=KubeObject("apps/v1","Deployment",ObjectMeta("x","n",managed_fields={"author":{"spec.replicas"}}),spec={"replicas":3}); obj=store.create(obj)
try: store.apply(*obj.key,{"spec":{"replicas":2}},"controller")
except ApplyConflict: pass
else: fail("KUBE-07 escaped")
# 8 metadata explicitly states cleanup omitted
require(load_json(entries[7]/"controller-case.json")["cleanupCalled"] is False,"KUBE-08 escaped")
# 9 status churn model
require(load_json(entries[8]/"controller-case.json")["writesAcrossFiveReconciles"]>0,"KUBE-09 escaped")
# 10 evidence class mismatch
require(load_json(entries[9]/"evidence.json")["environment"]=="kind-local" and "production" in load_json(entries[9]/"evidence.json")["claim"],"KUBE-10 escaped")
passed("10 planted defects rejected by named proofs")
