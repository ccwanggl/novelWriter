# -*- coding: utf-8 -*-
"""novelWriter Language Codes

 novelWriter – Language Codes
==============================
 Handles translating language codes to language names

 File History:
 Created: 2019-11-05 [0.4.0]

"""

import logging

logger = logging.getLogger(__name__)

class isoLanguage():

    ISO_639_1 = {
        "aa" : "Afar",
        "ab" : "Abkhazian",
        "ae" : "Avestan",
        "af" : "Afrikaans",
        "ak" : "Akan",
        "am" : "Amharic",
        "an" : "Aragonese",
        "ar" : "Arabic",
        "as" : "Assamese",
        "av" : "Avaric",
        "ay" : "Aymara",
        "az" : "Azerbaijani",
        "ba" : "Bashkir",
        "be" : "Belarusian",
        "bg" : "Bulgarian",
        "bh" : "Bihari languages",
        "bi" : "Bislama",
        "bm" : "Bambara",
        "bn" : "Bengali",
        "bo" : "Tibetan",
        "bo" : "Tibetan",
        "br" : "Breton",
        "bs" : "Bosnian",
        "ca" : "Catalan",
        "ce" : "Chechen",
        "ch" : "Chamorro",
        "co" : "Corsican",
        "cr" : "Cree",
        "cs" : "Czech",
        "cs" : "Czech",
        "cu" : "Church Slavic",
        "cv" : "Chuvash",
        "cy" : "Welsh",
        "cy" : "Welsh",
        "da" : "Danish",
        "de" : "German",
        "de" : "German",
        "dv" : "Divehi",
        "dz" : "Dzongkha",
        "ee" : "Ewe",
        "el" : "Modern Greek",
        "en" : "English",
        "eo" : "Esperanto",
        "es" : "Spanish",
        "et" : "Estonian",
        "eu" : "Basque",
        "eu" : "Basque",
        "fa" : "Persian",
        "fa" : "Persian",
        "ff" : "Fulah",
        "fi" : "Finnish",
        "fj" : "Fijian",
        "fo" : "Faroese",
        "fr" : "French",
        "fr" : "French",
        "fy" : "Western Frisian",
        "ga" : "Irish",
        "gd" : "Gaelic",
        "gl" : "Galician",
        "gn" : "Guarani",
        "gu" : "Gujarati",
        "gv" : "Manx",
        "ha" : "Hausa",
        "he" : "Hebrew",
        "hi" : "Hindi",
        "ho" : "Hiri Motu",
        "hr" : "Croatian",
        "ht" : "Haitian",
        "hu" : "Hungarian",
        "hy" : "Armenian",
        "hy" : "Armenian",
        "hz" : "Herero",
        "ia" : "Interlingua",
        "id" : "Indonesian",
        "ie" : "Interlingue",
        "ig" : "Igbo",
        "ii" : "Sichuan Yi",
        "ik" : "Inupiaq",
        "io" : "Ido",
        "is" : "Icelandic",
        "is" : "Icelandic",
        "it" : "Italian",
        "iu" : "Inuktitut",
        "ja" : "Japanese",
        "jv" : "Javanese",
        "ka" : "Georgian",
        "ka" : "Georgian",
        "kg" : "Kongo",
        "ki" : "Kikuyu",
        "kj" : "Kuanyama",
        "kk" : "Kazakh",
        "kl" : "Kalaallisut",
        "km" : "Central Khmer",
        "kn" : "Kannada",
        "ko" : "Korean",
        "kr" : "Kanuri",
        "ks" : "Kashmiri",
        "ku" : "Kurdish",
        "kv" : "Komi",
        "kw" : "Cornish",
        "ky" : "Kirghiz",
        "la" : "Latin",
        "lb" : "Luxembourgish",
        "lg" : "Ganda",
        "li" : "Limburgan",
        "ln" : "Lingala",
        "lo" : "Lao",
        "lt" : "Lithuanian",
        "lu" : "Luba-Katanga",
        "lv" : "Latvian",
        "mg" : "Malagasy",
        "mh" : "Marshallese",
        "mi" : "Maori",
        "mi" : "Maori",
        "mk" : "Macedonian",
        "mk" : "Macedonian",
        "ml" : "Malayalam",
        "mn" : "Mongolian",
        "mr" : "Marathi",
        "ms" : "Malay",
        "mt" : "Maltese",
        "my" : "Burmese",
        "na" : "Nauru",
        "nb" : "Norwegian Bokmål",
        "nd" : "North Ndebele",
        "ne" : "Nepali",
        "ng" : "Ndonga",
        "nl" : "Dutch",
        "nn" : "Norwegian Nynorsk",
        "no" : "Norwegian",
        "nr" : "South Ndebele",
        "nv" : "Navajo",
        "ny" : "Chichewa",
        "oc" : "Occitan",
        "oj" : "Ojibwa",
        "om" : "Oromo",
        "or" : "Oriya",
        "os" : "Ossetian",
        "pa" : "Panjabi",
        "pi" : "Pali",
        "pl" : "Polish",
        "ps" : "Pushto",
        "pt" : "Portuguese",
        "qu" : "Quechua",
        "rm" : "Romansh",
        "rn" : "Rundi",
        "ro" : "Romanian",
        "ru" : "Russian",
        "rw" : "Kinyarwanda",
        "sa" : "Sanskrit",
        "sc" : "Sardinian",
        "sd" : "Sindhi",
        "se" : "Northern Sami",
        "sg" : "Sango",
        "si" : "Sinhala",
        "sk" : "Slovak",
        "sk" : "Slovak",
        "sl" : "Slovenian",
        "sm" : "Samoan",
        "sn" : "Shona",
        "so" : "Somali",
        "sq" : "Albanian",
        "sq" : "Albanian",
        "sr" : "Serbian",
        "ss" : "Swati",
        "st" : "Southern Sotho",
        "su" : "Sundanese",
        "sv" : "Swedish",
        "sw" : "Swahili",
        "ta" : "Tamil",
        "te" : "Telugu",
        "tg" : "Tajik",
        "th" : "Thai",
        "ti" : "Tigrinya",
        "tk" : "Turkmen",
        "tl" : "Tagalog",
        "tn" : "Tswana",
        "to" : "Tonga",
        "tr" : "Turkish",
        "ts" : "Tsonga",
        "tt" : "Tatar",
        "tw" : "Twi",
        "ty" : "Tahitian",
        "ug" : "Uighur",
        "uk" : "Ukrainian",
        "ur" : "Urdu",
        "uz" : "Uzbek",
        "ve" : "Venda",
        "vi" : "Vietnamese",
        "vo" : "Volapük",
        "wa" : "Walloon",
        "wo" : "Wolof",
        "xh" : "Xhosa",
        "yi" : "Yiddish",
        "yo" : "Yoruba",
        "za" : "Zhuang",
        "zh" : "Chinese",
        "zh" : "Chinese",
        "zu" : "Zulu",
    }

