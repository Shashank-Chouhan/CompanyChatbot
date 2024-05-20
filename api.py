from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, HTTPException
import os
import application as backend
import functions as fn
import db_connection as dbc

app = FastAPI()

class UserInput(BaseModel):
    message: str
class Login(BaseModel):
    username: str
    password: str


# Allow requests from specific origins
origins = [
    "http://127.0.0.1:5500",  # Update this with your frontend URL
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/message")
async def send_message(user_input: UserInput):
    message = user_input.message
    response = backend.generate_response(message)
    
    return {"message": response}

@app.post("/login")
async def login(login: Login):
    username = login.username
    password = login.password
    # if user in db then msg = logged in successfully else try again
    msg = "fail"
    if username == 'admin' and password == 'admin123' :
        msg =  "success"
    return {"message": msg}


@app.post("/fileupload")
async def upload_file(file: UploadFile = File(...)):
    # Check if file is uploaded
    if not file:
        return {"message": "No file provided"}
    
    # Save the uploaded file to disk
    with open(file.filename, "wb") as f:
        f.write(await file.read())

    return {"message": "File uploaded successfully ", "filename": file.filename}


@app.get("/createdb")
async def create_database():
    list_of_pdfs_in_cwd = fn.list_pdf_files() #[a.pdf, b.pdf]

    for pdf in list_of_pdfs_in_cwd:
        li = fn.pdf_to_qa_text(pdf)
        print('list created')
        r = fn.append_text_to_database(li)
        # delete that file here
        os.remove(pdf)

    return {"message": r}


@app.get("/showdb")
async def show_database():
    text = dbc.show_qadb()
    print('########')
    print(text)
    return text


class IdQuestionAnswerRequest(BaseModel):
    id: int
    question: str
    answer: str


@app.post("/editquestion")
async def edit_question(request_data: IdQuestionAnswerRequest):
    # Extract data from request
    id = request_data.id
    question = request_data.question
    answer = request_data.answer
    print(id, question, answer)

    dbc.create_connection()
    res = dbc.update_qa_tuple_from_table(id, question, answer)
    k = None
    if res == 200:
        k = {"id": id, "question": question, "answer": answer}
    return k


@app.delete("/deletequestion/{id}")
async def delete_question(id: int):
    print(id)
    dbc.create_connection()
    res = dbc.delete_qa_tuple_from_table(id)
    k = None
    if res == f"Question number {id} deleted successfully.":
        k = {"message": f"Question number {id} deleted successfully."}

    return k


@app.delete("/deleteWholeDB")
async def delete_whole_db():
    dbc.create_connection()
    res = dbc.delete_whole_table()
    print(res)
    return {"message": "Entire database deleted successfully!"}


class QuestionAnswerPair(BaseModel):
    question: str
    answer: str

@app.post("/addQAPair")
async def send_message(qa_pair: QuestionAnswerPair):
    question = qa_pair.question
    answer = qa_pair.answer
    qa_tuple = (question, answer)
    dbc.create_connection()
    res = dbc.add_qa_tuple_in_table(qa_tuple)
    k = None
    if res == 200:
        k = {"message": "Question Answer pair added successfully"}
    return k
