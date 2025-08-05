from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Chargement des variables d'environnement
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration du serveur mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

@app.route('/api/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()
        
        # Validation des données
        if not all(key in data for key in ['email', 'phone', 'service']):
            return jsonify({'error': 'Données manquantes'}), 400

        # Création du message
        msg_body = f"""
        Nouveau message de contact:
        
        Email: {data['email']}
        Téléphone: {data['phone']}
        Service: {data['service']}
        Message: {data.get('message', 'Aucun message')}
        """

        msg = Message(
            subject='Nouveau message de contact',
            recipients=[os.getenv('MAIL_USERNAME')],
            body=msg_body
        )

        # Envoi du mail
        mail.send(msg)

        return jsonify({'message': 'Message envoyé avec succès'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
