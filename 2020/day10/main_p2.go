package main

import (
	"fmt"
	"io/ioutil"
	"sort"
	"strconv"
	"strings"
)

func main() {
	data, err := readInput("input.txt")
	if err != nil {
		fmt.Errorf("could not read input: %v", err)
	}

	var res int
	l := len(data)
	w := 25
	current := 0 + w
	for current < l {
		slice := data[current-w : current]
		target := data[current]
		v := isValid(slice, target)
		if !v {
			res = target
			break
		}
		current++
	}

	start := 0
	for data[start] < res {
		end := start + 1
		for data[end] < res {
			result := 0
			s := data[start:end]
			for j, v := range s {
				result += v
				if result == res {
					numbers := s[:j+1]
					sort.Ints(numbers)
					fmt.Printf("%v = %d\n", numbers, res)
					fmt.Printf("%d + %d = %d\n", numbers[0], numbers[len(numbers)-1], numbers[0]+numbers[len(numbers)-1])

					return
				}
			}
			end++
		}
		start++
	}
}

func isValid(in []int, target int) bool {
	var valid bool
	for i, e1 := range in[:len(in)-1] {
		for _, e2 := range in[i:] {
			total := e1 + e2
			if total == target {
				valid = true
			}
		}
	}
	return valid
}

func readInput(path string) ([]int, error) {
	f, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("could not open %s: %v", path, err)
	}

	d := make([]int, 0)
	for _, n := range strings.Split(strings.TrimSpace(string(f)), "\n") {
		i, _ := strconv.Atoi(n)
		d = append(d, i)
	}

	return d, nil
}
