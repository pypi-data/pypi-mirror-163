package odict

import (
	"encoding/json"
	"encoding/xml"
	"io"

	"github.com/imdario/mergo"
)

type Usage struct {
	POS         PartOfSpeech `json:"pos,omitempty" xml:"pos,attr"`
	Definitions []string     `json:"definitions,omitempty" xml:"definition"`
	Groups      []Group      `json:"groups,omitempty" xml:"group"`
	XMLName     xml.Name     `json:"-" xml:"usage"`
}

type UsageMap struct {
	Iterable map[PartOfSpeech]Usage
}

func (m *UsageMap) Set(key PartOfSpeech, value Usage) {
	m.Iterable[key] = value
}

func (m *UsageMap) Get(key PartOfSpeech) Usage {
	return m.Iterable[key]
}

func (m *UsageMap) Has(key PartOfSpeech) bool {
	_, ok := m.Iterable[key]
	return ok
}

func (m *UsageMap) Size() int {
	return len(m.Iterable)
}

func (m UsageMap) MarshalJSON() ([]byte, error) {
	return json.Marshal(m.Iterable)
}

func (m UsageMap) MarshalXML(e *xml.Encoder, start xml.StartElement) error {
	for key := range m.Iterable {
		e.Encode(m.Get(key))
	}
	return nil
}

func (m *UsageMap) UnmarshalXML(d *xml.Decoder, start xml.StartElement) error {
	var usage Usage

	d.DecodeElement(&usage, &start)

	if m.Iterable == nil {
		m.Iterable = make(map[PartOfSpeech]Usage)
	}

	if m.Has(usage.POS) {
		mergo.Merge(&usage, m.Get(usage.POS), mergo.WithAppendSlice)
	}

	m.Set(usage.POS, usage)

	for {
		_, err := d.Token()

		if err != nil {
			if err == io.EOF {
				return nil
			}
			return err
		}
	}
}
