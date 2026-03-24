import pandas as pd

# ==========================================
# 1. CARGAR Y OPTIMIZAR HABILIDADES
# ==========================================
hb = pd.read_csv("Habilidades.csv")
ph = pd.read_csv("Pokemon_Habilidad.csv")

# LIMPIEZA Y CONSISTENCIA (CamelCase)
hb['nombre_habilidad'] = (hb['nombre_habilidad']
                          .str.replace(r"[\[\]']", "", regex=True)
                          .str.strip()
                          .str.capitalize()) # ✅ Consistencia de Formato

# MAPEO E INTEGRIDAD
mapa_viejo_id = dict(zip(hb['id_habilidad'], hb['nombre_habilidad']))
hb_unica = hb.drop_duplicates(subset=['nombre_habilidad']).copy()
hb_unica['id_nuevo'] = range(1, len(hb_unica) + 1)

# ACTUALIZAR RELACIÓN (Pokemon_Habilidad)
ph['nombre_temp'] = ph['id_habilidad'].map(mapa_viejo_id)
mapa_nombre_nuevo_id = dict(zip(hb_unica['nombre_habilidad'], hb_unica['id_nuevo']))
ph['id_habilidad'] = ph['nombre_temp'].map(mapa_nombre_nuevo_id)

# GUARDAR HABILIDADES
hb_final = hb_unica[['id_nuevo', 'nombre_habilidad']].rename(columns={'id_nuevo': 'id_habilidad'})
ph_final = ph[['No_Pokedex', 'id_habilidad']]
hb_final.to_csv("Habilidades.csv", index=False)
ph_final.to_csv("Pokemon_Habilidad.csv", index=False)

# ==========================================
# 2. OPTIMIZAR TIPOS (Consistencia CamelCase)
# ==========================================
tipos = pd.read_csv("Tipos.csv")
tipos['nombre_tipo'] = tipos['nombre_tipo'].str.capitalize()
tipos.to_csv("Tipos.csv", index=False)

# ==========================================
# 3. REFACTORIZACIÓN DE TIPOS NUMÉRICOS
# ==========================================
# Optimizar Estadísticas (Forzar Enteros)
est = pd.read_csv("Estadisticas.csv")
cols_stats = ["Puntos_de_salud", "ataque", "defensa", "ataque_especial", 
              "defensa_especial", "velocidad", "total_base"]
est[cols_stats] = est[cols_stats].astype(int)
est.to_csv("Estadisticas.csv", index=False)

# Optimizar Efectividad (Asegurar Float para multiplicadores)
efec = pd.read_csv("Tipo_Efectividad.csv")
efec['multiplicador'] = efec['multiplicador'].astype(float)
efec.to_csv("Tipo_Efectividad.csv", index=False)

print("🚀 PROCESO DE OPTIMIZACIÓN COMPLETO 🚀")
print(f"✅ Habilidades unificadas: {len(hb_final)} registros.")
print("✅ Consistencia CamelCase aplicada a Tipos y Habilidades.")
print("✅ Tipado numérico (Int/Float) refactorizado con éxito.")