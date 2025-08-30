from difflib import get_close_matches
from typing import List, Optional


CLUBS = {
    100: {
        "name": "Akarana Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=100",
    },
    101: {
        "name": "Akaroa Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=101",
    },
    102: {
        "name": "Alexandra Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=102",
    },
    104: {
        "name": "Allan Grange Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=104",
    },
    105: {
        "name": "Amberley Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=105",
    },
    106: {
        "name": "Amuri Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=106",
    },
    107: {
        "name": "Apiti Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=107",
    },
    109: {
        "name": "Ardleigh Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=109",
    },
    110: {
        "name": "Arrowtown Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=110",
    },
    111: {
        "name": "Ashburton Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=111",
    },
    112: {
        "name": "Royal Auckland and Grange Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=112",
    },
    114: {
        "name": "Avondale Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=114",
    },
    115: {
        "name": "Awatere Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=115",
    },
    116: {
        "name": "Awhitu Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=116",
    },
    119: {
        "name": "Belleknowes Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=119",
    },
    120: {
        "name": "Blenheim Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=120",
    },
    121: {
        "name": "Bluff Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=121",
    },
    123: {
        "name": "Broadwood Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=123",
    },
    125: {
        "name": "Buckley Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=125",
    },
    127: {
        "name": "Cambridge Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=127",
    },
    128: {
        "name": "Carterton Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=128",
    },
    129: {
        "name": "Castlecliff Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=129",
    },
    130: {
        "name": "Castlepoint Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=130",
    },
    131: {
        "name": "Chamberlain Park Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=131",
    },
    132: {
        "name": "Charteris Bay Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=132",
    },
    134: {
        "name": "Cheviot Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=134",
    },
    136: {
        "name": "Christchurch Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=136",
    },
    137: {
        "name": "Clarks Beach Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=137",
    },
    138: {
        "name": "Clinton Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=138",
    },
    139: {
        "name": "Coringa Golf Club Inc.",
        "url": "https://www.golf.co.nz/club-detail?clubid=139",
    },
    140: {
        "name": "Coromandel Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=140",
    },
    141: {
        "name": "Cromwell Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=141",
    },
    143: {
        "name": "Culverden Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=143",
    },
    144: {
        "name": "Dannevirke Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=144",
    },
    145: {
        "name": "Dipton Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=145",
    },
    146: {
        "name": "Drummond Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=146",
    },
    148: {
        "name": "Dunstan Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=148",
    },
    149: {
        "name": "Eketahuna Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=149",
    },
    150: {
        "name": "Ellesmere Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=150",
    },
    151: {
        "name": "Eltham Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=151",
    },
    152: {
        "name": "Everglades Country Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=152",
    },
    153: {
        "name": "Fairlie Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=153",
    },
    156: {
        "name": "Fitzroy Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=156",
    },
    159: {
        "name": "Foxton Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=159",
    },
    160: {
        "name": "Geraldine District Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=160",
    },
    161: {
        "name": "Gisborne Park Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=161",
    },
    162: {
        "name": "Gladfield Country Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=162",
    },
    163: {
        "name": "Gleniti Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=163",
    },
    164: {
        "name": "Glenorchy Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=164",
    },
    165: {
        "name": "Golden Downs Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=165",
    },
    167: {
        "name": "Gore Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=167",
    },
    168: {
        "name": "Grande Vue Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=168",
    },
    170: {
        "name": "Green Acres Country Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=170",
    },
    171: {
        "name": "Greenacres Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=171",
    },
    172: {
        "name": "Greendale Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=172",
    },
    173: {
        "name": "Greymouth Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=173",
    },
    175: {
        "name": "Hagley Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=175",
    },
    176: {
        "name": "Hamilton Golf Club - St Andrews",
        "url": "https://www.golf.co.nz/club-detail?clubid=176",
    },
    177: {
        "name": "Hamurana Park Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=177",
    },
    178: {
        "name": "Hanmer Springs Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=178",
    },
    179: {
        "name": "Harewood Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=179",
    },
    180: {
        "name": "Hastings Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=180",
    },
    181: {
        "name": "Hauraki Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=181",
    },
    182: {
        "name": "Hawarden Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=182",
    },
    183: {
        "name": "Hawera Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=183",
    },
    184: {
        "name": "Hawkes Bay Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=184",
    },
    185: {
        "name": "Hawkestone Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=185",
    },
    186: {
        "name": "Hedgehope Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=186",
    },
    187: {
        "name": "Helensville Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=187",
    },
    188: {
        "name": "Heriot Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=188",
    },
    189: {
        "name": "Highfield Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=189",
    },
    190: {
        "name": "Hikurangi Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=190",
    },
    191: {
        "name": "Hinehopu Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=191",
    },
    192: {
        "name": "Hokitika Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=192",
    },
    193: {
        "name": "Hororata Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=193",
    },
    194: {
        "name": "Horsham Downs Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=194",
    },
    195: {
        "name": "Houhora Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=195",
    },
    196: {
        "name": "Howick Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=196",
    },
    197: {
        "name": "Huapai Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=197",
    },
    198: {
        "name": "Hukanui Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=198",
    },
    199: {
        "name": "Huntly Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=199",
    },
    203: {
        "name": "Inglewood Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=203",
    },
    204: {
        "name": "Invercargill Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=204",
    },
    205: {
        "name": "Island Park Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=205",
    },
    206: {
        "name": "Kaiapoi Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=206",
    },
    207: {
        "name": "Kaikohe Golf & Squash Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=207",
    },
    208: {
        "name": "Kaikoura Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=208",
    },
    210: {
        "name": "Kaitaia Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=210",
    },
    211: {
        "name": "Kaitake Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=211",
    },
    212: {
        "name": "Kaitangata Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=212",
    },
    213: {
        "name": "Kaituna Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=213",
    },
    214: {
        "name": "Kapiti Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=214",
    },
    215: {
        "name": "Karamea Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=215",
    },
    216: {
        "name": "Karori Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=216",
    },
    217: {
        "name": "Kawerau Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=217",
    },
    218: {
        "name": "Kawhia Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=218",
    },
    219: {
        "name": "Bay of Islands Golf Club Kerikeri Inc.",
        "url": "https://www.golf.co.nz/club-detail?clubid=219",
    },
    220: {
        "name": "Kingston Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=220",
    },
    221: {
        "name": "Kinloch Village Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=221",
    },
    222: {
        "name": "Kurow Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=222",
    },
    224: {
        "name": "Lake View Golf and Country Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=224",
    },
    225: {
        "name": "Lawrence Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=225",
    },
    226: {
        "name": "Levin Golf Club Inc.",
        "url": "https://www.golf.co.nz/club-detail?clubid=226",
    },
    227: {
        "name": "Lincoln Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=227",
    },
    228: {
        "name": "Linton Camp Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=228",
    },
    230: {
        "name": "Lower Waitaki Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=230",
    },
    231: {
        "name": "Lumsden Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=231",
    },
    232: {
        "name": "Mackenzie Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=232",
    },
    233: {
        "name": "Mahia Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=233",
    },
    234: {
        "name": "Mahunga Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=234",
    },
    236: {
        "name": "Manaia Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=236",
    },
    237: {
        "name": "Manawatu Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=237",
    },
    238: {
        "name": "Mangakino Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=238",
    },
    240: {
        "name": "Mangawhai Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=240",
    },
    241: {
        "name": "Maniototo Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=241",
    },
    244: {
        "name": "Manukorihi Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=244",
    },
    246: {
        "name": "Maraenui Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=246",
    },
    249: {
        "name": "Marlborough Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=249",
    },
    250: {
        "name": "Martinborough Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=250",
    },
    251: {
        "name": "Masterton Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=251",
    },
    252: {
        "name": "Matamata Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=252",
    },
    253: {
        "name": "The Dunes Matarangi Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=253",
    },
    255: {
        "name": "Mataura Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=255",
    },
    256: {
        "name": "Maungakiekie Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=256",
    },
    258: {
        "name": "Maungati Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=258",
    },
    260: {
        "name": "Mayfield Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=260",
    },
    261: {
        "name": "McLeans Island Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=261",
    },
    262: {
        "name": "Mercury Bay Golf & Country Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=262",
    },
    263: {
        "name": "Methven Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=263",
    },
    264: {
        "name": "Middlemarch Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=264",
    },
    265: {
        "name": "Millbrook Resort & Country Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=265",
    },
    266: {
        "name": "Miramar Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=266",
    },
    267: {
        "name": "Mornington Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=267",
    },
    268: {
        "name": "Morrinsville Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=268",
    },
    269: {
        "name": "Mossburn Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=269",
    },
    270: {
        "name": "Motueka Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=270",
    },
    271: {
        "name": "Mount Maunganui Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=271",
    },
    272: {
        "name": "Mt Nessing Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=272",
    },
    273: {
        "name": "Murchison Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=273",
    },
    274: {
        "name": "Muriwai Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=274",
    },
    275: {
        "name": "Murupara Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=275",
    },
    276: {
        "name": "Napier Golf Club Inc.",
        "url": "https://www.golf.co.nz/club-detail?clubid=276",
    },
    278: {
        "name": "Naseby Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=278",
    },
    279: {
        "name": "Nelson Golf Club Inc.",
        "url": "https://www.golf.co.nz/club-detail?clubid=279",
    },
    280: {
        "name": "Judgeford Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=280",
    },
    281: {
        "name": "New Plymouth Golf Club Inc.",
        "url": "https://www.golf.co.nz/club-detail?clubid=281",
    },
    282: {
        "name": "Ngahinepouri Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=282",
    },
    283: {
        "name": "Ngaruawahia Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=283",
    },
    285: {
        "name": "Ngunguru Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=285",
    },
    286: {
        "name": "Nightcaps Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=286",
    },
    287: {
        "name": "Nopera Bay Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=287",
    },
    288: {
        "name": "Norsewood Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=288",
    },
    289: {
        "name": "North Otago Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=289",
    },
    290: {
        "name": "North Shore Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=290",
    },
    291: {
        "name": "Northern Wairoa Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=291",
    },
    292: {
        "name": "Northland Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=292",
    },
    294: {
        "name": "Ohariu Valley Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=294",
    },
    297: {
        "name": "Okoroire Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=297",
    },
    298: {
        "name": "Omaha Beach Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=298",
    },
    299: {
        "name": "Omakau Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=299",
    },
    300: {
        "name": "Omanu Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=300",
    },
    301: {
        "name": "Omarama Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=301",
    },
    302: {
        "name": "Onewhero Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=302",
    },
    303: {
        "name": "Onga Onga Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=303",
    },
    304: {
        "name": "Opotiki Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=304",
    },
    305: {
        "name": "Opunake Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=305",
    },
    306: {
        "name": "Otago Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=306",
    },
    307: {
        "name": "Otaki Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=307",
    },
    308: {
        "name": "Otakou Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=308",
    },
    309: {
        "name": "Otautau Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=309",
    },
    310: {
        "name": "Otematata Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=310",
    },
    311: {
        "name": "Otumoetai Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=311",
    },
    312: {
        "name": "Owaka Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=312",
    },
    313: {
        "name": "Paeroa Golf Club Inc.",
        "url": "https://www.golf.co.nz/club-detail?clubid=313",
    },
    314: {
        "name": "Pahiatua Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=314",
    },
    315: {
        "name": "Pakuranga Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=315",
    },
    316: {
        "name": "Palmerston North Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=316",
    },
    318: {
        "name": "Paparoa Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=318",
    },
    320: {
        "name": "Paraparaumu Beach Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=320",
    },
    322: {
        "name": "Patea Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=322",
    },
    323: {
        "name": "Patearoa Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=323",
    },
    324: {
        "name": "Patutahi Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=324",
    },
    329: {
        "name": "Picton Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=329",
    },
    330: {
        "name": "The Pines Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=330",
    },
    331: {
        "name": "Piopio Aria Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=331",
    },
    332: {
        "name": "Pirongia Golf Club Inc.",
        "url": "https://www.golf.co.nz/club-detail?clubid=332",
    },
    333: {
        "name": "Pleasant Point Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=333",
    },
    334: {
        "name": "Pongaroa Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=334",
    },
    335: {
        "name": "Porangahau Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=335",
    },
    336: {
        "name": "Port Chalmers Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=336",
    },
    337: {
        "name": "Poverty Bay Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=337",
    },
    338: {
        "name": "Pukekohe Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=338",
    },
    339: {
        "name": "Puketitiri Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=339",
    },
    340: {
        "name": "Pungarehu Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=340",
    },
    341: {
        "name": "Pupuke Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=341",
    },
    342: {
        "name": "Purangi Golf & Country Club Inc.",
        "url": "https://www.golf.co.nz/club-detail?clubid=342",
    },
    345: {
        "name": "Queens Park Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=345",
    },
    348: {
        "name": "Raglan Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=348",
    },
    350: {
        "name": "Rakaia Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=350",
    },
    352: {
        "name": "Rangatira Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=352",
    },
    353: {
        "name": "Rangiora Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=353",
    },
    354: {
        "name": "Rangitikei Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=354",
    },
    356: {
        "name": "Rarangi Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=356",
    },
    357: {
        "name": "Rawene Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=357",
    },
    358: {
        "name": "Rawhiti Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=358",
    },
    359: {
        "name": "Redwood Park Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=359",
    },
    360: {
        "name": "Reefton Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=360",
    },
    361: {
        "name": "Remuera Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=361",
    },
    363: {
        "name": "Riversdale Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=363",
    },
    364: {
        "name": "Riversdale Beach Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=364",
    },
    365: {
        "name": "Riverton Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=365",
    },
    366: {
        "name": "RNZAF Auckland Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=366",
    },
    367: {
        "name": "RNZAF Woodbourne Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=367",
    },
    368: {
        "name": "Rotorua Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=368",
    },
    369: {
        "name": "Roxburgh Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=369",
    },
    371: {
        "name": "Russley Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=371",
    },
    372: {
        "name": "Scargill Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=372",
    },
    373: {
        "name": "Shandon Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=373",
    },
    374: {
        "name": "Sherwood Park Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=374",
    },
    375: {
        "name": "South Head Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=375",
    },
    377: {
        "name": "Springfield Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=377",
    },
    379: {
        "name": "St Clair Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=379",
    },
    380: {
        "name": "Stewart Alexander Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=380",
    },
    381: {
        "name": "Stratford Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=381",
    },
    382: {
        "name": "Strathmore Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=382",
    },
    383: {
        "name": "Tahuna Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=383",
    },
    384: {
        "name": "Tahunga Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=384",
    },
    385: {
        "name": "Tai Tapu Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=385",
    },
    386: {
        "name": "Taieri Lakes Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=386",
    },
    387: {
        "name": "Taihape Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=387",
    },
    388: {
        "name": "Tairua Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=388",
    },
    389: {
        "name": "Takaka Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=389",
    },
    390: {
        "name": "Takapau Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=390",
    },
    391: {
        "name": "Tapanui Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=391",
    },
    392: {
        "name": "Tapora Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=392",
    },
    394: {
        "name": "Tarras Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=394",
    },
    395: {
        "name": "Tasman Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=395",
    },
    400: {
        "name": "Tauranga Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=400",
    },
    401: {
        "name": "Tawhero Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=401",
    },
    402: {
        "name": "Te Akau Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=402",
    },
    403: {
        "name": "Te Anau Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=403",
    },
    404: {
        "name": "Te Aroha Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=404",
    },
    405: {
        "name": "Te Awamutu Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=405",
    },
    407: {
        "name": "Te Kowhai Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=407",
    },
    408: {
        "name": "Te Marua Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=408",
    },
    409: {
        "name": "Te Ngutu Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=409",
    },
    410: {
        "name": "Te Pohue Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=410",
    },
    411: {
        "name": "Te Puia Hot Springs Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=411",
    },
    412: {
        "name": "Te Puke Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=412",
    },
    413: {
        "name": "Templeton Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=413",
    },
    414: {
        "name": "Temuka Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=414",
    },
    416: {
        "name": "Thames Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=416",
    },
    417: {
        "name": "Takapuna Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=417",
    },
    419: {
        "name": "Timaru Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=419",
    },
    420: {
        "name": "Tinwald Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=420",
    },
    421: {
        "name": "Tirau Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=421",
    },
    422: {
        "name": "Titahi Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=422",
    },
    423: {
        "name": "Titirangi Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=423",
    },
    424: {
        "name": "Tokanui Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=424",
    },
    425: {
        "name": "Tokarahi Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=425",
    },
    426: {
        "name": "Toko Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=426",
    },
    427: {
        "name": "Tokoroa Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=427",
    },
    429: {
        "name": "Totaradale Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=429",
    },
    430: {
        "name": "Trentham Camp Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=430",
    },
    431: {
        "name": "Tuatapere Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=431",
    },
    433: {
        "name": "Twelve Oaks Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=433",
    },
    434: {
        "name": "Urenui Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=434",
    },
    435: {
        "name": "Waahi Taakaro Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=435",
    },
    438: {
        "name": "Waihi Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=438",
    },
    439: {
        "name": "Waikaia Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=439",
    },
    440: {
        "name": "Waikaka Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=440",
    },
    441: {
        "name": "Waikanae Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=441",
    },
    442: {
        "name": "Waikare Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=442",
    },
    444: {
        "name": "Waikite Valley Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=444",
    },
    445: {
        "name": "Waikohu Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=445",
    },
    446: {
        "name": "Waikouaiti Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=446",
    },
    447: {
        "name": "Waimarino Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=447",
    },
    448: {
        "name": "Waimate Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=448",
    },
    450: {
        "name": "Wainuiomata Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=450",
    },
    452: {
        "name": "Reporoa Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=452",
    },
    453: {
        "name": "Waiotira Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=453",
    },
    456: {
        "name": "Waipawa Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=456",
    },
    457: {
        "name": "Waipu Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=457",
    },
    458: {
        "name": "Waipukurau Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=458",
    },
    460: {
        "name": "Wairau Valley Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=460",
    },
    462: {
        "name": "Wairoa Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=462",
    },
    464: {
        "name": "Waitakere Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=464",
    },
    465: {
        "name": "Waitangi Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=465",
    },
    466: {
        "name": "Waitara Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=466",
    },
    467: {
        "name": "Waitemata Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=467",
    },
    468: {
        "name": "Waiterimu Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=468",
    },
    469: {
        "name": "Waitikiri Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=469",
    },
    470: {
        "name": "Waitoa Park Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=470",
    },
    471: {
        "name": "Waitomo Golf & Country Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=471",
    },
    472: {
        "name": "Waiuku Golf & Squash Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=472",
    },
    473: {
        "name": "Walton Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=473",
    },
    474: {
        "name": "Wanaka Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=474",
    },
    475: {
        "name": "Wanganui Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=475",
    },
    476: {
        "name": "Warkworth Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=476",
    },
    478: {
        "name": "Waverley Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=478",
    },
    479: {
        "name": "Weedons Country Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=479",
    },
    480: {
        "name": "Royal Wellington Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=480",
    },
    481: {
        "name": "Wellsford Golf Club Inc.",
        "url": "https://www.golf.co.nz/club-detail?clubid=481",
    },
    482: {
        "name": "Omokoroa Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=482",
    },
    483: {
        "name": "Westown Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=483",
    },
    484: {
        "name": "Westport Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=484",
    },
    485: {
        "name": "Whakatane Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=485",
    },
    487: {
        "name": "Whangaparaoa Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=487",
    },
    488: {
        "name": "Whangarei Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=488",
    },
    489: {
        "name": "Whangaroa Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=489",
    },
    490: {
        "name": "Whataroa Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=490",
    },
    491: {
        "name": "Whitford Park Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=491",
    },
    492: {
        "name": "Bottle Lake Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=492",
    },
    493: {
        "name": "Winton Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=493",
    },
    494: {
        "name": "Cape Turnagain Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=494",
    },
    495: {
        "name": "Wyndham Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=495",
    },
    514: {
        "name": "Ben Ohau Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=514",
    },
    515: {
        "name": "Maramarua Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=515",
    },
    516: {
        "name": "Waiheke Island Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=516",
    },
    517: {
        "name": "Fairview Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=517",
    },
    519: {
        "name": "Te Teko Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=519",
    },
    520: {
        "name": "Turangi Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=520",
    },
    521: {
        "name": "Burnham Golf Club Inc.",
        "url": "https://www.golf.co.nz/club-detail?clubid=521",
    },
    522: {
        "name": "Waimairi Beach Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=522",
    },
    523: {
        "name": "Waimakariri Gorge Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=523",
    },
    525: {
        "name": "Feilding Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=525",
    },
    526: {
        "name": "Marton Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=526",
    },
    527: {
        "name": "Okaihau Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=527",
    },
    528: {
        "name": "Balclutha Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=528",
    },
    529: {
        "name": "Ringa Ringa Heights Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=529",
    },
    530: {
        "name": "Putaruru Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=530",
    },
    531: {
        "name": "Taumarunui Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=531",
    },
    533: {
        "name": "Taupo Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=533",
    },
    534: {
        "name": "Queenstown Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=534",
    },
    535: {
        "name": "Pauanui Sports & Recreation Club Inc.",
        "url": "https://www.golf.co.nz/club-detail?clubid=535",
    },
    536: {
        "name": "Whangamata Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=536",
    },
    538: {
        "name": "Tolaga Bay Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=538",
    },
    541: {
        "name": "RNZAF Ohakea Base  Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=541",
    },
    542: {
        "name": "Terrace Downs High Country Resort & Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=542",
    },
    544: {
        "name": "RNZAF Wellington Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=544",
    },
    545: {
        "name": "Kauri Cliffs Golf Club & Lodge",
        "url": "https://www.golf.co.nz/club-detail?clubid=545",
    },
    548: {
        "name": "Auckland Regional Police Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=548",
    },
    550: {
        "name": "Clearwater Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=550",
    },
    552: {
        "name": "Lake Hawea  Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=552",
    },
    556: {
        "name": "Renner Park Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=556",
    },
    557: {
        "name": "Cape Kidnappers Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=557",
    },
    559: {
        "name": "Carrington Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=559",
    },
    560: {
        "name": "Maxwells Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=560",
    },
    562: {
        "name": "The Kinloch Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=562",
    },
    564: {
        "name": "Jacks Point Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=564",
    },
    565: {
        "name": "Wattle Downs Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=565",
    },
    566: {
        "name": "Pegasus Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=566",
    },
    567: {
        "name": "Boulcott's Farm Heritage Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=567",
    },
    569: {
        "name": "Karamu Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=569",
    },
    577: {
        "name": "Onekaka Links Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=577",
    },
    580: {
        "name": "Riverside Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=580",
    },
    582: {
        "name": "Hutt Park Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=582",
    },
    583: {
        "name": "Orlando Country Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=583",
    },
    584: {
        "name": "Tara Iti Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=584",
    },
    586: {
        "name": "Wainui Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=586",
    },
    590: {
        "name": "Te Arai Links Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=590",
    },
    592: {
        "name": "Ngawi Hitaround Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=592",
    },
    595: {
        "name": "Test Club Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=595",
    },
    901: {
        "name": "Overseas Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=901",
    },
    902: {
        "name": "Nomads Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=902",
    },
    904: {
        "name": "Futures Wakatipu Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=904",
    },
    906: {
        "name": "Devil's Own Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=906",
    },
    916: {
        "name": "Halo Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=916",
    },
    921: {
        "name": "Afrikaans Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=921",
    },
    925: {
        "name": "Hickory Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=925",
    },
    926: {
        "name": "Gumboot Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=926",
    },
    927: {
        "name": "Te Kahui Matatoa  Golf Club",
        "url": "https://www.golf.co.nz/club-detail?clubid=927",
    },
}


