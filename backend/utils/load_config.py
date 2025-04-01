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

        # API Configuration
        self.api = {
            "host": app_config["api"]["host"],
            "port": int(app_config["api"]["port"]),
            "endpoint": app_config["api"]["endpoint"]
        }

        # RAG config
        self.vectordb_dir = here(app_config["RAG"]["vectordb"])
        self.collection_name = str(app_config["RAG"]["collection_name"])
        self.k = int(app_config["RAG"]["k"])

        # OpenAI Models
        os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(model=app_config["openai_models"]["model"])
        self.embedding_model = str(app_config["openai_models"]["embedding_model"])

        # Tavily Search
        self.tavily_search_max_results = int(app_config["tavily_search"]["max_results"])

        # LangSmith
        os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
        os.environ["LANGCHAIN_TRACING_V2"] = str(app_config["langsmith"]["tracing"])
        os.environ["LANGCHAIN_PROJECT"] = str(app_config["langsmith"]["project_name"])

    def get_api_url(self) -> str:
        """Construct the full URL for the API endpoint from config file."""
        host = self.api["host"]
        port = self.api["port"]
        endpoint = self.api["endpoint"]
        return f"http://{host}:{port}{endpoint}"

    @classmethod
    def load(cls):
        """Factory method to load configuration."""
        return cls()
