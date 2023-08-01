import asyncio
import tkinter as tk
from tkinter import Canvas, Scrollbar, Text, StringVar
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import csv
from datetime import datetime
import configparser

# Список опций для байтового и словесного порядка
WORDORDER_OPTIONS = [Endian.Big, Endian.Little]

# Глобальные переменные для выбранных байтового порядка, словесного порядка, функции декодирования и экземпляра декодера бинарных данных
selected_byteorder = None
selected_wordorder = None
selected_decode_function = None
binary_payload_decoder_instance = None
results = []
# Список опций для функций декодирования
DECODE_FUNCTION_OPTIONS = {
    "decode_8bit_uint": "decode_8bit_uint",
    "decode_bits": "decode_bits",
    "decode_16bit_uint": "decode_16bit_uint",
    "decode_32bit_uint": "decode_32bit_uint",
    "decode_64bit_uint": "decode_64bit_uint",
    "decode_8bit_int": "decode_8bit_int",
    "decode_16bit_int": "decode_16bit_int",
    "decode_32bit_int": "decode_32bit_int",
    "decode_64bit_int": "decode_64bit_int",
    "decode_16bit_float": "decode_16bit_float",
    "decode_32bit_float": "decode_32bit_float",
    "decode_64bit_float": "decode_64bit_float",
    "decode_string": "decode_string"
}