def find_club_ids_by_name(club_name: str, max_matches: int = 5) -> List[int]:
    """
    Find club IDs by searching for the closest matching club names.
    
    Args:
        club_name: The club name to search for
        max_matches: Maximum number of matches to return (default: 5)
        
    Returns:
        List of club IDs ordered by match quality (best matches first)
    """
    if not club_name.strip():
        return []
    
    # Create a mapping of club names to IDs for efficient lookup
    name_to_ids = {}
    for club_id, club_info in CLUBS.items():
        name = club_info.get("name", "").lower()
        if name:
            if name not in name_to_ids:
                name_to_ids[name] = []
            name_to_ids[name].append(club_id)
    
    club_names = list(name_to_ids.keys())
    search_term = club_name.lower().strip()
    
    # First, try exact matches
    if search_term in name_to_ids:
        return name_to_ids[search_term][:max_matches]
    
    # Then try fuzzy matching using difflib
    close_matches = get_close_matches(
        search_term, 
        club_names, 
        n=max_matches, 
        cutoff=0.1  # Low cutoff to be more permissive
    )
    
    # Collect club IDs from the matched names
    result_ids = []
    for matched_name in close_matches:
        result_ids.extend(name_to_ids[matched_name])
    
    return result_ids[:max_matches]


def get_club_name_by_id(club_id: int) -> Optional[str]:
    """
    Get club name by club ID.
    
    Args:
        club_id: The club ID to look up
        
    Returns:
        Club name if found, None otherwise
    """
    club_info = CLUBS.get(club_id)
    return club_info.get("name") if club_info else None
