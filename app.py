import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        return jsonify({"response": "Luna sem chave no Render!"})
    
    try:
        client = Groq(api_key=api_key)
        # Usando o modelo mais atualizado e estável
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {"role": "system", "content": "Você é a Luna, consultora da Feminina Bijuteria. Seja breve e elegante."},
                {"role": "user", "content": user_message}
            ],
        )
        return jsonify({"response": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"response": f"Erro: {str(e)[:50]}"})

if __name__ == '__main__':
    app.run(debug=True)
