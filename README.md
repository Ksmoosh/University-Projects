# University-Projects
Here are samples of some of my codes done as university assignments.

## Microcontroller simulator

It is a simple Microcontroller simulator, written in Python with a help of PyQt, which can handle few Assembler
language commands and also 10 chosen interruption functions.

Functions of 21H interrupt handler:
- INT0:
  - closes application window
- INT1:
  - waits for standard input and saves character's ASCII value to AL register
- INT2:
  - reads value of register DL and writes the character that value represents (in ASCII code) to standard output, also moves that value to AL register
- INT3:
  - launches a new terminal window
- INT6:
  - reads a command from the standard input device directly to terminal and runs it (careful with commands!)
- INT2A:
  - sets registers with the current date:
    - AL with number of day in the week (where 0 means Monday and 6 means Sunday),
    - BL with number of day,
    - BH with number of month,
    - CX with number of year
- INT2C:
  - sets registers with the current time:
    - AH with number of hours,
    - AL with number of minutes,
    - BH with number of seconds,
    - BL with number of milliseconds
- INT30:
  - sets register AH with major system version and register AL with minor system version
- INT49:
  - clears all registers in the program
- INTED:
  - clears file used for saving and loading data
    
## Flow simulator

This one, is a small program simulating a flow of fluid between two containers, with containers sizes and drainage pipe size as variables. It plots the fluid level in both containers and magnitude of the flow.
