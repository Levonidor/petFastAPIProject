To start application:

    Create .env file
        Put in .env:
        URL_DATABASE = "postgresql://{user}:{password}@{ip}:{port}/{database_name}"

    Start via terminal:
        uvicorn main:app --reload 

