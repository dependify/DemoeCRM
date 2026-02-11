"""
Nigerian Data Generators for Evangelism CRM Demo
Contains realistic Nigerian names, locations, churches, and contact information.
"""

import random
from datetime import datetime, timedelta, date
from typing import List, Dict, Any, Optional
import uuid

# =============================================================================
# NIGERIAN NAMES DATA
# =============================================================================

NIGERIAN_FIRST_NAMES_MALE = [
    "Emmanuel", "Daniel", "Samuel", "David", "John", "Joseph", "Michael", "James",
    "Peter", "Paul", "Stephen", "Matthew", "Andrew", "Thomas", "Simon", "Timothy",
    "Abraham", "Isaac", "Jacob", "Moses", "Joshua", "Caleb", "Aaron", "Elijah",
    "Elisha", "Isaiah", "Jeremiah", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah",
    "Chinedu", "Chukwuemeka", "Obinna", "Chukwudi", "Chigozie", "Chima", "Chidi",
    "Ifeanyi", "Uchenna", "Uzoma", "Ugochukwu", "Uzochukwu", "Tochukwu", "Kelechi",
    "Olumide", "Olusegun", "Oluseun", "Olufemi", "Olumide", "Oluwasegun", "Oluwaseyi",
    "Oluwaseun", "Oluwafemi", "Oluwatosin", "Oluwatobi", "Oluwagbenga", "Oluwadamilare",
    "Adeola", "Adebayo", "Ademola", "Adeyemi", "Adewale", "Adegoke", "Adetokunbo",
    "Yakubu", "Yusuf", "Ibrahim", "Abubakar", "Mustapha", "Musa", "Suleiman", "Haruna",
    "Fatih", "Khalid", "Omar", "Bashir", "Aminu", "Kabir", "Umar", "Jibril",
    "Bamidele", "Ayodele", "Ayotunde", "Ayo", "Tunde", "Dele", "Wale", "Femi",
    "Kunle", "Segun", "Tosin", "Tayo", "Gbenga", "Gbadebo", "Bankole", "Akin",
    "Akintunde", "Akinwale", "Akinola", "Akinyemi", "Akinsola", "Akintayo"
]

NIGERIAN_FIRST_NAMES_FEMALE = [
    "Mary", "Sarah", "Elizabeth", "Grace", "Joy", "Peace", "Patience", "Faith",
    "Hope", "Charity", "Mercy", "Blessing", "Favour", "Gift", "Glory", "Precious",
    "Deborah", "Esther", "Ruth", "Hannah", "Abigail", "Rebecca", "Rachel", "Leah",
    "Martha", "Mary", "Anna", "Dorcas", "Lydia", "Priscilla", "Phoebe", "Junia",
    "Chioma", "Chidinma", "Chiamaka", "Chinonso", "Chinyere", "Chizoba", "Chinelo",
    "Ifeoma", "Ifeyinwa", "Ngozi", "Nkechi", "Nkiruka", "Nkem", "Adaeze", "Adaobi",
    "Oluchi", "Olufunke", "Olufunmilayo", "Oluremi", "Oluwatoyin", "Oluwakemi",
    "Oluwaseun", "Oluwafunmilayo", "Oluwatobi", "Oluwadamilola", "Oluwabusola",
    "Adebimpe", "Adebisi", "Adenike", "Adebola", "Adetutu", "Adepeju", "Aderonke",
    "Aisha", "Fatima", "Halima", "Hauwa", "Khadija", "Maryam", "Nafisa", "Rahila",
    "Safiya", "Zainab", "Amina", "Asmau", "Balaraba", "Fadila", "Hafsah", "Jamila",
    "Ayomide", "Ayobami", "Ayotunde", "Ayo", "Tunde", "Deborah", "Wunmi", "Funmi",
    "Kemi", "Segun", "Tosin", "Tayo", "Bimbo", "Bimpe", "Banke", "Akin",
    "Akindele", "Akinola", "Akintunde", "Akinsola", "Akintayo", "Akinwale"
]

