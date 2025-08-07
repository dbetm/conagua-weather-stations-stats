from typing import Optional
import pandas as pd
import matplotlib.pyplot as plt

from contants import MONTH_TO_MONTH_NAME


def plot_max_temperatures(
    max_temp_df: pd.DataFrame,
    station_name: str,
    days_per_period: int,
    extra_x_markers: dict,
    show: bool = True,
    title: Optional[str] = None,
    save_path: Optional[str] = None,
):
    plt.figure(figsize=(12, 6))

    # compute daily average max temperature
    daily_avg = max_temp_df.mean(axis=1)

    # Plot daily average of max temperature
    plt.plot(max_temp_df.index, daily_avg, label="Promedio", color="black")

    # Per year plot their serie
    for year in max_temp_df.columns:
        plt.plot(max_temp_df.index, max_temp_df[year], label=str(year))

    plt.xticks(ticks=range(0, len(max_temp_df), 10))

    # Add labels by month
    for marker, pos in extra_x_markers.items():
        plt.text(pos, plt.ylim()[0] - 1, marker, ha='center', va='top')
        #plt.text(pos, 13, marker, ha='center', va='top')

    # Setup plot
    if title:
        plt.title(f"{title} - Estación: {station_name}")
    else:
        plt.title(f"Temperaturas máximas diarias en la estación {station_name} (por año)")
    plt.xlabel(f"Día (1-{days_per_period})")
    plt.ylabel("Temperatura máxima (°C)")
    plt.legend(title="Año")
    plt.grid(True)

    #plt.ylim(bottom=15, top=45)
    #plt.yticks([15, 25, 30, 35, 40, 45])
    plt.tight_layout()

    if show:
        plt.show()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')


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