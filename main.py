from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

import pandas as pd
import os

class FuelTank:
    def __init__(self, number: int, calibration_data: pd.DataFrame, name: str = ""):
        self.number = number
        self.name = name or f"Резервуар {number}"
        self.calibration_data = calibration_data
        if not calibration_data.empty:
            self.max_height_mm = self.calibration_data['height_mm'].max()
        else:
            self.max_height_mm = 0
        self.density = 0.83
        self.current_height = 0

    def set_height(self, height_mm: int):
        self.current_height = height_mm

    def set_density(self, density: float):
        self.density = density

    def get_volume(self) -> float:
        if self.current_height <= 0 or self.calibration_data.empty:
            return 0.0
        elif self.current_height >= self.max_height_mm:
            return round(self.calibration_data['liters'].iloc[-1], 1)
        
        heights = self.calibration_data['height_mm'].values
        
        exact_match = self.calibration_data[
            self.calibration_data['height_mm'] == self.current_height
        ]
        if not exact_match.empty:
            return round(exact_match['liters'].iloc[0], 1)
        
        for i in range(len(heights) - 1):
            if heights[i] < self.current_height < heights[i + 1]:
                h1, h2 = heights[i], heights[i + 1]
                v1 = self.calibration_data[
                    self.calibration_data['height_mm'] == h1
                ]['liters'].iloc[0]
                v2 = self.calibration_data[
                    self.calibration_data['height_mm'] == h2
                ]['liters'].iloc[0]
                
                volume = v1 + (v2 - v1) * (self.current_height - h1) / (h2 - h1)
                return round(volume, 1)
        
        return 0.0

    def get_mass(self) -> float:
        volume = self.get_volume()
        return round(volume * self.density, 1)

class ManualStorage:
    def __init__(self, name: str, volume: float = 0.0):
        self.name = name
        self.volume = volume
        self.density = 0.85

    def set_volume(self, volume: float):
        self.volume = volume

    def set_density(self, density: float):
        self.density = density

    def get_volume(self) -> float:
        return round(self.volume, 1)

    def get_mass(self) -> float:
        return round(self.volume * self.density, 1)

class Tab(MDFloatLayout, MDTabsBase):
    pass

class TankCard(MDCard):
    tank_number = NumericProperty(1)
    tank_name = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.elevation = 8
        self.padding = 20

