package main

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func getNewsFromDB(db *mongo.Database) ([]*NewsStruct, error) {
	findOptions := options.Find()
	collection := db.Collection("collection")
	var newsStruct []*NewsStruct
	cur, err := collection.Find(context.TODO(), bson.D{{}}, findOptions)
	if err != nil {
		log.Fatal(err)
	}

	for cur.Next(context.TODO()) {
		var elem NewsDB
		err := cur.Decode(&elem)
		log.Println("Error loading category for news. ID:", elem.Preview.CategoryID, ", error: ", err)
		if err != nil {
			log.Print(err)
		}
		category, err := getCategoryById(elem.Preview.CategoryID)
		if err != nil {
			log.Println("Error loading category for news. ID:", elem.Preview.CategoryID, ", error: ", err)
			return []*NewsStruct{}, err
		}
		var contents []Content = make([]Content, len(elem.Content))
		for index, contentDB := range elem.Content {
			contents[index] = Content{Type: contentDB.Type}
			if contentDB.Type == "location" {
				id, err := strconv.Atoi(contentDB.Payload)
				if err != nil {
					log.Println("Error converting payload to category_id for news. ID:", contentDB.Payload, ", error: ", err)
					return []*NewsStruct{}, err
				}

				locationId := LocationId(id)
				content, err := getLocationById(locationId)
				if err != nil {
					log.Println("Error loading location for news. ID:", locationId, ", error: ", err)
					return []*NewsStruct{}, err
				}
				contents[index].Payload = content
			} else {
				contents[index].Payload = contentDB.Payload
			}
		}
		newELem := NewsStruct{
			Id:          elem.Id,
			Title:       elem.Title,
			Description: elem.Description,
			Preview: NewsPreview{
				Title:       elem.Preview.Title,
				Description: elem.Preview.Description,
				SourceName:  elem.Preview.SourceName,
				Image:       elem.Preview.Image,
				Category:    category,
			},
			SocInfo:  elem.SocInfo,
			Contents: contents,
		}

		newsStruct = append(newsStruct, &newELem)
	}
	return newsStruct, nil
}

func getNewsFromDBById(db *mongo.Database, id uint64) (NewsStruct, error) {
	collection := db.Collection("collection")

	newsDB := &NewsDB{}
	result := collection.FindOne(nil, bson.M{"id": id})
	err := result.Decode(newsDB)
	if err != nil {
		log.Println("Error loading news from db. ID:", id, ", error: ", err)
		return NewsStruct{}, err
	}

	category, err := getCategoryById(newsDB.Preview.CategoryID)
	if err != nil {
		log.Println("Error loading category for news. ID:", newsDB.Preview.CategoryID, ", error: ", err)
		return NewsStruct{}, err
	}

	var contents []Content = make([]Content, len(newsDB.Content))
	for index, contentDB := range newsDB.Content {
		contents[index] = Content{Type: contentDB.Type}
		if contentDB.Type == "location" {
			id, err := strconv.Atoi(contentDB.Payload)
			if err != nil {
				log.Println("Error converting payload to category_id for news. ID:", contentDB.Payload, ", error: ", err)
				return NewsStruct{}, err
			}

			locationId := LocationId(id)
			content, err := getLocationById(locationId)
			if err != nil {
				log.Println("Error loading location for news. ID:", locationId, ", error: ", err)
				return NewsStruct{}, err
			}

			contents[index].Payload = content
		} else {
			contents[index].Payload = contentDB.Payload
		}
	}

	return NewsStruct{
		Id:          newsDB.Id,
		Title:       newsDB.Title,
		Description: newsDB.Description,
		Preview: NewsPreview{
			Title:       newsDB.Preview.Title,
			Description: newsDB.Preview.Description,
			SourceName:  newsDB.Preview.SourceName,
			Image:       newsDB.Preview.Image,
			Category:    category,
		},
		SocInfo:  newsDB.SocInfo,
		Contents: contents,
	}, nil
}

var categoryIdMap = map[CategoryId]Category{}
var locationIdMap = map[LocationId]Location{}

func getLocationById(id LocationId) (location Location, err error) {
	location = locationIdMap[id]

	if location.Name == "" {
		url := fmt.Sprintf("http://postgrest:3000/gotorussia_travels_locations?id=eq.%d", id)
		resp, err := http.Get(url)
		if err != nil {
			log.Print("getLocationById GET error", err)
			return location, err
		}

		var incomingLocations []IncomingLocation
		err = json.NewDecoder(resp.Body).Decode(&incomingLocations)
		if err != nil {
			log.Print("getLocationById Decoding error ", err)
			return location, err
		}

		if len(incomingLocations) != 0 {
			var incomingLocation = incomingLocations[0]
			location = Location{Name: incomingLocation.Name, Id: incomingLocation.Id}
			locationIdMap[id] = location
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

func getCategoryById(id CategoryId) (category Category, err error) {
	category = categoryIdMap[id]

	if category.Name == "" {
		url := fmt.Sprintf("http://postgrest:3000/gotorussia_types_category?id=eq.%d", id)
		resp, err := http.Get(url)
		if err != nil {
			log.Print("getCategoryById GET error", err)
			return category, err
		}

		var incomingCategories []IncomingCategory
		err = json.NewDecoder(resp.Body).Decode(&incomingCategories)
		if err != nil {
			log.Print("getCategoryById Decoding error ", err)
			return category, err
		}

		if len(incomingCategories) != 0 {
			var incomingCategory = incomingCategories[0]
			category = Category{Name: incomingCategory.Name, Id: incomingCategory.Id}
			categoryIdMap[id] = category
			log.Printf("getCategoryById return from server name: %s , %d: ", category.Name, category.Id)
		} else {
			log.Print("getCategoryById return from server is null")
			return category, errors.New("no such category")
		}
	} else {
		log.Printf("getCategoryById return from cache name: %s , %d: ", category.Name, category.Id)
	}
	return category, nil
}

func GetNews(db *mongo.Database, w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	result := Result{
		Ok: true,
	}
	log.Print("getNewsFromDB before")
	news, err := getNewsFromDB(db)
	log.Print("getNewsFromDB fater")
	if err != nil {
		result := Result{
			Ok:          false,
			Description: "nil id",
		}
		_ = json.NewEncoder(w).Encode(result)
		return
	}

	result.Data = news

	_ = json.NewEncoder(w).Encode(result)
}

func GetNewsById(db *mongo.Database, w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	id, err := strconv.Atoi(params["id"])
	result := Result{
		Ok: true,
	}

	if err != nil {
		result := Result{
			Ok:          false,
			Description: "nil id",
		}
		_ = json.NewEncoder(w).Encode(result)
		return
	}

	news, err := getNewsFromDBById(db, uint64(id))
	if err != nil {
		result := Result{
			Ok:          false,
			Description: "nil id",
		}
		_ = json.NewEncoder(w).Encode(result)
		return
	}

	result.Data = news

	_ = json.NewEncoder(w).Encode(result)
}
