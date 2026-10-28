#!/usr/bin/env python3
from __future__ import annotations
import yaml
from common import ROOT, fail
resources=[]
for path in (ROOT/'capstone').rglob('*.yaml'):
    rel=path.relative_to(ROOT).as_posix()
    if '/charts/' in '/'+rel and '/templates/' in '/'+rel: continue
    if '.enc.yaml' in path.name: continue
    for doc in yaml.safe_load_all(path.read_text()):
        if isinstance(doc,dict) and {'apiVersion','kind','metadata'} <= set(doc): resources.append((path,doc))
if len(resources)<35: fail(f"too few Kubernetes resources: {len(resources)}")
for path,r in resources:
    meta=r.get('metadata') or {}
    if not meta.get('name'): fail(f"resource missing name: {path.relative_to(ROOT)}")
    podspec=None
    if r.get('kind')=='Pod': podspec=r.get('spec')
    elif r.get('kind') in {'Deployment','StatefulSet','DaemonSet','Job','Rollout'}:
        podspec=r.get('spec',{}).get('template',{}).get('spec')
    elif r.get('kind')=='CronJob': podspec=r.get('spec',{}).get('jobTemplate',{}).get('spec',{}).get('template',{}).get('spec')
    if isinstance(podspec,dict):
        for c in (podspec.get('initContainers') or [])+(podspec.get('containers') or []):
            image=str(c.get('image',''))
            if image and '@sha256:' not in image: fail(f"mutable image in {path.relative_to(ROOT)}: {image}")
prod=yaml.safe_load((ROOT/'capstone/controllers/argocd/application-prod.yaml').read_text())
auto=prod['spec']['syncPolicy']['automated']
if auto.get('prune') is not False: fail('production Argo Application must not ordinary-prune')
flux=yaml.safe_load((ROOT/'capstone/controllers/flux/infrastructure-kustomization.yaml').read_text())
if flux['spec'].get('prune') is not False: fail('protected Flux inventory must not prune')
print(f"PASS Kubernetes/controller manifest profile — {len(resources)} resources")
