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
    
    # Pegamos a chave aqui dentro para garantir que o Render leu a última versão
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        return jsonify({"response": "Oi! A Valéria esqueceu de colocar minha chave de ativação no painel do Render. Pode avisar ela?"})
    
    try:
        # Inicialização forçada com a chave recuperada
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
        # Isso vai imprimir o erro exato nos Logs do Render para a gente ler
        print(f"ERRO CRÍTICO NA LUNA: {str(e)}")
        return jsonify({"response": "Oi! Tive um soluço, fala com a Valéria no WhatsApp!"})

if __name__ == '__main__':
    app.run(debug=True)
