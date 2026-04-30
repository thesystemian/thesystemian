#!/usr/bin/env python3
import imaplib, smtplib, email, getpass, sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_password_manual(account_name):
    """Demande le code 16L manuellement à l'utilisateur"""
    print(f"\n🔑 Veuillez entrer le code 16 lettres pour {account_name}:")
    password = getpass.getpass("Code: ") 
    return password.strip()

def connect_gmail_imap(email_address):
    """Se connecte à Gmail via IMAP"""
    password = get_password_manual(email_address)
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(email_address, password)
        mail.select('inbox')
        return mail
    except Exception as e:
        print(f"❌ Erreur de connexion IMAP: {e}")
        sys.exit(1)

def connect_gmail_smtp(email_address):
    """Se connecte à Gmail via SMTP"""
    password = get_password_manual(email_address)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email_address, password)
        return server
    except Exception as e:
        print(f"❌ Erreur de connexion SMTP: {e}")
        sys.exit(1)

def list_emails(mail, account_name, limit=10):
    """Affiche les X derniers emails"""
    status, messages = mail.search(None, 'ALL')
    email_ids = messages[0].split()
    
    if not email_ids:
        print("\n📭 Boîte de réception vide.")
        return []
    
    latest_emails = email_ids[-limit:]
    email_list = []
    
    print(f"\n📬 Derniers emails pour {account_name}:\n")
    for i, e_id in enumerate(reversed(latest_emails), 1):
        status, msg_data = mail.fetch(e_id, '(RFC822.HEADER)')
        msg = email.message_from_bytes(msg_data[0][1])
        subject = msg.get('Subject', 'Sans objet')
        from_addr = msg.get('From', 'Inconnu')
        date = msg.get('Date', 'Date inconnue')
        email_list.append((i, e_id))
        print(f"{i}. De: {from_addr[:40]}... | Sujet: {subject[:40]}... | Date: {date[:20]}...")
    
    return email_list

def read_email(mail, email_num, email_list):
    """Lit un email spécifique - EXTRACTEUR DE TEXTE BRUT ROBUSTE"""
    if email_num <= 0 or email_num > len(email_list):
        print("❌ Numéro d'email invalide.")
        return
    
    actual_index, e_id = email_list[email_num - 1]
    status, msg_data = mail.fetch(e_id, '(RFC822)')
    msg = email.message_from_bytes(msg_data[0][1])
    
    body = ""
    
    # Cas 1 : Email multipart (contient plusieurs parties : texte, html, pièces jointes)
    if msg.is_multipart():
        # On cherche PRIORITAIREMENT la partie text/plain
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            # On ignore les pièces jointes
            if "attachment" in content_disposition:
                continue
            
            # Si on trouve du texte brut, on le prend et on arrête la boucle
            if content_type == "text/plain":
                try:
                    charset = part.get_content_charset() or 'utf-8'
                    body = part.get_payload(decode=True).decode(charset, errors='ignore')
                    break # Trouvé ! On sort de la boucle
                except Exception as e:
                    pass # Erreur de décodage, on essaie la suite
        
        # Si on n'a rien trouvé en text/plain (rare), on essaie de prendre le premier texte disponible
        if not body:
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
                    except:
                        pass
                        
    # Cas 2 : Email simple (pas de multipart)
    else:
        try:
            charset = msg.get_content_charset() or 'utf-8'
            body = msg.get_payload(decode=True).decode(charset, errors='ignore')
        except:
            body = "Impossible de décoder le corps du message."

    # Nettoyage final : si le body est vide ou contient juste des espaces
    if not body or not body.strip():
        body = "(Aucun contenu texte détecté dans cet email)"

    # Affichage propre
    print(f"\n{'='*70}")
    print(f"De: {msg.get('From')}")
    print(f"Sujet: {msg.get('Subject')}")
    print(f"Date: {msg.get('Date')}")
    print(f"{'='*70}")
    print(body[:2500])  # Limite à 2500 caractères pour éviter de spamer le terminal
    if len(body) > 2500:
        print("\n... (message tronqué)")
    print(f"{'='*70}\n")

