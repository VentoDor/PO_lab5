from locust import HttpUser, task

class WebsiteUser(HttpUser):
    host = "http://localhost:8080"  # Укажите правильный хост вашего сервера

    @task
    def index_page(self):
        self.client.get("/")

    @task
    def page2(self):
        self.client.get("/page2.html")