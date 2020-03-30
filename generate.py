import sys, os, json




name = sys.argv[1]

try:
    overwrite = int(sys.argv[2])
    assert overwrite == 1
    
except:
    overwrite = 0


cfg_path = os.path.join(name, "config.json")

cfg = json.loads(open(cfg_path).read())

categories = cfg["categories"]

for c in categories:
    if not os.path.exists(os.path.join(name, c)):
        os.mkdir(os.path.join(name, c))


challenges = cfg["challenges"]
columns = ["Challenge Name"] + list(map(lambda x: x.capitalize(), cfg["columns"]))

notes = "\n\n".join([f"## {key.capitalize()}" for key in cfg["index"]["notes"]])

challenges_header = "| " + " | ".join(columns) + " |"


index_template = f"""
# {name.strip('/')}

{notes}

# Challenges
{challenges_header}
{"|:-:"*len(columns) + "|"}
"""

namesCategory = {i:[] for i in cfg["categories"]}

for key, val in challenges.items():
    
    if not len(namesCategory[val["category"]]):
        namesCategory[val["category"]].append(key)
        continue


    comparisonGroup = namesCategory[val["category"]]
    
    for i in range(len(comparisonGroup)):
        compareTo = comparisonGroup[i]

        try:
            if int(challenges[compareTo]["points"]) > int(val["points"]):
                namesCategory[val["category"]].insert(i, key)
                break
        except KeyError:
            namesCategory[val["category"]].insert(i, key)
            break

    else:
        namesCategory[val["category"]].append(key)



categories = sorted(cfg["categories"])

for cat, challs in namesCategory.items():
    toAdd = ""
    for chall in challs:
        for col in columns:
            if col == "Challenge Name":
                toAdd += f"|[{chall}]({cat+'/'+chall.replace(' ', '-')+'.md'})"
                continue

            toAdd += "|" + challenges[chall][col.lower()]

        toAdd += "|\n"
        
    index_template += toAdd


for chall, amt in challenges.items():
    chall = chall.replace(" ", "-")
    fname = os.path.join(name, amt['category'].lower(), chall+".md")

    if overwrite:
        with open(fname, "w") as f:
            f.write(f"# {chall}\n{amt['category'].capitalize()}")#, {amt['points']}" + )

    else:
        if not os.path.exists(fname):
            with open(fname, "w") as f:
                f.write(f"# {chall}\n{amt['category'].capitalize()}")#, {amt['points']}")
                

if overwrite:
    with open(os.path.join(name, "index.md"), "w") as f:
        f.write(index_template)

else:
    if not os.path.exists(os.path.join(name, "README.md")):
            with open(os.path.join(name, "index.md"), "w") as f:
                f.write(index_template)