NIGERIAN_LAST_NAMES = [
    # Yoruba Surnames
    "Adeyemi", "Adeleke", "Adekunle", "Adesanya", "Adewale", "Adegoke", "Adetokunbo",
    "Adebayo", "Adebisi", "Adeniyi", "Adejumo", "Aderemi", "Adesina", "Adewumi",
    "Adeyinka", "Adeoye", "Adetunji", "Adelaja", "Adegbola", "Adegbite", "Adekanbi",
    "Ogunlesi", "Ogunsanya", "Ogundele", "Ogunwale", "Oguntade", "Ogunleye",
    "Ogunjobi", "Ogunnaike", "Ogunyemi", "Ogunrinde", "Ogunremi", "Ogunjimi",
    "Fashola", "Fasina", "Fasoro", "Fasusi", "Fasanya", "Fasonu", "Fasiku",
    "Bakare", "Balogun", "Bankole", "Bamidele", "Bamgbose", "Bamiro", "Bamtefa",
    "Oyediran", "Oyekan", "Oyelaran", "Oyelese", "Oyeleye", "Oyeniyi", "Oyewole",
    "Olaniyi", "Olaniran", "Olanipekun", "Olarewaju", "Olatunji", "Olatunde", "Olaoye",
    "Oni", "Onifade", "Onigbinde", "Oniyide", "Onipede", "Onipede", "Oniwinde",
    "Ojo", "Ojikutu", "Ojewale", "Ojoawo", "Ojogbon", "Ojutiku", "Ojulari",
    "Okunola", "Okunowo", "Okuneye", "Okungbowa", "Okunlola", "Okunola", "Okunniyi",
    "Oladipo", "Oladimeji", "Oladokun", "Oladoyin", "Oladunni", "Oladunjoye", "Oladapo",
    "Olajide", "Olajire", "Olajubu", "Olajumoke", "Olakunle", "Olalere", "Olamiju",
    "Olanrewaju", "Olatidoye", "Olatubosun", "Olatunbosun", "Olawale", "Olayemi",
    "Olowe", "Olowolayemo", "Olowookere", "Olowookorun", "Olowu", "Olowolagba",
    "Oshodi", "Oshin", "Oshinaike", "Osho", "Oshodi", "Oshungbure", "Oshuntokun",
    "Shonibare", "Shonubi", "Shonukan", "Shosanya", "Shoyombo", "Shoyinka",
    "Soyinka", "Soyombo", "Soyoye", "Soyelu", "Soyemi", "Soyannwo", "Soyele",
    "Ajao", "Ajala", "Ajani", "Ajayi", "Ajibade", "Ajibola", "Ajiboye", "Ajiboye",
    "Akindele", "Akinkugbe", "Akinleye", "Akinlade", "Akinmuda", "Akinola", "Akinpelu",
    "Akintola", "Akintunde", "Akinwale", "Akinwande", "Akinwumi", "Akinwunmi",
    "Akiode", "Akinyele", "Akinyemi", "Akintayo", "Akintola", "Akintunde",
    # Igbo Surnames
    "Okonkwo", "Okorie", "Okoro", "Okoye", "Okparaeke", "Okpara", "Okpalaugo",
    "Nnamdi", "Nnaji", "Nnadi", "Nnamani", "Nwagwu", "Nwachukwu", "Nwadike",
    "Nwaeze", "Nwagu", "Nwaiwu", "Nwaji", "Nwaka", "Nwakali", "Nwakanma",
    "Nwankwo", "Nwaogu", "Nwaogwugwu", "Nwaoha", "Nwaokolo", "Nwaokorie", "Nwaokocha",
    "Obi", "Obiakoeze", "Obialo", "Obiano", "Obienu", "Obika", "Obikwelu",
    "Okafor", "Okagbue", "Okala", "Okam", "Okani", "Okaro", "Okereafor",
    "Onu", "Onuoha", "Onukogu", "Onukwube", "Onuma", "Onungwa", "Onuigbo",
    "Eze", "Ezeani", "Ezeanya", "Ezebuiro", "Ezechukwu", "Ezeji", "Ezekwesili",
    "Ibe", "Ibeanu", "Ibegbulem", "Ibeji", "Ibekwe", "Ibenegbu", "Ibeneme",
    "Ude", "Udeagha", "Udeaja", "Udechukwu", "Udedibia", "Udegbunam", "Udeh",
    "Ugochukwu", "Ugoji", "Ugokwe", "Ugonna", "Ugoo", "Ugorji", "Ugwoke",
    "Okeke", "Okechukwu", "Okeke", "Okereke", "Okerenkegh", "Okere", "Okezie",
    "Chukwu", "Chukwudi", "Chukwuemeka", "Chukwuma", "Chukwumerije", "Chukwunyere",
    "Anya", "Anyanwu", "Anyaso", "Anyiam", "Anyaebosi", "Anyanwu", "Anyasor",
    "Madu", "Maduabuchi", "Madubuike", "Madueke", "Maduka", "Madukwe", "Madumere",
    "Ike", "Ikegwuonu", "Ikeji", "Ikekpeazu", "Ikemefuna", "Ikenna", "Ikeobi",
    "Uche", "Uchechukwu", "Uchegbu", "Uchendu", "Uchenna", "Uchenna", "Ucheoma",
    # Hausa/Fulani Surnames
    "Abdullahi", "Abubakar", "Adamu", "Ahmad", "Aliyu", "Aminu", "Atiku", "Bala",
    "Bashir", "Bello", "Danjuma", "Dauda", "Gambo", "Garba", "Gidado", "Goni",
    "Habib", "Hadi", "Hafiz", "Haliru", "Hamza", "Hassan", "Husaini", "Ibrahim",
    "Idris", "Isa", "Ismail", "Jafaru", "Jamilu", "Jibril", "Kabir", "Kaita",
    "Khalid", "Lawan", "Liman", "Maccido", "Madu", "Mahmud", "Mai", "Maikudi",
    "Mallam", "Mamman", "Modibbo", "Mohammed", "Musa", "Mustapha", "Nuhu",
    "Rabiu", "Sabo", "Sadiq", "Saidu", "Salihu", "Sani", "Shehu", "Suleiman",
    "Tijjani", "Umar", "Usman", "Yahaya", "Yakubu", "Yusuf", "Zakari", "Zubairu",
    # Other Nigerian Names
    "Peters", "Johnson", "Williams", "Davies", "Robinson", "Thompson", "Evans",
    "Walker", "White", "Green", "Hall", "Lewis", "Jackson", "Clarke"
]

# =============================================================================
# NIGERIAN LOCATIONS
# =============================================================================

