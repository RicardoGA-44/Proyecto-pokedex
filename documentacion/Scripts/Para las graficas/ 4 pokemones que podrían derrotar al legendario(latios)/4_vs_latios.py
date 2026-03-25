import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

def generar_grafica_climax_tactico():
    try:
        conn = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="espino2814", 
            database="pokemon_db"
        )
        
        query = """
        SELECT 
            p.nombre, 
            MAX(t.nombre_tipo) AS nombre_tipo, 
            MAX(e.total_base) AS total_base, 
            MAX(h.nombre_habilidad) AS nombre_habilidad
        FROM Pokemon_Base p
        JOIN Pokemon_Tipo pt ON p.No_Pokedex = pt.No_Pokedex
        JOIN Tipos t ON pt.id_tipo = t.id_tipo
        JOIN Estadisticas e ON p.No_Pokedex = e.No_Pokedex
        JOIN Pokemon_Habilidad ph ON p.No_Pokedex = ph.No_Pokedex
        JOIN Habilidades h ON ph.id_habilidad = h.id_habilidad
        WHERE p.nombre IN ('Glalie', 'Pheromosa', 'Floette', 'Mamoswine')
        GROUP BY p.nombre
        ORDER BY total_base DESC;
        """

        df = pd.read_sql(query, conn)

        def aplicar_logica_explicita(row):
            n, t, h = row['nombre'], row['nombre_tipo'], row['nombre_habilidad']
            if n == 'Glalie':
                f = f"FORTALEZA: Ventaja Elemental {t.upper()}. Inflige daño x2 masivo a Latios."
                h_desc = f"HABILIDAD [{h}]: Inmunidad al retroceso. Asegura ataques sin interrupciones."
            elif n == 'Pheromosa':
                f = f"FORTALEZA: Velocidad Superior. Supera los 110 puntos base de Latios para golpear primero."
                h_desc = f"HABILIDAD [{h}]: Efecto Bola de Nieve. Incrementa el Ataque tras cada baja operativa."
            elif n == 'Floette':
                f = f"FORTALEZA: Inmunidad de Tipo {t.upper()}. Recibe 0 daño de los movimientos Dragón de Latios."
                h_desc = f"HABILIDAD [{h}]: Blindaje de Stats. Impide que Latios reduzca las defensas del equipo."
            elif n == 'Mamoswine':
                f = f"FORTALEZA: Debilidad Crítica x4. Explota la vulnerabilidad combinada de Latios al Hielo."
                h_desc = f"HABILIDAD [{h}]: Estabilidad Mental. Inmune a Mofa; garantiza el uso de movimientos de estado."
            else:
                f, h_desc = "Atributos estándar", f"Habilidad: {h}"
            return f, h_desc

        df['Fortaleza'], df['Habilidad'] = zip(*df.apply(aplicar_logica_explicita, axis=1))
        
        # --- MODIFICACIÓN: Se elimina .clip(upper=100) ---
        df['Victoria'] = ((df['total_base'] / 7) + 22)

        plt.figure(figsize=(15, 8), facecolor='#0B0E11')
        ax = plt.gca()
        ax.set_facecolor('#13171C')

        colores_estables = ['#2E5A88', '#A93226', '#1E8449', '#D68910']
        barras = sns.barplot(x='Victoria', y='nombre', data=df, palette=colores_estables, edgecolor='white', linewidth=2.5)

        for i, bar in enumerate(barras.patches):
            pkm = df.iloc[i]
            # Se añade un pequeño texto al final de la barra para ver el valor exacto
            plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, f"{pkm['Victoria']:.1f}%", 
                     color='white', va='center', fontweight='bold')
            
            plt.text(1.5, bar.get_y() + 0.25, f"» UNIDAD: {pkm['nombre'].upper()} | PROTOCOLO: {pkm['nombre_tipo'].upper()}", color='white', fontweight='bold', fontsize=12)
            plt.text(1.5, bar.get_y() + 0.50, pkm['Fortaleza'], color='white', fontweight='bold', fontsize=11)
            plt.text(1.5, bar.get_y() + 0.75, pkm['Habilidad'], color='white', fontweight='bold', fontsize=11)

        plt.title('MODELO DE INCURSIÓN TÁCTICA: ANÁLISIS EXPLICITÓ VS LATIOS', color='white', fontsize=18, fontweight='bold', pad=30)
        plt.xlabel('PROBABILIDAD DE ÉXITO OPERATIVO (%)', color='white', fontweight='bold', fontsize=12)
        plt.ylabel('', color='white')

        # --- MODIFICACIÓN: Ajuste de rango de ticks para mostrar más allá del 100 ---
        max_val = int(df['Victoria'].max()) + 10
        plt.xticks(range(0, max_val, 10), color='white', fontweight='bold')
        plt.xlim(0, max_val)

        plt.yticks(color='white', fontweight='bold')
        plt.grid(axis='x', linestyle='--', alpha=0.1)
        plt.tight_layout()

        nombre_archivo = "Estrategia_Latios_Sobrepasada.png"
        plt.savefig(nombre_archivo, dpi=300, facecolor='#0B0E11')
        
        print(f"🚀 Gráfica guardada como: {nombre_archivo}")
        print("Cálculo de sobre-eficiencia completado.")
        plt.show()

    except Exception as e:
        print(f"❌ Error crítico: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    generar_grafica_climax_tactico()