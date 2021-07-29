# Webscraper for Ligainsider

## Prerequisites
Python >=3.6 is recommended. You need to install the following packages using pip:

```
pip3 install requests beautifulsoup schedule
```

## Execution
- Activate your conda environment or make sure you have all the packages installed using ```pip3```.
- In the terminal, execute ```nohup python3 main.py &``` This will start a scheduler that executes the function ```update_data``` defined in ```scraper.py``` at 00:05 every night.
- Note: The system (or WSL) needs to be running. The user can be logged off though and the terminal can be closed.
- Note: You can kill the process again using the process ID. This can be retrieved by running ```ps -ef | grep "python3 main.py"``` (the first number after the username). Then you can run ```kill <PID>``` to kill the process.