package main

type URL string

type NewsStruct struct {
	Title string `json:"title"`
	Description string `json:"description"`
	Image URL `json:"image"`
}

type Result struct {
	Result      string `json:"result"`
	Description string `json:"description"`
	News []NewsStruct `json:"news"`
}

type SocialInfo struct {
	NumOfLikes uint64 `json:"likes"`
	NumOfViews uint64 `json:"views"`
	IsLiked bool `json:"isLiked"`
}

type Content struct {
	ContentType string `json:"content"`
}
