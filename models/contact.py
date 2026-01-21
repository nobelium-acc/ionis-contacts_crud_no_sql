from config.database import db
from bson.objectid import ObjectId
from datetime import datetime


class Contact:
    # Attributs de classe
    collection = None

    def __init__(self, nom, prenom, telephone, email, adresse=None, _id=None):
        self._id = _id
        self.nom = nom
        self.prenom = prenom
        self.telephone = telephone
        self.email = email
        self.adresse = adresse
        self.date_creation = datetime.now()
        self.date_modification = datetime.now()

    # ============= MÉTHODES D'INSTANCE =============

    def to_dict(self):
        """Convertir en dictionnaire pour MongoDB"""
        pass

    def sauvegarder(self):
        """Sauvegarder le contact (INSERT ou UPDATE)"""
        pass

    def supprimer(self):
        """Supprimer ce contact"""
        pass

    # ============= MÉTHODES DE CLASSE (CRUD) =============

    @classmethod
    def init_collection(cls):
        """Initialiser la collection MongoDB"""
        pass

    @classmethod
    def ajouter(cls, nom, prenom, telephone, email, adresse=None):
        """Ajouter un nouveau contact"""
        pass

    @classmethod
    def modifier(cls, contact_id, **updates):
        """Modifier un contact existant"""
        updates["date_modification"] = datetime.now()

        result = cls.collection.update_one(
            {"_id": ObjectId(contact_id)},
            {"$set": updates}
    )

    return result.modified_count > 0
        pass

    @classmethod
    def supprimer_par_id(cls, contact_id):
        """Supprimer un contact par ID"""
        pass

    @classmethod
    def rechercher_par_nom(cls, nom):
        """Rechercher des contacts par nom"""
        pass

    @classmethod
    def rechercher_par_email(cls, email):
        """Rechercher un contact par email"""
        pass

    @classmethod
    def rechercher(cls, **criteres):
        """Recherche générique avec critères multiples"""
        pass

    @classmethod
    def lister_tous(cls, limit=None, skip=0, sort_by='nom'):
        """Lister tous les contacts avec pagination"""
        pass

    @classmethod
    def obtenir_par_id(cls, contact_id):
        """Récupérer un contact par son ID"""
        data = cls.collection.find_one({"_id": ObjectId(contact_id)})
        if data:
            return cls.from_dict(data)
        return None
        pass

    @classmethod
    def compter(cls):
        """Compter le nombre total de contacts"""
        pass

    # ============= MÉTHODES UTILITAIRES =============

    @staticmethod
    def from_dict(data):
        """Créer un Contact depuis un dictionnaire"""
        pass

    def __str__(self):
        """Représentation string du contact"""
        pass

    def __repr__(self):
        """Représentation debug du contact"""
        pass
