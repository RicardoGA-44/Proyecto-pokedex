import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")

def generar_reporte_complejidad_captura():
    try:
        # 1. Carga de datos (Ajustar nombre de archivo según tu CSV)
        df = pd.read_csv('csv_pokemon_limpio.csv')

        # 2. LIMPIEZA TÉCNICA: Convertir a numérico y manejar errores
        # Esto evita fallos si hay strings o espacios en blanco
        df['Probabilidad_de_captura'] = pd.to_numeric(df['Probabilidad_de_captura'], errors='coerce')
        df['Puntos_de_salud'] = pd.to_numeric(df['Puntos_de_salud'], errors='coerce')
        df['total_base'] = pd.to_numeric(df['total_base'], errors='coerce')

        # 3. DEFINICIÓN DE PENALIZADORES (Información Adicional / Comportamiento)
        # Basado en la investigación de mecánicas de huida, suicidio y recuperación
        mecanicas_reales = {
            'Beldum': 60,      # Suicidio por Recoil (Take Down)
            'Abra': 55,        # Fuga 100% Turno 1 (Teleport)
            'Entei': 45,       # Roaming / Rugido
            'Raikou': 45,      # Roaming / Rugido
            'Mewtwo': 40,      # HP Masivo + Presión + Recuperación
            'Wobbuffet': 30,   # Bloqueo Shadow Tag + Desgaste
            'Ditto': 25,       # Transformación (Copia stats del jugador)
            'Lugia': 20,       # Tanque de HP + Agotamiento de PP
            'Ho-Oh': 20,       # Tanque de HP + Agotamiento de PP
            'Kartana': 15      # Glass Cannon (Peligro de KO al capturador)
        }

        # 4. FILTRADO Y CÁLCULO DEL ÍNDICE
        # Seleccionamos solo las unidades que definimos para el Top 10
        df_top = df[df['nombre'].isin(mecanicas_reales.keys())].copy()

        def calcular_complejidad(row):
            # A) Inverso del Ratio (Dificultad Base)
            base_diff = 255 / row['Probabilidad_de_captura'] if row['Probabilidad_de_captura'] > 0 else 85
            
            # B) Factor HP (Presupuesto de Error/Turnos)
            hp_factor = row['Puntos_de_salud'] / 10
            
            # C) Penalizador por Comportamiento Externo
            penalty = mecanicas_reales.get(row['nombre'], 0)
            
            # D) Factor de Potencial (BST)
            power_factor = row['total_base'] / 100
            
            return base_diff + hp_factor + penalty + power_factor

        df_top['Indice_Dificultad'] = df_top.apply(calcular_complejidad, axis=1)

        # 5. ORDENAMIENTO DESCENDENTE
        df_top = df_top.sort_values(by='Indice_Dificultad', ascending=False)

        # 6. ESTÉTICA DE LA GRÁFICA (Estilo Reporte UPSRJ)
        plt.figure(figsize=(14, 8), facecolor='#0B0E11')
        ax = plt.gca()
        ax.set_facecolor('#13171C')

        # Usamos un degradado de rojos (Reds) para indicar Peligro/Dificultad
        colores = plt.cm.Reds(pd.Series(range(10, 0, -1)) / 10)

        barras = plt.bar(df_top['nombre'], df_top['Indice_Dificultad'], 
                         color=colores, edgecolor='white', linewidth=1.5)

        # Etiquetas de datos sobre las barras
        for bar in barras:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.1f}', 
                     color='white', ha='center', va='bottom', fontweight='bold')

        # Configuración de Títulos y Ejes
        plt.title('TOP 10 POKÉMON: ANÁLISIS DE COMPLEJIDAD DE CAPTURA', 
                  color='white', fontsize=16, fontweight='bold', pad=25)
        plt.xlabel('UNIDADES IDENTIFICADAS', color='white', fontweight='bold')
        plt.ylabel('ÍNDICE DE COMPLEJIDAD (BST + HP + MECÁNICA)', color='white', fontweight='bold')

        plt.xticks(rotation=30, color='white', fontweight='bold')
        plt.yticks(color='white')
        
        # Eliminar bordes para un look moderno
        for spine in ax.spines.values():
            spine.set_visible(False)
            
        plt.grid(axis='y', linestyle='--', alpha=0.1)
        plt.tight_layout()

        # Guardar y mostrar
        plt.savefig('grafica_top_10_dificultad.png', facecolor='#0B0E11')
        print("🚀 Reporte de Complejidad generado exitosamente.")
        plt.show()

    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo 'csv_pokemon_limpio.csv'.")
    except Exception as e:
        print(f"❌ Error crítico en el sistema: {e}")

if __name__ == "__main__":
    generar_reporte_complejidad_captura()