package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"time"
)

func consume(ch <-chan int) {
	for {
		select {
		case msg := <-ch:
			fmt.Println("Message from ch:", msg)
		case t := <-time.After(time.Second * 2):
			fmt.Println("timeout", t)
			return
		}
		// fmt.Println("rand int:", <-ch)
	}
}

func produce(ch chan<- int) {
	for {
		ch <- rand.Intn(1024) + 1000
		time.Sleep(1 * time.Second)
	}
}

var (
	a = []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100, 1000}
)

func main() {
	var ch chan int = make(chan int, 1)

	for i := 0; i < 10; i++ {
		x := i
		go func() {
			ch <- a[x]
		}()
	}

	go consume(ch)
	go produce(ch)
	var input string
	fmt.Println("\nPress any key to continue")
	reader := bufio.NewScanner(os.Stdin)
	if reader.Scan() {
		input = reader.Text()
	}
	fmt.Println(input)
}
