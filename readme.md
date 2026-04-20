# Step 1: Kafka Installation process
`wget https://downloads.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz`   # install from terminal 

`tar -xvzf kafka_2.13-3.7.0.tgz`  # extract tar file

# kafka server running process 
cd kafka_2.13-3.7.0 # change directory

::: cd /Downloads/kafka_2.13-3.7.0
1 . ON Kafka server zookeeper

# Main Machine 
::: `bin/zookeeper-server-start.sh config/zookeeper.properties`

Then on Kafka Broker:
# Main Machine 
::: `bin/kafka-server-start.sh config/server.properties`



# ################33
Install ollama 
then do ///ollama pull mistral ///  then /// ollama run mistral 


# . then Create topic for indivisual domain on Main server 

# Main Machine 
`bin/kafka-topics.sh --create --topic physics_topic --bootstrap-server localhost:9092`
`bin/kafka-topics.sh --create --topic math_topic --bootstrap-server localhost:9092`
`bin/kafka-topics.sh --create --topic biology_topic --bootstrap-server localhost:9092`
#  Check Which topic is created till now 
bin/kafka-topics.sh --list --bootstrap-server localhost:9092


# install packages in main server machine then run "Check_install_packages.py" to check installed properly or not
`pip install fastapi uvicorn jinja2 kafka-python requests `




3. Then on dfffernet domain on different computer 


# Machine 1 
`cd Math_server `
`python3 consumer.py`
# Install following packages on domain machine 
`pip install kafka-python requests`  # install packages in domain server machine then run "Check_install_packages.py" to check installed properly or not


# set main machine ip in each machine 

# Machine 2
`cd Physics_server `
`python3 consumer.py`

Ste4 .  Run Main server 
# Main Machine as
uvicorn app:app --port 8000 --reload    ## this is for query ask from terminal
uvicorn app1:app --port 8000           ## this is for query ask from UI

# Using webhook 
`uvicorn webhook:app --host 0.0.0.0 --port 8000`

5. Ask Query 
# Main Machine 

curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d '{"query":"Derivative of x^2"}'
