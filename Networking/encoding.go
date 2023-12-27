package main

import (
	"bytes"
	"encoding/binary"
	"io"
	"net"
)

type networkData struct {
	Request Request
	Addr    net.Addr
}

func generateRequest(players []player, reqType uint8) ([]byte, error) {
	// First, serialize the players
	// You have to do this because of the way binarisation works, if i didn't initially do this then i got issues with the
	// changeable size of binarisation or something.
	playerData, err := serialisePlayers(players)

	if err != nil {
		return nil, err
	}

	// Create a Request with the serialized player data as the payload
	req := newRequest(reqType, playerData)
	serialisedData, _ := serialiseRequest(req)
	// Return the data with no errors.
	return serialisedData, nil
}

func serialisePlayers(players []player) ([]byte, error) {
	buf := new(bytes.Buffer)
	for _, p := range players {
		err := binary.Write(buf, binary.LittleEndian, p)
		if err != nil {
			return nil, err
		}
	}
	return buf.Bytes(), nil
}

//Essentially the same process as serialisation except you get weird behaviour due to the fact it's really difficult to tell
// where the end of the payload actually is.

func deserialisePlayers(data []byte) ([]player, error) {
	var players []player
	buf := bytes.NewReader(data)
	// fmt.Printf("Received data length: %d bytes\n", len(data))

	for {
		var p player
		err := binary.Read(buf, binary.LittleEndian, &p)
		if err == io.EOF {
			break // End of data
		}
		if err != nil {
			return nil, err
		}
		players = append(players, p)
	}
	return players, nil
}

// Type 1byte -> PayloadLength -> 4bytes -> PayloadBytes -> payload length to end.
func serialiseRequest(req Request) ([]byte, error) {
	buf := new(bytes.Buffer)

	// Write the Type field
	if err := binary.Write(buf, binary.LittleEndian, req.Type); err != nil {
		return nil, err
	}

	// Write the length of the Payload
	payloadLength := int32(len(req.Payload))
	if err := binary.Write(buf, binary.LittleEndian, payloadLength); err != nil {
		return nil, err
	}

	// Write the Payload bytes
	if _, err := buf.Write(req.Payload); err != nil {
		return nil, err
	}

	return buf.Bytes(), nil
}

func deserialiseRequest(data []byte) (Request, error) {
	var req Request
	buf := bytes.NewReader(data)

	// Read the Type field
	if err := binary.Read(buf, binary.LittleEndian, &req.Type); err != nil {
		return Request{}, err
	}

	// Read the length of the Payload
	var payloadLength int32
	if err := binary.Read(buf, binary.LittleEndian, &payloadLength); err != nil {
		return Request{}, err
	}

	// Read the Payload bytes
	req.Payload = make([]byte, payloadLength)
	if _, err := buf.Read(req.Payload); err != nil {
		return Request{}, err
	}

	return req, nil
}
