package main

import "fmt"

func main() {
	i := newIndex()
	g := i.generateGame()
	g2 := i.generateGame()
	fmt.Println(*g)

	fmt.Println(i.nextGameID)
	fmt.Println(*g2)

	p := i.addPlayer(100, 100, 100, g.ID)
	fmt.Println(p)
	fmt.Println(*g)
	g.removePlayer(0)
	fmt.Println(*g)
}
