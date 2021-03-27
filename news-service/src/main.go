package main

import (
	"github.com/gorilla/mux"
	"log"
	"net/http"
)

func main() {
	r := mux.NewRouter()
	r.HandleFunc("news", GetNews).Methods("GET")
	r.HandleFunc("news/{id}", GetNewsById).Methods("GET")
	log.Fatal(http.ListenAndServe(":8000", r))
}
