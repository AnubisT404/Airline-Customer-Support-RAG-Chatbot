import os
from dotenv import load_dotenv
import yaml
from pyprojroot import here
from langchain_openai import ChatOpenAI

load_dotenv()

class LoadConfig:
    def __init__(self) -> None:
        with open(here("config.yml")) as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)
        
        # Data directories
        self.local_file = here(app_config["directories"]["local_file"])
        self.backup_file = here(app_config["directories"]["backup_file"])

        # RAG config
        self.vectordb_dir = here(app_config["RAG"]["vectordb"])
        self.collection_name = str(app_config["RAG"]["collection_name"])
        self.doc_dir = here(app_config["RAG"]["doc_dir"])
        self.chunk_size = int(app_config["RAG"]["chunk_size"])
        self.chunk_overlap = int(app_config["RAG"]["chunk_overlap"])
        self.k = int(app_config["RAG"]["k"])

        # URLs
        self.travel_db_url = app_config["urls"]["travel_db_url"]
        self.airline_policy_url = app_config["urls"]["airline_policy_url"]

        # OpenAI Models
        os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(model=app_config["openai_models"]["model"])
        self.embedding_model = str(app_config["openai_models"]["embedding_model"])

    @classmethod
    def load(cls):
        """Factory method to load configuration."""
        return cls()
