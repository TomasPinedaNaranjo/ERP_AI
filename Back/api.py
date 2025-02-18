# main.py

from DBConection import execute_supabase_query
from AI import generate_sql_query, generate_user_answer, regenerate_sql_query
from voiceRecognition import recognize_speech
from saveJson import save_to_json

def get_user_input_by_speech():
    """Get user input using speech recognition."""
    user_input = recognize_speech()
    return user_input

def get_user_input_by_text():
    """Get user input by typing."""
    user_input = input("Escribe: ")
    return user_input


def main():
    # Ask the user how they want to provide input
    print("Como quieres proporcionar tu pregunta")
    print("1. Comando de voz")
    print("2. Escribir")
    choice = input("Ingresa (1 o 2): ")

    # Get user input based on their choice
    if choice == "1":
        user_input = get_user_input_by_speech()
    elif choice == "2":
        user_input = get_user_input_by_text()
    else:
        print("Invalido.")
        return

    # Guard clause: Exit if no valid input
    if not user_input:
        print("No valid input detected. Exiting.")
        return

    # Step 1: Generate the query using AI
    generated_query = generate_sql_query(user_input)
    print(f"Generated Query: {generated_query}")

    # Step 2: Execute the query on Supabase
    query_result = execute_supabase_query(generated_query)
    print(f"Query Result: {query_result}")

    # Check if the query result has a error
    if isinstance(query_result, str) and "An error occurred" in query_result:
        print("Fallo la consulta, intentaremos nuevamente...")
        generated_query = regenerate_sql_query(user_input, query_result)
        print(f"Regenerated Query: {generated_query}")
        query_result = execute_supabase_query(generated_query)
        print(f"Query Result after regeneration: {query_result}")


    # Step 3: Generate user answer using AI
    user_answer = generate_user_answer(user_input, query_result)
    print(f"User Answer: {user_answer}")

    # Save the answer in a Json
    new_entry = {
        "generated_query": generated_query,
        "query_result": query_result,
        "user_answer": user_answer
    }

    save_to_json(new_entry)


# Run the program
if __name__ == "__main__":
    main()