NIGERIAN_STATES_LGAS = {
    "Lagos": {
        "capital": "Ikeja",
        "lgas": ["Ikeja", "Alimosho", "Ojo", "Mushin", "Ikorodu", "Eti-Osa", "Kosofe", 
                 "Apapa", "Ifako-Ijaiye", "Somolu", "Amuwo-Odofin", "Lagos Mainland",
                 "Ibeju-Lekki", "Agege", "Badagry", "Oshodi-Isolo", "Surulere", "Ajeromi-Ifelodun"],
        "areas": ["Victoria Island", "Lekki", "Ikoyi", "Yaba", "Surulere", "Ikeja GRA",
                  "Maryland", "Ogba", "Ojodu", "Magodo", "Gbagada", "Anthony", "Ilupeju",
                  "Festac", "Satellite Town", "Okota", "Isolo", "Ejigbo", "Shomolu",
                  "Bariga", "Akoka", "Igando", "Iyana Ipaja", "Egbeda", "Idimu", "Alakuko"]
    },
    "Oyo": {
        "capital": "Ibadan",
        "lgas": ["Ibadan North", "Ibadan South-West", "Ibadan South-East", "Ibadan North-West",
                 "Ibadan North-East", "Ogbomosho North", "Ogbomosho South", "Oyo East", "Oyo West",
                 "Saki East", "Saki West", "Iseyin", "Kajola", "Ibarapa East", "Ibarapa North",
                 "Ibarapa Central", "Orelope", "Olorunsogo", "Itesiwaju", "Iwajowa"],
        "areas": ["Bodija", "Moniya", "Eleyele", "Dugbe", "Mokola", "Sango", "Ojoo",
                  "Challenge", "Ring Road", "Moniya", "Apata", "Idi-Ape", "Oke-Ado",
                  "Molete", "Beere", "Oje", "Agodi", "Gate", "Jericho", "Onireke"]
    },
    "Ogun": {
        "capital": "Abeokuta",
        "lgas": ["Abeokuta North", "Abeokuta South", "Ado-Odo/Ota", "Ewekoro", "Ifo",
                 "Ijebu East", "Ijebu North", "Ijebu North East", "Ijebu Ode", "Ikenne",
                 "Imeko Afon", "Ipokia", "Obafemi Owode", "Odeda", "Odogbolu", "Remo North",
                 "Sagamu", "Yewa North", "Yewa South"],
        "areas": ["Sango-Ota", "Ijoko", "Agbara", "Atan", "Ifo", "Abeokuta", "Sagamu",
                  "Ijebu Ode", "Ilaro", "Ipokia", "Idiroko", "Ayetoro", "Imeko"]
    },
    "Ondo": {
        "capital": "Akure",
        "lgas": ["Akoko North-East", "Akoko North-West", "Akoko South-East", "Akoko South-West",
                 "Akure North", "Akure South", "Ese-Odo", "Idanre", "Ifedore", "Ilaje",
                 "Ile-Oluji/Okeigbo", "Irele", "Odigbo", "Okitipupa", "Ondo East", "Ondo West",
                 "Ose", "Owo"],
        "areas": ["Akure", "Ondo", "Owo", "Ikare", "Okitipupa", "Ile-Oluji", "Idanre",
                  "Oba-Akoko", "Ikare", "Arigidi", "Epinmi", "Ifon", "Igbokoda"]
    },
    "Osun": {
        "capital": "Osogbo",
        "lgas": ["Aiyedaade", "Aiyedire", "Atakunmosa East", "Atakunmosa West", "Boluwaduro",
                 "Boripe", "Ede North", "Ede South", "Egbedore", "Ejigbo", "Ife Central",
                 "Ife East", "Ife North", "Ife South", "Ifedayo", "Ifelodun", "Ila",
                 "Ilesa East", "Ilesa West", "Irepodun", "Irewole", "Isokan", "Iwo",
                 "Obokun", "Odo Otin", "Ola Oluwa", "Olorunda", "Oriade", "Orolu"],
        "areas": ["Osogbo", "Ile-Ife", "Ilesa", "Iwo", "Ejigbo", "Ikire", "Ila-Orangun",
                  "Ede", "Ikirun", "Ipetumodu", "Apomu", "Ode-Omu"]
    },
    "Ekiti": {
        "capital": "Ado-Ekiti",
        "lgas": ["Ado-Ekiti", "Efon", "Ekiti East", "Ekiti South-West", "Ekiti West",
                 "Emure", "Gbonyin", "Ido-Osi", "Ijero", "Ikere", "Ikole", "Ilejemeje",
                 "Irepodun/Ifelodun", "Ise/Orun", "Moba", "Oye"],
        "areas": ["Ado-Ekiti", "Ikere", "Ijero", "Oye", "Ikole", "Emure", "Ise", "Aramoko"]
    },
    "Kwara": {
        "capital": "Ilorin",
        "lgas": ["Asa", "Baruten", "Edu", "Ekiti", "Ifelodun", "Ilorin East", "Ilorin South",
                 "Ilorin West", "Irepodun", "Isin", "Kaiama", "Moro", "Offa", "Oke Ero",
                 "Oyun", "Pategi"],
        "areas": ["Ilorin", "Offa", "Omu-Aran", "Patigi", "Lafiagi", "Share"]
    },
    "Kano": {
        "capital": "Kano",
        "lgas": ["Ajingi", "Albasu", "Bagwai", "Bebeji", "Bichi", "Bunkure", "Dala",
                 "Dambatta", "Dawakin Kudu", "Dawakin Tofa", "Doguwa", "Fagge", "Gabasawa",
                 "Garko", "Garun Mallam", "Gaya", "Gezawa", "Gwale", "Gwarzo", "Kabo",
                 "Kano Municipal", "Karaye", "Kibiya", "Kiru", "Kumbotso", "Kunchi",
                 "Kura", "Madobi", "Makoda", "Minjibir", "Nasarawa", "Rano", "Rimin Gado",
                 "Rogo", "Shanono", "Sumaila", "Takai", "Tarauni", "Tofa", "Tsanyawa",
                 "Tudun Wada", "Ungogo", "Warawa", "Wudil"],
        "areas": ["Nasarawa GRA", "Bompai", "Sabon Gari", "Fagge", "Gwale", "Dala",
                  "Kano Municipal", "Tarauni", "Nasarawa", "Ungogo", "Fagge"]
    },
    "Kaduna": {
        "capital": "Kaduna",
        "lgas": ["Birnin Gwari", "Chikun", "Giwa", "Igabi", "Ikara", "Jaba", "Jema'a",
                 "Kachia", "Kaduna North", "Kaduna South", "Kagarko", "Kajuru", "Kaura",
                 "Kauru", "Kubau", "Kudan", "Lere", "Makarfi", "Sabon Gari", "Sanga",
                 "Soba", "Zangon Kataf", "Zaria"],
        "areas": ["Kaduna", "Zaria", "Kafanchan", "Barnawa", "Ungwan Rimi", "Tudun Wada",
                  "Sabon Tasha", "Kakuri", "Kawo", "Rigasa", "Sabo"]
    },
    "Katsina": {
        "capital": "Katsina",
        "lgas": ["Bakori", "Batagarawa", "Batsari", "Baure", "Bindawa", "Charanchi",
                 "Dan Musa", "Dandume", "Danja", "Daura", "Dutsi", "Dutsin Ma", "Faskari",
                 "Funtua", "Ingawa", "Jibia", "Kafur", "Kaita", "Kankara", "Kankia",
                 "Katsina", "Kurfi", "Kusada", "Mai'Adua", "Malumfashi", "Mani",
                 "Mashi", "Matazu", "Musawa", "Rimi", "Sabuwa", "Safana", "Sandamu",
                 "Zango"],
        "areas": ["Katsina", "Daura", "Funtua", "Malumfashi", "Kankia", "Jibia"]
    },
    "Borno": {
        "capital": "Maiduguri",
        "lgas": ["Abadam", "Askira/Uba", "Bama", "Bayo", "Biu", "Chibok", "Damboa",
                 "Dikwa", "Gubio", "Guzamala", "Gwoza", "Hawul", "Jere", "Kaga",
                 "Kala/Balge", "Konduga", "Kukawa", "Kwaya Kusar", "Mafa", "Magumeri",
                 "Maiduguri", "Marte", "Mobbar", "Monguno", "Ngala", "Nganzai", "Shani"],
        "areas": ["Maiduguri", "Biu", "Monguno", "Gwoza", "Bama", "Dikwa", "Konduga"]
    },
    "Rivers": {
        "capital": "Port Harcourt",
        "lgas": ["Abua/Odual", "Ahoada East", "Ahoada West", "Akuku-Toru", "Andoni",
                 "Asari-Toru", "Bonny", "Degema", "Eleme", "Emohua", "Etche", "Gokana",
                 "Ikwerre", "Khana", "Obio/Akpor", "Ogba/Egbema/Ndoni", "Ogu/Bolo",
                 "Okrika", "Omuma", "Opobo/Nkoro", "Oyigbo", "Port Harcourt", "Tai"],
        "areas": ["Port Harcourt", "Obio-Akpor", "Trans Amadi", "Rumukrushi", "Woji",
                  "Rumuomasi", "Diobu", "Borokiri", "Aggrey", "Old GRA", "New GRA"]
    },
    "Delta": {
        "capital": "Asaba",
        "lgas": ["Aniocha North", "Aniocha South", "Bomadi", "Burutu", "Ethiope East",
                 "Ethiope West", "Ika North East", "Ika South", "Isoko North", "Isoko South",
                 "Ndokwa East", "Ndokwa West", "Okpe", "Oshimili North", "Oshimili South",
                 "Patani", "Sapele", "Udu", "Ughelli North", "Ughelli South", "Ukwuani",
                 "Uvwie", "Warri North", "Warri South", "Warri South West"],
        "areas": ["Asaba", "Warri", "Sapele", "Ughelli", "Ozoro", "Agbor", "Oleh",
                  "Effurun", "Udu", "Ovwian", "Aladja", "Oghara"]
    },
    "Edo": {
        "capital": "Benin City",
        "lgas": ["Akoko-Edo", "Egor", "Esan Central", "Esan North-East", "Esan South-East",
                 "Esan West", "Etsako Central", "Etsako East", "Etsako West", "Igueben",
                 "Ikpoba Okha", "Orhionmwon", "Oredo", "Ovia North-East", "Ovia South-West",
                 "Owan East", "Owan West", "Uhunmwonde"],
        "areas": ["Benin City", "Auchi", "Ekpoma", "Uromi", "Sabongida-Ora", "Igarra"]
    },
    "Enugu": {
        "capital": "Enugu",
        "lgas": ["Aninri", "Awgu", "Enugu East", "Enugu North", "Enugu South", "Ezeagu",
                 "Igbo Etiti", "Igbo Eze North", "Igbo Eze South", "Isi Uzo", "Nkanu East",
                 "Nkanu West", "Nsukka", "Oji River", "Udenu", "Udi", "Uzo-Uwani"],
        "areas": ["Enugu", "Nsukka", "Agbani", "Awgu", "Udi", "Oji River", "Ngwo"]
    },
    "Anambra": {
        "capital": "Awka",
        "lgas": ["Aguata", "Anambra East", "Anambra West", "Anaocha", "Awka North",
                 "Awka South", "Ayamelum", "Dunukofia", "Ekwusigo", "Idemili North",
                 "Idemili South", "Ihiala", "Njikoka", "Nnewi North", "Nnewi South",
                 "Ogbaru", "Onitsha North", "Onitsha South", "Orumba North", "Orumba South",
                 "Oyi"],
        "areas": ["Onitsha", "Nnewi", "Awka", "Ekwulobia", "Ihiala", "Obosi", "Nkpor"]
    },
    "Imo": {
        "capital": "Owerri",
        "lgas": ["Aboh Mbaise", "Ahiazu Mbaise", "Ehime Mbano", "Ezinihitte", "Ideato North",
                 "Ideato South", "Ihitte/Uboma", "Ikeduru", "Isiala Mbano", "Isu", "Mbaitoli",
                 "Ngor Okpala", "Njaba", "Nkwerre", "Nwangele", "Obowo", "Oguta", "Ohaji/Egbema",
                 "Okigwe", "Orlu", "Orsu", "Oru East", "Oru West", "Owerri Municipal",
                 "Owerri North", "Owerri West"],
        "areas": ["Owerri", "Orlu", "Okigwe", "Oguta", "Mbaise", "Nkwerre", "Orji"]
    },
    "Abia": {
        "capital": "Umuahia",
        "lgas": ["Aba North", "Aba South", "Arochukwu", "Bende", "Ikwuano", "Isiala Ngwa North",
                 "Isiala Ngwa South", "Isuikwuato", "Obi Ngwa", "Ohafia", "Osisioma",
                 "Ugwunagbo", "Ukwa East", "Ukwa West", "Umuahia North", "Umuahia South",
                 "Umu Nneochi"],
        "areas": ["Aba", "Umuahia", "Ohafia", "Arochukwu", "Omoba", "Osisioma"]
    },
    "Akwa Ibom": {
        "capital": "Uyo",
        "lgas": ["Abak", "Eastern Obolo", "Eket", "Esit Eket", "Essien Udim", "Etim Ekpo",
                 "Etinan", "Ibeno", "Ibesikpo Asutan", "Ibiono Ibom", "Ika", "Ikono",
                 "Ikot Abasi", "Ikot Ekpene", "Ini", "Itu", "Mbo", "Mkpat Enin",
                 "Nsit Atai", "Nsit Ibom", "Nsit Ubium", "Obot Akara", "Okobo", "Onna",
                 "Oron", "Oruk Anam", "Udung Uko", "Ukanafun", "Uruan", "Urue Offong/Oruko",
                 "Uyo"],
        "areas": ["Uyo", "Eket", "Ikot Ekpene", "Oron", "Abak", "Etinan", "Ikot Abasi"]
    },
    "Cross River": {
        "capital": "Calabar",
        "lgas": ["Abi", "Akamkpa", "Akpabuyo", "Bakassi", "Bekwarra", "Biase", "Boki",
                 "Calabar Municipal", "Calabar South", "Etung", "Ikom", "Obanliku",
                 "Obubra", "Obudu", "Odukpani", "Ogoja", "Yakurr", "Yala"],
        "areas": ["Calabar", "Ikom", "Obudu", "Ogoja", "Ugep", "Obubra"]
    },
    "Plateau": {
        "capital": "Jos",
        "lgas": ["Barkin Ladi", "Bassa", "Bokkos", "Jos East", "Jos North", "Jos South",
                 "Kanam", "Kanke", "Langtang North", "Langtang South", "Mangu", "Mikang",
                 "Pankshin", "Qua'an Pan", "Riyom", "Shendam", "Wase"],
        "areas": ["Jos", "Bukuru", "Langtang", "Pankshin", "Shendam", "Mangu"]
    },
    "Niger": {
        "capital": "Minna",
        "lgas": ["Agaie", "Agwara", "Bida", "Borgu", "Bosso", "Chanchaga", "Edati",
                 "Gbako", "Gurara", "Katcha", "Kontagora", "Lapai", "Lavun", "Magama",
                 "Mariga", "Mashegu", "Mokwa", "Moya", "Paikoro", "Rafi", "Rijau",
                 "Shiroro", "Suleja", "Tafa", "Wushishi"],
        "areas": ["Minna", "Bida", "Suleja", "Kontagora", "New Bussa", "Lapai"]
    },
    "Sokoto": {
        "capital": "Sokoto",
        "lgas": ["Binji", "Bodinga", "Dange Shuni", "Gada", "Goronyo", "Gudu", "Gwadabawa",
                 "Illela", "Isa", "Kebbe", "Kware", "Rabah", "Sabon Birni", "Shagari",
                 "Silame", "Sokoto North", "Sokoto South", "Tambuwal", "Tangaza", "Tureta",
                 "Wamako", "Wurno", "Yabo"],
        "areas": ["Sokoto", "Tambuwal", "Gwadabawa", "Wamako", "Bodinga"]
    },
    "Zamfara": {
        "capital": "Gusau",
        "lgas": ["Anka", "Bakura", "Birnin Magaji/Kiyaw", "Bukkuyum", "Bungudu", "Gummi",
                 "Gusau", "Kaura Namoda", "Maradun", "Maru", "Shinkafi", "Talata Mafara",
                 "Chafe", "Zurmi"],
        "areas": ["Gusau", "Kaura Namoda", "Talata Mafara", "Anka", "Gummi"]
    },
    "Kebbi": {
        "capital": "Birnin Kebbi",
        "lgas": ["Aleiro", "Arewa Dandi", "Argungu", "Augie", "Bagudo", "Birnin Kebbi",
                 "Bunza", "Dandi", "Fakai", "Gwandu", "Jega", "Kalgo", "Koko/Besse",
                 "Maiyama", "Ngaski", "Sakaba", "Shanga", "Suru", "Wasagu/Danko", "Yauri",
                 "Zuru"],
        "areas": ["Birnin Kebbi", "Argungu", "Zuru", "Jega", "Yauri"]
    },
    "Yobe": {
        "capital": "Damaturu",
        "lgas": ["Bade", "Bursari", "Damaturu", "Fika", "Fune", "Geidam", "Gujba",
                 "Gulani", "Jakusko", "Karasuwa", "Machina", "Nangere", "Nguru",
                 "Potiskum", "Tarmuwa", "Yunusari", "Yusufari"],
        "areas": ["Damaturu", "Potiskum", "Gashua", "Nguru", "Geidam"]
    },
    "Adamawa": {
        "capital": "Yola",
        "lgas": ["Demsa", "Fufore", "Ganye", "Gayuk", "Girei", "Gombi", "Hong",
                 "Jada", "Lamurde", "Madagali", "Maiha", "Mayo-Belwa", "Michika",
                 "Mubi North", "Mubi South", "Numan", "Shelleng", "Song", "Toungo", "Yola North", "Yola South"],
        "areas": ["Yola", "Mubi", "Jimeta", "Numan", "Gombi", "Michika"]
    },
    "Taraba": {
        "capital": "Jalingo",
        "lgas": ["Ardo Kola", "Bali", "Donga", "Gashaka", "Gassol", "Ibi", "Jalingo",
                 "Karim Lamido", "Kurmi", "Lau", "Sardauna", "Takum", "Ussa", "Wukari",
                 "Yorro", "Zing"],
        "areas": ["Jalingo", "Wukari", "Bali", "Sardauna", "Gembu", "Zing"]
    },
    "Benue": {
        "capital": "Makurdi",
        "lgas": ["Ado", "Agatu", "Apa", "Buruku", "Gboko", "Guma", "Gwer East",
                 "Gwer West", "Katsina-Ala", "Konshisha", "Kwande", "Logo", "Makurdi",
                 "Obi", "Ogbadibo", "Ohimini", "Oju", "Okpokwu", "Otukpo", "Tarka",
                 "Ukum", "Ushongo", "Vandeikya"],
        "areas": ["Makurdi", "Otukpo", "Gboko", "Katsina-Ala", "Vandeikya", "Oju"]
    },
    "Ebonyi": {
        "capital": "Abakaliki",
        "lgas": ["Abakaliki", "Afikpo North", "Afikpo South", "Ebonyi", "Ezza North",
                 "Ezza South", "Ikwo", "Ishielu", "Ivo", "Izzi", "Ohaukwu", "Onicha"],
        "areas": ["Abakaliki", "Afikpo", "Onueke", "Ezza", "Ishielu"]
    },
    "Nasarawa": {
        "capital": "Lafia",
        "lgas": ["Akwanga", "Awe", "Doma", "Karu", "Keana", "Keffi", "Kokona",
                 "Lafia", "Nasarawa", "Nasarawa Egon", "Obi", "Toto", "Wamba"],
        "areas": ["Lafia", "Keffi", "Akwanga", "Nasarawa", "Karu", "Doma"]
    },
    "Gombe": {
        "capital": "Gombe",
        "lgas": ["Akko", "Balanga", "Billiri", "Dukku", "Funakaye", "Gombe", "Kaltungo",
                 "Kwami", "Nafada", "Shongom", "Yamaltu/Deba"],
        "areas": ["Gombe", "Kaltungo", "Billiri", "Dukku", "Nafada"]
    },
    "Bayelsa": {
        "capital": "Yenagoa",
        "lgas": ["Brass", "Ekeremor", "Kolokuma/Opokuma", "Nembe", "Ogbia", "Sagbama",
                 "Southern Ijaw", "Yenagoa"],
        "areas": ["Yenagoa", "Amassoma", "Brass", "Ogbia", "Sagbama"]
    },
    "Kogi": {
        "capital": "Lokoja",
        "lgas": ["Adavi", "Ajaokuta", "Ankpa", "Bassa", "Dekina", "Ibaji", "Idah",
                 "Igalamela-Odolu", "Ijumu", "Kabba/Bunu", "Kogi", "Lokoja", "Mopa-Muro",
                 "Ofu", "Ogori/Magongo", "Okehi", "Okene", "Olamaboro", "Omala", "Yagba East",
                 "Yagba West"],
        "areas": ["Lokoja", "Okene", "Anyigba", "Idah", "Kabba", "Ankpa"]
    },
    "FCT Abuja": {
        "capital": "Abuja",
        "lgas": ["Abaji", "Bwari", "Gwagwalada", "Kuje", "Kwali", "Municipal Area Council"],
        "areas": ["Wuse", "Garki", "Maitama", "Asokoro", "Jabi", "Utako", "Gwarinpa",
                  "Kubwa", "Lugbe", "Gwagwalada", "Bwari", "Kuje", "Nyanya", "Karu"]
    }
}

