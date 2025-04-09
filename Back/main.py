from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa CORS
import json
from DBConection import execute_supabase_query
from AI import generate_sql_query, generate_user_answer, regenerate_sql_query
from voiceRecognition import recognize_speech
from saveJson import save_to_json
from AIChat import generate_recomendations


app = Flask(__name__)
CORS(app)  # Habilita CORS para todos los dominios

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    data = request.get_json()
    user_input = data.get('user_input')
    
    if not user_input:
        return jsonify({"error": "No se proporcionó consulta"}), 400
    
    try:
        # Paso 1: Generar la consulta SQL con IA
        generated_query = generate_sql_query(user_input)
        
        # Paso 2: Ejecutar la consulta en Supabase
        query_result = execute_supabase_query(generated_query)
        
        # Verificar errores en la consulta
        if isinstance(query_result, str) and "An error occurred" in query_result:
            generated_query = regenerate_sql_query(user_input, query_result)
            query_result = execute_supabase_query(generated_query)
        
        # Paso 3: Generar respuesta para el usuario usando IA
        user_answer = generate_user_answer(user_input, query_result)
        
        # Paso 4: Generar estrategia usando IA
        strategy = generate_recomendations(user_answer, "estrategia")
        
        # Crear respuesta
        response = {
            "user_input": user_input,
            "generated_query": generated_query,
            "query_result": query_result,
            "user_answer": user_answer,
            "strategy": strategy,
            "status": "success"
        }
        
        # Guardar la respuesta en JSON (opcional)
        save_to_json(response)
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)