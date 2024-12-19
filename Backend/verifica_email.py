import dns.resolver
import smtplib
import re

def verify_email_smtp(email_address):
    """
    Verifica l'email tramite connessione SMTP e record MX.
    """
    sender = "your-email@example.com"  # Usa un indirizzo mittente valido

    # Verifica sintassi dell'email
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(email_regex, email_address):
        return False, "Formato email non valido."

    try:
        # Estrai il dominio dell'email
        domain = email_address.split('@')[-1]

        # Verifica che il dominio abbia record MX
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
        except dns.resolver.NoAnswer:
            return False, "Nessun record MX trovato per il dominio."
        except dns.resolver.NXDOMAIN:
            return False, "Il dominio non esiste."

        # Ordina i record MX per priorità
        mx_hosts = sorted(mx_records, key=lambda mx: mx.preference)

        # Prova a connettersi ai server MX
        for mx in mx_hosts:
            mx_host = str(mx.exchange).strip('.')
            try:
                with smtplib.SMTP(mx_host) as server:
                    server.set_debuglevel(0)  # Disabilita output di debug
                    server.helo()
                    server.mail(sender)
                    code, message = server.rcpt(email_address)

                    # Verifica il codice di risposta
                    if code == 250:
                        return True, "Email esistente."
                    elif code == 550:
                        return False, "Email non valida."
            except smtplib.SMTPConnectError:
                continue  # Prova il prossimo record MX
            except Exception as e:
                print(f"Errore con il server {mx_host}: {e}")
                continue

        return False, "Impossibile verificare l'email con i server MX disponibili."

    except Exception as e:
        print(f"Exception occurred: {e}")
        return False, "Errore durante la verifica dell'email."


def invia_mex(to, codice):
    my_email = "verifyemailgruppo28@gmail.com"
    password = "zkcpwqgvhrzjowgj"

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
        # connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=to,
                            msg="Subject:Codice di verifica\n\nInserire questo codice per effettuare la verifica: " + codice)