# =============================================================================
# NIGERIAN CHURCHES
# =============================================================================

NIGERIAN_CHURCHES = [
    # Pentecostal Churches
    {"name": "Living Faith Church (Winners Chapel)", "denomination": "Pentecostal", "headquarters": "Ota, Ogun State"},
    {"name": "Christ Embassy", "denomination": "Pentecostal", "headquarters": "Lagos"},
    {"name": "Mountain of Fire and Miracles Ministries", "denomination": "Pentecostal", "headquarters": "Lagos"},
    {"name": "Deeper Christian Life Ministry", "denomination": "Pentecostal", "headquarters": "Lagos"},
    {"name": "Daystar Christian Centre", "denomination": "Pentecostal", "headquarters": "Lagos"},
    {"name": "House on the Rock", "denomination": "Pentecostal", "headquarters": "Lagos"},
    {"name": "The Fountain of Life Church", "denomination": "Pentecostal", "headquarters": "Lagos"},
    {"name": "Covenant Christian Centre", "denomination": "Pentecostal", "headquarters": "Lagos"},
    {"name": "This Present House", "denomination": "Pentecostal", "headquarters": "Lagos"},
    {"name": "The Elevation Church", "denomination": "Pentecostal", "headquarters": "Lagos"},
    {"name": "Trinity House", "denomination": "Pentecostal", "headquarters": "Lagos"},
    {"name": "Salvation Ministries", "denomination": "Pentecostal", "headquarters": "Port Harcourt"},
    {"name": "Omega Power Ministries", "denomination": "Pentecostal", "headquarters": "Port Harcourt"},
    {"name": "Streams of Joy International", "denomination": "Pentecostal", "headquarters": "Abuja"},
    {"name": "Dunamis International Gospel Centre", "denomination": "Pentecostal", "headquarters": "Abuja"},
    {"name": "Commonwealth of Zion Assembly (COZA)", "denomination": "Pentecostal", "headquarters": "Abuja"},
    {"name": "Potter's House Christian Centre", "denomination": "Pentecostal", "headquarters": "Lagos"},
    {"name": "Foursquare Gospel Church", "denomination": "Pentecostal", "headquarters": "Lagos"},
    {"name": "Assemblies of God Church", "denomination": "Pentecostal", "headquarters": "Enugu"},
    {"name": "Apostolic Church Nigeria", "denomination": "Pentecostal", "headquarters": "Lagos"},
    {"name": "Redeemed Christian Church of God (RCCG)", "denomination": "Pentecostal", "headquarters": "Lagos"},
    {"name": "Mountain Top Life Church", "denomination": "Pentecostal", "headquarters": "Lagos"},
    {"name": "Rhema Chapel International", "denomination": "Pentecostal", "headquarters": "Ibadan"},
    {"name": "Grace Assembly", "denomination": "Pentecostal", "headquarters": "Lagos"},
    {"name": "Glory Tabernacle Ministries", "denomination": "Pentecostal", "headquarters": "Ilorin"},
    # Orthodox/Mainline Churches
    {"name": "Catholic Church of Nigeria", "denomination": "Catholic", "headquarters": "Abuja"},
    {"name": "Anglican Church of Nigeria", "denomination": "Anglican", "headquarters": "Abuja"},
    {"name": "Methodist Church Nigeria", "denomination": "Methodist", "headquarters": "Lagos"},
    {"name": "Presbyterian Church of Nigeria", "denomination": "Presbyterian", "headquarters": "Calabar"},
    {"name": "Baptist Convention of Nigeria", "denomination": "Baptist", "headquarters": "Ibadan"},
    {"name": "Lutheran Church of Nigeria", "denomination": "Lutheran", "headquarters": "Nsukka"},
    {"name": "Church of Nigeria (Anglican Communion)", "denomination": "Anglican", "headquarters": "Abuja"},
    {"name": "Cherubim and Seraphim Movement", "denomination": "Aladura", "headquarters": "Lagos"},
    {"name": "Celestial Church of Christ", "denomination": "Aladura", "headquarters": "Lagos"},
    {"name": "Church of the Lord (Aladura)", "denomination": "Aladura", "headquarters": "Ogere"},
]

