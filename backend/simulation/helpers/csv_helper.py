import os
import pandas as pd
from datetime import datetime

from ..agents import Transfer


class CsvLogger:

    # Ścieka do folderu z logami (ścieka względna do folderu backend obejmującego plik app.py)
    output_logs_dir_path = 'simulation/output_logs/'

    # Lista zawierająca obiekt DataFrame przyporządkowany kazdemu sektorowi, który reprezentuje las
    forest_sectors_dataframes = []

    # Nazwy kolumn dla tworzonych DataFrame'ów sektorów
    df_template_columns = [
        'air_humidity',
        'co2',
        'ffdi',
        'litter_moisture',
        'on_fire',
        'pm25',
        'sector_state',
        'temperature',
        'wind_directory',
        'wind_speed',
    ]

    # Konstruktor wywoływany w main.py w set_init_data() w momencie tworzenia obiektu typu CsvLogger
    def __init__(self, transfer: Transfer):
        self.transfer = transfer
        self.is_logging = False

    def init_logging_process(self):
        # Zainicjownanie obiektów DataFrame dla kazdego sektora lasu z jego stanem początkowym
        self.create_log_directory()
        sectors_data = self.transfer.get_sectors_data()
        for key in sectors_data:
            df_data = {}
            for column in self.df_template_columns:
                df_data[column] = '{}'.format(sectors_data[key][column])
            df_for_sector = pd.DataFrame(df_data, index=[0])
            self.forest_sectors_dataframes.append((key, df_for_sector))

    def create_log_directory(self):
        # Tworzę folder, w którym umieszczane będą foldery z logami dla kazdego sektora
        if not os.path.exists(self.output_logs_dir_path):
            os.makedirs(self.output_logs_dir_path)

        # Utworzenie folderu dla danej symulacji
        self.current_simulation_dir_name = datetime.now().strftime("%d-%b-%YT(%H:%M:%S)")
        current_simulation_logs_dir_path = self.output_logs_dir_path + self.current_simulation_dir_name
        if not os.path.exists(current_simulation_logs_dir_path):
            os.makedirs(current_simulation_logs_dir_path)

    def start(self):
        self.is_logging = True

    def stop(self):
        self.is_logging = False

    # Funkcja wywoływana w kazdej iteracji symulacji w main.py w ...  
    def log_current_forest_area_state(self):
        while self.is_logging:
            sectors_data = self.transfer.sectors_data
            # Dopisanie chwilowego stanu danego sektora do odpowiadającego mu obiektu DataFrame
            for key in sectors_data:
                df_data = {}
                for column in self.df_template_columns:
                    df_data[column] = sectors_data[key][column]
                new_row = pd.Series(df_data)

                df_tmp = self.forest_sectors_dataframes[key][1]
                df_tmp = df_tmp.append(new_row, ignore_index=True)
                self.forest_sectors_dataframes[key] = (key, df_tmp)

    # Funkcja wywoływana podczas zakończenia symulacji - po przyciśnięciu Reset
    def save_logs(self):
        for item in self.forest_sectors_dataframes:
            idx = item[0]
            df = item[1]
            df.to_csv(self.output_logs_dir_path + self.current_simulation_dir_name + "/sector_" + str(idx) + ".csv", index=False)
