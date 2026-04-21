import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# Sua chave continua aqui para funcionar direto
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
                    "content": "Você é a Luna, consultora de luxo da Feminina Bijuteria em Rio de Janeiro. A fundadora da loja é a Valéria. Você é extremamente educada, sofisticada e ajuda as clientes a escolherem as melhores semijoias. Jamais use o termo 'Dona' para se referir à Valéria, trate-a apenas pelo nome ou como 'nossa fundadora'. Sempre direcione para o WhatsApp se a cliente quiser comprar."
                },
                {"role": "user", "content": user_message}
            ],
        )
        response = completion.choices[0].message.content
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": "Oi! Tive um pequeno problema técnico, mas você pode falar diretamente com a Valéria no WhatsApp!"})

if __name__ == '__main__':
    app.run(debug=True)