# =============================================================================
# SERVICE/EVENT TYPES
# =============================================================================

SERVICE_TYPES = [
    "Sunday Service", "Midweek Service", "Prayer Meeting", "Bible Study",
    "Youth Service", "Children's Church", "Fellowship Meeting", "Evangelism Outreach",
    "Crusade", "Gospel Concert", "Seminar", "Workshop", "Conference",
    "Leadership Training", "Membership Class", "Water Baptism", "Holy Communion",
    "Night Vigil", "Thanksgiving Service", "Dedication Service", "Wedding",
    "Funeral Service", "Naming Ceremony", "House Fellowship", "Community Outreach"
]

EVENT_NAMES = [
    "January Special Revival", "Easter Celebration", "Workers' Retreat",
    "Annual Thanksgiving", "Youth Convention", "Women's Conference",
    "Men's Fellowship Summit", "Marriage Seminar", "Financial Freedom Series",
    "Healing and Deliverance Crusade", "Leadership Development Program",
    "New Members' Orientation", "Baptismal Class", "Foundation School",
    "Holy Ghost Congress", "Seven Days Fasting and Prayer", "New Year Service",
    "Christmas Carol", "End of Year Thanksgiving", "Church Anniversary",
    "Pastor's Appreciation Day", "Community Evangelism", "Campus Crusade",
    "Market Evangelism", "Hospital Visitation", "Prison Ministry",
    "Street Evangelism", "Door-to-Door Evangelism", "Online Evangelism"
]

