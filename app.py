import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Dados da loja
dados_loja = {
    "nome": "Feminina Bijuteria",
    "whatsapp": "5521999999999", # Troque pelo número real
    "descricao": "Semijoias exclusivas em Realengo. Curadoria feita com amor para realçar a sua força."
}

@app.route('/')
def home():
    return render_template('index.html', loja=dados_loja)

# Rota para o Chat da Luna funcionar
@app.route('/chat', methods=['POST'])
def chat():
    mensagem_usuario = request.json.get("mensagem")
    # Por enquanto, vamos simular a resposta para testar o site no ar
    # Depois conectamos sua chave da Groq aqui!
    resposta_luna = f"Oi! Sou a Luna. Você perguntou: '{mensagem_usuario}'. Em breve poderei te sugerir peças em tempo real!"
    return jsonify({"resposta": resposta_luna})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)