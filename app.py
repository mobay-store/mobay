from flask import Flask, request, render_template_string
from models import db
from routes import register_blueprints
import os
import csv
from datetime import datetime
from collections import Counter

def create_app():
    app = Flask(__name__)

    DATABASE_URL = os.environ.get("DATABASE_URL", "")
    app.config['SECRET_KEY'] = 'dev-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    register_blueprints(app)

    # --- INÍCIO DO MONITORAMENTO ---
    
    LOG_FILE = 'access_logs.csv'

    @app.before_app_request
    def log_to_csv():
        # Ignora arquivos estáticos e a própria rota do dashboard
        if request.endpoint and 'static' not in request.endpoint and 'show_stats' not in request.endpoint:
            try:
                with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                        request.endpoint, 
                        request.remote_addr
                    ])
            except:
                pass

    @app.route('/meu-dashboard-secreto')
    def show_stats():
        stats = Counter()
        try:
            with open(LOG_FILE, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        data_dia = row[0].split(' ')[0]
                        endpoint = row[1]
                        stats[f"{data_dia} | {endpoint}"] += 1
        except FileNotFoundError:
            return "<h1>Ainda não há dados coletados.</h1>"

        # Gera o HTML simples
        linhas = "".join([f"<tr><td>{k.split(' | ')[0]}</td><td>{k.split(' | ')[1]}</td><td>{v}</td></tr>" 
                         for k, v in sorted(stats.items(), reverse=True)])
        
        template = f"""
        <html>
            <head><title>Dashboard</title></head>
            <body style="font-family: sans-serif; padding: 20px;">
                <h2>Acessos por Dia e Endpoint</h2>
                <table border="1" cellpadding="10" style="border-collapse: collapse; width: 100%;">
                    <tr style="background: #eee;"><th>Data</th><th>Endpoint</th><th>Visitas</th></tr>
                    {linhas}
                </table>
            </body>
        </html>
        """
        return render_template_string(template)

    # --- FIM DO MONITORAMENTO ---

    return app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
