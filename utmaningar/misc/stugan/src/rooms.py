import time
import threading
import item
import hbsql
from room import Room
import utils 

# Code: 8-1-2-5
# Username: harald
# Password: snuffe

# ---------------------------------------------------------------------------------------
# Room 1 - Outside the cabbin
# ---------------------------------------------------------------------------------------
class Room1(Room):
    def __init__(self):
        super().__init__()
        self.doorUnlocked = False
        self.doorOpened = False
        self.keyFound = False
        super().setDesc("""Du står i en glänta, på en stenlagd stig som leder upp mot dörren till en liten
stuga. På båda sidor om stigen tittar en ovårdad gräsmatta här och där upp 
igenom det smältande snötäcket. Stugan är låg och byggd i grovt timmer med 
torvtak och ett ensamt fönster, med stängda fönsterluckor, bredvid en grov
dörr av kraftigt trä. Över de höga granarna som omger gläntan ser du solens 
gyllene strålar skina genom grenverket, men ljuset når inte hela vägen ned 
till gläntans botten som ligger i skugga.\n""")
        super().addItem("gläntan","En glänta i den djupa skogen, omgiven av höga granar.\n")
        super().addItem("stigen","En slarvigt stenlagd stig som leder upp mot den lilla stugan.\n")
        super().addItem("stugan","Den lilla stugan ser trivsam, men tom och övergiven, ut.\n")
        super().addItem("dörren","En stadig dörr av kraftigt mörkt trä. Den är väldigt stängd. Framför dörren\nligger en tilltuffsad dörrmatta på sned.\n")
        super().addItem("mattan|dörrmattan","En tilltuffsad och smuttsig dörrmatta som ligger på sniskan framför dörren. Det\nser ut som den flyttats på väldigt ofta.\n")
        super().addItem("gräset|gräsmattan|botten|marken","Gräsmattan är till stora delar täckt av smältande snö. Man ser bara fläckar av\nden som sticker upp här och där. Det som syns av den är ovårdat och spretigt.\n")
        super().addItem("snön|snötäcket","Snön ser blöt och slaskig ut. Den håller på att smälta bort. Om några dagar\när den nog borta.\n")
        super().addItem("taket|torvtaket","Stugans tak är gjort av torv. Även på taket håller snön på att smälta bort.\n")
        super().addItem("fönstret|fönsterluckorna","Det lilla fönstret är igensatt med stängda och fastrostade fönsterluckor.\n")
        super().addItem("skogen|granarna|träden","De mörka granarna står tätt och skogen ligger mörk och tyst runt den lilla\ngläntan.\n")
        super().addItem("solen|ljuset|solstrålarna|strålarna","Solens gyllene strålar silas genom granarna och faller grönskiftande över\nträden på motsatta sidan, men ljuset når inte hela vägen ned till gläntans\nbotten.\n")
        super().addItem("timmret|träet","Stugan är byggd av grovt timmer. Kanske är det granarna som stod här i gläntan\ninnan stugan byggdes.") 
    def queryAction(self,plr,str):
        if str == "öppna":
            return "Öppna vad?\n"
        if str == "öppna fönstret" or str == "öppna fönsterluckorna" or str == "öppna fönsterluckan":
            return "Du tar i för allt du är värd, men fönsterluckorna är fastrostade och går inte\natt öppna.\n"
        if str == "öppna dörren":
            if self.doorOpened:
                return "Dörren är redan öppen.\n"
            if not self.doorUnlocked:
                return "Du rycker i handtaget men dörren är låst.\n"
            self.doorOpened = True
            super().addItem("dörren","En stadig dörr av kraftigt mörkt trä. Den står på vid gavel så du kan gå in i\nom du vill. Framför dörren ligger en tilltuffsad dörrmatta på sned.\n")
            return "Du öppnar dörren och den glider upp med ett högt gnisslande.\n"
        if str == "lås upp dörren":
            if self.doorUnlocked:
                return "Dörren är redan olåst.\n"
            if not self.keyFound:
                return "Vad tänkte du låsa upp dörren med? Tänderna?\n"
            self.doorUnlocked = True
            return "Du sticker nyckeln i låset och vrider om. Du får ta i en del, för låset verkar\ninte ha öppnats på ganska länge, men till slut get det med sig med ett tydligt\n'klick'.\n"
        if str == "lyft dörrmattan" or str == "flytta dörrmattan" or str == "lyft mattan" or str == "flytta mattan" or str == "lyft på mattan" or str == "flytta på mattan":
            if self.keyFound:
                return "Du lyfter undan dörrmattan. Under den finns bara damm och grus eftersom nyckeln\nredan ligger i din ficka.\n"
            self.keyFound = True
            plr.addItem(item.Item("nyckel|nyckeln|rostig nyckel","En rostig nyckel","En grov och rostig gammal nyckel. Undrar var den passar.\n"))
            return "Du lyfter undan dörrmattan. Under den, bland damm och grus ligger en nyckel! Du\ntar snabbt upp den och stoppar den i fickan innan du lägger tillbaka dörrmattan.\n"
        return super().queryAction(plr,str)

    def move(self,str):
        if str == "in" or str == "in i stugan" or str == "in i huset":
            if not self.doorOpened:
                return 0, "Du kan inte gå in i stugan. Dörren är stängd.\n"
            return 1, "Du böjer dig lite för att inte slå i dörrkarmen och kliver in i stugan.\n"
        return super().move(str)

