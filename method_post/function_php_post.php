<?php
    /***
     * Methode GET
     * retourne les infos de l'user dans LDAP
     * si le résultat de la fonction n'est pas un array, c'est une erreur donc il suffit juste de l'afficher
     */
public function getUserPostMethode($adresse_serveur, $port_serveur, $login, $password)
{
    $url = "http://$adresse_serveur:$port_serveur/get_user_info";  // URL de l'API
    // Créer un tableau des données à envoyer dans le corps de la requête
    $data = json_encode([
        'username' => $login,
        'password' => $password
    ]);
    // Initialiser la session cURL
    $ch = curl_init();
    // Configurer cURL
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);  // Spécifier la méthode POST
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);  // Ajouter les données
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',  // Définir le type de contenu en JSON
        'Content-Length: ' . strlen($data)
    ]);

    $content = curl_exec($ch);  // Exécuter la requête
    if ($content === false) { // Vérifier si une erreur cURL est survenue
        return "Erreur de connexion cURL : " . curl_error($ch);
    }
    curl_close($ch); // Fermer la session cURL

    $arr_result = (array)json_decode($content);  // Convertir la réponse JSON en tableau
    if (is_array($arr_result) && isset($arr_result['error'])) {      // Vérifier les résultats
        if (str_contains($arr_result['error'], 'invalidCredentials')) {
            return "Login ou mot de passe erroné.";
        } else {
            return "Erreur de connexion LDAP, veuillez vérifier le paramétrage.";
        }
    } else {
        return $arr_result;  // Retourner les données de l'utilisateur
    }
}

public function auth()
{
    $adresse_serveur = '127.0.0.1';
    $port_serveur = '5000';
    $login = 'XXXXX';
    $password = '*******';
    $res = $this->getUserPostMethode($adresse_serveur, $port_serveur, $login, $password);
    return $res;
}