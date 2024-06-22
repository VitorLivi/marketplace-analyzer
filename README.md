# Marketplace Analyzer

The project was developed to aggregate data, create metrics, and send alerts to marketplace owners. It aims to improve their profits by analyzing the following: the number of customers making purchases, the busiest month for customers, the most popular day of the week, the frequency of visits by specific customers, the time spent in the marketplace, whether customers make purchases, and the ability to detect incidents involving weapons and suspicious individuals.

## How to start the project

- To start a mongoDB instance into your machine, run the command on the root project folder:

```
docker compose up
```

- Run the shell script to setup crons

```
sh /deploy/setup_crons.sh 
```

- Start project

```
python main.py
```

#### Technology
- Python
- Yolo
- Cv2
- MongoDB

#### Features
- Face recognition
- Weapon Recognition
- Data aggregation
- Local image storing

### People Detection

https://github.com/VitorLivi/marketplace-analyzer/assets/44207509/50b9f84c-a803-49d4-995a-5bd6a9a93b8a


### Weapon Detection

https://github.com/VitorLivi/marketplace-analyzer/assets/44207509/80fcc06a-6ea9-426f-bf64-240d3f9f6a97

### Database Aggregated Data

#### Day Client
![image](https://github.com/VitorLivi/marketplace-analyzer/assets/44207509/6db47a04-a29a-4694-b574-2af147c77849)

#### Monthly Client

![image](https://github.com/VitorLivi/marketplace-analyzer/assets/44207509/b72bf9e5-84fc-4f69-af75-b9f330eacb53)


### How it works

It gets frame by frame, applies the Yolo recognition model and the weapon recognition model separately, crops the person images, and stores them in a temp directory, an example bellow:

![1c186d3f-c965-4bf6-a0a8-aecf7bee1d90](https://github.com/VitorLivi/marketplace-analyzer/assets/44207509/c3b42c4e-a891-4e7c-9c46-15b31eff1319)

And then, in the next frame, it does again the same behavior but now it compares the images with face recognition and removes one of them if is similar. When the person exits from the frame for more than "x" number of seconds, it saves the person into database with metrics and saves the temp image into a "month/day/uuid" folder so we can get database information by the image and vice-versa.

It also has two cron jobs that aggregate data and are deployed using shell script, one to aggregate weekly analytics information and the other to aggregate monthly ones.

### Needs to be improved

- A better way to store images.
- A way to call the police or emit a physical alert when an incident happens.
- Improve code readability.
- Put everything in the project inside docker.
- Support real-world ip cam connection.


