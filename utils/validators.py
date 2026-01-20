import re


class Validator:
    """
    Classe pour valider les données des contacts
    """

    @staticmethod
    def valider_email(email):
        """
        Valider le format d'un email

        Args:
            email (str): Email à valider

        Returns:
            bool: True si valide, False sinon
        """
        if not email:
            return False

        # Regex simple pour email
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def valider_telephone(telephone):
        """
        Valider le format d'un téléphone

        Args:
            telephone (str): Numéro à valider

        Returns:
            bool: True si valide, False sinon
        """
        if not telephone:
            return False

        # Accepter les formats: +33612345678, 0612345678, 06 12 34 56 78, etc.
        # Supprimer les espaces et vérifier qu'il reste des chiffres
        clean = re.sub(r'[\s\-\.]', '', telephone)

        # Au moins 10 chiffres (peut commencer par +)
        pattern = r'^\+?[0-9]{10,15}$'
        return re.match(pattern, clean) is not None

    @staticmethod
    def valider_nom(nom):
        """
        Valider un nom (ne doit pas être vide)

        Args:
            nom (str): Nom à valider

        Returns:
            bool: True si valide, False sinon
        """
        return bool(nom and nom.strip())

    @staticmethod
    def valider_contact(nom, prenom, telephone, email):
        """
        Valider toutes les données d'un contact

        Args:
            nom (str): Nom du contact
            prenom (str): Prénom du contact
            telephone (str): Téléphone du contact
            email (str): Email du contact

        Returns:
            list: Liste des erreurs (vide si tout est valide)
        """
        erreurs = []

        # Valider le nom
        if not Validator.valider_nom(nom):
            erreurs.append("Le nom est obligatoire")

        # Valider le prénom
        if not Validator.valider_nom(prenom):
            erreurs.append("Le prénom est obligatoire")

        # Valider le téléphone
        if not Validator.valider_telephone(telephone):
            erreurs.append("Le numéro de téléphone est invalide")

        # Valider l'email
        if not Validator.valider_email(email):
            erreurs.append("L'adresse email est invalide")

        return erreurs