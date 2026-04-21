import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# O Render vai injetar a chave aqui automaticamente
api_key = os.environ.get("GROQ_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    
    if not api_key:
        return jsonify({"response": "Valéria, a chave sumiu do painel do Render!"})
    
    try:
        # Inicializamos aqui dentro para garantir que ele pegue a chave atualizada
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama3-8b-8192", 
            messages=[
                {"role": "system", "content": "Você é a Luna, consultora da Feminina Bijuteria. A fundadora é a Valéria. Seja elegante e sofisticada."},
                {"role": "user", "content": user_message}
            ],
        )
        return jsonify({"response": completion.choices[0].message.content})
    except Exception as e:
        print(f"ERRO: {e}")
        return jsonify({"response": "Oi! Tive um soluço, fala com a Valéria no WhatsApp!"})

if __name__ == '__main__':
    app.run(debug=True)