# ---------------------------------------------------------------------------------------
# Room 2 - Main room in cabbin
# ---------------------------------------------------------------------------------------

class Room2(Room):
    def __init__(self):
        super().__init__()
        self.lampLit = False
        self.bagSearched = False
        self.pouchSearched = False
        super().setDesc("""Du står inne i den mörka stugan. Ljuset som faller in genom den öppna dörren
lyser bara upp en bråkdel av rummet, resten ligger i totalt mörker. Det du ser
i konen av ljus utifrån är ett dammigt golv och ett litet bord med ett ensam, 
släckt talgljus på.\n""")
        super().addItem("stugan","Det inre av stugan ligger nästan helt i mörker.\n")
        super().addItem("ljuset","En svag ljuskon faller in från gläntan utanför.\n")
        super().addItem("mörkret","Det svaga ljuset klarar inte att tränga igenom det kompakta mörkret längre in i\nstugan. Mörkret ser mörkt ut.\n")
        super().addItem("talgljuset","Ett ensamt talgljus i en ljusstake av trä. Ljuset är släckt.\n")

        super().addItem("golvet|plankorna","Golvet består av grova plankor och är i stort behov av att sopas.\n")
        super().addItem("dörren","Dörren står öppen och du kan gå ut igen om du vill.\n")
        super().addItem("gläntan","Du kan inte se mycket av den här inifrån. Du måste gå ut igen om du vill titta\nnärmare på den.\n")
        super().addItem("ljusstaken","Ljusstaken är gjord av trä. Vackert snidad. Det sitter ett ensamt talgljus i\nden.\n")
        super().addItem("bordet","Bordet ser stabilt och välbyggt ut. Det står en ljusstake med ett ensamt\ntalgljus i på bordet. Bredvid ljusstaken ligger en liten jutepåse.\n")
        super().addItem("påsen|jutepåsen","En ganska liten påse gjord av jute. Du kanske ska leta i den för att se om den\ninnehåller något intressant?\n")

    def queryAction(self,plr,str):
        if str == "leta i jutepåsen" or str == "leta i påsen" or str == "sök i jutepåsen" or str == "sök i påsen":
            if self.bagSearched:
                return "Det finns inget mer i påsen. Den är helt tom.\n"
            self.bagSearched = True
            plr.addItem(item.Item("elddonet|flintan|stålet","Ett elddon","En konstfullt smidd bygel av stål med en tillhörande bit av finaste flinta.\n"))
            return "Du sticker ned handen i den lilla påsen och fiskar upp ett elddon som du tar med\ndig.\n"
        if str == "leta i pungen" or str == "leta i bältespungen" or str == "sök i pungen" or str == "sök i bältespungen":
            if not self.lampLit:
                return super().queryAction(plr,str)
            if self.pouchSearched:
                return "Det finns inget mer i bältespungen. Den är helt tom.\n"
            self.pouchSearched = True
            plr.addItem(item.ReadItem("träbiten|runorna på träbiten","En träbit","En liten polerad träbit med ett antal runor på. Kan du läsa runor?\n"," Sleipners ben\n Odens ögon\n Urds systrar\n Tyrs fingrar\n"))
            plr.addItem(item.Item("mynten|silvermynten","En handfull silvermynt","En handfull kantstötta och slitna silvermynt från olika delar av världen.\n"))
            plr.addItem(item.Item("kroken|fiskekroken","En fiskekrok","En grovt smidd fiskekrok som trots allt ser ganska vass ut. Vilken tur att du\ninte stack dig!\n"))
            return "Snabbt gräver du upp allt du hittar i bältespungen och tar det med dig.\n"
        if str == "tänd":
            return "Vad är det du försöker tända?\n"
        if str == "tänd talgljuset" or str == "tänd ljuset":
            if self.lampLit:
                return "Ljuset är redan tänt, brinner med en gulaktig låga och sprider ett varmt sken i\nstugan.\n"
            if not plr.getItem("elddonet"):
                return "Du försöker tända ljuset både med varma tankar och kraften av vänskap, men\nljuset förblir släckt. Du behöver något mer påtagligt för att tända det med.\n"
            self.lampLit = True
            super().setDesc("""Du står i ett rum som liknar ett långhus i miniatyr. I den högra ändan finns en
upphöjd plattform där det står en vackert utsirad tron och i motsatta ändan av
rummet hänger ett draperi som delvis döljer någon slags alkov bakom sig. Vid 
väggen mittemot dörren finns en eldstad och i mitten av rummet står det lilla 
bordet med det tända ljuset och sprider ett mjukt, fladdrande sken som får 
skuggorna att dansa längs golvet och väggarna.\n""")
            super().addItem("stugan","""Insidan av den lilla stugan är som ett långhus i miniatyr. I en ena ändan finns
en lite upphöjd plattform där det står en vackert utsirad tron. I mitten står
det lilla bordet med ljuset på och i andra ändan finns ett draperi som delvis
döljer någon slags alkov som ligger bortom draperiet.\n""")
            super().addItem("rummet|huvudrummet","""Rummet du står i liknar huvudrummet i ett klassiskt långhus, fast mindre. I 
en ena ändan finns en lite upphöjd plattform där det står en vackert utsirad
tron. I mitten står det lilla bordet med ljuset på och i andra ändan finns 
ett draperi som delvis döljer någon slags alkov som ligger bortom draperiet.\n""")
            super().addItem("ljuset","Det varma, fladdrande ljuset från det brinnande talgljuset får skuggorna att\ndansa runt i rummet. Ett blekt ljus faller även in från gläntan utanför.\n")
            super().addItem("mörkret","Talgljuset sprider ett varmt sken i rummet, men lite mörker finns det kvar i hörnen..\n")
            super().addItem("talgljuset","Ett ensamt talgljus i en ljusstake av trä. Det är tänt och sprider ett\nfladdrande, gyllene sken i rummet.\n")
            super().addItem("skuggorna","Skuggorna dansar runt i skenet från det lilla ljuset på bordet.\n")
            super().addItem("draperiet","Ett mörkrött draperi som delvis täcker ingången till en liten alkov i vänstra\ndelen av stugan.\n")
            super().addItem("alkoven","En liten alkov i vänstra delen av stugan. Ett mörkrött draperi täcker delvis\ningången men den utgör inget hinder för att gå in dit.\n")
            super().addItem("långhuset","Stugan är byggd som ett klassiskt långhus, men i mindre skala.\n")
            super().addItem("askan","Svart, vit och grå. Rester efter den eld som brunnit där. Det finns ganska\nmycket av det i den urbrunna eldstaden.\n")
            super().addItem("väggen|väggarna|timmret","Väggarna består av grovt timmer och är ganska sotiga.\n")
            super().addItem("eldstaden|stenen|askan","En eldstad av huggen sten. Det finns varken eld eller glöd i den, bara aska. Du\nser inte till någon ved att tända den med heller.\n")
            super().addItem("sotet","Ett tunnt lager av svart sot finns på det mesta här inne. Troligen kommer det från eldstaden.\n")
            super().addItem("plattformen","En upphöjd del av golvet i den högra delen av rummet. Det står en tronliknande\nstol på den.\n")
            super().addItem("tronen|stolen","""En vackert utsirad tron av mörkt trä. Det ligger en fårskinsfäll i den, troligen
för bekvämlighetens skull. Ett bälte med en bältespung ligger slarvigt slängd ovanpå fällen.\n""")
            super().addItem("fällen|fårskinnsfällen","En lurvig fäll ligger på tronen, troligtvis för att den som sitter där ska sitta\nbekvämt. Ett bälte med en bältespung ligger slarvigt slängd ovanpå fällen.\n")
            super().addItem("bältet|pungen|bältespungen","Läderbältet med den vidhängande bältespungen ligger på tronen. Bältespungen ser\nganska välfylld ut.\n")
            
            return "Du använder elddonet för att tända det lilla ljuset och efter ett par försök\nlyckas du få fyr på det. Ett varmt sken sprider sig i den lilla stugan.\n"
        return super().queryAction(plr,str)

    def move(self,str):
        if str == "in" or str == "in i alkoven" or str == "förbi draperiet":
            if not self.lampLit:
                return 0, "Du kan inte gå längre in i stugan. Det är bäckmörkt där inne!\n"
            return 1, "Du håller undan draperiet och kliver in i alkoven innanför.\n"
        if str == "ut" or str == "ut ur stugan" or str == "ut i gläntan":
            return 2, "Du böjer dig lite för att inte slå i dörrkarmen och kliver ut ur stugan.\n"
        return super().move(str)

        
