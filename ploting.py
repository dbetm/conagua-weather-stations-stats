from typing import Optional
import pandas as pd
import matplotlib.pyplot as plt

from contants import MONTH_TO_MONTH_NAME


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


def plot_accumulated_precipitation(
    aligned_data: pd.DataFrame,
    station_name: str,
    months: list,
    additional_legend: Optional[str] = None,
):
    aligned_data.plot(kind='bar', figsize=(10, 6))
    monthly_period = f"{MONTH_TO_MONTH_NAME[months[0]]} - {MONTH_TO_MONTH_NAME[months[-1]]}"

    plt.title(
        f'Lluvia acumulada por mes ({monthly_period}). Estación {station_name}'
    )
    plt.ylabel('Precipitación (mm)')
    plt.xlabel('Mes')
    plt.legend(title='Año')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    if additional_legend:
        plt.gcf().text(
            1.02, 0.5, additional_legend, fontsize=10, va='center', ha='left', transform=plt.gca().transAxes
        )

    plt.tight_layout()
    plt.show()