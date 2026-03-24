import pandas as pd

# =========================
# 1. CARGAR CSV LIMPIO
# =========================
df = pd.read_csv("csv_pokemon_limpio.csv")

# =========================
# 2. TABLA Pokemon_Base
# =========================
pokemon_base = df[[
    "No_Pokedex",
    "nombre",
    "Probabilidad_de_captura"
]].copy()

pokemon_base.to_csv("Pokemon_Base.csv", index=False)

# =========================
# 3. TABLA Estadisticas
# =========================
estadisticas = df[[
    "No_Pokedex",
    "Puntos_de_salud",
    "ataque",
    "defensa",
    "ataque_especial",
    "defensa_especial",
    "velocidad",
    "total_base"
]].copy()

estadisticas.to_csv("Estadisticas.csv", index=False)

# =========================
# 4. TABLA Tipos
# =========================
tipos_unicos = pd.concat([df["tipo1"], df["tipo2"]]).dropna().unique()

tipos = pd.DataFrame({
    "id_tipo": range(1, len(tipos_unicos) + 1),
    "nombre_tipo": tipos_unicos
})

tipos.to_csv("Tipos.csv", index=False)

mapa_tipos = dict(zip(tipos["nombre_tipo"], tipos["id_tipo"]))

# =========================
# 5. TABLA Pokemon_Tipo
# =========================
pokemon_tipo = []

for _, row in df.iterrows():
    if pd.notna(row["tipo1"]):
        pokemon_tipo.append([row["No_Pokedex"], mapa_tipos[row["tipo1"]]])
    
    if pd.notna(row["tipo2"]) and row["tipo2"] != "No aplica":
        pokemon_tipo.append([row["No_Pokedex"], mapa_tipos[row["tipo2"]]])

pokemon_tipo_df = pd.DataFrame(pokemon_tipo, columns=["No_Pokedex", "id_tipo"])
pokemon_tipo_df.to_csv("Pokemon_Tipo.csv", index=False)

# =========================
# 6. TABLA Habilidades
# =========================
habilidades_set = set()

for habilidades in df["habilidades"].dropna():  # 🔥 corregido
    for h in str(habilidades).split(","):
        h = h.strip()
        if h:
            habilidades_set.add(h)

habilidades_lista = sorted(list(habilidades_set))

habilidades = pd.DataFrame({
    "id_habilidad": range(1, len(habilidades_lista) + 1),
    "nombre_habilidad": habilidades_lista
})

habilidades.to_csv("Habilidades.csv", index=False)

mapa_habilidades = dict(zip(habilidades["nombre_habilidad"], habilidades["id_habilidad"]))
# =========================
# 7. TABLA Pokemon_Habilidad
# =========================
pokemon_habilidad = []

for _, row in df.iterrows():
    if pd.notna(row["habilidades"]):  # 🔥 corregido
        for h in str(row["habilidades"]).split(","):
            h = h.strip()
            if h in mapa_habilidades:
                pokemon_habilidad.append([
                    row["No_Pokedex"],
                    mapa_habilidades[h]
                ])

pokemon_habilidad_df = pd.DataFrame(
    pokemon_habilidad,
    columns=["No_Pokedex", "id_habilidad"]
)

pokemon_habilidad_df.to_csv("Pokemon_Habilidad.csv", index=False)

# =========================
# 8. TABLA Tipo_Efectividad (REAL)
# =========================

# 1. Normalizar nombres en el DataFrame (Poner la primera en Mayúscula)
tipos["nombre_tipo"] = tipos["nombre_tipo"].str.capitalize()

