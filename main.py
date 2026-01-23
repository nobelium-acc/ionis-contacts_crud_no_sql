from tabulate import tabulate
from config.database import db
from models.contact import Contact


def afficher_menu():
    """Afficher le menu principal"""
    print("\n" + "=" * 50)
    print("CARNET DE CONTACTS")
    print("=" * 50)
    print("1. Ajouter un contact")
    print("2. Modifier un contact")
    print("3. Supprimer un contact")
    print("4. Rechercher un contact")
    print("5. Lister tous les contacts")
    print("6. Importer des contacts (JSON/CSV)")
    print("7. Exporter mes contacts (JSON/CSV)")
    print("8. Quitter")
    print("=" * 50)


def ajouter_contact_cli():

    print("\n" + "=" * 50)
    print("AJOUTER UN NOUVEAU CONTACT")
    print("=" * 50)

    try:
        nom = input("\nNom: ").strip()
        prenom = input("Prénom: ").strip()
        telephone = input("Téléphone: ").strip()
        email = input("Email: ").strip()


        print("\nAdresse (optionnel - appuyez sur Entrée pour passer):")
        rue = input("Rue: ").strip()
        ville = input("Ville: ").strip()
        code_postal = input("Code postal: ").strip()
        pays = input("Pays: ").strip()

        adresse = None
        if rue or ville or code_postal or pays:
            adresse = {
                'rue': rue,
                'ville': ville,
                'code_postal': code_postal,
                'pays': pays
            }

        # Ajouter le contact
        contact = Contact.create(nom, prenom, telephone, email, adresse)

        print(f"\nContact ajouté avec succès!")
        print(f"ID: {contact._id}")
        print(f"{contact}")

    except ValueError as e:
        print(f"\n{e}")
    except Exception as e:
        print(f"\nErreur: {e}")

    input("\nAppuyez sur Entrée pour continuer...")




def modifier_contact_cli():
    print("\n" + "=" * 50)
    print("MODIFIER UN CONTACT")
    print("=" * 50)

    try:
        contact_id = input("\nID du contact à modifier : ").strip()

        # Récupérer le contact
        contact = Contact.get_by_id(contact_id)

        if not contact:
            print("\nContact introuvable.")
            input("\nAppuyez sur Entrée pour continuer...")
            return

        print("\nContact actuel :")
        print(contact)

        print("\nLaissez vide pour conserver la valeur actuelle\n")


        nom = input(f"Nom [{contact.nom}] : ").strip() or contact.nom
        prenom = input(f"Prénom [{contact.prenom}] : ").strip() or contact.prenom
        telephone = input(f"Téléphone [{contact.telephone}] : ").strip() or contact.telephone
        email = input(f"Email [{contact.email}] : ").strip() or contact.email

        # Adresse
        adresse_actuelle = contact.adresse or {}
        print("\nAdresse :")

        rue = input(f"Rue [{adresse_actuelle.get('rue', '')}] : ").strip() or adresse_actuelle.get('rue')
        ville = input(f"Ville [{adresse_actuelle.get('ville', '')}] : ").strip() or adresse_actuelle.get('ville')
        code_postal = input(
            f"Code postal [{adresse_actuelle.get('code_postal', '')}] : ").strip() or adresse_actuelle.get(
            'code_postal')
        pays = input(f"Pays [{adresse_actuelle.get('pays', '')}] : ").strip() or adresse_actuelle.get('pays')

        adresse = None
        if rue or ville or code_postal or pays:
            adresse = {
                "rue": rue,
                "ville": ville,
                "code_postal": code_postal,
                "pays": pays
            }

        # Mise à jour
        Contact.update(
            contact_id,
            nom=nom,
            prenom=prenom,
            telephone=telephone,
            email=email,
            adresse=adresse
        )

        print("\nContact modifié avec succès !")
    except ValueError as e:
        print(f"Une erreur est survenue lors de l'update {e}")

    input("\nAppuyez sur Entrée pour continuer...")