# =============================================================================
# OCCUPATIONS
# =============================================================================

OCCUPATIONS = [
    # Professional
    "Teacher", "Lecturer", "Doctor", "Nurse", "Pharmacist", "Lawyer", "Engineer",
    "Accountant", "Banker", "Architect", "Surveyor", "Civil Servant",
    # Business
    "Business Owner", "Trader", "Entrepreneur", "Importer", "Exporter",
    "Fashion Designer", "Tailor", "Carpenter", "Mason", "Electrician",
    "Plumber", "Mechanic", "Driver", "Transport Operator",
    # Technology
    "Software Developer", "Web Developer", "Graphic Designer", "Data Analyst",
    "IT Consultant", "Network Engineer", "Cybersecurity Analyst",
    # Services
    "Hair Stylist", "Barber", "Chef", "Caterer", "Event Planner",
    "Photographer", "Videographer", "Musician", "Actor", "Artist",
    # Others
    "Student", "Unemployed", "Retired", "Housewife", "Househusband",
    "Farmer", "Fisherman", "Security Personnel", "Cleaner", "Sales Representative",
    "Marketing Executive", "Human Resources Manager", "Admin Officer"
]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_nigerian_phone() -> str:
    """Generate a valid Nigerian phone number."""
    networks = [
        "0803", "0805", "0806", "0807", "0809",  # MTN
        "0810", "0813", "0814", "0816", "0818",  # MTN
        "0903", "0906", "0913", "0916",          # MTN
        "0802", "0808", "0812", "0708", "0902",  # Airtel
        "0907", "0901", "0912", "0911",          # Airtel
        "0809", "0817", "0818", "0908", "0909",  # 9mobile
        "0805", "0705", "0815", "0811", "0905",  # Glo
        "0915", "0913",                            # Glo
    ]
    prefix = random.choice(networks)
    suffix = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    return prefix + suffix


