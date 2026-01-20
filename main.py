from config.database import db
from models.contact import Contact
# from utils.file_manager import FileManager
# from utils.validators import Validator


# ============= FONCTIONS MENU =============

def afficher_menu():
    """Afficher le menu principal"""
    print("\n" + "=" * 50)
    print("         CARNET DE CONTACTS")
    print("=" * 50)
    print("1. Ajouter un contact")
    print("2. Modifier un contact")
    print("3. Supprimer un contact")
    print("4. Rechercher un contact")
    print("5. Lister tous les contacts")
    print("6. Importer des contacts (JSON/CSV)")
    print("7. Exporter des contacts")
    print("8. Quitter")
    print("=" * 50)


def ajouter_contact_cli():
    """Interface CLI pour ajouter un contact"""
    # 1. Demander nom, prenom, tel, email
    # 2. Valider avec Validator
    # 3. Appeler Contact.ajouter()
    # 4. Afficher confirmation
    pass


def modifier_contact_cli():
    """Interface CLI pour modifier un contact"""
    # 1. Demander ID ou rechercher par nom
    # 2. Afficher contact actuel
    # 3. Demander nouvelles valeurs
    # 4. Appeler Contact.modifier()
    # 5. Afficher confirmation
    pass


def supprimer_contact_cli():
    """Interface CLI pour supprimer un contact"""
    # 1. Demander ID ou rechercher
    # 2. Demander confirmation
    # 3. Appeler Contact.supprimer_par_id()
    # 4. Afficher confirmation
    pass


def rechercher_contact_cli():
    """Interface CLI pour rechercher un contact"""
    # 1. Demander critère de recherche (nom, email, etc.)
    # 2. Appeler Contact.rechercher_par_nom() ou autre
    # 3. Afficher résultats
    pass


def lister_contacts_cli():
    """Interface CLI pour lister les contacts"""
    # 1. Appeler Contact.lister_tous()
    # 2. Afficher sous forme de tableau
    pass


def importer_contacts_cli():
    """Interface CLI pour importer des contacts"""
    # 1. Demander type de fichier (JSON/CSV)
    # 2. Demander chemin du fichier
    # 3. Appeler FileManager.importer_depuis_json() ou csv
    # 4. Afficher statistiques
    pass


def exporter_contacts_cli():
    """Interface CLI pour exporter des contacts"""
    # 1. Demander format (JSON/CSV)
    # 2. Demander chemin destination
    # 3. Appeler FileManager.exporter_vers_json() ou csv
    # 4. Afficher confirmation
    pass


# ============= FONCTION PRINCIPALE =============

def main():
    """Point d'entrée principal"""
    try:
        # Connexion à la base de données
        db.connect()
        Contact.init_collection()

        # Boucle principale du menu
        while True:
            afficher_menu()
            choix = input("\nVotre choix : ")

            if choix == '1':
                ajouter_contact_cli()
            elif choix == '2':
                modifier_contact_cli()
            elif choix == '3':
                supprimer_contact_cli()
            elif choix == '4':
                rechercher_contact_cli()
            elif choix == '5':
                lister_contacts_cli()
            elif choix == '6':
                importer_contacts_cli()
            elif choix == '7':
                exporter_contacts_cli()
            elif choix == '8':
                print("\nAu revoir !")
                break
            else:
                print("\n Choix invalide !")

    except KeyboardInterrupt:
        print("\n\nProgramme interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()