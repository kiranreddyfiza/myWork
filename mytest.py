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
from diagrams.aws.management import Cloudwatch
from diagrams.aws.analytics import GlueCrawlers
from diagrams.gcp.devtools import Scheduler
from diagrams.aws.network import ElasticLoadBalancing
from diagrams.aws.network import ElbApplicationLoadBalancer
from diagrams.aws.network import ElbClassicLoadBalancer
from diagrams.aws.network import ElbNetworkLoadBalancer
from diagrams.azure.network import LoadBalancers
from diagrams.gcp.network import LoadBalancing
from diagrams.azure.security import KeyVaults


graph_attr = {
    "fontsize": "50",
    "bgcolor": "white"
}

with Diagram(name="BHPL Architecture",direction="TB",graph_attr=graph_attr):
    
    users = Users("Users")
    
    
    
     
    
    with Cluster("GCP Cloud"):
        LoadBalancing = LoadBalancing("Google Load Balancer")
        with Cluster("Cloud SQL"):
            metadata = DatabaseForPostgresqlServers("Metadata Repository")
       

        with Cluster("Google Compute Engine"):      
         
            
            with Cluster("GCE VM"):
                with Cluster("Docker Compose"):
                    with Cluster("Docker Container3"):
                        orchestrator = ContainerInstances("Orchestrator")
                    with Cluster("Docker Container4"):
                        crawlers = GlueCrawlers("Crawlers")
                    with Cluster("Docker Container1"):
                        apiServer = Server("Backend HTTP API")
                    with Cluster("Docker Container2"):
                        scheduler = Scheduler("Scheduler")
                    
            scheduler >> orchestrator
            metadata >> Edge() << apiServer 
            metadata >> Edge() << crawlers
            metadata >> scheduler
            orchestrator >> metadata
            orchestrator >> crawlers     
        with Cluster("Dataproc"):
            AlmarenIngestionJob = Spark("Almaren Ingestion Job")
            
            orchestrator >> AlmarenIngestionJob
    with Cluster("On Prem"):
        with Cluster("Data Sources"):
            hive = Hive("Hive")            
            sources = [SQL("Netezza"),SQLServers("SQL Server"),hive,Oracle("Oracle"),MySQL("MySQL")]       
            

    with Cluster("Azure Cloud"):
        Vault = KeyVaults("Azure Key Valult")
        with Cluster("Target"):
            adls2 = DataLakeStoreGen1("ADLS2")
            
    apiServer >> Edge() << Vault
           
            
    apiServer >> Edge() << LoadBalancing >> Edge() << users
    AlmarenIngestionJob - Edge(label="Write to ADLS2", style="dashed", color="brown") >> adls2
    hive >> Edge(label="Apache Spark Jobs\n\n\n", style="dashed") >> Edge(style="dashed") >> AlmarenIngestionJob
    hive  >> Edge(style="dashed") >> crawlers