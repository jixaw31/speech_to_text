
# how to run locally
First clone this repo by using following command
````

git clone https://github.com/sajtj/speech-to-text.git

````
then 
````
cd speech-to-text

````
then set the .env file
````
OPENAI_API_KEY=your-openai-api-ky
````
then install the requirements
````
pip install -r requirements.txt
````
run the APIs
````
cd API/
uvicorn main:app --reload --host 0.0.0.0 --port 8000
````
test the APIs
````
cd frontend/
streamlit run app.py
````
