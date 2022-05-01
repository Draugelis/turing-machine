Turing Machine
==========================
Python script for emulating the turing machine behaviour. 

Wiki: https://en.wikipedia.org/wiki/Turing_machine

Usage 
--------------------------
1. Setup command file 
    * You may want to run `cp template.json my_commands.json` 
2. Run Python script - `python3 turing.py (-f / --file) path/to/file.json`
    * Each step will be printed out 
        ```
        000100000001111110000000000000000000000000010000
                ^
        000100000001111110000000000000000000000000010000
                        ^
        000100000001111111000000000000000000000000010000
                        ^
        000100000001111111000000000000000000000000010000
        ```
    * Final line will be steps taken 
        ```
        000100000000000000000000000000001111110000010000
                                        ^
        000100000000000000000000000000001111110000010000
                                        ^
        000100000000000000000000000000001111110000010000
                                        ^
        10001
        ```

Command files
--------------------------
Command file is stored in a JSON file 

**`X` state is for HALT**

```JSON
{
    "step_limit": 1000,
    "starting_position": 1,
    "tape": "00V0000000001111*A000000000001111*B000000000000000000000000ZR000000000H000000",
    "commands": [
        {
            "current_state": "0",
            "current_symbol": "0",
            "new_symbol": "0",
            "direction": "R", 
            "new_state": "0"
        },
        ...
        {
            "current_state": "21",
            "current_symbol": "1",
            "new_symbol": "1",
            "direction": "R", 
            "new_state": "X"
        }
    ]
}
```

