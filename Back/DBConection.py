import os
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def execute_supabase_query(query):
    try:
        # Execute the query using the Supabase client
        response = eval(query)
        return response.data
    except Exception as e:
        return f"An error occurred in the DB conection: {e}"