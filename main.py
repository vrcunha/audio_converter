import os
from pathlib import Path, PosixPath
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.properties import StringProperty

from kivymd.uix.list import OneLineIconListItem
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.menu import MDDropdownMenu


Window.size = (700, 300)

class IconListItem(OneLineIconListItem):
    icon = StringProperty()

class Media_Converter(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.screen = Builder.load_file('./media_converter.kv')
        self.path = str(Path(os.path.abspath(__file__)).home())
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path
        )
        menu_items = [
            {
                "viewclass": "IconListItem",
                "text": f"{i}",
                "height": dp(56),
                "on_release": lambda x=f"{i}": self.set_item(x),
            } for i in ['.mp3', '.wav', '.m4a', '.ogg', '.aac']
        ]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.drop_item,
            items=menu_items,
            position="top",
            width_mult=3,
        )
        self.menu.bind()

    def set_item(self, text_item):
        self.screen.ids.drop_item.set_item(text_item)
        self.suffix = text_item
        try:
            self.screen.ids.text_field_out.text = f'{self.input_file.stem}{text_item}'
        except AttributeError:
            pass
        self.menu.dismiss()
    
    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.accent_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        return self.screen

    def file_manager_open(self):
        self.file_manager.show(self.path)
        self.manager_open = True

    def select_path(self, path):
        self.exit_manager()
        self.input_file = Path(path)
        self.screen.ids.text_field_in.text = self.input_file.name
        try:
            self.screen.ids.text_field_out.text = f'{self.input_file.stem}{self.suffix}'
        except AttributeError:
            pass
    
    def mono_to_stereo(self):
        return '-filter_complex "[0:a][0:a]amerge=inputs=2[a]" -map "[a]"'
    
    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in [27, 8]:
            if self.manager_open:
                self.file_manager.close()
            return True

    def set_output_folder(self):
        output_path = Path(os.path.join(self.input_file.parent, 'output'))
        if not output_path.exists():
            os.mkdir(output_path)
        fname = self.screen.ids.text_field_out.text
        return f'{output_path}/{fname}'

    def convert(self):
        if isinstance(self.input_file, PosixPath):
            finput = self.input_file
            foutput = self.set_output_folder()
            comando = f'ffmpeg -i {finput} {foutput}'
            os.system(comando)
            toast(f'Process Finished.')


Media_Converter().run()