def send_email(smtp_server, from_addr, to_addr, subject, body):
    """Envoie un email"""
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        smtp_server.send_message(msg)
        print("✅ Email envoyé avec succès !")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi: {e}")

def delete_email(mail, email_num, email_list):
    """Supprime un email spécifique"""
    if email_num <= 0 or email_num > len(email_list):
        print("❌ Numéro d'email invalide.")
        return
    
    actual_index, e_id = email_list[email_num - 1]
    
    while True:
        confirm = input(f"⚠️  Voulez-vous vraiment supprimer cet email ? (o=oui, n=non): ").strip().lower()
        if confirm == 'o':
            try:
                mail.store(e_id, '+FLAGS', '\\Deleted')
                mail.expunge()
                print("✅ Email supprimé avec succès !")
                return
            except Exception as e:
                print(f"❌ Erreur lors de la suppression: {e}")
                return
        elif confirm == 'n':
            print("❌ Suppression annulée.")
            return
        else:
            print("❓ Commande non reconnue. Tapez 'o' pour oui ou 'n' pour non.")

def main():
    accounts = [
        ("daxricaud@gmail.com", "Admin"),
        ("daxrico@gmail.com", "Flux")
    ]
    
    print("\n🌸 PrimMail - Votre client mail CLI souverain 🌸\n")
    
    print("Comptes disponibles:")
    for i, (addr, name) in enumerate(accounts, 1):
        print(f"  {i}. {name} ({addr})")
    
    try:
        choice = int(input("\nChoisissez un compte (numéro): ")) - 1
        if choice < 0 or choice >= len(accounts):
            print("❌ Choix invalide.")
            return
        selected_account = accounts[choice][0]
    except ValueError:
        print("❌ Veuillez entrer un nombre.")
        return
    
    try:
        mail = connect_gmail_imap(selected_account)
        smtp = connect_gmail_smtp(selected_account)
        print(f"✅ Connecté à {selected_account}")
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        return
    
    while True:
        email_list = list_emails(mail, selected_account)
        
        if not email_list:
            user_input = input("\nVotre choix (q=quitter, e=envoyer un email): ").strip().lower()
        else:
            user_input = input("\nVotre choix (numéro pour lire, s=supprimer, e=envoyer, q=quitter): ").strip().lower()
        
        if user_input == 'q':
            break
        elif user_input == 'e':
            to_addr = input("Destinataire: ").strip()
            subject = input("Sujet: ").strip()
            print("Corps du message (tapez '.' sur une ligne seule pour terminer):")
            lines = []
            while True:
                line = input()
                if line == '.':
                    break
                lines.append(line)
            body = '\n'.join(lines)
            send_email(smtp, selected_account, to_addr, subject, body)
        elif user_input.isdigit():
            read_email(mail, int(user_input), email_list)
            
            delete_choice = input("Voulez-vous supprimer cet email ? (o=oui, n=non): ").strip().lower()
            if delete_choice == 'o':
                delete_email(mail, int(user_input), email_list)
                email_list = list_emails(mail, selected_account)
            elif delete_choice == 'n':
                print("❌ Suppression annulée.")
            else:
                print("❓ Commande non reconnue. Tapez 'o' pour oui ou 'n' pour non.")
        elif user_input == 's':
            if email_list:
                try:
                    num_to_delete = int(input("Numéro de l'email à supprimer: "))
                    delete_email(mail, num_to_delete, email_list)
                    email_list = list_emails(mail, selected_account)
                except ValueError:
                    print("❌ Veuillez entrer un nombre.")
            else:
                print("📭 Aucun email à supprimer.")
        else:
            print("❌ Commande non reconnue. Commandes disponibles: numéro, s, e, q")
    
    try:
        mail.close()
        mail.logout()
        smtp.quit()
    except:
        pass
    
    print("\n👋 À bientôt dans PrimMail !\n")

if __name__ == "__main__":
    main()