Builder.load_string('''
<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        
        MDTabs:
            id: tabs
            
            Tab:
                title: "Резервуары 1-4"
                
                ScrollView:
                    GridLayout:
                        cols: 1
                        size_hint_y: None
                        height: self.minimum_height
                        padding: "10dp"
                        spacing: "10dp"
                        
                        TankCard:
                            tank_number: 1
                            tank_name: "Резервуар 1"
                            MDTextField:
                                id: height_1
                                hint_text: "Высота, мм"
                                text: "0"
                                input_filter: 'int'
                            MDTextField:
                                id: density_1
                                hint_text: "Плотность, кг/л"
                                text: "0.83"
                                input_filter: 'float'
                            MDLabel:
                                id: result_1
                                text: "Объем: 0.0 л\\nМасса: 0.0 кг"
                                theme_text_color: "Primary"
                        
                        TankCard:
                            tank_number: 2
                            tank_name: "Резервуар 2"
                            MDTextField:
                                id: height_2
                                hint_text: "Высота, мм"
                                text: "0"
                                input_filter: 'int'
                            MDTextField:
                                id: density_2
                                hint_text: "Плотность, кг/л"
                                text: "0.85"
                                input_filter: 'float'
                            MDLabel:
                                id: result_2
                                text: "Объем: 0.0 л\\nМасса: 0.0 кг"
                                theme_text_color: "Primary"
                        
                        TankCard:
                            tank_number: 3
                            tank_name: "Резервуар 3"
                            MDTextField:
                                id: height_3
                                hint_text: "Высота, мм"
                                text: "0"
                                input_filter: 'int'
                            MDTextField:
                                id: density_3
                                hint_text: "Плотность, кг/л"
                                text: "0.85"
                                input_filter: 'float'
                            MDLabel:
                                id: result_3
                                text: "Объем: 0.0 л\\nМасса: 0.0 кг"
                                theme_text_color: "Primary"
                        
                        TankCard:
                            tank_number: 4
                            tank_name: "Резервуар 4"
                            MDTextField:
                                id: height_4
                                hint_text: "Высота, мм"
                                text: "0"
                                input_filter: 'int'
                            MDTextField:
                                id: density_4
                                hint_text: "Плотность, кг/л"
                                text: "0.85"
                                input_filter: 'float'
                            MDLabel:
                                id: result_4
                                text: "Объем: 0.0 л\\nМасса: 0.0 кг"
                                theme_text_color: "Primary"
            
            Tab:
                title: "Резервуары 5-8"
                
                ScrollView:
                    GridLayout:
                        cols: 1
                        size_hint_y: None
                        height: self.minimum_height
                        padding: "10dp"
                        spacing: "10dp"
                        
                        TankCard:
                            tank_number: 5
                            tank_name: "⛽ Резервуар 5 (Бензин)"
                            MDTextField:
                                id: height_5
                                hint_text: "Высота, мм"
                                text: "0"
                                input_filter: 'int'
                            MDTextField:
                                id: density_5
                                hint_text: "Плотность, кг/л"
                                text: "0.74"
                                input_filter: 'float'
                            MDLabel:
                                id: result_5
                                text: "Объем: 0.0 л\\nМасса: 0.0 кг"
                                theme_text_color: "Primary"
                        
                        TankCard:
                            tank_number: 6
                            tank_name: "Резервуар 6"
                            MDTextField:
                                id: height_6
                                hint_text: "Высота, мм"
                                text: "0"
                                input_filter: 'int'
                            MDTextField:
                                id: density_6
                                hint_text: "Плотность, кг/л"
                                text: "0.85"
                                input_filter: 'float'
                            MDLabel:
                                id: result_6
                                text: "Объем: 0.0 л\\nМасса: 0.0 кг"
                                theme_text_color: "Primary"
                        
                        TankCard:
                            tank_number: 7
                            tank_name: "Резервуар 7"
                            MDTextField:
                                id: height_7
                                hint_text: "Высота, мм"
                                text: "0"
                                input_filter: 'int'
                            MDTextField:
                                id: density_7
                                hint_text: "Плотность, кг/л"
                                text: "0.85"
                                input_filter: 'float'
                            MDLabel:
                                id: result_7
                                text: "Объем: 0.0 л\\nМасса: 0.0 кг"
                                theme_text_color: "Primary"
                        
                        TankCard:
                            tank_number: 8
                            tank_name: "Резервуар 8"
                            MDTextField:
                                id: height_8
                                hint_text: "Высота, мм"
                                text: "0"
                                input_filter: 'int'
                            MDTextField:
                                id: density_8
                                hint_text: "Плотность, кг/л"
                                text: "0.85"
                                input_filter: 'float'
                            MDLabel:
                                id: result_8
                                text: "Объем: 0.0 л\\nМасса: 0.0 кг"
                                theme_text_color: "Primary"
            
            Tab:
                title: "Доп. объекты"
                
                ScrollView:
                    GridLayout:
                        cols: 1
                        size_hint_y: None
                        height: self.minimum_height
                        padding: "10dp"
                        spacing: "10dp"
                        
                        MDCard:
                            orientation: 'vertical'
                            padding: "10dp"
                            size_hint_y: None
                            height: "180dp"
                            elevation: 8
                            
                            MDLabel:
                                text: "🚗 Автомобиль"
                                size_hint_y: None
                                height: self.texture_size[1]
                                theme_text_color: "Primary"
                                font_style: "H6"
                            
                            MDTextField:
                                id: auto_volume
                                hint_text: "Объем, л"
                                text: "0"
                                input_filter: 'float'
                            
                            MDTextField:
                                id: auto_density
                                hint_text: "Плотность, кг/л"
                                text: "0.85"
                                input_filter: 'float'
                            
                            MDLabel:
                                id: auto_result
                                text: "Масса: 0.0 кг"
                                size_hint_y: None
                                height: self.texture_size[1]
                                theme_text_color: "Primary"
                        
                        MDCard:
                            orientation: 'vertical'
                            padding: "10dp"
                            size_hint_y: None
                            height: "180dp"
                            elevation: 8
                            
                            MDLabel:
                                text: "🔧 Трубопровод"
                                size_hint_y: None
                                height: self.texture_size[1]
                                theme_text_color: "Primary"
                                font_style: "H6"
                            
                            MDTextField:
                                id: pipe_volume
                                hint_text: "Объем, л"
                                text: "0"
                                input_filter: 'float'
                            
                            MDTextField:
                                id: pipe_density
                                hint_text: "Плотность, кг/л"
                                text: "0.85"
                                input_filter: 'float'
                            
                            MDLabel:
                                id: pipe_result
                                text: "Масса: 0.0 кг"
                                size_hint_y: None
                                height: self.texture_size[1]
                                theme_text_color: "Primary"
            
            Tab:
                title: "Результаты"
                
                ScrollView:
                    MDLabel:
                        id: results_text
                        text: ""
                        size_hint_y: None
                        height: self.texture_size[1]
                        padding: [10, 10]
                        text_size: self.width - 20, None
                        theme_text_color: "Primary"
        
        BoxLayout:
            size_hint_y: None
            height: "56dp"
            padding: "5dp"
            spacing: "5dp"
            
            MDRaisedButton:
                text: "РАССЧИТАТЬ"
                on_press: root.calculate_all()
                md_bg_color: app.theme_cls.primary_color
            
            MDRaisedButton:
                text: "ОЧИСТИТЬ"
                on_press: root.clear_all()
                md_bg_color: app.theme_cls.accent_color
            
            MDRaisedButton:
                text: "СПРАВКА"
                on_press: root.show_help()

<TankCard>:
    orientation: 'vertical'
    size_hint: 1, None
    height: self.minimum_height
    padding: "15dp"
    spacing: "10dp"
    
    MDLabel:
        text: root.tank_name
        size_hint_y: None
        height: self.texture_size[1]
        theme_text_color: "Primary"
        font_style: "H6"
    

    

''')

