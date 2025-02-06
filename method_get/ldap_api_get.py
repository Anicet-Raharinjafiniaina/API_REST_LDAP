# à installer : pip install Flask ldap3 #


from flask import Flask, jsonify
import base64
from ldap3 import Server, Connection, ALL, NTLM

app = Flask(__name__)

# Configuration LDAP
LDAP_SERVER = 'ldap://xxxx.mg'
LDAP_PORT = 'XXX'
LDAP_DN = 'dc=xxxxx,dc=mg'
LDAP_DOMAIN = 'XXXX\\'

LDAP_ATTRIBUTES = [
    "sn", "samaccountname", "title", "physicaldeliveryofficename",
    "givenName", "department", "mail", "manager", "name", "cn", "thumbnailPhoto"
]

def authenticate_ldap(username, password):
    """ Authentifie un utilisateur et récupère ses informations LDAP + photo en base64 """
    try:
        server = Server(LDAP_SERVER, port=LDAP_PORT, get_info=ALL)
        user_dn = f"{LDAP_DOMAIN}{username}"

        # Connexion LDAP avec NTLM
        conn = Connection(server, user=user_dn, password=password, authentication=NTLM, auto_bind=True)

        # Recherche LDAP
        search_filter = f"(samaccountname={username})"
        conn.search(LDAP_DN, search_filter, attributes=LDAP_ATTRIBUTES)

        if not conn.entries:
            return "Utilisateur introuvable"

        user_data = conn.entries[0]

        # Extraction des infos utilisateur
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
        return f"Erreur de connexion LDAP : {e}"

# Modifier la route pour accepter des paramètres dans l'URL
@app.route('/get_user_info/<username>/<password>', methods=['GET'])
def get_user_info(username, password):
    """ Endpoint API pour obtenir les informations d'un utilisateur LDAP """
    result = authenticate_ldap(username, password)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
