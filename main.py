from fastapi import FastAPI


app = FastAPI()

def greet():
    return 'hello world'