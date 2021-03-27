package main

import (
	"encoding/json"
	"github.com/gorilla/mux"
	"log"
	"net/http"
	"strconv"
)

func getNewsFromBD() []NewsStruct {
	return []NewsStruct{}
}

func getNewsFromBDById(id uint64) NewsStruct {
	return NewsStruct{}
}

func GetNews(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	var result Result
	result.Result = "OK"
	news := getNewsFromBD()
	/*news := NewsStruct{
		Title:       "Nice news",
		Image:       URL("localhost/kek.img"),
		Description: "Text",
	}*/
	result.News = news
	_ = json.NewEncoder(w).Encode(result)
}

func GetNewsById(w http.ResponseWriter, r *http.Request) {
	log.Println("GetNewsById")
	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	id, err := strconv.Atoi(params["id"])
	if err != nil {
		var result Result
		result.Result = "not ok"
		result.Description = "nil id"
		json.NewEncoder(w).Encode(result)
		return
	}
	news := NewsStruct{
		Title:       "Nice news",
		Image:       URL("localhost/kek.img"),
		Description: "Text",
	}
	getNewsFromBDById(uint64(id))
	_ = json.NewEncoder(w).Encode(news)
}
