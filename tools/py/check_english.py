import json, re

en_words = ['the','and','for','with','from','that','this','are','you','your','our','we','to','of','in','is','it','on','as','at','be','by','or','an','if','up','so','do','no','go','me','us','my','he','she','they','them','their','there','then','than','when','where','what','who','how','why','which','while','will','would','could','should','may','might','can','shall','have','has','had','been','being','was','were','am','are','is','does','did','done','get','got','make','made','take','took','come','came','see','saw','know','knew','think','thought','say','said','tell','told','ask','asked','work','worked','try','tried','use','used','find','found','give','gave','look','looked','feel','felt','seem','seemed','want','wanted','show','showed','hear','heard','play','played','run','ran','move','moved','live','lived','believe','believed','bring','brought','happen','happened','write','wrote','provide','provided','sit','sat','stand','stood','lose','lost','pay','paid','meet','met','include','included','continue','continued','set','sets','learn','learned','change','changed','lead','led','understand','understood','watch','watched','follow','followed','stop','stopped','create','created','speak','spoke','allow','allowed','read','add','added','spend','spent','grow','grew','open','opened','walk','walked','offer','offered','remember','remembered','love','loved','consider','considered','appear','appeared','buy','bought','wait','waited','serve','served','die','died','send','sent','expect','expected','build','built','stay','stayed','fall','fell','cut','cuts','reach','reached','kill','killed','remain','remained','suggest','suggested','raise','raised','pass','passed','sell','sold','require','required','report','reported','decide','decided','pull','pulled','carry','carried','develop','developed','hope','hoped','drive','drove','break','broke','receive','received','agree','agreed','support','supported','remove','removed','return','returned','describe','described','apply','applied','avoid','avoided','prepare','prepared','compare','compared','declare','declared']

with open('translations/extract.json','r',encoding='utf-8') as f:
    data=json.load(f)

untranslated = [i for i in data if not i.get('translated')]
print(f'Untranslated fields: {len(untranslated)}')

has_english = []
for item in untranslated:
    text = item['original'].lower()
    found = [w for w in en_words if re.search(r'\b' + re.escape(w) + r'\b', text)]
    if found:
        has_english.append((item, found))

print(f'Fields with English words: {len(has_english)}')
for item, words in has_english[:30]:
    preview = item['original'][:100].replace('\n',' ')
    print(f'  Page {item["page_id"]} [{item["widget_type"]}] words={words[:5]}')
    print(f'    {preview}...')
    print()
