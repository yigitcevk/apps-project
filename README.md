# apps-project

- git clone
- docker-compose build
- docker-compose up
- http://localhost:3000/dashboard


### Kullanılan Teknolojiler

1. https://fastapi.tiangolo.com/, https://fastapi.tiangolo.com/tutorial/sql-databases/ (PostgreSQL)
2. https://vuejs.org/
3. https://www.docker.com/

TOKEN = "2906bad1fa1ee07630bf4029750872eda6a5c0e3b118cf5a"

app.post campaign is not implemented because its not mentioned.
could be added with : 
insert into campaigns (id, service_campaign_id, title, active, created_at)
values (157354267, 576423485, 'campaign1', true, '2000-07-23 18:10:25-07');
