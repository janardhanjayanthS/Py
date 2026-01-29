RUN CMD: 


- Run opensearch as a docker container

````
sudo docker run -d -p 9200:9200 -p 9600:
9600   -e "discovery.type=single-node"   -e "DISABLE_SECURITY_PLUGIN=true"   
-e "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m"   --name opensearch-no-security  
 opensearchproject/opensearch:latest
 ```bash


 - Then execute main.py
