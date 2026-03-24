import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import matplotlib.colors as mcolors

warnings.filterwarnings("ignore", category=UserWarning)

def generar_grafica_final_coloquio():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="espino2814",
            database="pokemon_db"
        )
        
        query = """
        SELECT p.nombre, t.nombre_tipo, e.total_base, 
               e.Puntos_de_salud, e.Ataque, e.Defensa, e.Ataque_Especial, e.Defensa_Especial, e.Velocidad
        FROM Pokemon_Base p
        JOIN Pokemon_Tipo pt ON p.No_Pokedex = pt.No_Pokedex
        JOIN Tipos t ON pt.id_tipo = t.id_tipo
        JOIN Estadisticas e ON p.No_Pokedex = e.No_Pokedex
        ORDER BY e.total_base DESC
        LIMIT 10;
        """
        df = pd.read_sql(query, conn)

        # 1. CÁLCULO Y NORMALIZACIÓN (600 BST = 20 IE)
        def calcular_ie(row):
            stats = [row['Puntos_de_salud'], row['Ataque'], row['Defensa'], 
                     row['Ataque_Especial'], row['Defensa_Especial'], row['Velocidad']]
            return (max(stats) / (row['total_base'] / 6)) * 10

        df['IE'] = df.apply(calcular_ie, axis=1)
        df['IE_Visual'] = df['IE'] * 30  # Factor 30 para que 20 IE = 600 BST

        # 2. ESTÉTICA
        plt.figure(figsize=(18, 9), facecolor='#0B0E11')
        ax = plt.gca()
        ax.set_facecolor('#13171C')

        tipos_unicos = df['nombre_tipo'].unique()
        colores_base = sns.color_palette("magma", n_colors=len(tipos_unicos))
        tipo_to_color = dict(zip(tipos_unicos, colores_base))

        def aclarar_color(color, factor=0.5):
            rgb = mcolors.to_rgb(color)
            return tuple((1-factor)*c + factor for c in rgb)

        df['color_base'] = df['nombre_tipo'].map(tipo_to_color)
        df['color_claro'] = df['color_base'].apply(aclarar_color)

        # 3. RENDERIZADO
        ax.barh(df['nombre'], df['total_base'], color=df['color_base'], 
                edgecolor='white', linewidth=1, alpha=0.8, height=0.7)

        ax.barh(df['nombre'], df['IE_Visual'], color=df['color_claro'], 
                edgecolor='white', linewidth=1.5, alpha=1.0, height=0.25)

        # 4. MARCADOR AMARILLO FOSFORESCENTE (IE 20 = 600)
        # Dibujamos una pequeña marca visual en el eje superior para referencia
        plt.text(600, -0.8, '20 IE', color='#CCFF00', fontweight='bold', 
                 ha='center', fontsize=12, bbox=dict(facecolor='black', alpha=0.5, edgecolor='#CCFF00'))
        plt.axvline(x=600, color='#CCFF00', linestyle=':', alpha=0.3)

        # 5. ETIQUETADO
        for i in range(len(df)):
            bst = df.iloc[i]['total_base']
            ie = df.iloc[i]['IE']
            plt.text(bst + 12, i, f"{int(bst)} BST | IE: {ie:.1f}", 
                     color='white', va='center', fontweight='bold', fontsize=10)

        # 6. TÍTULO Y LEYENDA TÉCNICA
        plt.title('MAPA DE DOMINANCIA GLOBAL: POTENCIA (BST) VS ESPECIALIZACIÓN (IE)', 
                  color='white', fontsize=18, fontweight='bold', pad=45)
        
        # Subtítulo explicativo de escalas
        plt.text(0.5, 1.02, 'Escalas: Potencia Total [0 - 800 BST] | Especialización [0 - 20 IE]', 
                 color='#CCFF00', fontsize=12, ha='center', va='bottom', transform=ax.transAxes, fontweight='bold')

        plt.xlabel('MAGNITUD DE DATOS (BST/IE)', color='white', fontweight='bold')
        plt.xticks(color='white', fontweight='bold')
        plt.yticks(color='white', fontsize=11, fontweight='bold')
        plt.xlim(0, 950)

        # Leyenda de tipos
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=tipo_to_color[t], edgecolor='white', label=t) for t in tipos_unicos]
        
        plt.legend(handles=legend_elements, title='Agrupación por Tipo', 
                   bbox_to_anchor=(1.02, 0.05), loc='lower left', 
                   facecolor='#13171C', edgecolor='white', labelcolor='white')

        for spine in ax.spines.values():
            spine.set_visible(False)
        plt.grid(axis='x', linestyle='--', alpha=0.03)
        
        plt.tight_layout()
        plt.savefig('grafica_maestra_final_coloquio.png', dpi=300, facecolor='#0B0E11')
        print("🚀 Gráfica definitiva con marcador de escala (20 IE : 600 BST) generada.")
        plt.show()

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    generar_grafica_final_coloquio()