package gitopsprobe

import (
    "crypto/sha256"
    "encoding/hex"
    "encoding/json"
    "fmt"
    "sort"
)

type Resource map[string]any

type Identity struct { Group, Kind, Namespace, Name string }

func identity(r Resource) (Identity, error) {
    api, _ := r["apiVersion"].(string)
    kind, _ := r["kind"].(string)
    meta, _ := r["metadata"].(map[string]any)
    name, _ := meta["name"].(string)
    ns, _ := meta["namespace"].(string)
    group := ""
    for i, c := range api { if c == '/' { group = api[:i]; break } }
    if kind == "" || name == "" { return Identity{}, fmt.Errorf("incomplete identity") }
    return Identity{group, kind, ns, name}, nil
}

func CanonicalSet(resources []Resource) ([]byte, error) {
    type entry struct { id Identity; data Resource }
    entries := make([]entry, 0, len(resources))
    seen := map[Identity]bool{}
    for _, r := range resources {
        id, err := identity(r); if err != nil { return nil, err }
        if seen[id] { return nil, fmt.Errorf("duplicate identity: %+v", id) }
        seen[id] = true
        cleaned := Resource{}
        for k, v := range r { if k != "status" { cleaned[k] = v } }
        entries = append(entries, entry{id, cleaned})
    }
    sort.Slice(entries, func(i,j int) bool {
        a,b:=entries[i].id,entries[j].id
        if a.Group!=b.Group{return a.Group<b.Group}; if a.Kind!=b.Kind{return a.Kind<b.Kind};
        if a.Namespace!=b.Namespace{return a.Namespace<b.Namespace}; return a.Name<b.Name
    })
    out:=make([]Resource,len(entries)); for i,e:=range entries{out[i]=e.data}
    return json.Marshal(out)
}

func Digest(resources []Resource) (string, error) {
    raw, err := CanonicalSet(resources); if err != nil { return "", err }
    sum := sha256.Sum256(raw)
    return "sha256:" + hex.EncodeToString(sum[:]), nil
}

type Diff struct { Missing, Extra, Changed []string }

func Compare(desired, live map[string]string) Diff {
    d:=Diff{}
    for k,v:=range desired { lv,ok:=live[k]; if !ok { d.Missing=append(d.Missing,k) } else if lv!=v { d.Changed=append(d.Changed,k) } }
    for k:=range live { if _,ok:=desired[k]; !ok { d.Extra=append(d.Extra,k) } }
    sort.Strings(d.Missing); sort.Strings(d.Extra); sort.Strings(d.Changed)
    return d
}
