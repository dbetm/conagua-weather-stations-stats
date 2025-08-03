import pandas as pd
import matplotlib.pyplot as plt


def plot_max_temperatures(
    max_temp_df: pd.DataFrame, station_name: str, days_per_period: int, extra_x_markers: dict
):
    plt.figure(figsize=(12, 6))

    # Itera sobre cada columna (cada año) y grafica su serie
    for year in max_temp_df.columns:
        plt.plot(max_temp_df.index, max_temp_df[year], label=str(year))

    plt.xticks(ticks=range(0, len(max_temp_df), 10))

    # Añadir etiquetas de meses clave
    for marker, pos in extra_x_markers.items():
        plt.text(pos, plt.ylim()[0] - 1, marker, ha='center', va='top')

    # Opciones de la gráfica
    plt.title(f"Temperaturas máximas diarias en la estación {station_name} (por año)")
    plt.xlabel("Día (0-91)")
    plt.ylabel("Temperatura máxima (°C)")
    plt.legend(title="Año")
    plt.grid(True)
    plt.tight_layout()
    plt.show()