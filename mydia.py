from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.analytics import Spark
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka,RabbitMQ
from diagrams.aws.database import Redshift
from diagrams.onprem.database import Postgresql, MySQL, Oracle, Cassandra
from diagrams.azure.database import SQLServers,CacheForRedis,DatabaseForPostgresqlServers
from diagrams.azure.compute import VM, AppServices
from diagrams.onprem.container import Docker
from diagrams.azure.analytics import DataLakeStoreGen1,SynapseAnalytics
from diagrams.onprem.compute import Server
from diagrams.onprem.analytics import Hive
from diagrams.onprem.search import Solr
from diagrams.onprem.security import Vault
from diagrams.saas.cdn import Cloudflare
from diagrams.azure.network import LoadBalancers,ApplicationGateway
from diagrams.custom import Custom
from diagrams.azure.compute import ContainerInstances
from diagrams.generic.database import SQL
from diagrams.programming.language import C,JavaScript
from diagrams.programming.flowchart import Document
from diagrams.aws.storage import SimpleStorageServiceS3Bucket
from diagrams.onprem.client import Users
from diagrams.azure.identity import ActiveDirectory
from diagrams.gcp.network import LoadBalancing
from diagrams.aws.storage import SimpleStorageServiceS3Bucket
from diagrams.aws.storage import SimpleStorageServiceS3Object
from diagrams.aws.storage import S3GlacierArchive
from diagrams.aws.storage import S3GlacierVault
from diagrams.aws.storage import S3Glacier
from diagrams.aws.storage import SimpleStorageServiceS3BucketWithObjects
from diagrams.aws.storage import Storage

graph_attr = {
    "fontsize": "45",
    "bgcolor": "white"
}

with Diagram(name="AbbVie Architucture",direction="TB",graph_attr=graph_attr):
    
    users = Users("Users")
    vpn = ApplicationGateway("VPN")
   

    with Cluster("On Prem"):
        with Cluster("Cloudera Cluster"):
            hive = Hive("Hive")
            sources = [hive]
            


    with Cluster("AWS"):
        s3Glacier = S3Glacier("Compressed S3 files")    

        with Cluster("EC2-Machine2"):
                ingestion = Spark("Ingestion Job")
                profile = Spark("Profile Job")
                index = Spark("Index Job")
                engine = [ingestion - profile -index]


        with Cluster("EC2-Machine1"):
            metadata = DatabaseForPostgresqlServers("Nabu Metadata")
            apiServer = Server("HTTP API Server")
            scheduler = AppServices("scheduler")
            templateService = AppServices("template service")
            crawlers = AppServices("crawlers")
            bots = ContainerInstances("BotWorks")
            kafka = Kafka("Kafka")
            solr = Solr("Solr")
            mqtt = RabbitMQ("MQTT")
            ui = Cloudflare("Web UI")
            vault = Vault("Vault")
            bots >> Edge() << kafka
            bots >> Edge() << metadata
            bots >> mqtt
            crawlers >> mqtt
            metadata >> Edge() << apiServer 
            ui >> Edge()  >> Edge(label="Access Nabu UI") << users
            metadata >> Edge() << crawlers
            metadata >> scheduler
            scheduler >> Edge() << kafka
            templateService << metadata
            templateService >> Edge() << apiServer
          
            
            apiServer >> Edge() << solr
            apiServer >> Edge() << vault
            

    
    
        
            
            
    bots >> Edge(label="BotWorks are lightweight units \nthat orchestrate Apache Spark\njobs execution\n\n\n\n\n",style="dashed",color="brown") >> ingestion
    index >> solr
    profile >> metadata
    s3Glacier >> Edge(style="dashed") >> ingestion
    engine >> vpn >> hive
    
    s3Glacier >> crawlers
   
    
    
    
    
    
    
    