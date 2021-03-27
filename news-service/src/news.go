package main

import (
	"encoding/json"
	"github.com/gorilla/mux"
	"net/http"
	"strconv"
)

func getNewsFromBD() ([]NewsStruct, error) {
	return []NewsStruct{}, nil
}

func getNewsFromBDById(id uint64) (NewsStruct, error) {
	return NewsStruct{}, nil
}

func GetNews(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	var result ResultMany
	result.Result = "OK"
	news, err := getNewsFromBD()

	if err != nil {
		result := Result{
			Result:"not ok",
			Description: "nil id",
		}
		_ = json.NewEncoder(w).Encode(result)
		return
	}
	result.News = news
	_ = json.NewEncoder(w).Encode(result)
}

func GetNewsById(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	id, err := strconv.Atoi(params["id"])
	if err != nil {
		result := Result{
			Result:"not ok",
			Description: "nil id",
		}
		_ = json.NewEncoder(w).Encode(result)
		return
	}
	result := Result{
		Result:"OK",
	}
	news, err := getNewsFromBDById(uint64(id))
	if err != nil {
		result := Result{
			Result:"not ok",
			Description: "nil id",
		}
		_ = json.NewEncoder(w).Encode(result)
		return
	}
	result.News = news
	_ = json.NewEncoder(w).Encode(result)
}
