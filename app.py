import os
from typing import List, Any, Optional

import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import firebase_admin
from firebase_admin import credentials, firestore


def initialize_firebase() -> firestore.Client:
    """Initialize Firebase application and return Firestore client."""
    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not cred_path:
        raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
    cred = credentials.Certificate(cred_path)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    return firestore.client()


def fetch_customer_data(collection: str = "customers") -> pd.DataFrame:
    """Fetch customer data from Firestore and return as DataFrame."""
    db = initialize_firebase()
    docs = db.collection(collection).stream()
    records: List[Any] = []
    for doc in docs:
        record = doc.to_dict()
        record["id"] = doc.id
        records.append(record)
    return pd.DataFrame(records)

def fetch_sales_data_csv(path: str) -> pd.DataFrame:
    """Read sample sales CSV for local testing."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} が見つかりません")
    return pd.read_csv(path)

def analyze_with_pandasai(question: str, df: pd.DataFrame) -> str:
    """Use PandasAI to answer question about the DataFrame."""
    llm = OpenAI(api_token=os.environ.get("OPENAI_API_KEY"))
    pandas_ai = PandasAI(llm)
    return pandas_ai.run(df, prompt=question)


def query_llm(question: str) -> str:
    """Orchestrate data fetching and analysis using PandasAI."""
    csv_path: Optional[str] = os.environ.get("SALES_DATA_CSV")
    if csv_path:
        data = fetch_sales_data_csv(csv_path)
    else:
        data = fetch_customer_data()
    answer = analyze_with_pandasai(question, data)
    return answer


if __name__ == "__main__":
    user_question = input("顧客について知りたいことを入力してください: ")
    try:
        response = query_llm(user_question)
        print("LLMの回答:\n", response)
    except Exception as exc:
        print("処理中にエラーが発生しました:", exc)
