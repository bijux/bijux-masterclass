package cni

import (
	"errors"
	"sort"
)

type Attachment struct {
	ID         string
	Generation int
	Address    string
	Active     bool
}

type State struct{ Attachments map[string]*Attachment }

func NewState() *State { return &State{Attachments: map[string]*Attachment{}} }

func (s *State) Add(id string, generation int, address string) (*Attachment, error) {
	if current, ok := s.Attachments[id]; ok && current.Active {
		if current.Generation == generation && current.Address == address {
			return current, nil
		}
		return nil, errors.New("attachment identity conflict")
	}
	item := &Attachment{ID: id, Generation: generation, Address: address, Active: true}
	s.Attachments[id] = item
	return item, nil
}

func (s *State) Check(id string) bool { item, ok := s.Attachments[id]; return ok && item.Active }
func (s *State) Del(id string) {
	if item, ok := s.Attachments[id]; ok {
		item.Active = false
	}
}
func (s *State) GC(known map[string]int) []string {
	removed := []string{}
	for id, item := range s.Attachments {
		if item.Active && known[id] != item.Generation {
			item.Active = false
			removed = append(removed, id)
		}
	}
	sort.Strings(removed)
	return removed
}
func Status(deps map[string]bool) bool {
	for _, ok := range deps {
		if !ok {
			return false
		}
	}
	return true
}
