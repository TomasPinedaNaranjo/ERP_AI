import json
from DBConection import execute_supabase_query
from AI import generate_sql_query, generate_user_answer, regenerate_sql_query
from voiceRecognition import recognize_speech
from saveJson import save_to_json
from AIChat import generate_recomendations

def main():
    print("Bienvenido al asistente de consultas SQL con IA")
    print("Escribe 'salir' para terminar el programa\n")
    
    while True:
        # Opción para entrada por voz o texto
        input_method = input("¿Quieres usar reconocimiento de voz? (s/n): ").strip().lower()
        
        if input_method == 's':
            print("Por favor habla ahora...")
            user_input = recognize_speech()
            if not user_input:
                print("No se pudo reconocer el audio. Intenta de nuevo o escribe tu consulta.")
                continue
            print(f"Consulta reconocida: {user_input}")
        else:
            user_input = input("\nIngresa tu consulta (o 'salir' para terminar): ").strip()
            if user_input.lower() == 'salir':
                break
        
        if not user_input:
            continue
        
        print("\nProcesando tu consulta...")
        
        try:
            # Paso 1: Generar la consulta SQL con IA
            generated_query = generate_sql_query(user_input)
            print(f"\nConsulta SQL generada:\n{generated_query}")
            
            # Paso 2: Ejecutar la consulta en Supabase
            query_result = execute_supabase_query(generated_query)
            
            # Verificar errores en la consulta
            if isinstance(query_result, str) and "An error occurred" in query_result:
                print("\nError detectado en la consulta SQL, regenerando...")
                generated_query = regenerate_sql_query(user_input, query_result)
                query_result = execute_supabase_query(generated_query)
                print(f"\nNueva consulta SQL generada:\n{generated_query}")
            
            # Paso 3: Generar respuesta para el usuario usando IA
            user_answer = generate_user_answer(user_input, query_result)
            print(f"\nRespuesta:\n{user_answer}")
            
            # Paso 4: Generar estrategia usando IA
            strategy = generate_recomendations(user_answer, "estrategia")
            print(f"\nRecomendaciones estratégicas:\n{strategy}")
            
            # Guardar la respuesta en un archivo JSON
            new_entry = {
                "user_input": user_input,
                "generated_query": generated_query,
                "query_result": query_result,
                "user_answer": user_answer,
                "strategy": strategy
            }
            save_to_json(new_entry)
            print("\nConsulta guardada en el archivo JSON.")
            
        except Exception as e:
            print(f"\nOcurrió un error al procesar tu consulta: {str(e)}")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()