# END Class isoLanguage

class isoCountry():

    ISO_3166_1_alpha_2 : {
        "AD" : "Andorra",
        "AE" : "United Arab Emirates",
        "AF" : "Afghanistan",
        "AG" : "Antigua and Barbuda",
        "AI" : "Anguilla",
        "AL" : "Albania",
        "AM" : "Armenia",
        "AO" : "Angola",
        "AQ" : "Antarctica",
        "AR" : "Argentina",
        "AS" : "American Samoa",
        "AT" : "Austria",
        "AU" : "Australia",
        "AW" : "Aruba",
        "AX" : "Åland Islands",
        "AZ" : "Azerbaijan",
        "BA" : "Bosnia and Herzegovina",
        "BB" : "Barbados",
        "BD" : "Bangladesh",
        "BE" : "Belgium",
        "BF" : "Burkina Faso",
        "BG" : "Bulgaria",
        "BH" : "Bahrain",
        "BI" : "Burundi",
        "BJ" : "Benin",
        "BL" : "Saint Barthélemy",
        "BM" : "Bermuda",
        "BN" : "Brunei Darussalam",
        "BO" : "Plurinational State of Bolivia",
        "BQ" : "Sint Eustatius and Saba Bonaire",
        "BR" : "Brazil",
        "BS" : "Bahamas",
        "BT" : "Bhutan",
        "BV" : "Bouvet Island",
        "BW" : "Botswana",
        "BY" : "Belarus",
        "BZ" : "Belize",
        "CA" : "Canada",
        "CC" : "Cocos (Keeling) Islands",
        "CD" : "The Democratic Republic of the Congo",
        "CF" : "Central African Republic",
        "CG" : "Congo",
        "CH" : "Switzerland",
        "CI" : "Côte d'Ivoire",
        "CK" : "Cook Islands",
        "CL" : "Chile",
        "CM" : "Cameroon",
        "CN" : "China",
        "CO" : "Colombia",
        "CR" : "Costa Rica",
        "CU" : "Cuba",
        "CV" : "Cape Verde",
        "CW" : "Curaçao",
        "CX" : "Christmas Island",
        "CY" : "Cyprus",
        "CZ" : "Czech Republic",
        "DE" : "Germany",
        "DJ" : "Djibouti",
        "DK" : "Denmark",
        "DM" : "Dominica",
        "DO" : "Dominican Republic",
        "DZ" : "Algeria",
        "EC" : "Ecuador",
        "EE" : "Estonia",
        "EG" : "Egypt",
        "EH" : "Western Sahara",
        "ER" : "Eritrea",
        "ES" : "Spain",
        "ET" : "Ethiopia",
        "FI" : "Finland",
        "FJ" : "Fiji",
        "FK" : "Falkland Islands (Malvinas)",
        "FM" : "Federated States of Micronesia",
        "FO" : "Faroe Islands",
        "FR" : "France",
        "GA" : "Gabon",
        "GB" : "United Kingdom",
        "GD" : "Grenada",
        "GE" : "Georgia",
        "GF" : "French Guiana",
        "GG" : "Guernsey",
        "GH" : "Ghana",
        "GI" : "Gibraltar",
        "GL" : "Greenland",
        "GM" : "Gambia",
        "GN" : "Guinea",
        "GP" : "Guadeloupe",
        "GQ" : "Equatorial Guinea",
        "GR" : "Greece",
        "GS" : "South Georgia and the South Sandwich Islands",
        "GT" : "Guatemala",
        "GU" : "Guam",
        "GW" : "Guinea-Bissau",
        "GY" : "Guyana",
        "HK" : "Hong Kong",
        "HM" : "Heard Island and McDonald Islands",
        "HN" : "Honduras",
        "HR" : "Croatia",
        "HT" : "Haiti",
        "HU" : "Hungary",
        "ID" : "Indonesia",
        "IE" : "Ireland",
        "IL" : "Israel",
        "IM" : "Isle of Man",
        "IN" : "India",
        "IO" : "British Indian Ocean Territory",
        "IQ" : "Iraq",
        "IR" : "Islamic Republic of Iran",
        "IS" : "Iceland",
        "IT" : "Italy",
        "JE" : "Jersey",
        "JM" : "Jamaica",
        "JO" : "Jordan",
        "JP" : "Japan",
        "KE" : "Kenya",
        "KG" : "Kyrgyzstan",
        "KH" : "Cambodia",
        "KI" : "Kiribati",
        "KM" : "Comoros",
        "KN" : "Saint Kitts and Nevis",
        "KP" : "Democratic People's Republic of Korea",
        "KR" : "Republic of Korea",
        "KW" : "Kuwait",
        "KY" : "Cayman Islands",
        "KZ" : "Kazakhstan",
        "LA" : "Lao People's Democratic Republic",
        "LB" : "Lebanon",
        "LC" : "Saint Lucia",
        "LI" : "Liechtenstein",
        "LK" : "Sri Lanka",
        "LR" : "Liberia",
        "LS" : "Lesotho",
        "LT" : "Lithuania",
        "LU" : "Luxembourg",
        "LV" : "Latvia",
        "LY" : "Libya",
        "MA" : "Morocco",
        "MC" : "Monaco",
        "MD" : "Republic of Moldova",
        "ME" : "Montenegro",
        "MF" : "Saint Martin (French part)",
        "MG" : "Madagascar",
        "MH" : "Marshall Islands",
        "MK" : "The Former Yugoslav Republic of Macedonia",
        "ML" : "Mali",
        "MM" : "Myanmar",
        "MN" : "Mongolia",
        "MO" : "Macao",
        "MP" : "Northern Mariana Islands",
        "MQ" : "Martinique",
        "MR" : "Mauritania",
        "MS" : "Montserrat",
        "MT" : "Malta",
        "MU" : "Mauritius",
        "MV" : "Maldives",
        "MW" : "Malawi",
        "MX" : "Mexico",
        "MY" : "Malaysia",
        "MZ" : "Mozambique",
        "NA" : "Namibia",
        "NC" : "New Caledonia",
        "NE" : "Niger",
        "NF" : "Norfolk Island",
        "NG" : "Nigeria",
        "NI" : "Nicaragua",
        "NL" : "Netherlands",
        "NO" : "Norway",
        "NP" : "Nepal",
        "NR" : "Nauru",
        "NU" : "Niue",
        "NZ" : "New Zealand",
        "OM" : "Oman",
        "PA" : "Panama",
        "PE" : "Peru",
        "PF" : "French Polynesia",
        "PG" : "Papua New Guinea",
        "PH" : "Philippines",
        "PK" : "Pakistan",
        "PL" : "Poland",
        "PM" : "Saint Pierre and Miquelon",
        "PN" : "Pitcairn",
        "PR" : "Puerto Rico",
        "PS" : "State of Palestine",
        "PT" : "Portugal",
        "PW" : "Palau",
        "PY" : "Paraguay",
        "QA" : "Qatar",
        "RE" : "Réunion",
        "RO" : "Romania",
        "RS" : "Serbia",
        "RU" : "Russian Federation",
        "RW" : "Rwanda",
        "SA" : "Saudi Arabia",
        "SB" : "Solomon Islands",
        "SC" : "Seychelles",
        "SD" : "Sudan",
        "SE" : "Sweden",
        "SG" : "Singapore",
        "SH" : "Saint Helena, Ascension and Tristan da Cunha",
        "SI" : "Slovenia",
        "SJ" : "Svalbard and Jan Mayen",
        "SK" : "Slovakia",
        "SL" : "Sierra Leone",
        "SM" : "San Marino",
        "SN" : "Senegal",
        "SO" : "Somalia",
        "SR" : "Suriname",
        "SS" : "South Sudan",
        "ST" : "Sao Tome and Principe",
        "SV" : "El Salvador",
        "SX" : "Sint Maarten",
        "SY" : "Syrian Arab Republic",
        "SZ" : "Swaziland",
        "TC" : "Turks and Caicos Islands",
        "TD" : "Chad",
        "TF" : "French Southern Territories",
        "TG" : "Togo",
        "TH" : "Thailand",
        "TJ" : "Tajikistan",
        "TK" : "Tokelau",
        "TL" : "Timor-Leste",
        "TM" : "Turkmenistan",
        "TN" : "Tunisia",
        "TO" : "Tonga",
        "TR" : "Turkey",
        "TT" : "Trinidad and Tobago",
        "TV" : "Tuvalu",
        "TW" : "Taiwan, Province of China",
        "TZ" : "United Republic of Tanzania",
        "UA" : "Ukraine",
        "UG" : "Uganda",
        "UM" : "United States Minor Outlying Islands",
        "US" : "United States",
        "UY" : "Uruguay",
        "UZ" : "Uzbekistan",
        "VA" : "Holy See (Vatican City State)",
        "VC" : "Saint Vincent and the Grenadines",
        "VE" : "Bolivarian Republic of Venezuela",
        "VG" : "British Virgin Islands",
        "VI" : "U.S. Virgin Islands",
        "VN" : "Viet Nam",
        "VU" : "Vanuatu",
        "WF" : "Wallis and Futuna",
        "WS" : "Samoa",
        "YE" : "Yemen",
        "YT" : "Mayotte",
        "ZA" : "South Africa",
        "ZM" : "Zambia",
        "ZW" : "Zimbabwe",
    }

# END Class isoCountry
