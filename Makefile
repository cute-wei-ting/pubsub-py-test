publish:
	pipenv run python publish.py
order-subscriber:
	pipenv run python pubsub-issue-1.py
no-order-subscriber:
	pipenv run python pubsub-issue-2-out-of-order.py
db:
	docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -d mysql
# gcloud auth application-default login 