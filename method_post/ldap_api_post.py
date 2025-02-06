from flask import Flask, request, jsonify
from ldap3 import Server, Connection, ALL, NTLM
import base64

app = Flask(__name__)

# Configuration LDAP (identique à celle que tu avais)
LDAP_SERVER = 'ldap://xxxx.mg'
LDAP_PORT = 'XXX'
LDAP_DN = 'dc=xxxxx,dc=mg'
LDAP_DOMAIN = 'XXXX\\'
LDAP_ATTRIBUTES = [
    "sn", "samaccountname", "title", "physicaldeliveryofficename",
    "givenName", "department", "mail", "manager", "name", "cn", "thumbnailPhoto"
]

@app.route('/get_user_info', methods=['POST'])
def get_user_info():
    # Récupérer les données de la requête POST
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Nom d'utilisateur et mot de passe sont requis"}), 400

    # Authentifier l'utilisateur via LDAP
    try:
        server = Server(LDAP_SERVER, port=LDAP_PORT, get_info=ALL)
        user_dn = f"{LDAP_DOMAIN}{username}"

        conn = Connection(server, user=user_dn, password=password, authentication=NTLM, auto_bind=True)

        # Recherche de l'utilisateur dans LDAP
        search_filter = f"(samaccountname={username})"
        conn.search(LDAP_DN, search_filter, attributes=LDAP_ATTRIBUTES)

        if not conn.entries:
            return jsonify({"error": "Utilisateur introuvable"}), 404

        user_data = conn.entries[0]
        user_info = {
	    "identifiant" : str(user_data.sAMAccountName),
            "nom": str(user_data.sn),
            "prenom": str(user_data.givenName),
            "titre": str(user_data.title),
            "bureau": str(user_data.physicalDeliveryOfficeName),
            "departement": str(user_data.department),
            "email": str(user_data.mail),
            "manager": str(user_data.manager),
            "nom_complet": str(user_data.name),
            "cn": str(user_data.cn),
            "photo": "Oui" if "thumbnailPhoto" in user_data else "Non"
        }

        # Base64 pour la photo si présente
        if 'thumbnailPhoto' in user_data:
            user_info['photo_Base64'] = base64.b64encode(user_data.thumbnailPhoto.values[0]).decode('utf-8')

        return jsonify(user_info)

    except Exception as e:
        return jsonify({"error": f"Erreur de connexion LDAP : {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