# ---------------------------------------------------------------------------------------
# Room 3 - Sleeping alcove
# ---------------------------------------------------------------------------------------

class Room3(Room):
    def __init__(self):
        super().__init__()
        self.bedMoved = False
        self.hatchOpen = False
        self.jewelFound = False
        self.stoneFound = False
        self.chestOpened = False
        super().setDesc("""Du står i en liten avskild alkov i ena änden av stugan. Ljuset som sipprar in 
från det större rummet är svagt, men tillräckligt för att du ska kunna se vad 
som finns här inne. Det är dock inte speciellt mycket. En obäddad säng står mot
den vänstra väggen och en kista står vid den motsatta. Det hänger en bonad av 
något slag på väggen ovanför sängen och på golvet ligger en björnfäll. En sköld
står lutad mot väggen rakt fram.\n""")
        super().addItem("golvet","En stor björnfäll täcker nästan hela golvet förutom under sängen där det ser\nut som det finns skrapmärken.\n")
        super().addItem("skrapmärkena","Golvet runt sängbenen har tydliga skrapmärken. Som om någon har flyttat sängen\nfram och tillbaka upprepade gånger.\n")
        super().addItem("fällen|björnfällen","En stor och sliten björnfäll som täcker nästan hela golvet. Det måste ha varit\nen riktig best när den var i livet.\n")
        super().addItem("skölden|sköldknappen","En rund sköld av trä med en sköldknapp av järn. Skölden har omväxlande vita och\nröda fält.\n")
        super().addItem("fälten","Skölden har omväxlande vita och röda fält. Totalt är det tre vita och tre röda fält.\n")
        super().addItem("kistan","En ganska stor och kraftig kista. Locket är stängt men du ser inget lås på den.\n")
        super().addItem("bonaden|bilden","En vävd bonad med något slags bild på. I dunklet är det svårt att avgöra vad det\när för bild, men det skulle kunna vara ett stiliserat 'B'.\n")
        super().addItem("alkoven","En liten avskild del av stugan som verkar användas som sovrum. Den är avskild\nfrån resten av stugan med ett mörkrött draperi. Det är ganska stökigt här inne.\n")
        super().addItem("rummet|stugan","Du ser bara den här lilla alkoven här inifrån. Den större delen av stugan ligger\npå andra sidan draperiet. Du kan lätt gå tillbaka dit om du skulle vilja.\n")
        super().addItem("sängen","Sängen ser välbyggd ut och är gjord av ljust trä och sängstolparna är vackert\nsnidade, men sängen är obäddad och sängkläderna är i en enda röra.\n") 
        super().addItem("sängbenen|sängstolpen|sängstolparna","""Vackert snidade sängstolpar. Längst upp på varje stolpe har konstnären snidat
fram ett djurhuvud, olika djur på varje stolpe. Snirkliga mönster följer 
stolpen nedåt och när du följer dem med blicken ser du att det är skrapmärken 
på golvet runt sängbenen. Det ser ut som om någon har flyttat på sängen.\n""")
        super().addItem("djurhuvudena","Det är ett björnhuvud, ett rävhuvud, ett ekorrhuvud och ett varghuvud. Riktigt\nvälgjorda, de ser nästan levande ut.\n")
        super().addItem("björnhuvudet","En träskulptur av huvudet på en rytande björn.\n")
        super().addItem("rävhuvudet","En träskulptur av huvudet på en smilande räv.\n")
        super().addItem("ekorrhuvudet","En träskulptur av huvudet på en tjattrande ekorre.\n")
        super().addItem("varghuvudet","En träskulptur av huvudet på en ylande varg.\n")
        super().addItem("sängkläderna","De ligger i en enda röra. Det skulle kunna finnas vad som helst gömt bland dem!\n")
        super().addItem("draperiet","Ett mörkrött draperi som skiljer av alkoven från resten av stugan.\n")

    def queryAction(self,plr,str):
        if str == "flytta sängen" or str == "flytta på sängen":
            if self.bedMoved:
                if self.hatchOpen:
                    return "Du kan inte flytta tillbaka sängen. Den öppna luckan är i vägen.\n"
                return "Vid närmare eftertanke så struntar du i att städa upp efter dig.\n"
            self.bedMoved = True
            super().addItem("sängen","""Sängen ser välbyggd ut och är gjord av ljust trä och sängstolparna är vackert
snidade, men sängen är obäddad och sänkläderna är i en enda röra. Någon har 
flyttat ut sängen från väggen och luckan som fanns under sängen ligger nu fri.\n""") 
            super().addItem("luckan","En kraftig lucka i golvet under sängen. Om du öppnar den kanske den leder någonstans.\n") 
            return "Du drar sängen åt sidan med ett ljudligt skrapande. Under sängen ser du, för utom damm, en kraftig lucka i golvet.\n"
        if str == "öppna luckan" or str == "öppna luckan i golvet":
            if not self.bedMoved:
                return super().queryAction(plr,str)
            if self.hatchOpen:
                return "Luckan är redan öppen.\n"
            self.hatchOpen = True
            super().addItem("luckan","En kraftig lucka i golvet under sängen. Den är öppen och genom den kan du se en\nbrant trappa som leder nedåt.\n") 
            return "Du tar tag i den tunga luckan och häver upp den med ett brak.\n"
        if str == "öppna kistan" or str == "öppna kistlocket":
            if self.chestOpened:
                return "Kistan är redan öppen.\n"
            self.chestOpened = True
            super().addItem("kistan","En ganska stor och kraftig kista. Locket är öppet och den verkar vara fylld med kläder.\n")
            return "Du fäller upp locket på kistan med ett ljudligt knarrande.\n"
        if str == "sök i kistan" or str == "leta i kistan" or str == "sök igenom kistan" or str == "leta igenom kistan":
            if not self.chestOpened:
                return "Du inser att det skulle vara lättare att leta i kistan om den var öppen.\n"
            if self.jewelFound:
                return "Du letar igenom innehållet i kistan en gång till, men hittar inget spännande.\n"
            self.jewelFound = True
            plr.addItem(item.Item("ädelstenen","En vacker grön ädelsten","En vackert slipad, grön ädelsten, formad som ett åttakantigt prisma.\n"))
            return "Du söker igenom innehållet i kistan och hittar en vacker liten ädelsten som du snabbt stoppar på dig.\n"
        if str == "sök i sängen" or str == "leta i sängen" or str == "sök igenom sängen" or str == "leta igenom sängen" or str == "sök i sängkläderna" or str == "leta i sängkläderna" or str == "sök igenom sängkläderna" or str == "leta igenom sängkläderna":
            if self.stoneFound:
                return "Du letar igenom sänkläderna en gång till, men det verkar inte finnas något mer att hitta.\n"
            self.stoneFound = True
            plr.addItem(item.ReadItem("stenen|runstenen","En väldigt, väldigt liten runsten","En väldigt liten runsten. Du kanske ska läsa vad som står på den.\n","""Snuffe, min följeslagare i sol och skugga.
Din mjuka päls, vakna blick och kloka steg.
     Efter solnedgången vilar du,
  ditt spinnande ekar nu från Valhall.
 Må du för evigt jaga i natten skogar.
     Harald lät hugga denna sten.\n"""))
            return "Du söker igenom sängkläderna och när du skakar dem ramlar en liten sten ut. Du plockar snabbt upp den.\n"
        return super().queryAction(plr,str)

    def move(self,str):
        if str == "ner" or str == "ned" or str == "ner genom luckan" or str == "ner för trappan" or str == "ner i källaren" or str == "ned för trappan" or str == "ned i källaren":
            if not self.bedMoved: 
                return super().move(str)
            if not self.hatchOpen: 
                return 0, "Luckan är inte öppen. Du kanske ska öppna den först.\n"
            return 1, "Försiktigt klättrar du ned genom luckan och går ner för trappan.\n"
        if str == "tillbaka" or str == "ut" or str == "förbi draperiet":
            return 2, "Du håller undan draperiet och går ut i rummet utanför.\n"
        return super().move(str)