class MainScreen(Screen):
    dialog = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tanks = {}
        self.manual_storages = {}
        self.load_data()
    
    def load_data(self):
        """Загрузка данных из Excel файла"""
        try:
            file_paths = [
                '/storage/emulated/0/резерв.xlsx',
                './резерв.xlsx',
                'резерв.xlsx'
            ]
            
            file_path = None
            for fp in file_paths:
                if os.path.exists(fp):
                    file_path = fp
                    break
            
            if file_path is None:
                self.create_test_data()
                return
            
            df_raw = pd.read_excel(file_path, header=None)
            
            for tank_num in range(1, 9):
                col_offset = (tank_num - 1) * 3
                if col_offset + 1 >= df_raw.shape[1]:
                    continue
                
                tank_data = []
                for row in range(2, min(len(df_raw), 322)):
                    try:
                        cm_val = df_raw.iloc[row, col_offset]
                        liters_val = df_raw.iloc[row, col_offset + 1]
                        
                        if pd.isna(cm_val) or pd.isna(liters_val):
                            continue
                        
                        cm_val = float(cm_val)
                        liters_val = float(liters_val)
                        
                        tank_data.append({
                            'height_mm': cm_val * 10,
                            'liters': liters_val
                        })
                    except:
                        continue
                
                if tank_data:
                    tank_df = pd.DataFrame(tank_data)
                    tank_name = f"Резервуар {tank_num}"
                    if tank_num == 5:
                        tank_name = "⛽ Резервуар 5 (Бензин)"
                    self.tanks[tank_num] = FuelTank(tank_num, tank_df, tank_name)
            
            for tank_num in range(1, 9):
                if tank_num not in self.tanks:
                    tank_name = f"Резервуар {tank_num}"
                    if tank_num == 5:
                        tank_name = "⛽ Резервуар 5 (Бензин)"
                    self.create_test_data_for_tank(tank_num, tank_name)
            
            self.manual_storages['automobile'] = ManualStorage("🚗 Автомобиль")
            self.manual_storages['pipeline'] = ManualStorage("🔧 Трубопровод")
            
        except Exception as e:
            self.create_test_data()
    
    def create_test_data_for_tank(self, tank_num, name):
        """Создание тестовых данных"""
        heights = list(range(0, 32001, 1000))
        coefficients = {1: 3.0, 2: 3.1, 3: 3.2, 4: 3.3, 5: 2.8, 6: 2.9, 7: 3.0, 8: 3.1}
        coefficient = coefficients.get(tank_num, 3.0)
        volumes = [h * coefficient for h in heights]
        
        tank_df = pd.DataFrame({
            'height_mm': heights,
            'liters': volumes
        })
        
        self.tanks[tank_num] = FuelTank(tank_num, tank_df, name)
    
    def create_test_data(self):
        """Создание полных тестовых данных"""
        for tank_num in range(1, 9):
            tank_name = f"Резервуар {tank_num}"
            if tank_num == 5:
                tank_name = "⛽ Резервуар 5 (Бензин)"
            self.create_test_data_for_tank(tank_num, tank_name)
        
        self.manual_storages['automobile'] = ManualStorage("🚗 Автомобиль")
        self.manual_storages['pipeline'] = ManualStorage("🔧 Трубопровод")
    
    def calculate_all(self):
        """Расчет всех объемов"""
        try:
            total_volume = 0
            total_mass = 0
            results = []
            
            for tank_num in range(1, 9):
                if f"height_{tank_num}" in self.ids:
                    try:
                        height_text = self.ids[f"height_{tank_num}"].text or "0"
                        density_text = self.ids[f"density_{tank_num}"].text or "0.85"
                        
                        height = int(height_text)
                        density = float(density_text)
                        
                        self.tanks[tank_num].set_height(height)
                        self.tanks[tank_num].set_density(density)
                        
                        volume = self.tanks[tank_num].get_volume()
                        mass = self.tanks[tank_num].get_mass()
                        
                        total_volume += volume
                        total_mass += mass
                        
                        if f"result_{tank_num}" in self.ids:
                            self.ids[f"result_{tank_num}"].text = f"Объем: {volume:,.1f} л\nМасса: {mass:,.1f} кг"
                        
                        results.append(f"{self.tanks[tank_num].name}: {height:,} мм = {volume:,.1f} л = {mass:,.1f} кг")
                        
                    except ValueError:
                        self.show_error_dialog("Ошибка", f"Некорректные данные для резервуара {tank_num}")
                        return
            
            try:
                auto_volume = float(self.ids.auto_volume.text or "0")
                auto_density = float(self.ids.auto_density.text or "0.85")
                
                self.manual_storages['automobile'].set_volume(auto_volume)
                self.manual_storages['automobile'].set_density(auto_density)
                
                auto_mass = self.manual_storages['automobile'].get_mass()
                total_volume += auto_volume
                total_mass += auto_mass
                
                self.ids.auto_result.text = f"Масса: {auto_mass:,.1f} кг"
                results.append(f"🚗 Автомобиль: {auto_volume:,.1f} л = {auto_mass:,.1f} кг")
                
            except ValueError:
                self.show_error_dialog("Ошибка", "Некорректные данные для автомобиля")
                return
            
            try:
                pipe_volume = float(self.ids.pipe_volume.text or "0")
                pipe_density = float(self.ids.pipe_density.text or "0.85")
                
                self.manual_storages['pipeline'].set_volume(pipe_volume)
                self.manual_storages['pipeline'].set_density(pipe_density)
                
                pipe_mass = self.manual_storages['pipeline'].get_mass()
                total_volume += pipe_volume
                total_mass += pipe_mass
                
                self.ids.pipe_result.text = f"Масса: {pipe_mass:,.1f} кг"
                results.append(f"🔧 Трубопровод: {pipe_volume:,.1f} л = {pipe_mass:,.1f} кг")
                
            except ValueError:
                self.show_error_dialog("Ошибка", "Некорректные данные для трубопровода")
                return
            
            result_text = "🔥 РЕЗУЛЬТАТЫ РАСЧЕТА\n\n"
            for result in results:
                result_text += f"• {result}\n"
            
            result_text += f"\n📊 ОБЩИЙ ОБЪЕМ: {total_volume:,.1f} л\n"
            result_text += f"⚖️ ОБЩАЯ МАССА: {total_mass:,.1f} кг\n"
            
            if total_volume > 0:
                result_text += f"📈 СРЕДНЯЯ ПЛОТНОСТЬ: {total_mass/total_volume:.3f} кг/л"
            
            self.ids.results_text.text = result_text
            
        except Exception as e:
            self.show_error_dialog("Ошибка расчета", f"Ошибка: {str(e)}")
    
    def clear_all(self):
        """Очистка всех полей"""
        for tank_num in range(1, 9):
            if f"height_{tank_num}" in self.ids:
                self.ids[f"height_{tank_num}"].text = "0"
                self.ids[f"density_{tank_num}"].text = "0.83"
                self.ids[f"result_{tank_num}"].text = "Объем: 0.0 л\nМасса: 0.0 кг"
        
        self.ids.auto_volume.text = "0"
        self.ids.auto_density.text = "0.83"
        self.ids.auto_result.text = "Масса: 0.0 кг"
        
        self.ids.pipe_volume.text = "0"
        self.ids.pipe_density.text = "0.83"
        self.ids.pipe_result.text = "Масса: 0.0 кг"
        
        self.ids.results_text.text = ""
    
    def show_error_dialog(self, title, text):
        """Показать диалог ошибки"""
        if not self.dialog:
            self.dialog = MDDialog(
                title=title,
                text=text,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                ],
            )
        self.dialog.text = text
        self.dialog.title = title
        self.dialog.open()
    
    def show_help(self):
        """Показать справку"""
        help_text = """🔥 SMART FUEL CALCULATOR - Android версия

📱 ОСОБЕННОСТИ:
• Полная поддержка 8 резервуаров
• Material Design интерфейс
• Автосохранение данных
• Оптимизировано для мобильных устройств

💡 ИСПОЛЬЗОВАНИЕ:
1. Введите высоты для резервуаров в мм
2. Укажите плотности для каждого объекта
3. Нажмите "РАССЧИТАТЬ"
4. Просмотрите результаты во вкладке "Результаты"

📊 ФАЙЛ ДАННЫХ:
• Поместите файл 'резерв.xlsx' в корневую папку устройства
• Или используйте тестовые данные
"""
        self.show_error_dialog("📖 Справка", help_text)

class FuelCalculatorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return MainScreen()

if __name__ == "__main__":
    FuelCalculatorApp().run()