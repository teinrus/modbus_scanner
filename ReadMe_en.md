## Modbus Scanner: Efficient Modbus TCP Device Scanning

Modbus Scanner is an efficient program that greatly simplifies the process of scanning Modbus TCP devices and conveniently decoding their data. Here are several key advantages that make this program a worthwhile choice:

1. **Intuitive Interface**: Modbus Scanner provides a simple and user-friendly graphical interface. You don't need to be an expert to use this program. All connection and decoding parameters are easily input.

2. **Fast Scanning**: The program performs Modbus TCP device scanning quickly and presents results in a convenient format. You can easily access register values and their contents.

3. **Flexible Settings**: Modbus Scanner allows you to choose byte order and word order for data decoding, as well as the decoding function. This enables adapting the program to different data types of Modbus TCP devices.

4. **Result Saving**: Scanning results can be easily saved to a CSV file for further analysis or sharing with colleagues. This is particularly useful for data storage and exchange.

5. **Convenient Configuration Loading**: We have added the automatic saving of connection and scanning parameters to the "config.ini" file. This allows you to preserve your settings between program launches.

6. **Modbus TCP Support**: The program exclusively works with Modbus TCP devices, ensuring high-speed and reliable communication.

7. **Open Source**: The program's source code is open to you. You can analyze it and make improvements if necessary.

8. **Simple Installation**: Installing the program and its dependencies is straightforward and does not require special skills. Follow the simple instructions for installing Python and necessary libraries.

# Usage of .exe File:
For more convenient program execution, you can use the executable file "modbus_scanner.exe". Ensure that the "config.ini" file is in the same folder as "modbus_scanner.exe" so that the program can successfully load the configuration.

# Usage
1. **Installation of Dependencies**: Before running the program, make sure you have Python and the necessary libraries installed. If you do not have Python or the libraries yet, follow these steps:

   - **Installing Python**: Go to the official Python website (https://www.python.org/), download the installer for your operating system, and follow the instructions to install Python.

   - **Installing Libraries**: Open the command prompt (terminal) and execute the following commands:

     ```
     pip install asyncio
     pip install tkinter
     pip install pymodbus
     ```

   > Note: The `tkinter` library is usually installed along with Python on most systems. If you encounter any issues with its installation or usage, refer to the official Python documentation.

2. **Project Download**: Download the source code of the program "modbus_scanner.py" from your source, such as GitHub or an archive.

3. **Running the Program**: After downloading the source code, navigate to the directory with the "modbus_scanner.py" file and run the program using the command:


4. **Graphical Interface**: After executing the command, a window with the Modbus Scanner graphical interface will open.

5. **Parameter Configuration**: In the interface, you can input the necessary connection parameters to the Modbus TCP device:

- Enter the IP address of the Modbus TCP device in the "IP Address" field.
- By default, the Modbus TCP port number is set to 502, but you can change it if needed by entering a new number in the "Port" field.
- Specify the starting register address for scanning in the "Start Address" field.
- Enter the number of registers to scan in the "NUM" field.

6. **Decoding Parameters**: To decode the received data, select the following parameters:

- "Byteorder": Choose the byte order - Little-Endian or Big-Endian.
- "Wordorder": Choose the word order - Little-Endian or Big-Endian.
- "Decode Function": Choose the data decoding function.

7. **Scanning and Data Display**: After providing all the parameters, click the "Start Scan" button to perform Modbus TCP device scanning. The scanning results will be displayed in the program's window.

8. **Saving Results**: If you want to save the scanning results to a CSV file, click the "Save Data" button. The data will be saved in a file with a name like: "data_year-month-day_IP_address.csv".

9. **Configuration Loading and Saving**: The program automatically loads and saves connection and scanning parameters to the "config.ini" file. This allows you to preserve your settings between program launches.

10. **Note**: The program only works with Modbus TCP devices. Ensure that the device is accessible on the network and responds to requests.

