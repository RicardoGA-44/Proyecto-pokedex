import pandas as pd

# Cargar archivo (debe estar en la misma carpeta que el script)
df = pd.read_csv("csv_pokemon_original.csv")

# =========================
# 1. ELIMINAR COLUMNAS
# =========================
columnas_eliminar = [
    "nombre_japones",
    "pasos_base_para_eclosion",
    "felicidad_base",
    "clasificación",
    "crecimiento_experiencia",
    "altura_(m)",
    "%_macho",
    "peso_(kg)",
    "generación",
    "es_legendario"
]

df = df.drop(columns=columnas_eliminar, errors='ignore')

# =========================
# 2. LIMPIAR ESPACIOS
# =========================
df.columns = df.columns.str.strip()

for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.strip()

# =========================
# 3. VALORES NULOS
# =========================
if "tipo2" in df.columns:
    df["tipo2"] = df["tipo2"].fillna("No aplica")

# =========================
# 4. GUARDAR CSV LIMPIO
# =========================
df.to_csv("pokemon_limpio.csv", index=False)

print("Archivo limpio generado: pokemon_limpio.csv")