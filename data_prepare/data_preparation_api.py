from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.download_data import prepare_airline_faq, prepare_travel_sql_db
from src.prepare_vector_db import PrepareVectorDB
from src.update_db_date import update_dates
from utils.load_config import LoadConfig
import os

app = FastAPI()
CFG = LoadConfig.load()

class DBPrepareRequest(BaseModel):
    force_refresh: bool = False

@app.post("/prepare-data/")
async def prepare_data(request: DBPrepareRequest):
    try:
        print("Starting data prepare process...")
        print(f"Vector DB Path: {CFG.vectordb_dir}")
        print(f"Local File: {CFG.local_file}")
        print(f"Backup File: {CFG.backup_file}")

        if os.path.exists(CFG.vectordb_dir):
            if request.force_refresh:
                print("Forced refresh requested. Preparing full refresh...")
                prepare_travel_sql_db(CFG.travel_db_url)
                print("Travel SQL DB prepared successfully.")
                prepare_airline_faq(CFG.airline_policy_url)
                print("Airline FAQ prepared successfully.")

                prepare_db_instance = PrepareVectorDB(
                    doc_dir=CFG.doc_dir,
                    chunk_size=CFG.chunk_size,
                    chunk_overlap=CFG.chunk_overlap,
                    embedding_model=CFG.embedding_model,
                    vectordb_dir=CFG.vectordb_dir,
                    collection_name=CFG.collection_name)
                prepare_db_instance.run()
                print("Vector database prepared successfully.")
                return {"message": "Data refreshed successfully."}
            else:
                print("Updating dates only...")
                update_dates(CFG.local_file, CFG.backup_file)
                print("Dates updated successfully.")
                return {"message": "Dates updated successfully."}
        else:
            print("Vector database not found. Preparing full refresh...")
            prepare_travel_sql_db(CFG.travel_db_url)
            print("Travel SQL DB prepared successfully.")
            prepare_airline_faq(CFG.airline_policy_url)
            print("Airline FAQ prepared successfully.")

            prepare_db_instance = PrepareVectorDB(
                doc_dir=CFG.doc_dir,
                chunk_size=CFG.chunk_size,
                chunk_overlap=CFG.chunk_overlap,
                embedding_model=CFG.embedding_model,
                vectordb_dir=CFG.vectordb_dir,
                collection_name=CFG.collection_name)
            prepare_db_instance.run()
            print("Vector database prepared successfully.")
            return {"message": "Data downloaded and vector database prepared successfully."}
        
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        

            