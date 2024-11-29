import smtplib
import dns.resolver

def verify_email_smtp(email_address):
    """
    Verifica l'email tramite connessione SMTP e record MX.
    """
    fake_sender = "no-reply@example.com"  # Mittente fittizio

    try:
        # Estrai il dominio dell'email
        domain = email_address.split('@')[-1]

        # Ottieni i record MX del dominio
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_host = str(mx_records[0].exchange)

        # Connettiti al server SMTP
        with smtplib.SMTP(mx_host) as server:
            server.set_debuglevel(0)  # Abilita output di debug
            server.helo()
            server.mail(fake_sender)
            code, message = server.rcpt(email_address)

            if code == 250:
                return True, "Email esistente."
            else:
                return False, f"Email non valida, si prega di inserire una mail esistente."

    except Exception as e:
        print(f"Exception occurred: {e}")
        return False, f"Email non valida, si prega di inserire una mail esistente."