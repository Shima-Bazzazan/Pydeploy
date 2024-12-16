import io
import cv2
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from fastapi.responses import StreamingResponse

app = FastAPI()

class ParentInfo(BaseModel):
    name: str
    
class DidYouKnow(BaseModel):
    fact: str

class ExternalResource(BaseModel):
    name: str
    url: HttpUrl
    description: Optional[str] = None
   
class Character(BaseModel):
    id: int
    name: str
    origin: str
    role: str
    description: str
    father: Optional[ParentInfo] = None
    mother: Optional[ParentInfo] = None
    did_you_know: Optional[List[DidYouKnow]] = None

class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    

external_resources = [
    {
        "name": "Divanesaz store",
        "url": "https://divanesaz.com/",
        "description": "Buy books, accessories, and products related to the world of Harry Potter"
        
    }
]

characters = [
    {
        "id": 1,
        "name": "Harry James Potter",
        "origin": "Gryffindor",
        "role": "Student",
        "description": "The Boy Who Lived, known for courage and loyalty.",
        "father": {"name": "James Potter"},
        "mother": {"name": "Lily Potter"},
        "did_you_know": [
            {"fact": "Harry was the only known wizard to survive the Killing Curse as a baby, making him famous even before he arrived at Hogwarts."},
        ],
    },
    {
        "id": 2,
        "name": "Hermione Jean Granger",
        "origin": "Gryffindor",
        "role": "Student",
        "description": "One of Harry Potter's best friends, the brightest witch of her age, who excels in academics and is known for her intelligence, bravery, and resourcefulness.",
        "father": {"name": "Mr. Granger"},
        "mother": {"name": "Mrs. Granger"},
        "did_you_know": [
            {"fact": "Hermione was Muggle-born and outperformed most pure-bloods at Hogwarts. She played a critical role in the fight against Lord Voldemort."},
        ],
    },
    {
        "id": 3,
        "name": "Ronald Bilius Weasley",
        "origin": "Gryffindor",
        "role": "Student",
        "description": "Harry's loyal best friend, known for his sense of humor and unwavering support, who grows into a confident and reliable ally.",
        "father": {"name": "Arthur Weasley"},
        "mother": {"name": "Molly Weasley"},
        "did_you_know": [
            {"fact": "Ron, coming from a loving but modest family, provided Harry with emotional support and friendship crucial for their journey."},
        ],
    },
    {
        "id": 4,
        "name": "Albus Percival Wulfric Brian Dumbledore",
        "origin": "Gryffindor",
        "role": "Headmaster of Hogwarts",
        "description": "A legendary wizard, mentor to Harry, known for wisdom, kindness, and complexity. Guided the Wizarding World through tumultuous times.",
        "father": {"name": "Percival Dumbledore"},
        "mother": {"name": "Kendra Dumbledore"},
        "did_you_know": [
            {"fact": "Dumbledore was the only wizard Voldemort truly feared. His strategic planning was key in Voldemort's downfall."},
        ],
    },
    {
        "id": 5,
        "name": "Severus Snape",
        "origin": "Slytherin",
        "role": "Potions Master, Professor, Head of Slytherin, Headmaster",
        "description": "A complex character, initially seeming antagonistic but ultimately revealed as brave and self-sacrificing, secretly protecting Harry.",
        "father": {"name": "Tobias Snape"},
        "mother": {"name": "Eileen Snape"},
        "did_you_know": [
            {"fact": "Snape's love for Lily Potter influenced his actions. He served as a double agent, crucial in Voldemort's defeat."},
        ],
    },
     {
        "id": 6,
        "name": "Tom Marvolo Riddle (Lord Voldemort)",
        "origin": "Slytherin",
        "role": "Dark Lord",
        "description": "The main antagonist of the series, a power-hungry and cruel Dark wizard who sought to dominate the Wizarding World.",
        "father": {"name": "Tom Riddle Sr"},
        "mother": {"name": "Merope Gaunt"},
        "did_you_know": [
            {"fact": "Voldemort created multiple Horcruxes to evade death. His obsession with blood purity defined his terror."},
        ],
    },
    {
        "id": 7,
        "name": "Neville Longbottom",
        "origin": "Gryffindor",
        "role": "Student, later Herbology Professor",
        "description": "A shy boy who gradually found courage, becoming a hero and playing a key role in the final battle against Voldemort.",
        "father": {"name": "Frank Longbottom"},
        "mother": {"name": "Alice Longbottom"},
        "did_you_know": [
            {"fact": "Neville destroyed one of Voldemort's Horcruxes. His journey shows how perseverance can bloom into true bravery."},
        ],
    },
    {
        "id": 8,
        "name": "Draco Lucius Malfoy",
        "origin": "Slytherin",
        "role": "Student",
        "description": "A pure-blood wizard from a wealthy family, often antagonistic towards Harry and friends, known for arrogance and prejudice.",
        "father": {"name": "Lucius Malfoy"},
        "mother": {"name": "Narcissa Malfoy"},
        "did_you_know": [
            {"fact": "Despite his early cruelty, Draco showed doubt in serving Voldemort. He never fully embraced evil as many feared."},
        ],
    },
]


