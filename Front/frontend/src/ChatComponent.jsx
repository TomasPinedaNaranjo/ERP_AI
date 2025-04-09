import { useState } from 'react';
import axios from 'axios';

const ChatComponent = () => {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const res = await axios.post('http://localhost:5000/api/chat', {
        user_input: input
      });
      
      setResponse(res.data);
    } catch (err) {
      setError(err.response?.data?.message || 'Error al conectar con el servidor');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Chat con IA para SQL</h1>
      
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', gap: '10px' }}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Escribe tu consulta..."
            style={{ flex: 1, padding: '8px' }}
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Enviando...' : 'Enviar'}
          </button>
        </div>
      </form>
      
      {error && (
        <div style={{ color: 'red', margin: '10px 0' }}>
          Error: {error}
        </div>
      )}
      
      {response && (
        <div style={{ marginTop: '20px' }}>
          <h2>Respuesta:</h2>
          <div style={{ background: '#f5f5f5', padding: '15px', borderRadius: '5px' }}>
            <p>{response.user_answer}</p>
          </div>
          
          <h3>Consulta SQL generada:</h3>
          <pre style={{ 
            background: '#282c34', 
            color: 'white', 
            padding: '15px', 
            borderRadius: '5px',
            overflowX: 'auto'
          }}>
            {response.generated_query}
          </pre>
          
          <h3>Resultados:</h3>
          <pre style={{ 
            background: '#f5f5f5', 
            padding: '15px', 
            borderRadius: '5px',
            overflowX: 'auto',
            maxHeight: '300px',
            overflowY: 'auto'
          }}>
            {JSON.stringify(response.query_result, null, 2)}
          </pre>
          
          <h3>Recomendaciones:</h3>
          <div style={{ background: '#e8f4f8', padding: '15px', borderRadius: '5px' }}>
            <p>{response.strategy}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatComponent;