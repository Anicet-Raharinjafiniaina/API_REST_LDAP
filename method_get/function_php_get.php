<?php    /***
     * Methode GET
     * retourne les infos de l'user dans LDAP
     * si le résultat de la fonction n'est pas un array, c'est une erreur donc il suffit juste de l'afficher
     */
    public function getUser($adresse_serveur, $port_serveur, $login, $password)
    {
        $url = "http://$adresse_serveur:$port_serveur/get_user_info/$login/$password";
        $content = @file_get_contents($url); // Utilisation de @ pour supprimer les avertissements PHP
        if ($content === false) { // Afficher un message d'erreur si l'URL est injoignable
            return "Connexion au serveur échouée.";
        }
        $arr_result = (array)json_decode($content); // changer en array
        if (is_array($arr_result) && isset($arr_result[0])) {
            if (str_contains($arr_result[0], 'invalidCredentials')) {
                return  "Login ou mot de passe erroné.";
            } else {
                return "Erreur de connexion LDAP, veuillez vérifier le paramètrage.";
            }
        } else {
            return $arr_result;
        }
    }

    public function auth()
    {
        $adresse_serveur = '127.0.0.1';
        $port_serveur = '5000';
        $login = 'XXXXXX';
        $password = '********';
        $res= $this->getUser($adresse_serveur, $port_serveur, $login, $password);
       return $res;
    }