# ---------------------------------------------------------------------------------------
# Room 4 - Cellar
# ---------------------------------------------------------------------------------------

def screenMessages(p,r):
    time.sleep(2)
    while r.screenMessageCnt < 5:
        if r.screenMessageCnt == 0:
            utils.out("\nPlötsligt dyker det upp runor på den lysande fyrkanten.\n")
            r.addItem("runorna","Runor som lyser med en annan färg än den omgivande fyrkanten. Det står:\n\n > HB-OS startar. Vänta...\n\n")
            r.addItem("fyrkanten|skärmen","""En blekt lysande fyrkant, nästan som en skärm, infälld i väggen. Runt den sitter
en ram av metall. Överst i ramen sitter en liten grön ädelsten och lyser svagt.
I mitten av fyrkanten finns det runor som lyser med en annan färg än den 
omgivande fyrkanten. Det står:

 > HB-OS startar. Vänta...
 \n""")
        if r.screenMessageCnt == 1:
            utils.out("\nRunorna på den lysande fyrkanten förändras.\n")
            r.addItem("runorna","Runor som lyser med en annan färg än den omgivande fyrkanten. Det står:\n\n > HB-OS Laddar subsystem. Vänta...\n\n")
            r.addItem("fyrkanten|skärmen","""En blekt lysande fyrkant, nästan som en skärm, infälld i väggen. Runt den sitter
en ram av metall. Överst i ramen sitter en liten grön ädelsten och lyser svagt.
I mitten av fyrkanten finns det runor som lyser med en annan färg än den 
omgivande fyrkanten. Det står:

 > HB-OS Laddar subsystem. Vänta...
 \n""")
        if r.screenMessageCnt == 2:
            utils.out("\nRunorna på den lysande fyrkanten förändras igen.\n")
            r.addItem("runorna","Runor som lyser med en annan färg än den omgivande fyrkanten. Det står:\n\n > Subsystem laddade.\n > Startar HB-SQL service. Vänta...\n\n")
            r.addItem("fyrkanten|skärmen","""En blekt lysande fyrkant, nästan som en skärm, infälld i väggen. Runt den sitter
en ram av metall. Överst i ramen sitter en liten grön ädelsten och lyser svagt.
I mitten av fyrkanten finns det runor som lyser med en annan färg än den 
omgivande fyrkanten. Det står:

 > Subsystem laddade.
 > Startar HB-SQL service. Vänta...
 \n""")
        if r.screenMessageCnt == 3:
            utils.out("\nRunorna på den lysande fyrkanten förändras ytterligare en gång.\n")
            r.addItem("runorna","Runor som lyser med en annan färg än den omgivande fyrkanten. Det står:\n\n > Systemet är redo.\n > Startar gränssnitt. Vänta...\n\n")
            r.addItem("fyrkanten|skärmen","""En blekt lysande fyrkant, nästan som en skärm, infälld i väggen. Runt den sitter
en ram av metall. Överst i ramen sitter en liten grön ädelsten och lyser svagt.
I mitten av fyrkanten finns det runor som lyser med en annan färg än den 
omgivande fyrkanten. Det står:

 > Systemet är redo.
 > Startar gränssnitt. Vänta...
 \n""")
        if r.screenMessageCnt == 4:
            utils.out("\nÅter igen förändras runorna på den lysande fyrkanten.\n")
            r.addItem("runorna","Runor som lyser med en annan färg än den omgivande fyrkanten. Det står:\n\n > Redo för autentisering.\n > Säg ditt namn.\n\n")
            r.addItem("fyrkanten|skärmen","""En blekt lysande fyrkant, nästan som en skärm, infälld i väggen. Runt den sitter
en ram av metall. Överst i ramen sitter en liten grön ädelsten och lyser svagt.
I mitten av fyrkanten finns det runor som lyser med en annan färg än den 
omgivande fyrkanten. Det står:

 > Redo för autentisering.
 > Säg ditt namn.
 \n""")
        r.screenMessageCnt += 1
        time.sleep(10)
    r.screenBusy = False

