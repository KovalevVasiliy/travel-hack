package main

import (
	"encoding/json"
	"fmt"
)

type CategoryId uint64
type LocationId uint64

type Category struct {
	Id   CategoryId `json:"category_id"`
	Name string     `json:"category_name"`
}

type SocialInfo struct {
	NumOfLikes uint64 `json:"likes" bson:"likes"`
	NumOfViews uint64 `json:"views" bson:"views"`
	IsLiked    bool   `json:"is_liked" bson:"is_liked"`
}

type NewsPreview struct {
	Title       string   `json:"title"`
	Description string   `json:"description"`
	Category    Category `json:"category"`
	SourceName  string   `json:"source_name"`
	Image       string   `json:"image"`
}

type Location struct {
	Name       string     `json:"name"`
	Id         LocationId `json:"location_id"`
	IsFavorite bool       `json:"is_favorite"`
	Images string `json:"images"`
}

type Content struct {
	Type    string      `json:"type"`
	Payload interface{} `json:"payload"`
}

type NewsStruct struct {
	Title       string      `json:"title"`
	Description string      `json:"description"`
	Preview     NewsPreview `json:"preview"`
	SocInfo     SocialInfo  `json:"social_info"`
	Contents    []Content   `json:"content"`
}

type NewsPreviewDB struct {
	Title       string     `json:"title" bson:"title"`
	Description string     `json:"description" bson:"description"`
	CategoryID  CategoryId `json:"category_id" bson:"category_id"`
	SourceName  string     `json:"source_name"  bson:"source_name"`
	Image       string     `json:"image" bson:"image"`
}

type ContentDB struct {
	Type    string `json:"type" bson:"type"`
	Payload string `json:"payload" bson:"payload"`
}

type NewsDB struct {
	Title       string        `json:"title" bson:"title"`
	Description string        `json:"description" bson:"description"`
	Preview     NewsPreviewDB `json:"preview"  bson:"preview"`
	SocInfo     SocialInfo    `json:"social_info" bson:"social_info"`
	Content     []ContentDB   `json:"content"  bson:"content"`
}

type IncomingCategory struct {
	Name string     `json:"name"`
	Id   CategoryId `json:"id"`
}

type IncomingLocation struct {
	Name string     `json:"object_title"`
	Id   LocationId `json:"id"`
}

type Result struct {
	Ok          bool        `json:"ok"`
	Description string      `json:"description"`
	Data        interface{} `json:"data"`
}

func (content *Content) MarshalJSON() ([]byte, error) {
	var buffer struct {
		Result map[string]string `json:"result"`
	}
	buffer.Result = make(map[string]string)

	buffer.Result["type"] = content.Type

	if content.Type == "location" {
		payload, err := json.Marshal(content.Payload.(Location))
		if err != nil {
			return nil, err
		}
		buffer.Result["payload"] = string(payload)
	} else {
		buffer.Result["payload"] = fmt.Sprintf("%v", content.Payload)
	}

	return json.Marshal(&buffer)
}
