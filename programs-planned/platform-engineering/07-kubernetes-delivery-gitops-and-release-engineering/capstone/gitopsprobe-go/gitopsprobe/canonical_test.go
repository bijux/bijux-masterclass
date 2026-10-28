package gitopsprobe

import "testing"

func TestDigestIgnoresStatusAndOrder(t *testing.T) {
    a:=Resource{"apiVersion":"v1","kind":"ConfigMap","metadata":map[string]any{"name":"a","namespace":"n"},"data":map[string]any{"x":"1"}}
    b:=Resource{"apiVersion":"v1","kind":"Service","metadata":map[string]any{"name":"b","namespace":"n"},"spec":map[string]any{"ports":[]any{map[string]any{"port":80.0}}},"status":map[string]any{"x":"server"}}
    d1,e:=Digest([]Resource{a,b}); if e!=nil{t.Fatal(e)}
    delete(b,"status")
    d2,e:=Digest([]Resource{b,a}); if e!=nil{t.Fatal(e)}
    if d1!=d2{t.Fatalf("digest changed: %s %s",d1,d2)}
}
func TestDuplicateIdentityRejected(t *testing.T){
    a:=Resource{"apiVersion":"v1","kind":"ConfigMap","metadata":map[string]any{"name":"a"}}
    if _,e:=Digest([]Resource{a,a}); e==nil{t.Fatal("expected duplicate rejection")}
}
func TestCompare(t *testing.T){
    d:=Compare(map[string]string{"a":"1","b":"2"},map[string]string{"b":"3","c":"4"})
    if len(d.Missing)!=1||d.Missing[0]!="a"||len(d.Changed)!=1||d.Changed[0]!="b"||len(d.Extra)!=1||d.Extra[0]!="c"{t.Fatalf("bad diff: %+v",d)}
}
