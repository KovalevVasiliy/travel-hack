FROM golang:alpine as builder

RUN apk update && apk add --no-cache git ca-certificates tzdata && update-ca-certificates

WORKDIR /opt/app

COPY /news-service/src .

RUN ls
RUN go get -d -v ./...
RUN go install -v ./...

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags='-w -s -extldflags "-static"' -a \
    -o /opt/app/bin/news-service .

FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /opt/app/bin/migreBot /opt/app/bin/migreBot

CMD ["/opt/app/bin/news-service"]