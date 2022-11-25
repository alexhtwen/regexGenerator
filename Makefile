up:
	docker-compose -f docker-compose.yml up
upd:
	docker-compose -f docker-compose.yml up -d
down:
	docker-compose -f docker-compose.yml down
rmi:
	docker rmi regex_generator-image
exec:
	docker exec -it regex_generator-container bash