def screenReact(p,r,str):
    if r.screedOpened or r.screenMessageCnt < 5:
        return
    time.sleep(1)
    utils.out("\nRunorna på den lysande fyrkanten förändras.\n")
    r.addItem("runorna","Runor som lyser med en annan färg än den omgivande fyrkanten. Det står:\n\n > Hanterar användarinput.\n > Vänta...\n\n")
    r.addItem("fyrkanten|skärmen","""En blekt lysande fyrkant, nästan som en skärm, infälld i väggen. Runt den sitter
en ram av metall. Överst i ramen sitter en liten grön ädelsten och lyser svagt.
I mitten av fyrkanten finns det runor som lyser med en annan färg än den 
omgivande fyrkanten. Det står:

 > Hanterar användarinput.
 > Vänta...\n""")
    time.sleep(4)
    r.screenBusy = False
    if str == "byt användare":
        utils.out("\nRunorna på den lysande fyrkanten förändras igen.\n")
        r.addItem("runorna","Runor som lyser med en annan färg än den omgivande fyrkanten. Det står:\n\n > Redo för autentisering.\n > Säg ditt namn.\n\n")
        r.addItem("fyrkanten|skärmen","""En blekt lysande fyrkant, nästan som en skärm, infälld i väggen. Runt den sitter
en ram av metall. Överst i ramen sitter en liten grön ädelsten och lyser svagt.
I mitten av fyrkanten finns det runor som lyser med en annan färg än den 
omgivande fyrkanten. Det står:

 > Redo för autentisering.
 > Säg ditt namn.
 \n""")
        r.user = ""
        return
    if r.user:
        if hbsql.checkPassword(p,r.user,str):
            utils.out("\nDen lysande fyrkanten blinkar till och slocknar och avslöjar en liten nisch som var dold bakom den.\n")
            r.setDesc("""Du står i en liten källare. Runt omkring dig, längs alla väggar utom den högra,
står det lådor, tunnor och säckar av olika slag. En brant trappa leder upp till
en öppen lucka i taket. Golv och väggar består av plankor och en kraftig lukt 
av jord och fukt fyller luften. Ljuset här nere kommer från en en liten 
ädelsten som lyser ovanför en öppen nisch i en högra väggen.\n""")
            r.addItem("runorna","Fyrkanen har slocknat och försvunnit. Det syns inga runor längre.\n")
            r.addItem("fyrkanten|skärmen","Fyrkanten har slocknat och försvunnit och avslöjar en liten nisch som var dold\nbakom den.\n")
            r.addItem("nischen","Ett litet urgröpning i väggen där den lystande fyrkanten tidigare var. Det står\nett litet skrin i nischen.\n")
            r.addItem("skrinet","Ett litet skrin som ser ut att sitta fast i nischen. På framsidan av det kan du\nse fyra hjul med siffror på.\n")
            r.screedOpened = True
            return

        utils.out("\nRunorna på den lysande fyrkanten förändras igen.\n")
        r.addItem("runorna",f'Runor som lyser med en annan färg än den omgivande fyrkanten. Det står:\n\n > Felaktigt lösenord!\n > Välkommen användare: {r.user}\n > För att öppna, säg ditt lösenord.\n > För byta användare, säg \"byt användare\".\n\n')
        r.addItem("fyrkanten|skärmen",f"""En blekt lysande fyrkant, nästan som en skärm, infälld i väggen. Runt den sitter
en ram av metall. Överst i ramen sitter en liten grön ädelsten och lyser svagt.
I mitten av fyrkanten finns det runor som lyser med en annan färg än den 
omgivande fyrkanten. Det står:

 > Felaktigt lösenord!
 > Välkommen användare: {r.user}
 > För att öppna, säg ditt lösenord.
 > För byta användare, säg \"byt användare\".
 \n""")
        return
      
    if hbsql.checkUser(p,str):
        utils.out("\nRunorna på den lysande fyrkanten förändras igen.\n")
        r.addItem("runorna",f'Runor som lyser med en annan färg än den omgivande fyrkanten. Det står:\n\n > Välkommen användare: {str}\n > För att öppna, säg ditt lösenord.\n > För byta användare, säg \"byt användare\".\n\n')
        r.addItem("fyrkanten|skärmen",f"""En blekt lysande fyrkant, nästan som en skärm, infälld i väggen. Runt den sitter
en ram av metall. Överst i ramen sitter en liten grön ädelsten och lyser svagt.
I mitten av fyrkanten finns det runor som lyser med en annan färg än den 
omgivande fyrkanten. Det står:

 > Välkommen användare: {str}
 > För att öppna, säg ditt lösenord.
 > För byta användare, säg \"byt användare\".
 \n""")
        r.user = str
        return
    utils.out("\nRunorna på den lysande fyrkanten förändras igen.\n")
    r.addItem("runorna","Runor som lyser med en annan färg än den omgivande fyrkanten. Det står:\n\n > Okänt användarnamn.\n > Redo för autentisering.\n > Säg ditt namn.\n\n")
    r.addItem("fyrkanten|skärmen","""En blekt lysande fyrkant, nästan som en skärm, infälld i väggen. Runt den sitter
en ram av metall. Överst i ramen sitter en liten grön ädelsten och lyser svagt.
I mitten av fyrkanten finns det runor som lyser med en annan färg än den 
omgivande fyrkanten. Det står:

 > Okänt användarnamn.
 > Redo för autentisering.
 > Säg ditt namn.
 \n""")
    return
        