def supprimer_contact_cli():
    print("\n" + "=" * 50)
    print("SUPPRIMER UN CONTACT")
    print("=" * 50)

    try:
        contact_id = input("\nID du contact à supprimer : ").strip()
        choice = input("\nConfirmez la supression : Entrée pour confirmer, or tapez 'q' pour annuler: ")
        if choice == "":
            print("Supression...")
            Contact.delete(contact_id)
        elif choice.lower() == "q":
            print("Suppression annulée !")
    except Exception as e:
        print(f"Une erreur est survenue lors de la suppression {e}")

    input("\nAppuyez sur Entrée pour continuer...")



def rechercher_contact_cli():
    try:
        print("\nQue voulez vous rechercher ? ")
        search_input = input("\nVotre recherche : ")

        print("\n" + "=" * 100)
        print("Recherche de contacts")
        print("=" * 100)

        contacts = Contact.find(search_input)
        if not contacts:
            print("\nAucun contact dans le carnet.")
            input("\nAppuyez sur Entrée pour continuer...")
            return


        headers = ["ID", "Nom", "Prénom", "Email", "Téléphone", "Ville"]
        rows = []

        for contact in contacts:
            rows.append([
                contact._id,
                # str(contact._id)[:8] + "...",
                contact.nom,
                contact.prenom,
                contact.email,
                contact.telephone,
                contact.adresse.get('ville', 'N/A') if contact.adresse else 'N/A'
            ])

        # Afficher le tableau
        print("\n")
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        print(f"\nTotal: {len(contacts)} contact(s)")
    except Exception as e:
        print(f"\nErreur lors de la recherche: {e}")


    input("\nAppuyez sur Entrée pour continuer...")


def lister_contacts_cli():
    print("\n" + "=" * 100)
    print("LISTE DES CONTACTS")
    print("=" * 100)

    try:
        # Récupérer tous les contacts
        contacts = Contact.get_all()

        if not contacts:
            print("\nAucun contact dans le carnet.")
            input("\nAppuyez sur Entrée pour continuer...")
            return

        headers = ["ID", "Nom", "Prénom", "Email", "Téléphone", "Ville"]
        rows = []

        for contact in contacts:
            rows.append([
                # str(contact._id)[:8] + "...",
                contact._id,
                contact.nom,
                contact.prenom,
                contact.email,
                contact.telephone,
                contact.adresse.get('ville', 'N/A') if contact.adresse else 'N/A'
            ])

        print("\n")
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        print(f"\nTotal: {len(contacts)} contact(s)")

    except Exception as e:
        print(f"\nErreur lors du listage: {e}")

    input("\nAppuyez sur Entrée pour continuer...")



def importer_contacts_cli():
    print("\n" + "=" * 100)
    print("IMPORT DE CONTACTS")
    print("=" * 100)
    print("\nChoisissez un format")
    print("\t1- JSON")
    print("\t2- CSV")

    choice = input("Choix : ").strip()
    try:
        if choice == "1":
            path = Contact.import_contacts("json")
        elif choice == "2":
            path = Contact.import_contacts("csv")
        else:
            print("Erreur : Choix invalide")

        print(f"Import terminé : {path}")
    except Exception as e:
        print(f"\nErreur lors de l'import... : {e}")

    input("\nAppuyez sur Entrée pour continuer...")


def exporter_contacts_cli():
    print("\n" + "=" * 100)
    print("EXPORT DES CONTACTS")
    print("=" * 100)
    print("\nChoisissez un format")
    print("\t1- JSON")
    print("\t2- CSV")

    choice = input("Choix : ").strip()
    try:
        if choice == "1":
            path = Contact.export_contacts("json")
        elif choice == "2":
            path = Contact.export_contacts("csv")
        else:
            print("Erreur : Choix invalide")

        print(f"Export terminé : {path}")
    except Exception as e:
        print(f"\nErreur lors de l'export : {e}")

    input("\nAppuyez sur Entrée pour continuer...")





def main():
    """Point d'entrée principal"""
    try:
        # Connexion à la base de données
        db.connect()
        Contact.init_collection()

        # Menu et programme
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
        print(f"\n Erreur : {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()