package main

import (
    "encoding/json"
    "fmt"
    "os"
    "example.invalid/atlas/gitopsprobe/gitopsprobe"
)
func main(){
    var resources []gitopsprobe.Resource
    if err:=json.NewDecoder(os.Stdin).Decode(&resources);err!=nil{fmt.Fprintln(os.Stderr,err);os.Exit(2)}
    digest,err:=gitopsprobe.Digest(resources);if err!=nil{fmt.Fprintln(os.Stderr,err);os.Exit(1)}
    fmt.Println(digest)
}
