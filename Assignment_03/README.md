
# Harry Potter API⚡

This API allows you to explore the magical world of Harry Potter to some extent.
The API has been deployed here:

https://pydeploy-jncz.onrender.com
  
## How to install  
```
pip install -r requirements.txt
```  

### How to Run  
First you need to run this commnad in terminal to start the api 
```
uvicorn main:app
```  
The base URL of the API endpoints is: 127.0.0.1:8000  

### Endpoints:
1 - 127.0.0.1:8000/characters 

This endpoint provides a list of 8 prominent characters from the Harry Potter series along with their details.

1. Harry James Potter
2. Hermione Jean Granger
3. Ronald Bilius Weasley
4. Albus Percival Wulfric Brian Dumbledore
5. Severus Snape
6. Tom Marvolo Riddle (Lord Voldemort)
7. Neville Longbottom
8. Draco Lucius Malfoy

2 - 127.0.0.1:8000/characters/{character_id}

Instead of "characters" you can enter the ID of any character to retrieve the description of that character.

Example :  
```
127.0.0.1:8000/characters/2
```
3 - 127.0.0.1:8000/{character_id}/image

Instead of using "characters," you can enter any "character_id," and it will display the corresponding image.

Example : 
```
127.0.0.1:8000/5/image
```  
<img src="images\Severus_Snape.jpg" width="200">

```
127.0.0.1:8000/6/image
```  
<img src="images\Lord_Voldemort.jpg" width="300">

4 - 127.0.0.1:8000/books

This endpoint provides the Harry Potter book series.

5 - 127.0.0.1:8000/external-resources

This endpoint introduces the "Dementor" website.
your ultimate destination for the Harry Potter book series, accessories, and other magical items!

