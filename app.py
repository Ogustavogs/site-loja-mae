import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# Tenta pegar a chave do Render, se não achar, usa a que você me passou
api_key = os.environ.get("GROQ_API_KEY", "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")
client = Groq(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system", 
                    "content": "Você é a Luna, a consultora de moda inteligente da loja Feminina Bijuteria, no Rio de Janeiro. Sua chefe é a Dona Maria. Você é elegante, carinhosa e especialista em semijoias (colares, brincos, anéis). Ajude as clientes a escolherem peças que combinem com seu estilo e sempre sugira que elas chamem a Dona Maria no WhatsApp para finalizar a compra."
                },
                {"role": "user", "content": user_message}
            ],
        )
        response = completion.choices[0].message.content
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": "Oi, linda! Estou ajustando meus brilhos. Pode falar com a Dona Maria no WhatsApp enquanto isso?"})

if __name__ == '__main__':
    app.run(debug=True)
