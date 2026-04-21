import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# Aqui está o segredo: ele tenta ler a chave do Render (Ambiente Seguro)
# Se não achar nada, ele usa a chave reserva que deixamos aqui
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
                    "content": (
                        "Você é a Luna, a consultora de estilo oficial da Feminina Bijuteria. "
                        "Sua fundadora se chama Valéria. Você é sofisticada, acolhedora e elegante. "
                        "Nunca use o termo 'Dona' para se referir à Valéria; chame-a pelo nome ou 'nossa curadora'. "
                        "Seu objetivo é ajudar as clientes a escolherem semijoias incríveis. "
                        "Sempre que falarem de compra ou preço, direcione para o WhatsApp: https://wa.me/5521989626714"
                    )
                },
                {"role": "user", "content": user_message}
            ],
        )
        response = completion.choices[0].message.content
        return jsonify({"response": response})
    except Exception as e:
        print(f"Erro na Luna: {e}")
        return jsonify({"response": "Oi! Tive um pequeno soluço aqui na conexão, mas você pode falar com a Valéria agora mesmo no WhatsApp!"})

if __name__ == '__main__':
    app.run(debug=True)
