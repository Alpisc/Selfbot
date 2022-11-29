@echo off
:A
echo Selection.
echo:
echo (1) Selfbot
echo (2) Setup
echo (3) Dependencies
echo (4) Exit
set /p selection=choice: 
echo choice is: %selection%
echo:

if %selection% NEQ 1 (
    if %selection% NEQ 2 (
        if %selection% NEQ 3 (
            if %selection% NEQ 4 (
                cls 
                echo "%selection%" is an invalid choice
                echo:
                goto :A
            )
        )
    )
)

if %selection% EQU 1 (
    echo Starting Selfbot ...
    python3 .content/selfbot.py
) else (
    if %selection% EQU 2 (
        echo Starting Setup
        python3 .content/setup_wizard.py
        echo:
        echo Setup finished
        pause
        cls
        goto :A
    ) else (
        if %selection% EQU 3 (
            echo Installing dependencies
            pip install -r .content/requirements.txt
            echo:
            echo Finished installing dependencies
            pause
            cls
            goto :A
        ) else (
            if %selection% EQU 4 (
                echo Exiting ...
                exit
            )
        )
    )
)

pause