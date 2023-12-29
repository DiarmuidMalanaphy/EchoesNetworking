package main

import (
	"fmt"
	"net"
	"os"
)

func listen(reqChan chan<- networkData) {

	addr, err := net.ResolveUDPAddr("udp", ":8000") // Listen on all interfaces
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	conn, err := net.ListenUDP("udp", addr)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	defer conn.Close()
	buffer := make([]byte, 1024)

	fmt.Println("UDP server listening on port 8000...")
	for {

		n, remoteAddr, err := conn.ReadFromUDP(buffer)

		req, err := deserialiseRequest(buffer[:n])

		if err != nil {
			fmt.Println(err)
			continue
		}

		// We then relay this information back to main through the requests channel
		// Useful way for goroutines to communicate.
		reqChan <- networkData{Request: req, Addr: remoteAddr}
	}
}

func sendUDP(address string, data []byte) error {
	// Resolve the UDP address
	udpAddr, err := net.ResolveUDPAddr("udp", address)
	if err != nil {
		return err
	}
	localAddr, err := net.ResolveUDPAddr("udp", ":8000")
	if err != nil {
		return err
	}

	// Establish a UDP connection
	conn, err := net.DialUDP("udp", localAddr, udpAddr)
	if err != nil {
		return err
	}
	defer conn.Close()

	// Send the data
	_, err = conn.Write(data)
	if err != nil {
		return err
	}

	return nil
}
