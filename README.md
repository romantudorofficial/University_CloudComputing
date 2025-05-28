# University - Cloud Computing


## Homework 1

### How to Run

- open console -> open project folder -> venv\Scripts\activate
- open http://localhost:8000/books
- open POSTMAN


## Homework 2

### How to Run

- backend folder -> venv\Scripts\activate -> pip install -r requirements.txt -> python app.py
- books_service folder -> python server.py
- frontend -> npm run serve
- http://localhost:8000/books
- http://localhost:5000/api/books
- open http://localhost:8081/ - the app is here


# Homework 3

### Details

- [Google Cloud Project Link](https://console.cloud.google.com/home/dashboard?invt=Abt8_w&project=proiect-cloudcomputing)
- Standard Environment
- 5 services
- maximum 2 can be Google Cloud API
- description of project: webpage which show famous YouTube videos and their description in many languages

- Important Details:

    - MySQL:

        - instance: homework3-db
        - password: homework3-db
        - databases:
            - videosite
        - users:
            - username: flaskuser
            - password: flaskuser
        - public ip address:
            - 34.118.52.224

    - Project ID:

        - proiect-cloudcomputing

- technologies used:

    - backend:
    
        - Python
        - Flask

    - frontend:
    
        - Vue.js

    - services:

        - general:

            - [Cloud SQL (Database Service - MySQL)](https://console.cloud.google.com/sql/choose-instance-engine?invt=Abt9Bg&project=proiect-cloudcomputing)
            - [Cloud Run (Backend Service, Deployment)](https://console.cloud.google.com/run?invt=Abt8_w&project=proiect-cloudcomputing)
            - [Firebase Hosting (Frontend Service)](https://console.cloud.google.com/firebase?invt=Abt9vw&project=proiect-cloudcomputing)
        
        - APIs:

            - [Cloud Translation API (Translation)](https://console.cloud.google.com/apis/library/translate.googleapis.com?invt=Abt9DA&project=skilled-mile-455515-t8)
            - [YouTube API (YouTube Video Insertion)](https://console.cloud.google.com/apis/library/youtube.googleapis.com?invt=Abt9HA&project=skilled-mile-455515-t8)


### How to Set Up

- install Node.js and npm
- install Python and pip
- install Google Cloud CLI, enter the consolde and sign in into the Google account
- install Firebase CLI: npm install -g firebase-tools
- make a Docker account and install Docker Desktop
- move to folder homework_3/backend and run in the terminal:
    - python -m venv venv
    - venv\Scripts\activate
    - pip install flask
    - pip install -r requirements.txt
    - docker build -t flask-backend .
    - docker run -p 5000:8080 flask-backend
    - open http://localhost:5000/
- move to folder homework_3/frontend and run in the terminal:
    - vue create .
    - npm run serve
    - open http://localhost:8081/
- go to https://console.cloud.google.com/sql
- move to folder homework_3/frontend and run in the terminal:
    - firebase login
    - firebase init hosting
    - npm run build
- move to backend:
    - gcloud builds submit --tag gcr.io/proiect-cloudcomputing/flask-app
    - gcloud run deploy flask-app --image gcr.io/proiect-cloudcomputing/flask-app --platform managed --region us-central1 --allow-unauthenticated
    - open https://flask-app-460494010492.us-central1.run.app
- move to frontend:
    - firebase deploy --only hosting
    - open https://proiect-cloudcomputing.web.app
- move to backend:
    - gcloud app deploy
    - open https://proiect-cloudcomputing.lm.r.appspot.com

### How to Run

- go to homework_3/backend and run:
    - venv\Scripts\activate
    - docker run -p 5000:8080 flask-backend
    - open http://localhost:5000/
- go to homework_3/frontend and run:
    - npm run serve


### To Do

- the tutorials from the standard environment
- install Google Cloud CLI



# Homework 4

## Details

- Azure Subscription ID: 15bf7f47-96e2-4be2-8464-0beade54756b
- Server Name: sql-booklib-ne.database.windows.net
- Server User: myadmin
- Server Password: p67ff3!!
- Database: db_booklib
- Storage account name: booklibstorage
- Resource Group Name: rg-booklib

- Services:
    - Azure Blob Storage: for storing images about the books

- Login to Azure: az login
- az account list --output table

- Activate venv in backend: .\venv\Scripts\Activate.ps1
- Run Backend: python app.py
- Run Backend: http://localhost:5000/books, http://127.0.0.1:5000/

- Run Frontend: enter booklib and "npm run dev"
- Run FrontEnd: http://localhost:5173/



# Homework 5

## Details

- [Google Docs](https://docs.google.com/document/d/1L7iReFzSX7P0EVzTikkht936jbWATc_edEz8Oukzf7M/edit?tab=t.0#heading=h.kpzdaztrb40i)
- [Google Forms](https://docs.google.com/forms/d/1_7UPnVG13WCS6NKMq6XNo0OmozkR8YxadX8SzsblLTY/edit)
- [Canva Business Canvas](https://www.canva.com/design/DAGnVVVxPO0/E8essRQE8k-k2am5-I91bg/edit?utm_content=DAGnVVVxPO0&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)



# Project

## Details

- cloud platform: Azure
- Technologies: Azure, JavaWebToken
- resource group name: projectCC
- MySQL flexible server (all databases):
    - name: db-server-cc 
    - administrator login: adminsql
    - password: adminsql25!
    - estimated cost: USD 17/month
- API Management service:
    - name: apim-projectcc
    - org name: team
    - pricing tear: Developer
- Application Service Plan:
    - name: plan-projectcc
    - os: linux
    - pricing plan: Basic B1
- WebApp for every microservice:
    - authentication service web app:
        - name: auth-service-cc
        - runtime stack: Python 3.12
        - db for authentication service:
            - name: authdb
            - char set: utf8
            - collation: utf8_general_ci
    - events service webapp:
        - name: events-service
        - runtime stack: Python 3.12
        - db for events service:
            - name: eventsdb
            - char set: utf8
            - collation: utf8_general_ci
    - centralize sport fields service
    - authorization service
    - manual verification service
- JavaWebToken:
    - secret: iFrnhMbRyUn02DjHydSNqmGhrHY4S_5JAU9RkLKtYdXI26KxKsXcj-999ms8u5tC
- types of users:
    - simple
    - owner
- connection strings:
Connection string for authdb:
Server=db-server-cc.mysql.database.azure.com;
Database=authdb;
User ID=adminsql@db-server-cc;
Password=adminsql25!;
SslMode=Required;

Connection string for eventsdb:
Server=db-server-cc.mysql.database.azure.com;
Database=eventsdb;
User ID=adminsql@db-server-cc;
Password=adminsql25!;
SslMode=Required;