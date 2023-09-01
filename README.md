# author-app-api
Documentation for the api is provided via Swagger 
http://127.0.0.1:8000/api/docs/

Steps to follow:
  -> Create a virtual env (Eg: python -m venv env)
  -> Activate virtual environment (Eg: venv\Scripts\activate)
  -> pip install -r requirements.txt
  -> python manage.py runserver

urls to check:
http://127.0.0.1:8000/api/docs/
1) First /api/user/create/   -- for creating an user
2) Generate token /api/user/token/
3) Authorize the token via clicking Authorize and then inside tokenAuth -- [[Token your_token]]
  
