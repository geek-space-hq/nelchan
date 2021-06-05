NAME:=nelchan

build: 
	docker build -t $(NAME):main -f ./docker/Dockerfile .

restart: 
	stop start

start: 
	docker run -it --env-file .env $(NAME):main