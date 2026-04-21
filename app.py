import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# Tenta ler do Render, se não tiver, usa a que você criou agora
api_key = os.environ.get("GROQ_API_KEY", "SUA_CHAVE_NOVA_AQUI")

try:
    # Forçamos a inicialização do cliente dentro da rota para evitar erro de boot
    client = Groq(api_key=api_key)
except Exception as e:
    print(f"Erro ao iniciar Groq: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    
    try:
        # Usando o modelo 70b que é mais estável para conversas longas
        completion = client.chat.completions.create(
            model="llama3-70b-8192", 
            messages=[
                {
                    "role": "system", 
                    "content": "Você é a Luna, consultora da Feminina Bijuteria. A fundadora é a Valéria. Seja elegante e direcione para o WhatsApp: https://wa.me/5521989626714"
                },
                {"role": "user", "content": user_message}
            ],
        )
        response = completion.choices[0].message.content
        return jsonify({"response": response})
    except Exception as e:
        # Se der erro, ele vai imprimir no log do Render o motivo real
        print(f"ERRO REAL DA API: {e}")
        return jsonify({"response": "Oi! Tive um soluço na conexão. Pode falar com a Valéria no WhatsApp enquanto eu me recupero?"})

if __name__ == '__main__':
    app.run(debug=True)
