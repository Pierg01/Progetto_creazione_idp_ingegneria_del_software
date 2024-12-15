# CALM-IdP:
 Calm-IdP è un sistema di Identity Provider (IdP) con supporto per OAuth e autenticazione a due fattori (2FA).  

il nome CALM è l’acronimo nato dall'unione dei cognomi degli sviluppatori,un gioco di parole che rispecchia il nostro obiettivo:
garantire un senso di tranquillità ai nostri utenti quando si affidano al nostro servizio di autenticazione

### Utente: 
È la persona che a cui sono associati le informazioni o i dati. L'utente decide se dare o meno il permesso per accedere a questi dati.

### Client: 
È l'host che si utilizza per accedere ai servizi online.

### Server delle risorse: 
È il "custode" dei dati dell'utente. Per esempio il server che contiene informazioni personali dell'utente.

### Server di autorizzazione IdP (Authorization Server)
È il "controllore" che gestisce il processo di concessione o negazione dei permessi.

##### Come funziona:
Utente tramite Client vuole accedere ai dati dell'utente.
L'utente dà il permesso attraverso il Server di autorizzazione, che fornisce un token di accesso all'applicazione.
Questo token viene usato per accedere ai dati specifici sul Server delle risorse, per un periodo di tempo limitato.

In pratica, OAuth è un sistema che permette all'utente di controllare a quali informazioni un'applicazione può accedere, senza che debba fornire direttamente la sua password all'app.


### *Definizione Componeneti*
   - *Resource Owner (Utente)*
   - *Client (host richiede l'accesso)*
   - *Resource Server (Server che contiene le risorse protette)*
   - *Authorization Server (Server che autentica e autorizza)*

###  *Resource Server*
Il server delle risorse implementato in Node, contiene le risorse a cui si tenta di accedere una volta autenticati.

###  *Authorization Server*
   Il *Authorization Server* è la parte fondamentale del sistema OAuth. Sarà responsabile di:
   - *Autenticare* l'utente.
   - *Emettere i token: L'Authorization Server deve generare **token di accesso *. Questi token permettono al client di accedere alle risorse protette senza richiedere nuovamente le credenziali dell'utente.
   - *Gestire le autorizzazioni*: L'utente dovrà essere in grado di approvare o negare l'accesso ai suoi dati da parte del client.


   


