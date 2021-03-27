package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"github.com/gorilla/mux"
	"log"
	"net/http"
	"strconv"
)

func getNewsFromBD() ([]NewsStruct, error) {
	return []NewsStruct{}, nil
}

func getNewsFromBDById(id uint64) (NewsStruct, error) {
	return NewsStruct{}, nil
}

var categoryIdMap = map[CategoryId]Category{}
var locationIdMap = map[LocationId]Location{}


func getLocationById(id LocationId) (location Location, err error) {
	location = locationIdMap[id]
	if location.Name == "" {
		url := fmt.Sprintf("http://postgrest:3000/locations?location_id=%d", id)
		resp, err := http.Get(url)
		if err != nil {
			log.Print("getLocationById GET error", err)
			return location, err
		}
		var locations []Location
		err = json.NewDecoder(resp.Body).Decode(&locations)
		if err != nil {
			log.Print("getLocationById Decoding error ", err)
			return location, err
		}
		if len(locations) != 0 {
			location = locations[0]
			locationIdMap[id] = locations[0]
			log.Printf("getLocationById return from server name: %s , %d: ", location.Name, location.Id)
		} else {
			log.Print("getLocationById return from server is null")
			return location, errors.New("no such location")
		}
	} else {
		log.Printf("getLocationById return from cache name: %s , %d: ", location.Name, location.Id)
	}
	return location, nil
}


func GetLocationById(w http.ResponseWriter, r *http.Request) {
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
	location, err := getLocationById(LocationId(id))
	if err != nil {
		result := Result{
			Result:"not ok",
			Description: "no such location",
		}
		_ = json.NewEncoder(w).Encode(result)
		return
	}
	result.Data = location
	_ = json.NewEncoder(w).Encode(result)
}

func getCategoryById(id CategoryId) (category Category, err error) {
	category = categoryIdMap[id]
	if category.Name == "" {
		url := fmt.Sprintf("http://postgrest:3000/categories?category_id=%d", id)
		resp, err := http.Get(url)
		if err != nil {
			log.Print("getCategoryById GET error", err)
			return category, err
		}
		var categories []Category
		err = json.NewDecoder(resp.Body).Decode(&categories)
		if err != nil {
			log.Print("getCategoryById Decoding error ", err)
			return category, err
		}
		if len(categories) != 0 {
			category = categories[0]
			categoryIdMap[id] = categories[0]
			log.Printf("getCategoryById return from server name: %s , %d: ", category.Name, category.Id)
		} else {
			log.Print("getCategoryById return from server is null")
			return category, errors.New("no such location")
		}
	} else {
		log.Printf("getCategoryById return from cache name: %s , %d: ", category.Name, category.Id)
	}
	return category, nil
}


func GetCategoryById(w http.ResponseWriter, r *http.Request) {
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
	category, err := getCategoryById(CategoryId(id))
	if err != nil {
		result := Result{
			Result:"not ok",
			Description: "no such category",
		}
		_ = json.NewEncoder(w).Encode(result)
		return
	}
	result.Data = category
	_ = json.NewEncoder(w).Encode(result)
}

func GetNews(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	var result Result
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
	result.Data = news
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
	result.Data = news
	_ = json.NewEncoder(w).Encode(result)
}
