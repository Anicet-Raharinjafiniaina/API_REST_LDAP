# à installer : pycryptodome #

import getpass
import base64
from ldap3 import Server, Connection, ALL, NTLM

# Configuration LDAP
LDAP_SERVER = 'ldap://xxxxx.mg'
LDAP_PORT = XXX
LDAP_DN = 'dc=xxxx,dc=mg'
LDAP_DOMAIN = 'XXXXX\\'

# Attributs à récupérer
LDAP_ATTRIBUTES = [
    "sn", "samaccountname", "title", "physicaldeliveryofficename",
    "givenName", "department", "mail", "manager", "name", "cn", "thumbnailPhoto"
]


def authenticate_ldap(username, password):
    """ Authentifie l'utilisateur et récupère ses informations LDAP + photo en base64 """
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
            "Nom": str(user_data.sn) if "sn" in user_data else "",
            "Prénom": str(user_data.givenName) if "givenName" in user_data else "",
            "Identifiant": str(user_data.samaccountname) if "samaccountname" in user_data else "",
            "Titre": str(user_data.title) if "title" in user_data else "",
            "Bureau": str(user_data.physicalDeliveryOfficeName) if "physicalDeliveryOfficeName" in user_data else "",
            "Département": str(user_data.department) if "department" in user_data else "",
            "Email": str(user_data.mail) if "mail" in user_data else "",
            "Manager": str(user_data.manager) if "manager" in user_data else "",
            "Nom complet": str(user_data.name) if "name" in user_data else "",
            "CN": str(user_data.cn) if "cn" in user_data else "",
        }

        # 📌 Convertir la photo en base64
        if "thumbnailPhoto" in user_data and user_data.thumbnailPhoto.value:
            photo_data = user_data.thumbnailPhoto.value  # Bytes de la photo
            photo_base64 = base64.b64encode(photo_data).decode("utf-8")  # Conversion en base64
            user_info["Photo"] = photo_base64  # Ajoute la photo encodée dans le résultat
        else:
            user_info["Photo"] = None  # Aucun visuel dispo

        return user_info

    except Exception as e:
        return f"Erreur de connexion LDAP : {e}"


if __name__ == '__main__':
    username = input("Entrez votre identifiant LDAP : ")
    password = getpass.getpass("Entrez votre mot de passe LDAP (caché) : ")

    result = authenticate_ldap(username, password)
    print("\nRésultat de l'authentification :\n", result)
