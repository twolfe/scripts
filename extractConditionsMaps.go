//Spinner displays an animation while computing the 45th Fibonacci number.
//Make a package from this and formal tests
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"strconv"
)

type Polymorphism struct{
	Gene string
	Pos int
	Ref string
	Alt string
	Ch string
	P1 string
	P2 string
    //Diagnostic bool //for string organised code 
}

func main() {
	// Use _, ok := m["gene"] to check if gene is already in the map
    //Data: a map of polymorphisms with entries true for dignostic SNP and false for no-diagnotic SNP
    data := make(map[Polymorphism]bool) //Change from map to array, slices. No searching, just running through + order to check previous polymorphism
	file, _ := os.Open(os.Args[1])
	populate(file, data)
	file.Close()
    
    //Print formated polymorphisms 
    //(chr(polymorphism.Gene) & nt_exact(polymorphism.Pos, polymorphism.Alt))
    //make an argument based parental condition P1 or P2
    i := 0
    for polymorphism, diagnostic := range data {
        if diagnostic && i == 0 {
            fmt.Println("(chr(", polymorphism.Gene, ") & nt_exact(", polymorphism.Pos, ",", polymorphism.Alt, "))")
            i = 1
        } else if diagnostic && i != 0 {
            fmt.Println("| (chr(", polymorphism.Gene, ") & nt_exact(", polymorphism.Pos, ",", polymorphism.Alt, "))")
        }
    }
}

//Function: make a map containing polymorphisms as keys and dignosis as entries from HyLiTE input
func populate(f *os.File, data map[Polymorphism]bool) {
	input := bufio.NewScanner(f)
	for input.Scan() {
		line := input.Text()
		entry := strings.Split(line, "\t") 
        p, err := strconv.Atoi(entry[1])
		// Check that postion does exist and is really a postion (header is not a position)
		if err == nil {
            polymorphism := Polymorphism{entry[0], p, entry[2], entry[3], entry[4], entry[5], entry[6]}
            data[polymorphism] = diagnosis(polymorphism)
		}
	}
}

//Function: returns whether a polymorphism is diagnotic or not
func diagnosis(polymorphism Polymorphism) bool {
    diagnostic := false
    //Condition: SNP is fixed and ancestral in either parents
    if (polymorphism.P1 == "0,0" && polymorphism.P2 == "1,1") || (polymorphism.P1 == "1,1" && polymorphism.P2 == "0,0") {
        diagnostic = true
    //Condition: fixed but non-ancestral SNP
    } /*else-if condition fixed but non-ancestral SNP {
        diagnostic = true
    }*/
    return diagnostic
}
//Problemaric conditions: when non-fixed parental SNP but different alleles between parents