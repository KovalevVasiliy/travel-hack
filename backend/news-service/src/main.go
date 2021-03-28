package main

import (
	"log"
	"net/http"
	"os"
	"time"

	"context"

	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type App struct {
	Router *mux.Router
	DB     *mongo.Database
}

var ctx = context.TODO() // actually TODO

type RequestHandlerFunction func(db *mongo.Database, w http.ResponseWriter, r *http.Request)

func (app *App) handleRequest(handler RequestHandlerFunction) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		handler(app.DB, w, r)
	}
}

func main() {
	mongoURI := os.Getenv("APP_MONGO_URI")
	dbName := os.Getenv("APP_MONGO_DB")
	log.Println("Connecting to", dbName)

	headersOk := handlers.AllowedHeaders([]string{"X-Requested-With"})
	originsOk := handlers.AllowedOrigins([]string{"*"})
	methodsOk := handlers.AllowedMethods([]string{"GET", "HEAD", "POST", "PUT", "OPTIONS"})

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	client, err := mongo.Connect(ctx, options.Client().ApplyURI(mongoURI))
	if err != nil {
		log.Fatalf("Error while connecting to mongo: %v\n", err)
	}

	app := App{DB: client.Database(dbName), Router: mux.NewRouter()}

	app.Router.HandleFunc("/news/all", app.handleRequest(GetNews)).Methods("GET")
	app.Router.HandleFunc("/news/{id}", app.handleRequest(GetNewsById)).Methods("GET")
	log.Fatal(http.ListenAndServe(":8000", handlers.CORS(originsOk, headersOk, methodsOk)(app.Router)))
}
