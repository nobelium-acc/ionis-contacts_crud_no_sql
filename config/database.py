from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from pymongo.server_api import ServerApi


class Database:
    """
    Classe Singleton pour gérer la connexion MongoDB Atlas
    """
    _instance = None

    def __new__(cls):
        """
        Pattern Singleton - une seule instance de connexion
        """
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """
        Initialisation de la connexion (appelé une seule fois grâce au Singleton)
        """
        if self._initialized:
            return

        self.client = None
        self.db = None
        self._initialized = True

    def connect(self, db_name=None):

        try:
            # Config - Connection à la Db Mongo Atlas
            mongo_uri = "mongodb+srv://db_admin:KpRPQo527Eg126QU@cluster0.8jlxb82.mongodb.net/?appName=Cluster0"
            database_name = "carnet_contacts"

            print(f"Connexion à MongoDB Atlas...")

            # Créer le client MongoDB avec ServerApi
            self.client = MongoClient(
                mongo_uri,
                server_api=ServerApi('1'),
                serverSelectionTimeoutMS=5000,  # Timeout de 5 secondes
                connectTimeoutMS=5000
            )

            # Tester la connexion avec ping
            self.client.admin.command('ping')

            # Sélectionner la base de données
            self.db = self.client[database_name]

            print(f"Connecté à MongoDB Atlas - Base de données: '{database_name}'")

            return self

        except ValueError as e:
            print(f"{e}")
            raise

        except ServerSelectionTimeoutError:
            print("Erreur: Impossible de se connecter à MongoDB Atlas (timeout)")
            print("Vérifiez:")
            print("1. Votre connexion Internet")
            print("2. L'URI MongoDB")
            print("3. La valeur du mot de passe")
            print("4. Les règles du pare-feu MongoDB Atlas (IP Whitelist)")
            raise

        except ConnectionFailure as e:
            print(f"Erreur de connexion à MongoDB Atlas: {e}")
            raise

        except Exception as e:
            print(f"Erreur inattendue lors de la connexion: {e}")
            raise

    def get_collection(self, collection_name):
        """Récupérer une collection"""
        if self.db is None:
            raise RuntimeError(
                "DB non connectée. "
                "Appelez d'abord db.connect() avant d'accéder aux collections"
            )

        return self.db[collection_name]

    def close(self):
        """Fermer la connexion"""
        if self.db is None:
            raise RuntimeError(
                "DB non connectée. "
                "Appelez d'abord db.connect() avant d'accéder aux collections"
            )
        self.client.close()


# Instance globale
db = Database()