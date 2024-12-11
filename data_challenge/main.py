from flask import Flask, request, render_template
import sqlite3
import pandas as pd
import plotly.express as px

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    # Conexão com o banco de dados
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    
    # Carregar dados do banco para a lista
    data = []
    for c in cur.execute("SELECT * FROM data"):
        data.append(c)

    # Inserção de dados ao banco, caso seja POST
    if request.method == "POST":
        first_name = request.form.get("first", "Vazio")
        last_name = request.form.get("last", "Vazio")
        participation = request.form.get("participation", "0")  # Garante valor padrão 0
        print(first_name, last_name, participation)
        
        cur.execute("INSERT INTO data VALUES (?, ?, ?)", (first_name, last_name, int(participation)))
        con.commit()

        # Atualizar os dados após inserção
        data = []
        for c in cur.execute("SELECT * FROM data"):
            data.append(c)
    
    con.close()

    # Converter dados do banco em DataFrame
    df = pd.DataFrame(data, columns=["First Name", "Last Name", "Participation"])

    # Gerar gráfico de pizza com dados do banco
    fig = px.pie(df, values="Participation", names="First Name", hole=0.3)

    # Renderizar template ao passar os dados e o gráfico
    return render_template('index.html', data=data, fig=fig.to_html(full_html=False))

if __name__ == "__main__":
    app.run(debug=True)
