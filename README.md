# Flying Wizard
> A remake of Flappy Bird featuring a wizard.

This is a game where you play as a wizard on a broomstick who must avoid obstacles to achieve a high score. This game is based on the mechanics of Flappy Bird.

## To run the game:
 1. Ensure your system has the software needed:
    - **[Python 3](https://www.python.org/downloads/) with Pip**
        #### On Windows
        Download the executable from the [website](https://www.python.org/downloads/) and go through the installer.
        #### On Linux
        Python may be preinstalled on your system, however if it isn't,
        use your distribution's package manager to install it.  
        >On many distributions, python is preinstalled, but Pip is not.  
        > **To Install Pip:**  
        > - On Ubuntu: `sudo apt install python3-pip`
        > - On Fedora: `sudo dnf install python3-pip`

 2. Clone the github repository by running
 `git clone https://github.com/vegan-cheese/flying-wizard.git`
 3. Enter the directory:  
 `cd flying-wizard`
 4. Create a python virtual environment:  
 `python3 -m venv game_environment`
 5. Install pygame in the environment:  
     - Windows Powershell - `./game_environment/Scripts/pip install pygame`  
     - Bash - `./game_environment/bin/pip install pygame`
 6. Run the game:
     - Windows Powershell - `./game_environment/Scripts/python src/main.py`
      - Bash - `./game_environment/bin/python src/main.py`
