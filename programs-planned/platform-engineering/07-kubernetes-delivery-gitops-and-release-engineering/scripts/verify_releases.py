#!/usr/bin/env python3
from __future__ import annotations
from common import ROOT, fail, load_json
from atlas_delivery.models import ArtifactSet, DesiredRevision, EvidenceGate, ReleaseCandidate
from atlas_delivery.release import classify_release
expected={
 'accepted.json':'accepted','rejected-mutable-artifact.json':'rejected','rejected-protected-prune.json':'rejected',
 'rejected-unsafe-hook.json':'rejected','rejected-health-only.json':'rejected',
 'review-required-secret-native.json':'review-required','not-executed-live-cluster.json':'not-executed'}
for name,want in expected.items():
    d=load_json(ROOT/'capstone/releases'/name); r=d['revision']; a=r['artifacts']
    revision=DesiredRevision(r['releaseId'],r['environment'],r['commit'],r['renderer'],r['rendererVersion'],r['renderDigest'],ArtifactSet(tuple(a['imageDigests']),a.get('chartDigest'),a.get('sourceArtifactDigest')),r.get('predecessor'))
    gates=[EvidenceGate(g['name'],g['status'],g['subject'],g['reason'],g.get('blocker',True),g.get('expiresAt')) for g in d['gates']]
    got,_=classify_release(ReleaseCandidate(revision,gates,d.get('approvals',[]),d.get('protectedDeletions',[]),d.get('rollbackFrontier','traffic-and-manifest')))
    if got!=want: fail(f"{name}: expected {want}, got {got}")
print(f"PASS release classification — {len(expected)} candidates")
