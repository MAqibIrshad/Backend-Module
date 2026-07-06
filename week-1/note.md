I have initialized a simple empty array named tasks
Then I import BaseModel from pydantic to validate request and response ie., TaskRequest, TaskResponse
Then I make a simple POST end point "/create-task". with reponse model as TaskResponse and Request model as TaskRequest
I also import status and HTTP Exception from fastapi module.
Then i make a simple get endpoint to get all tasks in array
Then i make another endpoint to get task by id
Lastly, I also made /task/search query parameter adjusted in end point url to search task by name