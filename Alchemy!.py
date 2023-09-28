from tkinter import *
from tkinter import ttk
from random import randint
from PIL import Image, ImageTk
import ctypes as ct # для изменения цвета полоски от файлого менеджера у окна

import sqlite3 as sql3
# Cursor
cursor = sql3.connect('settings.db')
# Функции для SQLite запросов
def execute(command, *args):
    'Function for comfort'
    with cursor:
        return cursor.execute(command, args)

def change(table='Settings', parameter='using_language', set_obj='ru', where_obj=None, where_value=None):
    '''Change something in table
    arguments:
    table-table to change
    parameter-which setting should be changed
    set_obj-what to change
    where_obj-filter_parameter
    where_value-filter_value'''
    command_change=f'''
    UPDATE {table}
    SET {parameter} = '{set_obj}'
    '''
    if where_obj!=None and where_value!=None:
        command_change=f'''
        UPDATE {table}
        SET {parameter} = '{set_obj}'
        WHERE {where_obj} = '{where_value}';
        '''
    else:
        command_change=f'''
        UPDATE {table}
        SET {parameter} = '{set_obj}'
        '''
     
    execute(command_change)

def get(table, where_obj=None, where_value=None, tag='*'):
    '''Get informations from the table
    arguments:
    table-table to get
    where_obj-filter_parameter
    where_value-filter_value
    result requires one of functions convert_[data_type]
    '''
    cursor.row_factory = sql3.Row
    conn = cursor.cursor()
    if where_obj!=None and where_value!=None:
        command_get=f'''
        SELECT {tag}
        FROM {table}
        WHERE {where_obj} = '{where_value}';
        '''
    else:
        command_get=f'''
        SELECT {tag}
        FROM {table};
        '''      
    return conn.execute(command_get)

def convert_dict(obj_to_convert):
    'Convertation get result to dict'
    return [dict(row) for row in obj_to_convert.fetchall()]

def convert_str(obj_to_convert):
    'Convertation get result to str'
    to_return = [list(row) for row in obj_to_convert.fetchall()]
    return to_return[0][0]

def convert_list(obj_to_convert):
    'Convertation get result to list'
    return [list[0] for list in [list(row) for row in obj_to_convert.fetchall()]]
# импорт не сохраняющихся в базе данных переменных
import variables
from variables import width, height, take, screen_width, screen_height, canvas, options_width, options_height, path_menu
from variables import mini, escape_press, last_tag_of_overlap, coords_xy, path, element_counter, all_elements

window = Tk()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_geometry = str(width) + 'x' + str(height) + '+' + str(int(screen_width//2)-int((width//2))) + '+' + str(int(screen_height//2)-int((height//2)))
window.geometry(window_geometry)

window.configure(bg='#A0FFFE')
window.title(convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='title')))
# иконки
icon_to_exit = ImageTk.PhotoImage(Image.open(path+'icon.png').resize((30, 30)))
icon = ImageTk.PhotoImage(Image.open(path+'icon.png'))
window.iconphoto(False, icon)

canvas = Canvas(window, width=screen_width+10, height=screen_height, bg='#cdf2ff') # +10, потому что один пискель получался без canvas
# узнаю кол-во элементов
import classes
import inspect
current_module = inspect.getmembers(classes, inspect.isclass)
all_elements = len(current_module) # Один класс оказался Photoimage

from classes import *


# Вспомогательная функция для отсутствия лагов при изменении окна
def resizing():
    global resize
    try:
        window.after_cancel(resize)
        variables.resize = False
    except: pass
    if variables.resize == False:
        variables.resize = True
        resize = window.after(50, lambda: resize_images())