class FlaggPlate(item.ReadItem):
    def __init__(self,iid,name,desc):
        f = open("flag.txt","r")
        text = f.read()
        f.close()
        super().__init__(iid,name,desc,f'Min största hemlighet är:\n {text}\n/Harald\n')

    def flagFound(self,plr):
        # Player found the flag!
        return

class Room4(Room):
    def __init__(self):
        super().__init__()
        self.user = "" 
        self.screenMessageCnt = 0
        self.boxesMoved = False
        self.screenActivated = False
        self.screenBusy = False
        self.screedOpened = False
        self.wheel1 = 0
        self.wheel2 = 0
        self.wheel3 = 0
        self.wheel4 = 0
        self.boxOpened = False
        self.plateTaken = False
        super().setDesc("""Du står i en liten källare. Runt omkring dig, längs alla väggar, står det 
lådor, tunnor och säckar av olika slag. En brant trappa leder upp till en öppen
lucka i taket. Golv och väggar består av plankor och en kraftig lukt av jord 
och fukt fyller luften. Det finns ingen ljuskälla här nere och ljuset som 
faller in genom luckan övanför dig borde inte vara tillräckligt för att lysa 
upp rummet, men ett underligt blekt sken med oklart ursprung gör ändå att du 
kan se.\n""")
        super().addItem("rummet|källaren","Rummet är ganska litet och fyllt med massa lådor, säckar och tunnor.\n")
        super().addItem("tunnorna|säckarna","Massa tunnor och säckar står huller om buller i rummet.\n")
        super().addItem("lådorna","Massor av lådor står uppställda mot den högra väggen. Det bleka ljuset verkar\nkomma från något bakom dem. Du kanske kan flytta på dem för att se vad som\norsakar det?\n")
        super().addItem("luckan|trappan","En trappa leder upp till luckan i taket. Du kan gå upp för den för att komma ut ur källaren igen.\n")
        super().addItem("golvet|väggarna","Golvet och väggarna är gjorda av plankor. Genom gliporna mellan dem kan du se\nden mörka, fuktiga jorden. Den högra väggen är nästan helt täckt av lådor, så\nden ser du inte mycket av.\n")
        super().addItem("väggen|högra väggen","Den högra väggen är nästan helt täck av lådor. Det verkar nästan som om det\nbleka ljuset är starkare i den änden av rummet.\n")
        super().addItem("gliporna|jorden","Du ser den mörka jorden i gliporna mellan plankorna som väggarna och golvet är gjorda av.\n")
        super().addItem("plankorna","Grova plankor som slipats släta av åren.\n")
        super().addItem("ljuskällan","Det är svårt att avgöra var det bleka ljuset kommer ifrån.\n")
        super().addItem("skenet|ljuset|bleka ljuset|bleka skenet","Ett blekt, kallt sken, nästan vitt. Det verkar komma från den högra delen av rummet.\n")

    def queryAction(self,plr,str):
        if str == "flytta på lådorna" or str == "flytta undan lådorna" or str == "flytta lådorna":
            if self.boxesMoved:
                return "Du har redan flyttat undan lådorna. Det verkar onödigt att ställa tillbaka dem.\n"
            self.boxesMoved = True

            super().setDesc("""Du står i en liten källare. Runt omkring dig, längs alla väggar utom den högra,
står det lådor, tunnor och säckar av olika slag. En brant trappa leder upp till
en öppen lucka i taket. Golv och väggar består av plankor och en kraftig lukt 
av jord och fukt fyller luften. Ljuset här nere kommer från en fyrkant av okänt
material, infälld i den högra väggen, som lyser med ett blek sken.\n""")

            super().addItem("tunnorna|säckarna","Massa lådor, tunnor och säckar står huller om buller över allt i rummet utom längs den högra väggen.\n")
            super().addItem("lådorna","Massor av lådor, tunnor och säckar står huller om buller över allt i rummet utom\nlängs den högra väggen.\n")
            super().addItem("golvet|väggarna","Golvet och väggarna är gjorda av plankor. Genom gliporna mellan dem kan du se\nden mörka, fuktiga jorden. I den högra väggen finns en blekt lysande fyrkant infälld.\n")
            super().addItem("väggen|högra väggen","Den högra väggen är gjord av samma plankor som resten av väggarna men en bit upp\npå väggen finns en fyrkant av något okänt material infälld.\n")
            super().addItem("ljuskällan","Det bleka ljuset kommer från den högra väggen.\n")
            super().addItem("skenet|ljuset|bleka ljuset|bleka skenet","Ett blekt, kallt sken, nästan vitt. Det kommer från den högra delen av rummet.\n")

            super().addItem("fyrkanten|skärmen","En blekt lysande fyrkant infälld i väggen. Runt den sitter en ram av metall.\nÖverst i ramen verkar det finnas ett litet hål.\n")
            super().addItem("materialet","Det är svårt att avgöra vad det är för slags material. Det ser nästan\ngenomskinligt ut, som om det var gjort av ljus.\n")
            super().addItem("ramen","En ram av metall runt den lysande fyrkanten. Överst i ramen finns det ett litet hål.\n")
            super().addItem("hålet","Ett litet hål längs upp i ramen. Det är format som en åttahörning och är mycket påtagligt tomt.\n")

            return "Du flyttar mödosamt undan lådorna från den högra väggen och bakom dem finns en\nsvagt lysande fyrkant, ungefär en gånger en meter, en bit upp på väggen.\n"
        if str == "tryck in ädelstenen i hålet" or str == "stoppa in ädelstenen i hålet" or str == "stoppa ädelstenen i hålet" or str == "för in ädelstenen i hålet" or str == "sätt in ädelstenen i hålet" or str == "sätt ädelstenen i hålet":
            if not self.boxesMoved:
                return super().queryAction(plr,str)
            if self.screenActivated:
                return "Ädelstenen sitter redan i hålet.\n"
            i = plr.getItem("ädelstenen")
            if not i:
                return "Om du ändå bara hade en passande ädelsten.\n"

            plr.removeItem(i)
            self.screenActivated = True

            super().addItem("fyrkanten|skärmen","En blekt lysande fyrkant, nästan som en skärm, infälld i väggen. Runt den sitter\nen ram av metall. Överst i ramen sitter en liten grön ädelsten och lyser svagt.\n")
            super().addItem("ramen","En ram av metall runt den lysande fyrkanten. Överst i ramen sitter en liten grön ädelsten och lyser svagt.\n")
            super().addItem("hålet","Det sitter en liten grön ädelsten i hålet och lyser svart.\n")
            super().addItem("ädelstenen","Den lilla ädelstenen i väggen lyser med ett svagt sken.\n")

            t = threading.Thread(target=screenMessages,args=(plr,self, ))
            t.start()
        
            return "Du trycker in den lilla ädelstenen i hålet i ramen och den börjar omedelbart lysa.\n"
        args = str.split(" ",1)
        if args:
            if args[0] == "vrid":
                if not self.screedOpened:
                    return super().queryAction(plr,str)
                if len(args) < 2:
                    return "Vad försöker du vrida? Första, andra, tredje eller fjärde hjulet?\n"
                # Wheel 1
                if args[1] == "första hjulet upp" or args[1] == "första hjulet uppåt":
                    if self.wheel1 == 9:
                        self.wheel1 = 0
                    else:
                        self.wheel1 += 1
                    return f'Du vrider första hjulet uppåt, till {self.wheel1}\n'
                if args[1] == "första hjulet ned" or args[1] == "första hjulet nedåt":
                    if self.wheel1 == 0:
                        self.wheel1 = 9
                    else:
                        self.wheel1 -= 1
                    return f'Du vrider första hjulet nedåt till {self.wheel1}\n'
                # Wheel 2
                if args[1] == "andra hjulet upp" or args[1] == "andra hjulet uppåt":
                    if self.wheel2 == 9:
                        self.wheel2 = 0
                    else:
                        self.wheel2 += 1
                    return f'Du vrider andra hjulet uppåt till {self.wheel2}\n'
                if args[1] == "andra hjulet ned" or args[1] == "andra hjulet nedåt":
                    if self.wheel2 == 0:
                        self.wheel2 = 9
                    else:
                        self.wheel2 -= 1
                    return f'Du vrider andra hjulet uppåt till {self.wheel2}\n'
                # Wheel 3
                if args[1] == "tredje hjulet upp" or args[1] == "tredje hjulet uppåt":
                    if self.wheel3 == 9:
                        self.wheel3 = 0
                    else:
                        self.wheel3 += 1
                    return f'Du vrider tredje hjulet uppåt till {self.wheel3}\n'
                if args[1] == "tredje hjulet ned" or args[1] == "tredje hjulet nedåt":
                    if self.wheel3 == 0:
                        self.wheel3 = 9
                    else:
                        self.wheel3 -= 1
                    return f'Du vrider tredje hjulet nedåt till {self.wheel3}\n'
                # Wheel 4
                if args[1] == "fjärde hjulet upp" or args[1] == "fjärde hjulet uppåt":
                    if self.wheel4 == 9:
                        self.wheel4 = 0
                    else:
                        self.wheel4 += 1
                    return f'Du vrider fjärde hjulet uppåt till {self.wheel4}\n'
                if args[1] == "fjärde hjulet ned" or args[1] == "fjärde hjulet nedåt":
                    if self.wheel4 == 0:
                        self.wheel4 = 9
                    else:
                        self.wheel4 -= 1
                    return f'Du vrider fjärde hjulet nedåt till {self.wheel1}\n'
                return "Försöker du vrida första, andra, tredje eller fjärde hjulet uppåt eller nedåt?\n"
        if str == "öppna skrinet":
            if not self.screedOpened:
                return super().queryAction(plr,str)
            if self.wheel1 != 8 or self.wheel2 != 1 or self.wheel3 != 2 or self.wheel4 != 5:
                return "Du försöker öppna skrinet, men det verkar vara låst.\n"
            self.boxOpened = True
            super().addItem("skrinet","Ett litet skrin som ser ut att sitta fast i nischen. Locket är öppet och du kan\nse en liten bronsplatta ligga i skrinet. På framsidan av det kan du se fyra hjul\nmed siffror på.\n")
            super().addItem("plattan|bronsplattan","En liten bronsplatta som ligger i skrinet. Du kanske kan ta den?\n")
            return "Du fäller upp locket på det lilla skrinet.\n"
        return super().queryAction(plr,str)

    def queryItem(self,str):
        if self.screedOpened and str == "siffrorna" or str == "hjulen":
            return f'De små hjulen på skrinet är inställda på {self.wheel1}-{self.wheel2}-{self.wheel3}-{self.wheel4}.\nDet ser ut som att du kan vrida hjulen upp eller ner för att ändra siffrorna.\n'            
        return super().queryItem(str)

    def say(self,plr,str):
        if self.screenBusy or self.screedOpened:
            return
        self.screenBusy = True
        t = threading.Thread(target=screenReact,args=(plr,self,str, ))
        t.start()
        return

    def take(self,plr,str):
        if str == "bronsplattan" or str == "bronsplattan från skrinet" or str == "plattan" or str == "plattan från skrinet":
            if not self.boxOpened or self.plateTaken:
                return super().take(plr,str)
            super().addItem("skrinet","Ett litet skrin som ser ut att sitta fast i nischen. Locket är öppet men skrinet\nser tomt ut. På framsidan av det kan du se fyra hjul med siffror på.\n")
            super().removeItem("plattan|bronsplattan")
            self.plateTaken = True
            plr.addItem(FlaggPlate("plattan|bronsplattan","En liten bronsplatta","En blankpolerad platta av brons. Det står något skrivet på den.\n"))
            return "Du plockar upp en lilla bronsplattan ur skrinet.\n"
        return super().take(plr,str)


    def move(self,str):
        if str == "upp" or str == "upp genom luckan" or str == "upp för trappan" or str == "upp ur källaren":
            return 2, "Försiktigt klättrar du upp för trappan och upp genom luckan.\n"
        return super().move(str)
