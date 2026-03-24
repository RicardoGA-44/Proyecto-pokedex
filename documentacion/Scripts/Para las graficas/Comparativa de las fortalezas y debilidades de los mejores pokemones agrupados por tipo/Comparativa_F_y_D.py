import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

def generar_grafica_3_final_absoluta():
    try:
        conn = mysql.connector.connect(
            host="localhost", 
            user="root",
            password="espino2814", 
            database="pokemon_db"
        )
        
        query = """
        SELECT p.nombre, t.nombre_tipo, e.total_base
        FROM Pokemon_Base p
        JOIN Pokemon_Tipo pt ON p.No_Pokedex = pt.No_Pokedex
        JOIN Tipos t ON pt.id_tipo = t.id_tipo
        JOIN Estadisticas e ON p.No_Pokedex = e.No_Pokedex
        ORDER BY e.total_base DESC LIMIT 10;
        """

        df = pd.read_sql(query, conn)
        # Ordenamos para agrupar por tipo visualmente
        df = df.sort_values(by='nombre_tipo')

        # Diccionario de efectividades (F: Fortalezas / D: Debilidades)
        efectividades = {
            'Dragon':  {'F': ['Dragon'], 'D': ['Ice', 'Fairy', 'Dragon']},
            'Ground':  {'F': ['Electric', 'Fire', 'Rock', 'Steel'], 'D': ['Water', 'Grass', 'Ice']},
            'Psychic': {'F': ['Fighting', 'Poison'], 'D': ['Bug', 'Ghost', 'Dark']},
            'Water':   {'F': ['Fire', 'Ground', 'Rock'], 'D': ['Electric', 'Grass']},
            'Steel':   {'F': ['Ice', 'Rock', 'Fairy'], 'D': ['Fire', 'Fighting', 'Ground']},
            'Normal':  {'F': ['Ninguno'], 'D': ['Fighting']},
            'Rock':    {'F': ['Fire', 'Ice', 'Flying', 'Bug'], 'D': ['Water', 'Grass', 'Fighting', 'Ground', 'Steel']}
        }

        palette = {
            'Dragon': ('#00F2FF', '#004D52'), 
            'Ground': ('#E0C068', '#5E512C'),
            'Psychic': ('#F85888', '#632336'), 
            'Water': ('#6890F0', '#2B3C63'),
            'Steel': ('#B8B8D0', '#4A4A54'), 
            'Normal': ('#A8A878', '#424230'),
            'Rock': ('#B8A038', '#4A4016')
        }

        plt.figure(figsize=(20, 11), facecolor='#0B0E11')
        ax = plt.gca()
        ax.set_facecolor('#13171C')

        top_10_tipos = df['nombre_tipo'].tolist()
        y_pos = range(len(df))
        ancho = 0.35
        BASE_100 = 100 

        for i, row in df.iterrows():
            idx = df.index.get_loc(i)
            c_claro, c_fuerte = palette.get(row['nombre_tipo'], ('#FFFFFF', '#444444'))
            info = efectividades.get(row['nombre_tipo'])

            # Lógica de porcentajes basada en el Top 10 actual
            pct_cobertura = (sum(1 for t in top_10_tipos if t in info['F']) / 10) * 100
            pct_riesgo = (sum(1 for t in top_10_tipos if t in info['D']) / 10) * 100

            # --- BARRA FORTALEZA / BST (Barra más grande) ---
            plt.barh(idx - ancho/2, row['total_base'], ancho, color=c_claro, alpha=0.9, zorder=3)
            
            # Texto corregido: Incluye Dominancia, BST y Fortalezas Elementales
            txt_fortalezas = f"DOMINANCIA: {pct_cobertura}% | BST: {row['total_base']} | FUERTE CONTRA: {info['F']}"
            plt.text(10, idx - ancho/2, txt_fortalezas, 
                     color='black', va='center', fontweight='bold', fontsize=9)

            # --- BARRA VULNERABILIDAD (Barra superior oscura) ---
            longitud_vulnerabilidad = BASE_100 + ((pct_riesgo / 100) * (800 - BASE_100))
            plt.barh(idx + ancho/2, longitud_vulnerabilidad, ancho, color=c_fuerte, alpha=0.9, zorder=3)
            
            # Texto informativo de debilidades
            txt_riesgo = f"RIESGO: {pct_riesgo}% | DÉBIL A: {info['D']}"
            plt.text(10, idx + ancho/2, txt_riesgo, 
                     color='white', va='center', fontweight='bold', fontsize=9)

        # Configuración de Ejes
        plt.xlim(0, 850)
        plt.xticks([0, 100, 200, 300, 400, 500, 600, 700, 800], color='white', fontsize=11, fontweight='bold')
        
        plt.xlabel("ESC. TOTAL DE STATS (0-800) | ESC. DE PORCENTAJE DE RIESGO (100-800)", 
                   color='white', labelpad=20, fontweight='bold', fontsize=12)

        plt.yticks(y_pos, [f"{n.upper()} [{t.upper()}]" for n, t in zip(df['nombre'], df['nombre_tipo'])], 
                   color='white', fontweight='bold', fontsize=10)

        plt.title('Top 10 pokemon: POTENCIA BASE (PROS) VS. VULNERABILIDAD (CONTRAS)', 
                  color='white', fontsize=18, fontweight='bold', pad=50, y=0.92)
        
        plt.grid(axis='x', color='#333333', linestyle='--', alpha=0.3, zorder=0)
        for s in ['top', 'right']: 
            ax.spines[s].set_visible(False)

        ax.spines['bottom'].set_color('#444444')
        ax.spines['left'].set_color('#444444')

        plt.tight_layout(pad=5)
        plt.savefig("Grafica_Final_Fortalezas.png", dpi=300, facecolor='#0B0E11')
        plt.show()

    except Exception as e: 
        print(f"Error: {e}")

    finally: 
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    generar_grafica_3_final_absoluta()