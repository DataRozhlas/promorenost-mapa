# %%
import pandas as pd
import json
# %%
ok = pd.read_excel('./analyza.xlsx', sheet_name='výsledky')
ob = pd.read_excel('./analyza.xlsx', sheet_name='výsledky obce')

# %%
ob = ob[ob.obyvatel >= 10000]
# %%
with open('./okresy.json', 'r', encoding='utf-8') as f:
    ok_jsn = json.loads(f.read())

with open('./obce.json', 'r', encoding='utf-8') as f:
    ob_jsn = json.loads(f.read())

# %%
# napojeni dat obci
for obec in ob.values:
    ftr = list(filter(lambda x: x['properties']['KOD_OBEC'] == str(obec[0]), ob_jsn['features']))[0]
    ftr['properties']['nazob'] = obec[1]
    ftr['properties']['podil'] = round(obec[8] / 100, 3)

# %%
ob_jsn['features'] = list(filter(lambda x: 'nazob' in x['properties'], ob_jsn['features']))
# %%
def prep(ftr):
    if 'KOD_OBEC' in ftr['properties']:
        ftr['properties'].pop('KOD_OBEC', None)
    out = list(ftr['properties'].values())
    out.append(ftr['geometry']['coordinates'])
    return out

# %%
ob_out = list(map(prep, ob_jsn['features']))

# %%
# napojeni dat okresu
for okres in ok.values:
    ftr = list(filter(lambda x: x['properties']['NAZ_LAU1'].rstrip() == str(okres[0]), ok_jsn['features']))[0]
    ftr['properties']['podil'] = round(okres[2], 3)

# %%
ok_out = list(map(prep, ok_jsn['features']))

# %%
# prohodit XY
for val in ok_out:
    for vert in val[2]:
        for coord in vert:
            coord.reverse()
# %%
for val in ob_out:
    val[2].reverse()
# %%
with open('../data.js', 'w', encoding='utf-8') as f:
    f.write('const ok = ' + json.dumps(ok_out, ensure_ascii=False) + ';\n'
        + 'const ob = ' + json.dumps(ob_out, ensure_ascii=False) + ';'
    )
