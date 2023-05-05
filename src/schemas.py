from pydantic import BaseModel, Field

class LoginCredetials(BaseModel):
    username: str
    password: str

class GetTaskSchema(BaseModel):
    username: str

class TaskSchema(BaseModel):
    id: str
    text: str
    type: str
    subject: str
    paragraph: int
    totalParagraphs: int
    question: int = None
    totalQuestions: int = None