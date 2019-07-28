package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"runtime"
	"sync"
	"time"
)

var (
	a  = []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100, 1000}
	wg sync.WaitGroup
)

func calcSquares(number int, op chan<- int) {
	sum := 0
	for number != 0 {
		digit := number % 10
		sum += digit * digit
		number /= 10
	}
	op <- sum
}

func calcCubes(number int, op chan<- int) { // send to channel instead of return
	sum := 0
	for number != 0 {
		digit := number % 10
		sum += digit * digit * digit
		number /= 10
	}
	op <- sum
}

func consume(ch <-chan int) {
	for {
		select {
		case msg := <-ch:
			fmt.Println("Message from ch:", msg)
		case t := <-time.After(time.Second * 5):
			fmt.Println("timeout", t)
			return
		}
		// fmt.Println("rand int:", <-ch)
	}
}

func produce(ch chan<- int) {
	for {
		random := rand.Intn(10)
		ch <- random + 1024
		time.Sleep(time.Duration(random) * time.Second)
	}
}

func chanTest0() {
	var ball = make(chan string)
	kickBall := func(playerName string) {
		for {
			fmt.Println(<-ball, "kicked the ball, received by", playerName)
			time.Sleep(1 * time.Second)
			ball <- playerName
		}
	}
	go kickBall("John")
	go kickBall("Alice")
	go kickBall("Bob")
	go kickBall("Emily")
	ball <- "Start" // kick off
	// ball <- "referee2" // kick off
	time.Sleep(9 * time.Second)
	wg.Wait()
}

func chanTest1() {
	fibonacci := func() chan uint64 {
		ch := make(chan uint64)
		go func() {
			var x, v, max uint64 = 0, 1, 1 << 63
			for ; v < max; ch <- v { // send value to channel
				x, v = v, x+v
			}
			close(ch)
		}()
		return ch
	}
	fn, x, i := fibonacci(), uint64(0), 0
	var ok bool = true
	for ; ok; i++ { // here
		x, ok = <-fn
		time.Sleep(200 * time.Millisecond)
		fmt.Printf("%3d: %d\n", i, x)
	}
}

func chanTest2() {
	var ch chan int = make(chan int, 1) // bufferred channel

	for i := 0; i < 10; i++ {
		x := i
		go func() {
			ch <- a[x]
		}()
	}

	go consume(ch)
	go produce(ch)
	// wg.Wait()
	// close(ch)

	var input string
	fmt.Println("\nPress any key to continue")
	reader := bufio.NewScanner(os.Stdin)
	if reader.Scan() {
		input = reader.Text()
	}
	fmt.Println(input)
}

func chanTest3() {
	c := make(chan string, 2)
	trySend := func(v string) {
		select {
		case c <- v:
		default: // go here if c is full.
		}
	}
	tryReceive := func() string {
		for {
			select {
			case v := <-c:
				return v
			case t := <-time.After(time.Second * 5):
				fmt.Println("timeout", t)
				return "timed out"
			default:
				return "-" // go here if c is empty
			}
		}
	}
	trySend("Hello!") // succeed to send
	trySend("Hi!")    // succeed to send
	// Fail to send, but will not block.
	trySend("Bye!")
	// The following two lines will
	// both succeed to receive.
	fmt.Println(tryReceive()) // Hello!
	fmt.Println(tryReceive()) // Hi!
	// The following line fails to receive.
	fmt.Println(tryReceive()) // -
}

func chanTest4() {
	ch := make(chan int) // try bufferred or unbufferred

	go func(ch chan int) {
		for i := 1; i <= 10; i++ {
			time.Sleep(100 * time.Millisecond)
			fmt.Println("Func goroutine sends data: ", i)
			ch <- i
		}
		close(ch)
	}(ch)

	fmt.Println("Main sleeps 2 seconds")
	time.Sleep(time.Second * 2)

	fmt.Println("Main begins receiving data")
	for d := range ch {
		fmt.Println("Main received data:", d)
	}
}

func CalculateValue(c chan int) {
	value := rand.Intn(10)
	fmt.Println("Produced Random Value: {}", value)
	time.Sleep(1000 * time.Millisecond)
	c <- value
	fmt.Println("Sent out:", value)
}

func chanTest5() {
	fmt.Println("Go Channel Tutorial")

	valueChannel := make(chan int, 2)
	defer close(valueChannel)

	go CalculateValue(valueChannel)
	go CalculateValue(valueChannel)

	values := <-valueChannel
	fmt.Println(values)

	time.Sleep(1000 * time.Millisecond)
}

func write1(c chan int) {
	for i := 0; i < 5; i++ {
		time.Sleep(300 * time.Millisecond)
		c <- i
	}
}
func write2(c chan int) {
	for i := 50; i < 100; i += 10 {
		time.Sleep(100 * time.Millisecond)
		c <- i
	}
}
func read2(c1, c2 chan int) {
	timeout := time.After(2 * time.Second)
Loop:
	for {
		select {
		case v1 := <-c1:
			fmt.Println(v1)
		case v2 := <-c2:
			fmt.Println(v2)
		case <-timeout:
			fmt.Println("timeout")
			break Loop
		default: //
			fmt.Println("default")
			time.Sleep(250 * time.Millisecond)
		}
	}
}

func chanTest6() {
	c1 := make(chan int)
	c2 := make(chan int)
	go write1(c1)
	go write2(c2) // write2 is faster than write1
	read2(c1, c2)
}

func main() {

	fmt.Println("- Max number of threads:", runtime.NumCPU())

	chanTest6()
}