books = [
    {
        "id": 1,
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J.K. Rowling",
        "description": "The first book in the Harry Potter series tells the story of a new beginning for Harry and his friends.",
    },
    {
        "id": 2,
        "title": "Harry Potter and the Chamber of Secrets",
        "author": "J.K. Rowling",
        "description": "In the second book, Harry faces dark secrets and the Chamber of Secrets.",
    },
    {
        "id": 3,
        "title": "Harry Potter and the Prisoner of Azkaban",
        "author": "J.K. Rowling",
        "description": "Harry encounters the escaped prisoner Sirius Black in the third book.",
    },
    {
        "id": 4,
        "title": "Harry Potter and the Goblet of Fire",
        "author": "J.K. Rowling",
        "description": "In the fourth book, Harry participates in the Triwizard Tournament and faces new dangers.",
    },
    {
        "id": 5,
        "title": "Harry Potter and the Order of the Phoenix",
        "author": "J.K. Rowling",
        "description": "Harry faces the rise of Voldemort's power and the formation of the Order of the Phoenix in the fifth book.",
    },
    {
        "id": 6,
        "title": "Harry Potter and the Half-Blood Prince",
        "author": "J.K. Rowling",
        "description": "In the sixth book, Harry discovers the secrets of Voldemort's past and faces new dangers.",
    },
    {
        "id": 7,
        "title": "Harry Potter and the Deathly Hallows",
        "author": "J.K. Rowling",
        "description": "The seventh book, which narrates the end of the Harry Potter series and depicts the final battle with Voldemort.",
    },
]

@app.get("/")
def root():
    return "Welcome To Harry Potter API"

@app.get("/characters", response_model=List[Character])
def get_characters():
    return characters

@app.get("/characters/{character_id}", response_model=Character)
def get_character(character_id: int):
    for character in characters:
        if character["id"] == character_id:
            return character
    raise HTTPException(status_code=404, detail="Personality not found!")

@app.get("/{character_id}/image")                
def image(character_id):
    if character_id == "1":
        image = cv2.imread("images/Harry.jpg")
        _, encoded_image = cv2.imencode(".png", image)
        return StreamingResponse(io.BytesIO(encoded_image.tobytes()), media_type = "image/jpg")
    
    elif character_id == "2":
        image = cv2.imread("images/Hermione.jpg")
        _, encoded_image = cv2.imencode(".png", image)
        return StreamingResponse(io.BytesIO(encoded_image.tobytes()), media_type = "image/jpg")
    
    elif character_id == "3":
        image = cv2.imread("images/Ronald.jpg")
        _, encoded_image = cv2.imencode(".png", image)
        return StreamingResponse(io.BytesIO(encoded_image.tobytes()), media_type = "image/jpg")
    
    elif character_id == "4":
        image = cv2.imread("images/Albus_Dumbledore.jpg")
        _, encoded_image = cv2.imencode(".png", image)
        return StreamingResponse(io.BytesIO(encoded_image.tobytes()), media_type = "image/jpg")
    
    elif character_id == "5":
        image = cv2.imread("images/Severus_Snape.jpg")
        _, encoded_image = cv2.imencode(".png", image)
        return StreamingResponse(io.BytesIO(encoded_image.tobytes()), media_type = "image/jpg")
    
    elif character_id == "6":
        image = cv2.imread("images/Lord_Voldemort.jpg")
        _, encoded_image = cv2.imencode(".png", image)
        return StreamingResponse(io.BytesIO(encoded_image.tobytes()), media_type = "image/jpg")
    
    elif character_id == "7":
        image = cv2.imread("images/Neville.jpg")
        _, encoded_image = cv2.imencode(".png", image)
        return StreamingResponse(io.BytesIO(encoded_image.tobytes()), media_type = "image/jpg")
    
    elif character_id == "8":
        image = cv2.imread("images/Draco.jpg")
        _, encoded_image = cv2.imencode(".png", image)
        return StreamingResponse(io.BytesIO(encoded_image.tobytes()), media_type = "image/jpg")
    
    else:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
                            detail = "Just enter the ID number of the desired character.")


@app.get("/books", response_model=List[Book])
def get_books():
    return books

@app.get("/external-resources", response_model=List[ExternalResource])
def get_external_resources():
    return external_resources