def generate_nigerian_email(first_name: str, last_name: str) -> str:
    """Generate a realistic Nigerian email address."""
    domains = [
        "gmail.com", "yahoo.com", "hotmail.com", "outlook.com",
        "icloud.com", "mail.com", "yahoomail.com"
    ]
    patterns = [
        f"{first_name.lower()}.{last_name.lower()}",
        f"{first_name.lower()}{last_name.lower()}",
        f"{first_name.lower()}_{last_name.lower()}",
        f"{first_name.lower()}{last_name.lower()}{random.randint(1, 999)}",
        f"{last_name.lower()}.{first_name.lower()}",
        f"{first_name.lower()[0]}{last_name.lower()}",
        f"{first_name.lower()}{last_name.lower()[0]}",
    ]
    return random.choice(patterns) + "@" + random.choice(domains)


def generate_nigerian_address(state: str = None, area: str = None) -> Dict[str, str]:
    """Generate a realistic Nigerian address."""
    if state is None:
        state = random.choice(list(NIGERIAN_STATES_LGAS.keys()))
    
    state_data = NIGERIAN_STATES_LGAS[state]
    lga = random.choice(state_data["lgas"])
    area = area or random.choice(state_data["areas"])
    
    street_types = ["Street", "Road", "Avenue", "Close", "Crescent", "Drive", "Way", "Lane"]
    street_names = [
        "Church", "Market", "Hospital", "School", "Community", "Unity", "Peace",
        "Liberty", "Independence", "Adekunle", "Ogunleye", "Adesanya", "Ojo",
        "Emmanuel", "Grace", "Faith", "Hope", "Charity", "Victory", "Success",
        "Unity", "Cooperative", "Industrial", "Commercial", "Residential"
    ]
    
    street = f"{random.randint(1, 200)} {random.choice(street_names)} {random.choice(street_types)}"
    
    return {
        "street": street,
        "area": area,
        "city": state_data["capital"] if state == state else area,
        "lga": lga,
        "state": state,
        "full_address": f"{street}, {area}, {lga}, {state}, Nigeria"
    }