def resize_images():
    variables.resize = False
    global width, height, photo_options_frame, photo_options_button, photo_options_buttonv2, options_width, options_height, photo_options_button_press
    global photo_options_button_pressv2, photo_settings_frame, coords_xy, mini
    # Переменные
    width = window.winfo_width()
    height = window.winfo_height()
    mini = min(height, width)
    options_width = mini//2-mini//19
    options_height = mini//2-mini//9
    # Рамочки
    photo_options_frame = ImageTk.PhotoImage(copy_image_options_frame.resize((mini, mini)))
    photo_settings_frame = ImageTk.PhotoImage(copy_image_settings_frame.resize((mini, mini)))
    # Кнопочки
    photo_options_button = ImageTk.PhotoImage(copy_image_options_button.resize((int(mini//2.3), mini//8)))
    photo_options_buttonv2 = ImageTk.PhotoImage(copy_image_options_buttonv2.resize((int(mini//2.5), mini//8)))
    # Нажатые кнопочки
    photo_options_button_press = ImageTk.PhotoImage(copy_image_options_button_press.resize((int(mini//2.3), mini//8)))
    photo_options_button_pressv2 = ImageTk.PhotoImage(copy_image_options_button_pressv2.resize((int(mini//2.5), mini//8)))
    # Изменение холстов
    canvas.itemconfigure('menu', image=photo_options_frame)
    canvas.itemconfigure('options_canvas', width=options_width, height=options_height)
    canvas.itemconfigure('settings_canvas', width=mini, height=mini)
    # Изменение изображений
    settings_buttons_canvas.itemconfigure('frame', image=photo_settings_frame)
    options_buttons_canvas.itemconfigure('buttonsv1', image=photo_options_button)
    settings_buttons_canvas.itemconfigure('buttonsv1', image=photo_options_button)
    settings_buttons_canvas.itemconfigure('buttonsv2', image=photo_options_buttonv2)
    options_buttons_canvas.itemconfigure('pressv1', image=photo_options_button_press)
    settings_buttons_canvas.itemconfigure('pressv2', image=photo_options_button_pressv2)
    # Изменение шрифтов
    options_buttons_canvas.itemconfigure('options_text', font=('Comic Sans MS', mini//26))
    settings_buttons_canvas.itemconfigure('options_text', font=('Comic Sans MS', mini//26))
    settings_buttons_canvas.itemconfigure('options_small_text', font=('Comic Sans MS', mini//30))
    # Изменение координат
    coords_xy = [int(mini//2.3)//2, mini//16]
    coords_options()

def coords_options():
    canvas.coords('menu', width//1.975, height//1.975)
    canvas.coords('options_canvas', width//1.975, height//1.975)
    canvas.coords('settings_canvas', width//1.975, height//1.975)
    canvas.coords('element_counter_text', width, 0)
    options_buttons_canvas.coords('continue_button', options_width//2, options_height//6)
    options_buttons_canvas.coords('settings_button', options_width//2, options_height//2)
    options_buttons_canvas.coords('exit_button', options_width//2, options_height//1.2)
    settings_buttons_canvas.coords('language_button', mini//3.375, mini//6)
    settings_buttons_canvas.coords('signature_button', mini//1.425, mini//6)
    settings_buttons_canvas.coords('winframe_button', mini//1.425, mini//3.35)
    settings_buttons_canvas.coords('saves_button', mini//3.375, mini//3.35)
    settings_buttons_canvas.coords('take_button', mini//1.425, mini//2.325)
    settings_buttons_canvas.coords('take_text', mini//3.375, mini//2.325)
    settings_buttons_canvas.coords('double_button', mini//1.425, mini//1.775)
    settings_buttons_canvas.coords('double_text', mini//3.375, mini//1.775)
    settings_buttons_canvas.coords('settings_open_button', mini//1.425, mini//1.435)
    settings_buttons_canvas.coords('settings_open_text', mini//3.375, mini//1.435)
    settings_buttons_canvas.coords('done_button', mini//2, mini//1.2)
    settings_buttons_canvas.coords('frame', mini//2, mini//2)

    global coords_buttons
    coords_buttons = [
    {'continue_button': [options_width//2+width//2-options_width//2, options_height//6+int(height//1.975)-options_height//2]},
    {'exit_button': [options_width//2+width//2-options_width//2, int(options_height//1.2)+int(height//1.975)-options_height//2]},
    {'settings_button': [options_width//2+width//2-options_width//2, options_height//2+int(height//1.975)-options_height//2]},
    {'language_button': [mini//3.375+width//2-mini//2, mini//6.05+height//2-mini//2]},
    {'signature_button': [int(mini//1.425)+width//2-mini//2, mini//6.05+height//2-mini//2]},
    {'winframe_button': [int(mini//1.425)+width//2-mini//2, mini//3.35+height//2-mini//2]},
    {'saves_button': [int(mini//3.375)+width//2-mini//2, mini//3.35+height//2-mini//2]},
    {'take_button': [int(mini//1.425)+width//2-mini//2, mini//2.325+height//2-mini//2]},
    {'double_button': [int(mini//1.425)+width//2-mini//2, mini//1.775+height//2-mini//2]},
    {'settings_open_button': [int(mini//1.425)+width//2-mini//2, mini//1.435+height//2-mini//2]},
    {'done_button': [mini//2+width//2-mini//2, mini//1.2+height//2-mini//2]}
    ]

def init_options_buttons_canvas():
    global image_options_frame, copy_image_options_frame, photo_options_frame, image_options_button, copy_image_options_button, photo_options_button
    global copy_image_options_buttonv2, photo_options_buttonv2, options_buttons_canvas
    global image_options_button_press, copy_image_options_button_press, photo_options_button_press, coords_xy
    global copy_image_options_button_pressv2, photo_options_button_pressv2, options_buttons_canvas, coords_buttons
    global settings_buttons_canvas, copy_image_settings_frame, photo_settings_frame
    # кнопочка открывающая меню
    photo_menu_button = ImageTk.PhotoImage(image=Image.open(path_menu+'menu_button.png'))
    photo_menu_button_press = ImageTk.PhotoImage(image=Image.open(path_menu+'menu_button_press.png'))
    canvas.create_image(0, 0, anchor='nw', image=photo_menu_button, tags=['menu_button', 'sett_button'])
    canvas.tag_bind('menu_button', '<Button-1>', lambda event: esc_press())
    canvas.tag_bind('menu_button', '<Enter>', lambda event: canvas.itemconfigure('menu_button', image=photo_menu_button_press))
    canvas.tag_bind('menu_button', '<Leave>', lambda event: canvas.itemconfigure('menu_button', image=photo_menu_button))
    # картинка рамки меню
    image_options_frame = Image.open(path_menu+'options_frame.png')
    copy_image_options_frame = image_options_frame.copy()
    photo_options_frame = ImageTk.PhotoImage(image_options_frame.resize((mini, mini)))
    # картинка рамки настроек
    image_settings_frame = Image.open(path_menu+'set_frame.png')
    copy_image_settings_frame = image_settings_frame.copy()
    photo_settings_frame = ImageTk.PhotoImage(image_settings_frame.resize((mini, mini)))
    # картинки кнопочек
    image_options_button = Image.open(path_menu+'button.png')
    image_options_button_press = Image.open(path_menu+'button_press.png')
    copy_image_options_button = copy_image_options_buttonv2 = image_options_button.copy()
    copy_image_options_button_press = copy_image_options_button_pressv2 = image_options_button_press.copy()
    photo_options_button = ImageTk.PhotoImage(image_options_button.resize((int(mini//2.3), mini//8)))
    photo_options_buttonv2 = ImageTk.PhotoImage(image_options_button.resize((int(mini//2.5), mini//8)))
    photo_options_button_press = ImageTk.PhotoImage(image_options_button_press.resize((int(mini//2.3), mini//8)))
    photo_options_button_pressv2 = ImageTk.PhotoImage(image_options_button_press.resize((int(mini//2.5), mini//8)))
    # холсты
    options_buttons_canvas = Canvas(bg='#A0FFFE', highlightbackground='#A0FFFE', width=options_width, height=options_height)
    settings_buttons_canvas = Canvas(bg='#A0FFFE', width=mini, height=mini, borderwidth=0)
    # создание кнопочек меню
    options_buttons_canvas.create_image(options_width//2, options_height//6, anchor=CENTER, image=photo_options_button, tags=['buttonsv1', 'continue_button', 'continue'])
    options_buttons_canvas.create_image(options_width//2, options_height//2, anchor=CENTER, image=photo_options_button, tags=['buttonsv1', 'settings_button', 'settings'])
    options_buttons_canvas.create_image(options_width//2, options_height//1.2, anchor=CENTER, image=photo_options_button, tags=['buttonsv1', 'exit_button', 'exit'])
    # создание текста на кнопочках меню 
    options_buttons_canvas.create_text(options_width//2, options_height//6, text=convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='continue_text')), font=('Comic Sans MS', mini//26), tags=['continue_text', 'options_text', 'continue', 'texts'])
    options_buttons_canvas.create_text(options_width//2, options_height//2, text=convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='settings_text')), font=('Comic Sans MS', mini//26), tags=['settings_text', 'options_text', 'settings', 'texts'])
    options_buttons_canvas.create_text(options_width//2, options_height//1.2, text=convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='exit_text')), font=('Comic Sans MS', mini//26), tags=['exit_text', 'options_text', 'exit', 'texts'])
    # создание рамки настроек
    settings_buttons_canvas.create_image(mini//2, mini//2, anchor=CENTER, image=photo_settings_frame, tags=['frame'])
    # создание кнопочек настроек
    settings_buttons_canvas.create_image(mini//3.375, mini//6, anchor=CENTER, image=photo_options_buttonv2, tags=['buttonsv2', 'setting', 'language_button', 'language'])
    settings_buttons_canvas.create_image(mini//1.425, mini//6, anchor=CENTER, image=photo_options_buttonv2, tags=['buttonsv2', 'signature_button', 'signature'])
    settings_buttons_canvas.create_image(mini//1.425, mini//3.35, anchor=CENTER, image=photo_options_buttonv2, tags=['buttonsv2', 'winframe_button', 'winframe'])
    settings_buttons_canvas.create_image(mini//3.375, mini//3.35, anchor=CENTER, image=photo_options_buttonv2, tags=['buttonsv2', 'saves_button', 'saves']) # mini//1.425, mini//2.325
    settings_buttons_canvas.create_image(mini//1.425, mini//2.325, anchor=CENTER, image=photo_options_buttonv2, tags=['buttonsv2', 'take_button', 'take'])
    settings_buttons_canvas.create_image(mini//1.425, mini//1.775, anchor=CENTER, image=photo_options_buttonv2, tags=['buttonsv2', 'double_button', 'double'])
    settings_buttons_canvas.create_image(mini//1.425, mini//1.435, anchor=CENTER, image=photo_options_buttonv2, tags=['buttonsv2', 'settings_open_button', 'settings_open'])
    settings_buttons_canvas.create_image(mini//2, mini//1.2, anchor=CENTER, image=photo_options_buttonv2, tags=['buttonsv2', 'done_button', 'done'])
    # создание текста на кнопочках настроек 
    settings_buttons_canvas.create_text(mini//3.375, mini//6.5, text=convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='language_text')), font=('Comic Sans MS', mini//26), tags=['language_text', 'setting',  'options_text', 'language', 'texts'])
    settings_buttons_canvas.create_text(mini//1.425, mini//6.5, text=convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='signature_text')), font=('Comic Sans MS', mini//26), tags=[ 'signature_text', 'options_text', 'signature', 'texts'])
    settings_buttons_canvas.create_text(mini//1.425, mini//3.5, text=convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='winframe_text')), font=('Comic Sans MS', mini//26), tags=[ 'winframe_text', 'options_text', 'winframe', 'texts'])
    settings_buttons_canvas.create_text(mini//3.375, mini//3.5, text=convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='saves_text')), font=('Comic Sans MS', mini//26), tags=[ 'saves_text', 'options_text', 'saves', 'texts'])
    settings_buttons_canvas.create_text(mini//3.375, mini//2.325, text=convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='take_text')), font=('Comic Sans MS', mini//26), tags=[ 'take_text', 'options_text', 'texts'])
    settings_buttons_canvas.create_text(mini//2, mini//1.21, text=convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='done_text')), font=('Comic Sans MS', mini//26), tags=[ 'done_text', 'options_text','done', 'texts'])
    # текст рядом с кнопками управления
    text_take=convert_str(get('Settings', tag='take_button'))
    text_take ='<'+ text_take+'>' if '<' not in text_take or '>' not in text_take else text_take
    settings_buttons_canvas.create_text(mini//1.425, mini//2.4, text=text_take.replace('Button', 'Mouse'), font=('Comic Sans MS', mini//30), fill='black', tags=[ 'take_button_text', 'options_small_text', 'take', 'b0'])
    settings_buttons_canvas.create_text(mini//3.375, mini//1.775, text=convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='double_text')), font=('Comic Sans MS', mini//26), tags=[ 'double_text', 'options_text', 'texts'])
    text_double=convert_str(get('Settings', tag='double_button'))
    text_double ='<'+ text_double+'>' if '<' not in text_double or '>' not in text_double else text_double
    settings_buttons_canvas.create_text(mini//1.425, mini//1.8, text=text_double.replace('Button', 'Mouse'), font=('Comic Sans MS', mini//30), fill='black', tags=[ 'double_button_text', 'options_small_text', 'double', 'b1'])
    settings_buttons_canvas.create_text(mini//3.375, mini//1.435, text=convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='settings_open_text')), font=('Comic Sans MS', mini//26), tags=['settings_open_text', 'options_text', 'texts'])
    text_settings_open=convert_str(get('Settings', tag='settings_open_button'))
    text_settings_open ='<'+ text_settings_open+'>' if '<' not in text_settings_open or '>' not in text_settings_open else text_settings_open
    settings_buttons_canvas.create_text(mini//1.425, mini//1.465, text=text_settings_open.replace('Button', 'Mouse'), font=('Comic Sans MS', mini//30), fill='black', tags=[ 'settings_open_button_text', 'options_small_text', 'settings_open', 'b2'])
    # создание всех меню на основном холсте
    canvas.create_image(width//1.975, height//1.975, anchor=CENTER, image=photo_options_frame, tags=['options', 'menu'], state='hidden')
    canvas.create_window(width//1.975, height//1.975, window=options_buttons_canvas, tags=['options', 'options_canvas'], state='hidden')
    canvas.create_window(width//1.975, height//1.975, anchor=CENTER, window=settings_buttons_canvas, tags=['settings', 'settings_canvas'], state='hidden')
    coords_xy = [int(mini//2.3)//2, mini//16]

    options_buttons_canvas.tag_bind('continue', '<Button-1>', lambda event: esc_press())
    options_buttons_canvas.tag_bind('settings', '<Button-1>', lambda event: open_settings())
    settings_buttons_canvas.tag_bind('language', '<Button-1>', lambda event: languages())
    settings_buttons_canvas.tag_bind('signature', '<Button-1>', lambda event: signature_visibility())
    settings_buttons_canvas.tag_bind('winframe', '<Button-1>', lambda event: winstyles())
    settings_buttons_canvas.tag_bind('saves', '<Button-1>', lambda event: window_ok_cancel('saves'))
    settings_buttons_canvas.tag_bind('done', '<Button-1>', lambda event: esc_press())
    settings_buttons_canvas.tag_bind('take', '<Button-1>', lambda event: bindings('take'))
    settings_buttons_canvas.tag_bind('double', '<Button-1>', lambda event: bindings('double'))
    settings_buttons_canvas.tag_bind('settings_open', '<Button-1>', lambda event: bindings('settings_open'))
    options_buttons_canvas.tag_bind('exit', '<Button-1>', lambda event: window_ok_cancel('exit'))
# Очень мудрёный код, который сложно дорабатывать в трёх следующих функциях
def buttons_esc():
    cursors_x = window.winfo_pointerx() - window.winfo_rootx()
    cursors_y = window.winfo_pointery() - window.winfo_rooty()
    global last_tag_of_overlap, escape_press
    coord_x = coords_xy[0]
    coord_y = coords_xy[1]
    tag_of_overlap = find_overlap_buttons(cursors_x, coord_x, cursors_y, coord_y)
    if tag_of_overlap == None:
        button_unpress()
    else:
        button_press(tag_of_overlap)

    if last_tag_of_overlap != tag_of_overlap: # Обработка предыдущего нажатого
        button_unpress(last_tag_of_overlap)
    last_tag_of_overlap = tag_of_overlap

    if escape_press:
        window.after(34, lambda: buttons_esc())

def button_press(tag): # Нажать на кнопку
    if len(options_buttons_canvas.find_withtag('pressv1'))==0:
        options_buttons_canvas.addtag_withtag('pressv1', tag)
        image = photo_options_button_press

        options_buttons_canvas.itemconfigure(tag, image=image)
        if tag == 'continue_button': options_buttons_canvas.coords('continue_text', options_width//2, int(options_height//5))
        if tag == 'settings_button': options_buttons_canvas.coords('settings_text', options_width//2, options_height//1.85)
        if tag == 'exit_button': options_buttons_canvas.coords('exit_text', options_width//2, int(options_height//1.2))
    if len(settings_buttons_canvas.find_withtag('pressv2'))==0:
        settings_buttons_canvas.addtag_withtag('pressv2', tag)
        image = photo_options_button_pressv2
        settings_buttons_canvas.itemconfigure(tag, image=image)

        if tag == 'language_button': settings_buttons_canvas.coords('language_text', int(mini//3.375), int(mini//5.985))
        if tag == 'signature_button': settings_buttons_canvas.coords('signature_text', int(mini//1.425), int(mini//5.85))
        if tag == 'winframe_button': settings_buttons_canvas.coords('winframe_text', int(mini//1.425), int(mini//3.325))
        if tag == 'saves_button': settings_buttons_canvas.coords('saves_text', int(mini//3.375), int(mini//3.325))
        if tag == 'take_button': settings_buttons_canvas.coords('take_button_text', int(mini//1.425), int(mini//2.3))
        if tag == 'double_button': settings_buttons_canvas.coords('double_button_text', int(mini//1.425), int(mini//1.75))
        if tag == 'settings_open_button': settings_buttons_canvas.coords('settings_open_button_text', int(mini//1.425), int(mini//1.4305))
        if tag == 'done_button': settings_buttons_canvas.coords('done_text', mini//2, int(mini//1.185))

def button_unpress(last_tag=None): # Отпустить кнопку
    # Картинки
    if len(options_buttons_canvas.find_withtag('pressv1'))!=0:
        options_buttons_canvas.dtag('pressv1', 'pressv1')
        options_buttons_canvas.itemconfigure('buttonsv1', image=photo_options_button)
    if len(settings_buttons_canvas.find_withtag('pressv2'))!=0:
        settings_buttons_canvas.dtag('pressv2', 'pressv2')
        settings_buttons_canvas.itemconfigure('buttonsv2', image=photo_options_buttonv2)

    if last_tag != None:
        options_buttons_canvas.dtag(last_tag, 'pressv1')
        settings_buttons_canvas.dtag(last_tag, 'pressv2')
        options_buttons_canvas.itemconfigure('buttonsv1', image=photo_options_button)
        options_buttons_canvas.itemconfigure('buttonsv2', image=photo_options_buttonv2)

        settings_buttons_canvas.itemconfigure('buttonsv1', image=photo_options_button)
        settings_buttons_canvas.itemconfigure('buttonsv2', image=photo_options_buttonv2)
    # Подъём текста
    options_buttons_canvas.coords('continue_text', options_width//2, int(options_height//6.05))
    options_buttons_canvas.coords('settings_text', options_width//2, int(options_height//2.05))
    options_buttons_canvas.coords('exit_text', options_width//2, int(options_height//1.25))
    settings_buttons_canvas.coords('language_text', int(mini//3.375), int(mini//6.5))
    settings_buttons_canvas.coords('signature_text', mini//1.425, int(mini//6.5))
    settings_buttons_canvas.coords('winframe_text', mini//1.425, int(mini//3.5))
    settings_buttons_canvas.coords('saves_text', mini//3.375, int(mini//3.5))
    settings_buttons_canvas.coords('take_button_text', mini//1.425, int(mini//2.4))
    settings_buttons_canvas.coords('double_button_text', mini//1.425, int(mini//1.8))
    settings_buttons_canvas.coords('settings_open_button_text', mini//1.425, int(mini//1.465))
    settings_buttons_canvas.coords('done_text', mini//2, int(mini//1.21))

def esc_press():
    global escape_press, last_tag_of_overlap
    last_tag_of_overlap = None

    if canvas.itemconfigure('options', 'state')[-1] == 'normal': # Закрытие главного меню
        escape_press = False
        window.unbind('<Expose>')
        window.bind('<Expose>', lambda event: canvas.coords('element_counter_text', window.winfo_width(), 0))
        window.bind(convert_str(get('Settings', tag='take_button')), lambda event: on_click())

        canvas.itemconfigure('options', state='hidden')
        canvas.itemconfigure('sett_button', state='normal')

    elif canvas.itemconfigure('options', 'state')[-1] == 'hidden': # Открытие главного меню
        global take
        take = False
        escape_press = True
        window.unbind('<Expose>')
        window.bind('<Expose>', lambda event: resizing())
        window.unbind(convert_str(get('Settings', tag='take_button')))
        window.unbind(convert_str(get('Settings', tag='double_button')))

        canvas.tag_raise('options','all')
        canvas.itemconfigure('options', state='normal')
        canvas.itemconfigure('sett_button', state='disabled')

        resize_images()
        buttons_esc()

    else: # Закрытие меню настроек
        open_settings()

def open_settings():
    if canvas.itemconfigure('options', 'state')[-1] == 'disabled': # Закрытие меню настроек
        canvas.itemconfigure('settings', state='hidden')
        canvas.itemconfigure('options', state='normal')
    elif canvas.itemconfigure('options', 'state')[-1] == 'normal': # Открытие меню настроек
        canvas.itemconfigure('settings', state='normal')
        canvas.itemconfigure('options', state='disabled')

def find_overlap_buttons(cursors_x, coord_x, cursors_y, coord_y):
    x1 = cursors_x - coord_x
    y1 = cursors_y - coord_y
    x2 = cursors_x + coord_x
    y2 = cursors_y + coord_y
    tag_of_overlap = []
    for button_dict in coords_buttons:
        name_button = next(iter(button_dict))
        v2button_list = ['language_button', 'signature_button', 'done_button', 'winframe_button', 'saves_button', 'take_button', 'double_button', 'settings_open_button'] # add all buttonsv2
        if name_button in v2button_list:
            x1r = cursors_x - int(coord_x//1.1)
            x2r = cursors_x + int(coord_x//1.1)
        else:
            x1r = x1
            x2r = x2
        xy = button_dict[name_button]
        if x1r<=xy[0]<=x2r and y1<=xy[1]<=y2:
            tag_of_overlap.append(name_button)
    if len(tag_of_overlap) != 0:
        if canvas.itemconfigure('settings', 'state')[-1] == 'hidden':
            return tag_of_overlap[0]
        else:
            return tag_of_overlap[-1]

def signature_visibility():
    if convert_str(get('Settings', tag='signatures_visibility'))=='True':
        canvas.itemconfigure('texts', state='hidden')
        change(parameter='signatures_visibility', set_obj='False')
    else:
        canvas.itemconfigure('texts', state='normal')
        change(parameter='signatures_visibility', set_obj='True')

def languages():
    if convert_str(get('Settings', tag='using_language'))=='ru':
        change(parameter='using_language', set_obj='eng')
    elif convert_str(get('Settings', tag='using_language'))=='eng':
        change(parameter='using_language', set_obj='ru')
    new_language_dict = convert_dict(get('Languages', 'language', convert_str(get('Settings', tag='using_language'))))[0]

    for id_with_texts in options_buttons_canvas.find_withtag('texts'):
        first_tag = options_buttons_canvas.gettags(id_with_texts)[0]
        options_buttons_canvas.itemconfigure(first_tag, text=new_language_dict[first_tag])

    for id_with_texts in settings_buttons_canvas.find_withtag('texts'):
        first_tag = settings_buttons_canvas.gettags(id_with_texts)[0]
        settings_buttons_canvas.itemconfigure(first_tag, text=new_language_dict[first_tag])

    for id_with_texts in canvas.find_withtag('texts'):
        first_tag = canvas.gettags(id_with_texts)[0]
        canvas.itemconfigure(first_tag, text=new_language_dict[first_tag])

    canvas.itemconfigure('element_counter_text', text=new_language_dict['element_counter_text']+str(element_counter)+'/'+str(all_elements))
    window.title(new_language_dict['title'])
# та самая функция, ради которой импортирован ctypes
def style_window(color):
    window.update()
    HWND = ct.windll.user32.GetParent(window.winfo_id())
    if color == 'dark':
        ct.windll.dwmapi.DwmSetWindowAttribute(HWND, 19, ct.byref(ct.c_int(1)), ct.sizeof(ct.c_int))
        ct.windll.dwmapi.DwmSetWindowAttribute(HWND, 20, ct.byref(ct.c_int(1)), ct.sizeof(ct.c_int))
    elif color == 'light':
        ct.windll.dwmapi.DwmSetWindowAttribute(HWND, 19, ct.byref(ct.c_int(0)), ct.sizeof(ct.c_int))
        ct.windll.dwmapi.DwmSetWindowAttribute(HWND, 20, ct.byref(ct.c_int(0)), ct.sizeof(ct.c_int))

def winstyles(): # Сейчас: True - Светлая, False - Тёмная
    if convert_str(get('Settings', tag='theme'))=='light': # Делаем тёмную тему
        change(parameter='theme', set_obj='dark')
        win_width = width
        win_height = height
        window.geometry(str(win_width-1)+'x'+str(win_height-1))
        try: style_window('dark') # На всякий случай поставлю блок try, ведь оно вообще должно работать только с windows 11, а у меня 10 и работает
        except: pass
        canvas.configure(bg='#222246')
        settings_buttons_canvas.configure(highlightbackground='#222246')
        window.geometry(str(win_width)+'x'+str(win_height))
        canvas.itemconfigure('elements_text', fill='white')
        canvas.itemconfigure('element_counter_text', fill='white')
    else: # Делаем светлую тему
        change(parameter='theme', set_obj='light')
        win_width = width
        win_height = height
        window.geometry(str(win_width-1)+'x'+str(win_height-1))
        try: style_window('light')
        except: pass
        canvas.configure(bg='#cdf2ff')
        settings_buttons_canvas.configure(highlightbackground='#cdf2ff')
        window.geometry(str(win_width)+'x'+str(win_height))
        canvas.itemconfigure('elements_text', fill='black')
        canvas.itemconfigure('element_counter_text', fill='black')

def new_game():
    window.destroy()
    command_reset ='''
    UPDATE 'Collection'
    SET collect = 'False'
    WHERE element NOT IN ('Fire', 'Water', 'Earth', 'Air');
    '''
    execute(command_reset)
    import os
    os.system('python main.py')
# Собственные диалоговые окна
def window_ok_cancel(type_w):
    def move_close_window_help():
        global coords_exit_xy
        coords_exit_xy = [exit_window.winfo_pointerx() - exit_window.winfo_rootx(), exit_window.winfo_pointery() - exit_window.winfo_rooty()]

    def move_close_window():
        mouse_x = exit_window.winfo_pointerx() - coords_exit_xy[0]
        mouse_y = exit_window.winfo_pointery() - coords_exit_xy[1]
        exit_window.geometry('+' + str(mouse_x) + '+' + str(mouse_y))

    styles = ttk.Style()
    styles.configure('Comic.TButton', font=('Comic Sans MS', 15))

    exit_window = Toplevel(window)
    exit_window.overrideredirect(True)
    exit_window.geometry('315x250+' + str(int(screen_width//2)-150) + '+' + str(int(screen_height//2)-95))
    exit_window.focus_set()
    exit_window.grab_set()

    if type_w == 'exit':
        name_window_text = convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='name_exit_text'))
        question_text = convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='question_exit_text')).replace('\\n', '\n')
        command_ok = lambda: window.destroy()
    elif type_w == 'saves':
        name_window_text = convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='name_reset_saves_text'))
        question_text = convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='question_reset_saves_text')).replace('\\n', '\n')
        command_ok = lambda: new_game()

    if convert_str(get('Settings', tag='theme'))=='light':
        styles.configure('Focus.Comic.TButton', background='#0078d7') # Обводка кнопок при фокусе
        exit_window.config(bg='#cdf2ff') # задний фон окна f9f0ff
        label_close = Label(master=exit_window, text='X', bg='#e4fffc', fg='black', font=('Comic Sans MS', 15))
        label_close.bind('<Enter>', lambda event: label_close.configure(bg='red', fg='white'))
        label_close.bind('<Leave>', lambda event: label_close.configure(bg='#e4fffc', fg='black'))
        label_icon = Label(master=exit_window, image=icon_to_exit, bg='#e4fffc')
        label_name = Label(master=exit_window, text=name_window_text, bg='#e4fffc', fg='black', font=('Comic Sans MS', 14), anchor='w')
        Label(master=exit_window, text=question_text, bg='#cdf2ff', fg='black', font=('Comic Sans MS', 15)).place(x=160, y=100, anchor='center')
        Label(master=exit_window, bg='#f0f0f0').place(x=0, y=250, width=315, height=80, anchor='sw')
    else:
        styles.configure('Focus.Comic.TButton', background='#ff8728')
        exit_window.config(bg='#222246') # 060f00 
        label_close = Label(master=exit_window, text='X', bg='#1b0003', fg='white', font=('Comic Sans MS', 15))
        label_close.bind('<Enter>', lambda event: label_close.configure(bg='red', fg='white'))
        label_close.bind('<Leave>', lambda event: label_close.configure(bg='#1b0003', fg='white'))
        label_icon = Label(master=exit_window, image=icon_to_exit, bg='#1b0003')
        label_name = Label(master=exit_window, text=name_window_text, bg='#1b0003', fg='white', font=('Comic Sans MS', 14), anchor='w')
        Label(master=exit_window, text=question_text, bg='#222246', fg='white', font=('Comic Sans MS', 15)).place(x=160, y=100, anchor='center')
        Label(master=exit_window, bg='#0f0f0f').place(x=0, y=250, width=315, height=80, anchor='sw')

    label_close.place(x=315, y=0, width=45, height=30, anchor='ne')
    label_icon.place(x=0, y=0, width=30, height=30)
    label_name.place(x=30, y=0, width=240, height=30)

    label_close.bind('<Button-1>', lambda event: exit_window.destroy())
    label_name.bind('<Button-1>', lambda event: move_close_window_help())
    label_name.bind('<B1-Motion>', lambda event: move_close_window())

    button_ok = ttk.Button(master=exit_window, style='Comic.TButton', text=convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='ok')), command=command_ok)
    button_ok.place(x=100, y=210, width=100, height=35, anchor='center')
    button_cancel = ttk.Button(master=exit_window, style='Comic.TButton', text=convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='cancel')), command=lambda: exit_window.destroy())
    button_cancel.place(x=225, y=210, width=100, height=35, anchor='center')

    button_ok.focus_set()

    button_ok.bind('<Return>', lambda event: command_ok())
    button_ok.bind('<Right>', lambda event: button_cancel.focus_set())
    button_ok.bind('<Left>', lambda event: button_cancel.focus_set())
    button_ok.bind('<FocusIn>', lambda event: button_ok.configure(style='Focus.Comic.TButton'))
    button_ok.bind('<FocusOut>', lambda event: button_ok.configure(style='Comic.TButton'))

    button_cancel.bind('<Return>', lambda event: exit_window.destroy())
    button_cancel.bind('<Right>', lambda event:button_ok.focus_set())
    button_cancel.bind('<Left>', lambda event: button_ok.focus_set()())
    button_cancel.bind('<FocusIn>', lambda event: button_cancel.configure(style='Focus.Comic.TButton'))
    button_cancel.bind('<FocusOut>', lambda event: button_cancel.configure(style='Comic.TButton'))

    exit_window.wait_window()
    exit_window.mainloop()

dict_binds = {'take': convert_str(get('Settings', tag='take_button')), 'double': convert_str(get('Settings', tag='double_button')), 'settings_open': convert_str(get('Settings', tag='settings_open_button'))}
# Слишком сложный алгоритм определения нажатой кнопки, не хочется даже оптимизировать, переписать, дописывать, в ближайшее время уж точно.
change_bind = False
def which_key(event, button):
    save = lambda button, bind: change('Settings', button+'_button', bind)
    global change_bind
    trying = True
    if event.num != '??':
        settings_buttons_canvas.itemconfigure(button+'_button_text', text=f'<Mouse-{event.num}>')
        save(button, f'<Button-{event.num}>')
    elif event.keysym != '??' and event.char != '??': # 
        try:
            save(button, int(event.keysym)) # Если это цифра
            settings_buttons_canvas.itemconfigure(button+'_button_text', text=int(event.keysym))
        except:
            save(button, '<' + str(event.keysym) + '>')
            settings_buttons_canvas.itemconfigure(button+'_button_text', text='<' + str(event.keysym) + '>')
    else:
        settings_buttons_canvas.itemconfigure(button+'_button_text', text=convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='another_layout_text')), fill='red')
        trying = False
    if trying:
        dict_binds[button] = convert_str(get('Settings', tag=button+'_button'))
        list_binds = [dict_binds[button] for button in dict_binds]
        iterations = {}
        for bind, index in zip(list_binds, range(len(list_binds))):
            if bind in iterations:
                iterations[bind].append(index)
            else:
                iterations[bind] = [index]
        have_iter = False
        for bind in iterations:
            if len(iterations[bind]) > 1:
                iteration_button = iterations[bind]
                for tag in iteration_button:
                    settings_buttons_canvas.itemconfigure('b'+str(tag), fill='red')
                    have_iter = True
            else:
                settings_buttons_canvas.itemconfigure('b'+str(iterations[bind][0]), fill='black')
        change_bind = False
        window.unbind('<Key>')
        window.unbind('<Any-Button>')
        if not have_iter:
            window.after(100, lambda: window.bind(convert_str(get('Settings', tag='settings_open_button')), lambda event: esc_press()))
            window.after(100, lambda: settings_buttons_canvas.tag_bind('done', '<Button-1>', lambda event: esc_press()))
        settings_buttons_canvas.tag_bind('language', '<Button-1>', lambda event: languages())
        settings_buttons_canvas.tag_bind('signature', '<Button-1>', lambda event: signature_visibility())
        settings_buttons_canvas.tag_bind('winframe', '<Button-1>', lambda event: winstyles())
        settings_buttons_canvas.tag_bind('saves', '<Button-1>', lambda event: window_ok_cancel('saves'))

def bindings(button):
    global change_bind # True - изменяется, False - не изменяется
    if not change_bind:
        window.unbind(dict_binds[button])
        settings_buttons_canvas.itemconfigure(button+'_button_text', text=convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='press_any_key_text')))
        window.bind('<Key>', lambda event: which_key(event, button))
        window.after(100, lambda: window.bind('<Any-Button>', lambda event: which_key(event, button)))
        window.unbind(convert_str(get('Settings', tag='settings_open_button')))
        settings_buttons_canvas.tag_unbind('language', '<Button-1>')
        settings_buttons_canvas.tag_unbind('signature', '<Button-1>')
        settings_buttons_canvas.tag_unbind('winframe', '<Button-1>')
        settings_buttons_canvas.tag_unbind('saves', '<Button-1>')
        settings_buttons_canvas.tag_unbind('done', '<Button-1>')
        change_bind = True

def find_overlap_elem(x1, y1, x2, y2):
    list_obj = []
    num = -1
    list_indexes = []
    for element_dict in coords:
        num += 1
        if next(iter(element_dict)) != 'element_object':
            xy = element_dict[next(iter(element_dict))]
            if x1 <= xy[0] <= x2 and y1 <= xy[1] <= y2:
                list_obj.append(next(iter(element_dict)))
                list_indexes.append(num-1)
    return list_obj, list_indexes

def on_click():
    global take
    cursors_x = window.winfo_pointerx() - window.winfo_rootx()
    cursors_y = window.winfo_pointery() - window.winfo_rooty()
    if take == True:
        take = False
        window.unbind(convert_str(get('Settings', tag='double_button')))
        canvas.itemconfigure('sett_button', state='normal')
        trash, elements_id = find_overlap_elem(cursors_x-80, cursors_y-80, cursors_x+80, cursors_y+90)

        if len(elements_id) == 2:
            element_id_1 = elements_id[0]
            element_id_2 = elements_id[1]
            element_1 = elements[element_id_1][next(iter(elements[element_id_1]))]
            element_2 = elements[element_id_2][next(iter(elements[element_id_2]))]
            new_element_object = element_1 + element_2
            if new_element_object:
                new_element_class = new_element_object.__class__.__name__
                adding(new_element_class, new_element_object)
    else:
        elements_over, id_elements = find_overlap_elem(cursors_x-80, cursors_y-80, cursors_x+80, cursors_y+90)
        if len(elements_over)>0:
            take = True
            element = elements_over[-1]
            id_element = id_elements[-1]
            window.bind(convert_str(get('Settings', tag='double_button')), lambda event: double(id_element))
            canvas.itemconfigure('sett_button', state='disabled')
            move(element, id_element)

def move(image, id_image):
    global take, coords
    image_tag = str(image.__class__.__name__).lower()
    text_tag = image_tag + '_text'
    mouse_x = window.winfo_pointerx() - window.winfo_rootx()
    mouse_y = window.winfo_pointery() - window.winfo_rooty()

    canvas.coords(image_tag, mouse_x, mouse_y)
    canvas.coords(text_tag, mouse_x, mouse_y+100)

    coords[id_image+1][next(iter(coords[id_image+1]))] = [mouse_x, mouse_y]
    if take == True:
        window.after(34, lambda: move(image, id_image))

def double(image_id):
    element = elements[image_id][next(iter(elements[image_id]))]
    new_element_object = element + element
    if new_element_object:
        new_element_class = new_element_object.__class__.__name__
        adding(new_element_class, new_element_object)

def adding(new_element_class, new_element_object):
    if not any(new_element_class in dict for dict in elements):
        mouse_x = window.winfo_pointerx() - window.winfo_rootx()
        mouse_y = window.winfo_pointery() - window.winfo_rooty()
        canvas.create_image(mouse_x, mouse_y, image=new_element_object.image, tags=[str(new_element_class).lower()]) # convert_str(get('Settings', tag='signatures_visibility'))
        state='normal' if convert_str(get('Settings', tag='signatures_visibility'))=='True' else 'hidden'
        fillcolor = 'white' if convert_str(get('Settings', tag='theme'))=='dark' else 'black'
        canvas.create_text(mouse_x, mouse_y+100, text=convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag=new_element_class.lower()+'_text')), fill=fillcolor, font=('Comic Sans MS', 30), tags=[str(new_element_class).lower()+'_text', 'texts', 'elements_text'], state=state)
        elements.append({new_element_class: new_element_object})
        coords.append({new_element_object: [mouse_x, mouse_y]})
        change('Collection', 'collect', 'True', 'element', new_element_class)
        global element_counter
        element_counter+=1
        canvas.itemconfigure('element_counter_text', text=convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='element_counter_text'))+str(element_counter)+'/'+str(all_elements))
        canvas.tag_raise('element_counter_text','all')
        canvas.tag_raise('menu_button','all')

init_options_buttons_canvas()
canvas.place(x=-5, y=-5)

elements = [{element_class: eval(element_class+'()')} for element_class in convert_list(get('Collection', 'collect', 'True', tag='element'))]
coords = [{'element_object': ['x', 'y']}] # Делать один словарь нецелесообразно

for element_dict in elements:
    locals().update(element_dict)
    element = element_dict[next(iter(element_dict))]
    random_x = randint(50, width-95)
    random_y = randint(50, height-105)
    canvas.create_image(random_x, random_y, image=element.image, tags=[str(next(iter(element_dict))).lower(), 'images'])
    state = 'normal' if convert_str(get('Settings', tag='signatures_visibility'))=='True' else 'hidden'
    fillcolor = 'black' if variables.this_style else 'white'
    canvas.create_text(random_x, random_y+100, text=convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag=next(iter(element_dict)).lower()+'_text')), fill=fillcolor, font=('Comic Sans MS', 30), tags=[str(next(iter(element_dict))).lower()+'_text', 'texts', 'elements_text'], state=state)
    coords.append({element: [random_x, random_y]})

element_counter = len(elements)
canvas.create_text(640, 0, anchor='ne', text=convert_str(get('Languages', where_obj='language', where_value=convert_str(get('Settings', tag='using_language')), tag='element_counter_text'))+str(element_counter)+'/'+str(all_elements), font=('Comic Sans MS', 25), tags=['element_counter_text'])

if convert_str(get('Settings', tag='theme'))=='dark': # Делаю тёмную тему, если установлена
    win_width = width
    win_height = height
    window.geometry(str(win_width-1)+'x'+str(win_height-1))
    try: style_window('dark') # На всякий случай поставлю блок try
    except: pass
    canvas.configure(bg='#222246')
    settings_buttons_canvas.configure(highlightbackground='#222246')
    window.geometry(str(win_width)+'x'+str(win_height))
    canvas.itemconfigure('elements_text', fill='white')
    canvas.itemconfigure('element_counter_text', fill='white')
else: # Делаю светлую тему, если установлена
    win_width = width
    win_height = height
    window.geometry(str(win_width-1)+'x'+str(win_height-1))
    try: style_window('light')
    except: pass
    canvas.configure(bg='#cdf2ff')
    settings_buttons_canvas.configure(highlightbackground='#cdf2ff')
    window.geometry(str(win_width)+'x'+str(win_height))
    canvas.itemconfigure('elements_text', fill='black')
    canvas.itemconfigure('element_counter_text', fill='black')

canvas.tag_raise('element_counter_text', 'all')
canvas.tag_raise('menu_button', 'all')

window.bind(convert_str(get('Settings', tag='take_button')), lambda event: on_click())
window.bind(convert_str(get('Settings', tag='settings_open_button')), lambda event: esc_press())
window.bind('<Expose>', lambda event: canvas.coords('element_counter_text', window.winfo_width(), 0))


window.mainloop()
cursor.close()

# Специально оставляю много зелени из функции coords_options. С этим ненужным кодом я мучился, добавляя новые кнопки...
    # tuple_tags = options_buttons_canvas.gettags(options_buttons_canvas.find_withtag('pressv1'))+settings_buttons_canvas.gettags(settings_buttons_canvas.find_withtag('pressv2'))
    # if not 'continue' in tuple_tags: options_buttons_canvas.coords('continue_text', options_width//2, options_height//6.05)
    # if not 'settings' in tuple_tags: options_buttons_canvas.coords('settings_text', options_width//2, options_height//2.05)
    # if not 'exit' in tuple_tags: options_buttons_canvas.coords('exit_text', options_width//2, options_height//1.25)
    # if not 'language' in tuple_tags: settings_buttons_canvas.coords('language_text', mini//3.375, mini//6.5)
    # if not 'signature' in tuple_tags: settings_buttons_canvas.coords('signature_text', mini//1.425, mini//6.5)
    # if not 'winframe' in tuple_tags: settings_buttons_canvas.coords('winframe_text', mini//1.425, mini//3.5)
    # if not 'saves' in tuple_tags: settings_buttons_canvas.coords('saves_text', mini//3.375, mini//3.5)
    # if not 'take' in tuple_tags: settings_buttons_canvas.coords('take_button_text', mini//1.425, mini//2.4)
    # if not 'double' in tuple_tags: settings_buttons_canvas.coords('double_button_text', mini//1.425, mini//1.8)
    # if not 'settings_open' in tuple_tags: settings_buttons_canvas.coords('settings_open_button_text', mini//1.425, mini//1.465)
    # if not 'done' in tuple_tags: settings_buttons_canvas.coords('done_text', mini//2, mini//1.21)