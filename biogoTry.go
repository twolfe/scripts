package main

//Import the required libraries:
import (
	"fmt"
	"io"
	"os"

	"github.com/biogo/biogo/feat"
	"github.com/biogo/biogo/io/featio/bed"
	"github.com/biogo/hts/bam"
	"github.com/biogo/hts/sam"
)

func main() {
	//Open BED file for reading:
	inBed, err := os.Open(os.Args[2])
	//Panic if something goes wrong:
	if err != nil {
		panic(err)
	}

	//Create a new reader for 3-column BED format:
	bedReader, err := bed.NewReader(inBed, 3)
	if err != nil {
		panic(err)
	}

	//Initialise a new map for storing the features:
	featMap := make(map[feat.Feature]int)
	for {
		//Read next BED record:
		bedRec, err := bedReader.Read()
		//Break out at EOF:
		if err == io.EOF {
			break
		}
		//Store feature in map:
		featMap[bedRec] = 0
	}
	//Create a new BAM reader with maximum
	//concurrency:
	bamReader, err := bam.NewReader(ifh, 0)
	if err != nil {
		panic(err)
	}

	for {
		//Read next record:
		record, err := bamReader.Read()
		//Break out of loop if we reached the end
		//of the file:
		if err == io.EOF {
			break
		}
		// Print out record name if read is mapped:
		if record.Flags&sam.Unmapped == 0 {
			//Iterate over features:
			for feat := range featMap {
				// If read position is inside feature range increment feature count:
				if record.Pos >= feat.Start() && record.Pos < feat.End() {
					featMap[feat]++
				}
			}
		}
	}

	//Print out results in BED format:
	for feat, cov := range featMap {
		fmt.Printf("%s\t%d\t%d\t%d\n", feat.Location(), feat.Start(), feat.End(), cov)
	}
}