def generate_nigerian_person(gender: str = None) -> Dict[str, Any]:
    """Generate a complete Nigerian person profile."""
    gender = gender or random.choice(["male", "female"])
    
    if gender == "male":
        first_name = random.choice(NIGERIAN_FIRST_NAMES_MALE)
    else:
        first_name = random.choice(NIGERIAN_FIRST_NAMES_FEMALE)
    
    last_name = random.choice(NIGERIAN_LAST_NAMES)
    
    # Generate date of birth (between 18 and 70 years ago)
    today = date.today()
    age = random.randint(18, 70)
    dob = today - timedelta(days=age * 365 + random.randint(0, 365))
    
    address_data = generate_nigerian_address()
    
    return {
        "first_name": first_name,
        "last_name": last_name,
        "full_name": f"{first_name} {last_name}",
        "gender": gender,
        "phone": generate_nigerian_phone(),
        "email": generate_nigerian_email(first_name, last_name),
        "date_of_birth": dob.isoformat(),
        "address": address_data["full_address"],
        "city": address_data["city"],
        "state": address_data["state"],
        "lga": address_data["lga"],
        "occupation": random.choice(OCCUPATIONS),
    }


def get_random_state() -> str:
    """Get a random Nigerian state."""
    return random.choice(list(NIGERIAN_STATES_LGAS.keys()))


def get_church_branches(main_church: Dict, count: int = 5) -> List[Dict]:
    """Generate branch locations for a church."""
    branches = []
    states_used = set()
    
    for i in range(count):
        # Try to get different states
        available_states = [s for s in NIGERIAN_STATES_LGAS.keys() if s not in states_used]
        if not available_states:
            available_states = list(NIGERIAN_STATES_LGAS.keys())
        
        state = random.choice(available_states)
        states_used.add(state)
        
        state_data = NIGERIAN_STATES_LGAS[state]
        city = state_data["capital"]
        
        branches.append({
            "id": str(uuid.uuid4()),
            "name": f"{main_church['name']} - {city} Branch",
            "city": city,
            "state": state,
            "address": generate_nigerian_address(state)["full_address"],
            "pastor": generate_nigerian_person("male" if random.random() > 0.1 else "female")["full_name"],
            "phone": generate_nigerian_phone(),
        })
    
    return branches


# =============================================================================
# DEMO CONFIGURATION
# =============================================================================

DEMO_CONFIG = {
    "church_name": "Grace Evangelical Ministries",
    "church_location": "Lagos, Nigeria",
    "demo_database_name": "evangelism_crm_demo",
    "demo_client_id": "demo-church-lagos",
    "admin_email": "admin@graceevangelical.demo",
    "admin_password": "Demo@2025",
    "default_workers_count": 15,
    "default_converts_count": 500,
    "default_services_count": 20,
    "default_outreaches_count": 10,
}

if __name__ == "__main__":
    # Test the generators
    print("Testing Nigerian Data Generators...")
    print("\n" + "="*60)
    print("Sample Nigerian Person:")
    print("="*60)
    person = generate_nigerian_person()
    for key, value in person.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*60)
    print("Sample Churches:")
    print("="*60)
    for church in random.sample(NIGERIAN_CHURCHES, 3):
        print(f"  - {church['name']} ({church['denomination']})")
    
    print("\n" + "="*60)
    print(f"Demo Configuration: {DEMO_CONFIG['church_name']}")
    print("="*60)
