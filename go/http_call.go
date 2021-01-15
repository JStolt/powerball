//http_call.go
package main

import (
//	"io"
	"time"
//	"os"
	"net/http"
	"log"
	"strconv"
	"fmt"
	"strings"
	"github.com/PuerkitoBio/goquery"
)




func main() {

	var rows [][]string
	start := 1992
	now := time.Now()
	thisyear := now.Year()

	for i := start; i <= thisyear; i++ {
    		p := "https://www.lottery.net/powerball/numbers/"
  		index := 42 
		q := p[:index] + strconv.Itoa(i) + p[index:]

		response, err := http.Get(q)
		if err != nil {
			log.Fatal(err)
		}
		defer response.Body.Close()

		//Goquery
		document, err := goquery.NewDocumentFromReader(response.Body)
		if err != nil {
			log.Fatal("Error loading HTTP response body. ", err)
		}


		var row []string
		document.Find("tbody").Each(func(index int, tablehtml *goquery.Selection) {
			tablehtml.Find("tr").Each(func(indextr int, rowhtml *goquery.Selection) {
				rowhtml.Find("a").Each(func(dtidx int, rowdate *goquery.Selection) {
					stuff, _ := rowdate.Attr("href")
					s := strings.Split(stuff, "/")
					//fmt.Printf("%s", s)
					row = append(row, s[3])
				})
				
				rowhtml.Find(".results.powerball").Each(func(pbidx int, tablecell *goquery.Selection) {
					s := tablecell.Text()
					words := strings.Fields(s)
					for _, sval := range words {
						row = append(row, sval)
					}
				})
				rows = append(rows, row)
				row = nil
			})
		})

		//for indx, item := range rows {
			//fmt.Println(indx, "=>", item)
		//}

		//APPROACH 1
		//working!
		//document.Find(".results.powerball").Each(func(index int, element *goquery.Selection) {
			////stuff, _ := element.Attr("class")
			//s := element.Text()
			//words := strings.Fields(s)
			//fmt.Printf("%s\n", words)
		//})
		//working!
		//document.Find("tbody").Find("a").Each(func(index int, element *goquery.Selection) {
			//stuff, ok := element.Attr("href")
			//if ok {
				//s := strings.Split(stuff, "/")
				//fmt.Printf("%s\n", s[3])
				////fmt.Printf("\n")
				////fmt.Printf("Type: %T\n", element)
			//}
			
		//})

		//Find all powerballs
		//document.Find("tbody").Each(processElement)
	}

	fmt.Printf("%s\n", rows)
}