# Функция сканирования Modbus TCP
async def modbus_tcp_scan(ip, port=502, unit_id=1, st_address=4000, n_registers=100, byte=None, word=None, decode_function=None, count=100):
    # Выводим значения аргументов функции в консоль
    print(ip, port, unit_id, st_address, n_registers, byte, word, decode_function, count)
    try:
        client = ModbusTcpClient(ip, port)
        if not client.connect():
            print(f"Failed to connect to {ip}:{port}")
            return []

        results = []

        decoder = None  # Инициализируем переменную для декодера

        for register in range(st_address-1, st_address + n_registers):
            response = client.read_holding_registers(register, 2, unit_id)

            if response.isError():
                pass
            else:
                # Декодируем данные с использованием указанных байтового порядка и словесного порядка
                if byte == "<" and word == "<":
                    decoder = BinaryPayloadDecoder.fromRegisters(response.registers, byteorder=Endian.Little, wordorder=Endian.Little)
                elif byte == "<" and word == ">":
                    decoder = BinaryPayloadDecoder.fromRegisters(response.registers, byteorder=Endian.Little, wordorder=Endian.Big)
                elif byte == ">" and word == "<":
                    decoder = BinaryPayloadDecoder.fromRegisters(response.registers, byteorder=Endian.Big, wordorder=Endian.Little)
                elif byte == ">" and word == ">":
                    decoder = BinaryPayloadDecoder.fromRegisters(response.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                        
                if decoder is not None:
                    # Используем выбранную функцию декодирования
                    if decode_function == "decode_8bit_uint":
                        decoded_data = decoder.decode_8bit_uint()
                    elif decode_function == "decode_bits":
                        decoded_data = decoder.decode_bits(1)
                    elif decode_function == "decode_16bit_uint":
                        decoded_data = decoder.decode_16bit_uint()
                    elif decode_function == "decode_32bit_uint":
                        decoded_data = decoder.decode_32bit_uint()
                    elif decode_function == "decode_64bit_uint":
                        decoded_data = decoder.decode_64bit_uint()
                    elif decode_function == "decode_8bit_int":
                        decoded_data = decoder.decode_8bit_int()
                    elif decode_function == "decode_16bit_int":
                        decoded_data = decoder.decode_16bit_int()
                    elif decode_function == "decode_32bit_int":
                        decoded_data = decoder.decode_32bit_int()
                    elif decode_function == "decode_64bit_int":
                        decoded_data = decoder.decode_64bit_int()
                    elif decode_function == "decode_16bit_float":
                        decoded_data = decoder.decode_16bit_float()
                    elif decode_function == "decode_32bit_float":
                        decoded_data = decoder.decode_32bit_float()
                    elif decode_function == "decode_64bit_float":
                        decoded_data = decoder.decode_64bit_float()
                    elif decode_function == "decode_string":
                        decoded_data = decoder.decode_string(1)  # Указываем размер строки для декодирования

                    print(f"Register: {register} - Data: {decoded_data}")
                    results.append((register, decoded_data))

        client.close()

        return results

    except ModbusIOException as e:
        print(f"Modbus IO error: {e}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

# Функция обновления данных на холсте
def update_data():
    global target_ip, results, scanned_data
    target_ip = ip_entry.get()
    byteo = selected_byteorder.get()
    wordo = selected_wordorder.get()
    decode_function = selected_decode_function.get()
    count = count_entry.get()  # Получаем значение count из поля ввода
    unit_id = unit_id_entry.get() 

    text_data = "Scanned Data:\n"
    # Перед первым сканированием очищаем результаты
    results.clear()

    # Сканируем устройства Modbus TCP и сохраняем результаты в переменную results
    results = loop.run_until_complete(modbus_tcp_scan(ip=target_ip, st_address=int(start_address), n_registers=int(num_registers), byte=byteo, word=wordo, decode_function=decode_function, count=int(count),unit_id=int(unit_id)))  # Передаём значение count в функцию

    for register, decoded_data in results:
        text_data += f"Register: {register} - Data: {decoded_data}\n"

    # Сбрасываем scanned_data перед обновлением данных
    scanned_data = text_data

    # Очищаем виджет текста и вставляем обновлённые данные
    data_text.configure(state="normal")
    data_text.delete(1.0, "end")
    data_text.insert("end", scanned_data)
    data_text.configure(state="disabled")

    
    # Обновляем область прокрутки холста и обновляем окно
    canvas.configure(scrollregion=canvas.bbox("all"))
    window.update_idletasks()

# Функция сохранения данных в CSV-файл
def save_data_to_csv(results):
    date_string = datetime.now().strftime("%Y-%m-%d")
    file_name = f"data_{date_string}_{target_ip}.csv"

    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Register", "Data"])
        for register, decoded_data in results:
            writer.writerow([register, decoded_data])
    print(f"Данные сохранены в {file_name}")

# Функция сохранения данных в конфигурационный файл
def save_config_to_file(target_ip, port, start_address, num_registers, byteorder, wordorder, decode_function, count,unit_id):
    config = configparser.ConfigParser()
    config['Modbus'] = {
        'target_ip': target_ip,
        'port': port,
        'start_address': start_address,
        'num_registers': num_registers,
        'byteorder': byteorder,
        'wordorder': wordorder,
        'decode_function': decode_function,  # Включаем значение decode_function в конфигурацию
        'count': count,
        'unit_id':unit_id
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# Функция загрузки конфигурации из конфигурационного файла
def load_config_from_file():
    config = configparser.ConfigParser()
    if not config.read('config.ini'):
    # Если файл не существует, создаем его с базовыми значениями
        config['Modbus'] = {
            'target_ip': '',
            'port': '502',
            'start_address': '4000',
            'num_registers': '100',
            'byteorder': '>',
            'wordorder': '>',
            'decode_function': 'decode_16bit_uint',
            'count': '100'
        }
    config.read('config.ini')
    return config['Modbus']

# Функция обработки события прокрутки колесика мыши
def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

# Функция запуска сканирования Modbus и сохранения данных
def start_modbus_scan_and_save():
    global target_ip, port, start_address, num_registers, binary_payload_decoder_instance, results, unit_id

    # Получаем значения из полей ввода и выпадающих списков
    target_ip = ip_entry.get()
    port = port_entry.get()
    start_address = start_address_entry.get()
    num_registers = start_num_entry.get()

    # Получаем выбранные значения для байтового порядка, словесного порядка и функции декодирования
    byteorder_value = selected_byteorder.get()
    wordorder_value = selected_wordorder.get()
    decode_function_value = selected_decode_function.get()

    # Сохраняем target_ip, port, start_address, num_registers, byteorder, wordorder и decode_function в файл конфигурации перед сканированием
    save_config_to_file(target_ip, port, start_address, num_registers, byteorder_value, wordorder_value, decode_function_value, count_entry.get(), unit_id_entry.get())

    # Если результаты сканирования уже есть в переменной results, то не проводим повторное сканирование
    if not results:
        results = loop.run_until_complete(modbus_tcp_scan(target_ip, port=int(port), st_address=int(start_address), n_registers=int(num_registers), byte=byteorder_value, word=wordorder_value, decode_function=decode_function_value, count=int(count_entry.get()),unit_id=int(unit_id_entry.get())))

    update_data()

    # Создаём экземпляр декодера бинарных данных на основе выбранного байтового порядка и словесного порядка
    binary_payload_decoder_instance = BinaryPayloadDecoder.fromRegisters([], byteorder=byteorder_value, wordorder=wordorder_value)

# Функция создания выпадающего списка для выбора байтового порядка
def create_byteorder_dropdown(frame):
    global selected_byteorder

    byteorder_label = tk.Label(frame, text="Byteorder")
    byteorder_label.pack(side="left")

    selected_byteorder = StringVar(window)
    selected_byteorder.set(Endian.Little)  # Устанавливаем значение по умолчанию

    byteorder_dropdown = tk.OptionMenu(frame, selected_byteorder, *WORDORDER_OPTIONS)
    byteorder_dropdown.pack(side="left")

# Функция создания выпадающего списка для выбора словесного порядка
def create_wordorder_dropdown(frame):
    global selected_wordorder

    wordorder_label = tk.Label(frame, text="Wordorder")
    wordorder_label.pack(side="left")

    selected_wordorder = StringVar(window)
    selected_wordorder.set(Endian.Little)  # Устанавливаем значение по умолчанию

    wordorder_dropdown = tk.OptionMenu(frame, selected_wordorder, *WORDORDER_OPTIONS)
    wordorder_dropdown.pack(side="left")

# Функция создания выпадающего списка для выбора функции декодирования
def create_decode_function_dropdown(frame):
    global selected_decode_function
    decode_function_label = tk.Label(frame, text="Decode Function")
    decode_function_label.pack(side="left")

    selected_decode_function = tk.StringVar(window)
    selected_decode_function.set(list(DECODE_FUNCTION_OPTIONS.keys())[0])  # Устанавливаем значение по умолчанию

    decode_function_dropdown = tk.OptionMenu(frame, selected_decode_function, *DECODE_FUNCTION_OPTIONS.keys())
    decode_function_dropdown.pack(side="left")

# Функция создания поля ввода для параметра "Count"
def create_count_input(frame):
    count_entry = tk.Entry(frame)
    count_entry.pack(side="left")
    count_entry.insert(0, count)
    return count_entry

# Функция создания поля ввода для параметра "Unit Id"
def create_unit_id_input(frame):
    unit_id_entry = tk.Entry(frame)
    unit_id_entry.pack(side="left")
    unit_id_entry.insert(0, unit_id)
    return unit_id_entry

if __name__ == "__main__":
    # Загрузка конфигурации из файла
    config = load_config_from_file()
    target_ip = config.get('target_ip', fallback='')
    port = config.get('port', fallback='502')
    start_address = config.get('start_address', fallback='1')
    num_registers = config.get('num_registers', fallback='100')
    byteorder = config.get('byteorder')
    wordorder = config.get('wordorder')
    decode_function = config.get('decode_function')
    count = config.get('count', fallback='2')
    unit_id = config.get('unit_id', fallback='1')

    # Создание главного окна приложения
    window = tk.Tk()
    window.title("Модбас Сканер")
    window.geometry("400x600")
    window.resizable(False, False)
    
    # Основной фрейм для размещения элементов управления
    main_frame = tk.Frame(window)
    main_frame.pack(side="top", padx=10, pady=10)

    # Фрейм для элементов управления с сеткой расположения
    control_frame = tk.Frame(main_frame)
    control_frame.pack(anchor="w", padx=10, pady=5)

    create_byteorder_dropdown(control_frame)
    create_wordorder_dropdown(control_frame)

    control_frame2 = tk.Frame(main_frame)
    control_frame2.pack(anchor="w", padx=10, pady=5)
    create_decode_function_dropdown(control_frame2)

    # Фрейм для ввода IP и порта с расположением по горизонтали
    ip_port_frame = tk.Frame(main_frame)
    ip_port_frame.pack(anchor="w", padx=10, pady=5)

    ip_label = tk.Label(ip_port_frame, text="IP адрес:", width=10)
    ip_label.pack(side="left")

    ip_entry = tk.Entry(ip_port_frame, width=15)
    ip_entry.pack(side="left")
    ip_entry.insert(0, target_ip)

    port_label = tk.Label(ip_port_frame, text="Порт:", width=10, padx=4)
    port_label.pack(side="left")

    port_entry = tk.Entry(ip_port_frame, width=5)
    port_entry.pack(side="left")
    port_entry.insert(0, port)

    # Фрейм для ввода параметров Count и Id с расположением по горизонтали
    input_frame = tk.Frame(main_frame)
    input_frame.pack(anchor="w", padx=10, pady=5)

    count_label = tk.Label(input_frame, text="Count:", width=10)
    count_label.pack(side="left")

    count_entry = create_count_input(input_frame)
    count_entry.pack(side="left")

    unit_id_label = tk.Label(input_frame, text="Id :", width=5, padx=6)
    unit_id_label.pack(side="left")

    unit_id_entry = create_unit_id_input(input_frame)
    unit_id_entry.pack(side="left")

    # Фрейм для параметров Start Address и NUM с расположением по горизонтали
    address_num_frame = tk.Frame(main_frame)
    address_num_frame.pack(anchor="w", padx=10, pady=5)

    start_address_label = tk.Label(address_num_frame, text="Start Address:", width=12)
    start_address_label.pack(side="left")

    start_address_entry = tk.Entry(address_num_frame, width=8)
    start_address_entry.pack(side="left")
    start_address_entry.insert(0, start_address)

    start_num_label = tk.Label(address_num_frame, text="NUM:", width=5)
    start_num_label.pack(side="left")

    start_num_entry = tk.Entry(address_num_frame, width=5)
    start_num_entry.pack(side="left")
    start_num_entry.insert(0, num_registers)
        
    # Фрейм с кнопками
    button_frame = tk.Frame(window)
    button_frame.pack(side="top", pady=10)

    start_button = tk.Button(button_frame, text="Start Scan", command=start_modbus_scan_and_save)
    start_button.pack(side="left")

    save_button = tk.Button(button_frame, text="Save Data", command=lambda: save_data_to_csv(results))
    save_button.pack(side="left")

    # Описание данных
    label = tk.Label(window, text="Scanned Data:", font=("Arial", 12))
    label.pack(padx=10, pady=10)

    # Холст с возможностью прокрутки
    canvas = Canvas(window, width=300, height=300)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=canvas.yview)

    frame_canvas = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_canvas, anchor="nw")

    loop = asyncio.get_event_loop()
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    data_text = Text(frame_canvas, wrap="none", font=("Arial", 12), state="disabled")
    data_text.pack(fill="both", expand=True)
    data_text.bind("<MouseWheel>", on_mousewheel)

    window.mainloop()


