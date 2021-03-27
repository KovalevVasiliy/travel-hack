package main

import (
	"github.com/gorilla/mux"
	"log"
	"net/http"
)

func main() {
	r := mux.NewRouter()
	r.HandleFunc("/news", GetNews).Methods("GET")
	r.HandleFunc("/news/{id}", GetNewsById).Methods("GET")
	r.HandleFunc("/category/{id}", GetCategoryById).Methods("GET")
	r.HandleFunc("/location/{id}", GetLocationById).Methods("GET")
	log.Fatal(http.ListenAndServe(":8000", r))
}
