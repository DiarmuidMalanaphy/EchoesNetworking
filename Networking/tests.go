package main

func multipleSendTest() {
	serverAddr := "127.0.0.1:8000" //Local Host

	for i := 1; i <= 50; i++ {
		testPlayers := make([]player, 1)
		testPlayers[0] = newPlayer(1, 1, 1, int16(i), 1)
		testReq, _ := generateRequest(testPlayers, uint8(0))

		sendUDP(serverAddr, testReq)
	}
}
