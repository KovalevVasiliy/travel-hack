package main

import (
	"encoding/json"
	"github.com/gorilla/mux"
	"log"
	"net/http"
)

type Result struct {
	Result      string `json:"result"`
	Description string `json:"news"`
}

func getNews(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	var result Result
	result.Result = "OK"
	result.Description = "Nice balls"
	_ = json.NewEncoder(w).Encode(result)
}

func main() {
	r := mux.NewRouter()
	r.HandleFunc("/news", getNews).Methods("GET")
	log.Fatal(http.ListenAndServe(":8000", r))
}
