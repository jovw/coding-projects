# Usage

## Running the Program
This program has been written in Python 3.

### Using Visual Studio Code or PyCharm:
You can open it in Visual Studio Code or PyCharm and execute the code in the `rdt_main.py` file.

### Using the Terminal:
Open a new terminal window for the file and execute the following command:

```
python3 rdt_main.py
```

## Testing Different String Sizes
In `rdt_main.py`, you have the option of sending either a short or a long string. 
Uncomment the option you would like to execute.

## Testing Various Unreliable Scenarios
In `rdt_main.py`, you can set different flags based on the scenario you intend to test.
By default, they are all set to False, ensuring reliable data transfer.

```python
outOfOrder = False
dropPackets = False
delayPackets = False
dataErrors = False
```

