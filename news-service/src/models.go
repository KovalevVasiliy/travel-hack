package main

type CategoryId uint64
type LocationId uint64

type NewsStruct struct {
	Title string `json:"title"`
	Description string `json:"description"`
	SocInfo SocialInfo `json:"social_info"`
	Contents []Content `json:"contents"`
	Categories []CategoryId `json:"categories"`
}

type Category struct {
	Id CategoryId `json:"category_id"`
	Name string `json:"category_name"`
}

type Location struct {
	Name      string `json:"name"`
	Id LocationId `json:"location_id"`
	IsFavorite bool `json:"is_favorite"`
}

type Result struct {
	Result      string `json:"result"`
	Description string `json:"description"`
	Data interface{} `json:"data"`
}

type SocialInfo struct {
	NumOfLikes uint64 `json:"likes"`
	NumOfViews uint64 `json:"views"`
	IsLiked bool `json:"is_liked"`
}

type Content struct {
	ContentType string `json:"content"`
}
