# -*- coding: utf-8 -*-
# """
# Created on Mon Jan 15 20:31:52 2018

# @author: Manvenddra
# """

lang={"Bulgarian":"bg",
"Bengali":"bn",
"Catalan":"ca",
"Chinese Simplified":"zh-CN",
"Chinese Traditional":"zh-TW",
"Croatian":"hr",
"Czech":"cs",
"Danish":"da",
"Dutch":"nl",
"English":"en",
"Estonian":"et",
"Filipino":"tl",
"Finnish":"fi",
"French":"fr",
"Galician":"gl",
"German":"de",
"Gujarati":"gu",
"Greek":"el",
"Hebrew":"iw",
"Hindi":"hi",
"Hungarian":"hu",
"Icelandic":"is",
"Indonesian":"id",
"Irish":"ga",
"Italian":"it",
"Japanese":"ja",
"Korean":"ko",
"Kannada":"kn",
"Latvian":"lv",
"Lithuanian":"lt",
"Macedonian":"mk",
"Malay":"ms",
"Maltese":"mt",
"Norwegian":"no",
"Persian":"fa",
"Polish":"pl",
"Portuguese":"pt",
"Romanian":"ro",
"Russian":"ru",
"Serbian":"sr",
"Slovak":"sk",
"Slovenian":"sl",
"Spanish":"es",
"Swahili":"sw",
"Swedish":"sv",
"Tamil":"ta",
"Telugu":"te",
"Thai":"th",
"Turkish":"tr",
"Ukrainian":"uk",
"Vietnamese":"vi",
"Welsh":"cy",
"Yiddish":"yi"}


from PIL import Image
import pytesseract
from googletrans import Translator
translator = Translator()
im = Image.open(<Full Image Path>)
text = pytesseract.image_to_string(im)
print("Image Text contains: %s", text)

text=(text.strip()).lower()
text=text.replace("\n", " ")
text=text.replace("  ", " ")
#print(text)
lan=input("In which Language you want the response ?: ")
if text is not None and lan in lang.keys():
    res=translator.translate(text, dest=lang[lan])
    print((res.text))
