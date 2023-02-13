import math
import datetime
from rich.console import Console
console = Console()
from rich import traceback
traceback.install()

def error(pred):
    actual_bpm = float(input("Acutal BPM: "))
    error = (abs(actual_bpm - pred)/actual_bpm)*100
    console.print("Calculated error", error, style="blink bold red underline on white")
    return error