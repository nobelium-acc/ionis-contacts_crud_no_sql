from config.database import db
from bson.objectid import ObjectId
from datetime import datetime

from utils.file_manager import export_json, export_csv, import_json, import_csv
from utils.validators import Validator


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
        contact_dict = {
            'nom': self.nom,
            'prenom': self.prenom,
            'telephone': self.telephone,
            'email': self.email,
            'adresse': self.adresse,
            'date_creation': self.date_creation,
            'date_modification': self.date_modification
        }

        # Ajouter l'ID seulement s'il existe
        if self._id:
            contact_dict['_id'] = self._id

        return contact_dict

    def __str__(self):
        """Représentation string du contact"""
        return f"{self.prenom} {self.nom} - {self.email} - {self.telephone}"

    def __repr__(self):
        """Représentation debug du contact"""
        return f"<Contact: {self.prenom} {self.nom} ({self.email})>"

    # ============= MÉTHODES DE CLASSE (CRUD) =============

    @classmethod
    def init_collection(cls):
        """Initialiser la collection MongoDB"""
        if cls.collection is None:
            cls.collection = db.get_collection('contacts')

            # Créer des index pour optimiser les recherches
            # Email unique
            cls.collection.create_index("email", unique=True)
            # Index sur nom et prénom pour recherches rapides
            cls.collection.create_index("nom")
            cls.collection.create_index([("nom", 1), ("prenom", 1)])

            print("✅ Collection 'contacts' initialisée avec index")

    @classmethod
    def create(cls, nom, prenom, telephone, email, adresse=None):
        """Ajouter un nouveau contact"""
        if cls.collection is None:
            cls.init_collection()

            # 1. Valider les données
        erreurs = Validator.valider_contact(nom, prenom, telephone, email)
        if erreurs:
            raise ValueError(f"Données invalides: {', '.join(erreurs)}")

        # 2. Vérifier si l'email existe déjà
        contact_existant = cls.collection.find_one({'email': email})
        if contact_existant:
            raise Exception(f"Un contact avec l'email '{email}' existe déjà!")

        # 3. Créer le contact
        contact = cls(nom, prenom, telephone, email, adresse)

        # 4. Insérer dans MongoDB
        try:
            result = cls.collection.insert_one(contact.to_dict())
            contact._id = result.inserted_id

            print(f"Contact ajouté: {contact}")
            return contact

        except Exception as e:
            print(f"Erreur lors de l'ajout du contact: {e}")
            raise

    @classmethod
    def update(cls, contact_id, **updates):
        """Modifier un contact existant"""
        from bson import ObjectId

        fields = {k: v for k, v in updates.items() if v is not None}

        if not fields:
            raise ValueError("Aucune donnée à modifier")

        result = cls.collection.update_one(
            {"_id": ObjectId(contact_id)},
            {"$set": fields}
        )

        if result.matched_count == 0:
            raise ValueError("Contact introuvable")

        return True

    @classmethod
    def delete(cls, contact_id):
        """Supprimer un contact par ID"""
        if cls.collection is None:
            cls.init_collection()

        try:
            return cls.collection.delete_one({"_id": ObjectId(contact_id)})
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            return []

    @classmethod
    def get_by_name(cls, nom):
        """Rechercher des contacts par nom"""
        if cls.collection is None:
            cls.init_collection()

        try:
            # Recherche insensible à la casse avec regex
            import re
            regex = re.compile(nom, re.IGNORECASE)

            results = cls.collection.find({
                '$or': [
                    {'nom': {'$regex': regex}},
                    {'prenom': {'$regex': regex}}
                ]
            })

            contacts = [cls.from_dict(data) for data in results]
            return contacts
        except Exception as e:
            print(f"Erreur lors de la recherche: {e}")
            return []

    @classmethod
    def get_by_email(cls, email):
        """Recherche par email (partiel, insensible à la casse)"""
        if cls.collection is None:
            cls.init_collection()

        try:
            import re
            regex = re.compile(re.escape(email), re.IGNORECASE)

            results = cls.collection.find({
                "email": {"$regex": regex}
            })

            return [cls.from_dict(data) for data in results]

        except Exception as e:
            print(f"Erreur lors de la recherche par email: {e}")
            return []

    @classmethod
    def find(cls, value):
        if cls.collection is None:
            cls.init_collection()

        try:
            contact_by_id = cls.get_by_id(value)
            if contact_by_id:
                return [contact_by_id]
            import re
            regex = re.compile(re.escape(value), re.IGNORECASE)

            results = cls.collection.find({
                "$or": [
                    {"nom": {"$regex": regex}},
                    {"prenom": {"$regex": regex}},
                    {"email": {"$regex": regex}},
                    {"telephone": {"$regex": regex}},
                ]
            })

            return [cls.from_dict(data) for data in results]

        except Exception as e:
            print(f"Erreur lors de la recherche par email: {e}")
            return []


    @classmethod
    def get_by_telephone(cls, telephone):
        """Recherche par numéro de téléphone (partiel, insensible à la casse)"""
        if cls.collection is None:
            cls.init_collection()

        try:
            import re
            regex = re.compile(re.escape(telephone), re.IGNORECASE)

            results = cls.collection.find({
                "telephone": {"$regex": regex}
            })

            return [cls.from_dict(data) for data in results]

        except Exception as e:
            print(f"Erreur lors de la recherche par téléphone: {e}")
            return []


    @classmethod
    def get_all(cls, limit=None, skip=0, sort_by='nom'):
        """Lister tous les contacts avec pagination"""
        if cls.collection is None:
            cls.init_collection()

        try:
            query = cls.collection.find().sort(sort_by, 1)

            if skip:
                query = query.skip(skip)

            if limit:
                query = query.limit(limit)

            contacts = [cls.from_dict(data) for data in query]
            return contacts

        except Exception as e:
            print(f"Erreur lors du listage: {e}")
            return []

    @classmethod
    def get_by_id(cls, contact_id):
        """Récupérer un contact par son ID"""
        """
                Récupérer un contact par son ID

                Args:
                    contact_id (str or ObjectId): ID du contact

                Returns:
                    Contact or None: Le contact trouvé ou None
                """
        if cls.collection is None:
            cls.init_collection()

        try:
            # Convertir en ObjectId si c'est une string
            if isinstance(contact_id, str):
                contact_id = ObjectId(contact_id)

            data = cls.collection.find_one({'_id': contact_id})

            if data:
                return cls.from_dict(data)
            return None

        except Exception as e:
            print(f"Erreur lors de la récupération: {e}")
            return None

    @classmethod
    def count(cls):
        """Compter le nombre total de contacts"""
        if cls.collection is None:
            cls.init_collection()

        return cls.collection.count_documents({})

    # ============= MÉTHODES UTILITAIRES =============

    @staticmethod
    def from_dict(data):
        """Créer un Contact depuis un dictionnaire"""
        return Contact(
            nom=data.get('nom'),
            prenom=data.get('prenom'),
            telephone=data.get('telephone'),
            email=data.get('email'),
            adresse=data.get('adresse', {}),
            _id=data.get('_id')
        )

    from utils.file_manager import export_json, export_csv

    @classmethod
    def export_contacts(cls, format="json"):
        if cls.collection is None:
            cls.init_collection()

        contacts = []
        for c in cls.collection.find():
            c["_id"] = str(c["_id"])
            contacts.append(c)

        if format == "json":
            return export_json(contacts, "contacts.json")

        if format == "csv":
            return export_csv(contacts, "contacts.csv")

        raise ValueError("Unsupported export format")

    @classmethod
    def import_contacts(cls, format="json"):
        if cls.collection is None:
            cls.init_collection()

        data = []
        if format == "json":
            data = import_json("contacts.json")

        if format == "csv":
            data = import_csv("contacts.csv")

        return cls.collection.insert_many(data)



