Eindopdracht Dodo klonen

Keuzevak Django – Hogeschool Rotterdam 

**Intro** 
Deze opdracht dient in een tweetal gemaakt te worden. De beoordeling zal plaatsvinden zoals 
omschreven in de cursushandleiding. De verwachte duur dat je er per persoon mee bezig bent staat 
hier ook vermeld. Je hoeft geen logboek bij te houden.  
Vermeld de namen van jullie tweetal op de inlogpagina.  

Maak een Github project voor je opdracht en voeg ook de docent toe hieraan, github naam: Krul-HR. 
Via de GitHub commits zullen we zien of er door iedereen in het team gelijkwaardig werk is geleverd. 

**Opdracht** 

**Dodo vogels klonen**

Wetenschappers in Wageningen zijn bezig met het klonen van dodo vogels. De wetenschappers 
willen een website waarop ze updates kunnen bijhouden over de vogels.  

Een gebruiker (wetenschapper) kan zich registreren en inloggen. Op zijn profiel wordt zijn 
woonplaats, geboortedatum en hoogst behaalde diploma bijgehouden. De gebruiker kan deze 
dingen updaten via de website.
Een gebruiker kan een nieuwe ‘update’ (welke dodo, wanneer en een omschrijving) toevoegen. 
Updates kunnen alleen gedaan worden voor levende dodo’s.
 
Een gebruiker kan melden dat een dodo is overleden. Een admin moet dit goedkeuren voordat het 
verder op de website wordt verwerkt.  
Een gebruiker kan een ‘newsfeed’ pagina openen, hierop zijn alle updates van alle dodo’s zichtbaar, 
op chronologische volgorde.  
Een gebruiker kan op een pagina al zijn eigen updates inzien, aanpassen en verwijderen.  

De admin kan overleden dodo’s goedkeuren.  
De admin kan zelf dodo’s als overleden melden, dit wordt dan automatisch goedgekeurd. 
De admin kan een nieuwe dodo toevoegen.  
De admin kan updates van alle dodo’s verwijderen (niet aanpassen). 

**Bijkomende functionaliteiten**
Een gebruiker kan zijn wachtwoord updaten.  

Gebruikers hebben een profielpagina, waarop je van de betreffende gebruiker al zijn updates kan 
zien. (Denk aan je profiel op Instagram waar al je berichten op staan). Hier kan je op komen door 
bijvoorbeeld in de newsfeed op de naam van de gebruiker te klikken.  

Een gebruiker mag niet op één dag meerdere updates geven over dezelfde dodo. 

Er is een Dodo pagina, waarop de details van één dodo te vinden zijn. Het laat alle updates van de 
betreffende dodo zien. Maar ook informatie over hoe oud de dodo is en of hij nog leeft. Hier kan je 
op komen door bijvoorbeeld in de newsfeed op de naam van de dodo te klikken.  

Vanaf de Dodo pagina kan een gebruiker een nieuwe update aanmaken, dan komt hij op die pagina 
terecht en is de gekozen dodo direct geselecteerd.  

**Models** 

**Dodo** 
Name 
DateOfBirth 
Alive (Boolean) 
DeadApproved 
DeadApprovedBy (FK) 

**Update** 
Dodo (FK) 
User (FK) 
Date 
Description 

**Profile (connected to User)**
User (FK) 
Grade 
City 
DateOfBirth 

