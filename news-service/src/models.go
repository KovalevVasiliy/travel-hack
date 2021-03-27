package main

type URL string
type CategoryId uint64

type NewsStruct struct {
	Title string `json:"title"`
	Description string `json:"description"`
	SocInfo SocialInfo `json:"social_info"`
	Contents []Content `json:"contents"`
	Categories []CategoryId `json:"categories"`
}

type ResultMany struct {
	Result      string `json:"result"`
	Description string `json:"description"`
	News []NewsStruct `json:"news"`
}

type Result struct {
	Result      string `json:"result"`
	Description string `json:"description"`
	News NewsStruct `json:"news"`
}

type SocialInfo struct {
	NumOfLikes uint64 `json:"likes"`
	NumOfViews uint64 `json:"views"`
	IsLiked bool `json:"is_liked"`
}

type Content struct {
	ContentType string `json:"content"`
}