# 2. 🔥 ACTUALIZAR EL MAPA DE TIPOS (Esto arregla el KeyError)
# Ahora el mapa tendrá las llaves con Mayúscula: {'Grass': 1, 'Fire': 2...}
mapa_tipos = dict(zip(tipos["nombre_tipo"], tipos["id_tipo"]))
# Definir efectividad
efectividad = {
    "Normal": {"Rock": 0.5, "Ghost": 0, "Steel": 0.5},
    "Fire": {"Grass": 2, "Ice": 2, "Bug": 2, "Steel": 2,
             "Fire": 0.5, "Water": 0.5, "Rock": 0.5, "Dragon": 0.5},
    "Water": {"Fire": 2, "Ground": 2, "Rock": 2,
              "Water": 0.5, "Grass": 0.5, "Dragon": 0.5},
    "Electric": {"Water": 2, "Flying": 2,
                 "Electric": 0.5, "Grass": 0.5, "Dragon": 0.5, "Ground": 0},
    "Grass": {"Water": 2, "Ground": 2, "Rock": 2,
              "Fire": 0.5, "Grass": 0.5, "Poison": 0.5,
              "Flying": 0.5, "Bug": 0.5, "Dragon": 0.5, "Steel": 0.5},
    "Ice": {"Grass": 2, "Ground": 2, "Flying": 2, "Dragon": 2,
            "Fire": 0.5, "Water": 0.5, "Ice": 0.5, "Steel": 0.5},
    "Fighting": {"Normal": 2, "Ice": 2, "Rock": 2, "Dark": 2, "Steel": 2,
                 "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5,
                 "Bug": 0.5, "Fairy": 0.5, "Ghost": 0},
    "Poison": {"Grass": 2, "Fairy": 2,
               "Poison": 0.5, "Ground": 0.5, "Rock": 0.5,
               "Ghost": 0.5, "Steel": 0},
    "Ground": {"Fire": 2, "Electric": 2, "Poison": 2,
               "Rock": 2, "Steel": 2,
               "Grass": 0.5, "Bug": 0.5, "Flying": 0},
    "Flying": {"Grass": 2, "Fighting": 2, "Bug": 2,
               "Electric": 0.5, "Rock": 0.5, "Steel": 0.5},
    "Psychic": {"Fighting": 2, "Poison": 2,
                "Psychic": 0.5, "Steel": 0.5, "Dark": 0},
    "Bug": {"Grass": 2, "Psychic": 2, "Dark": 2,
            "Fire": 0.5, "Fighting": 0.5, "Poison": 0.5,
            "Flying": 0.5, "Ghost": 0.5, "Steel": 0.5, "Fairy": 0.5},
    "Rock": {"Fire": 2, "Ice": 2, "Flying": 2, "Bug": 2,
             "Fighting": 0.5, "Ground": 0.5, "Steel": 0.5},
    "Ghost": {"Psychic": 2, "Ghost": 2,
              "Dark": 0.5, "Normal": 0},
    "Dragon": {"Dragon": 2, "Steel": 0.5, "Fairy": 0},
    "Dark": {"Psychic": 2, "Ghost": 2,
             "Fighting": 0.5, "Dark": 0.5, "Fairy": 0.5},
    "Steel": {"Ice": 2, "Rock": 2, "Fairy": 2,
              "Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Steel": 0.5},
    "Fairy": {"Fighting": 2, "Dragon": 2, "Dark": 2,
              "Fire": 0.5, "Poison": 0.5, "Steel": 0.5}
}

tipo_efectividad = []

# 4. Generar la matriz
for atacante in tipos["nombre_tipo"]:
    for defensor in tipos["nombre_tipo"]:
        mult = 1.0
        
        # Ahora atacante y defensor son "Grass", "Fire", etc.
        if atacante in efectividad and defensor in efectividad[atacante]:
            mult = efectividad[atacante][defensor]

        tipo_efectividad.append([
            mapa_tipos[atacante],
            mapa_tipos[defensor],
            mult
        ])

tipo_efectividad_df = pd.DataFrame(
    tipo_efectividad, 
    columns=["id_tipo_ataque", "id_tipo_defensa", "multiplicador"]
)

tipo_efectividad_df.to_csv("Tipo_Efectividad.csv", index=False)
# =========================
# FINAL
# =========================
print("✔ Normalización completa con matriz real de efectividad")