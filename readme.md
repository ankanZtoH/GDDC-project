
Run these 2 command in 
::: cd /Downloads/kafka_2.13-3.7.0
1 . ON Kafka server zookeeper
# Main Machine 
::: bin/zookeeper-server-start.sh config/zookeeper.properties

Then on Kafka Broker:
# Main Machine 
::: bin/kafka-server-start.sh config/server.properties

2 . then Create topic for indivisual domain on Main server 

# Main Machine 
bin/kafka-topics.sh --create --topic physics_topic --bootstrap-server localhost:9092
bin/kafka-topics.sh --create --topic math_topic --bootstrap-server localhost:9092
bin/kafka-topics.sh --create --topic biology_topic --bootstrap-server localhost:9092



3. Then on dfffernet domain on different computer 


# Machine 1 
cd Math_server 
python3 consumer.py
# Install following packages
'pip install kafka-python requests'

# set main machine ip in each machine 

# Machine 2
cd Physics_server 
python3 consumer.py




4 .  Run Main server 
# Main Machine as
uvicorn app:app --port 8000 --reload


5. Ask Query 
# Main Machine 

curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d '{"query":"Derivative of x^2"}'


