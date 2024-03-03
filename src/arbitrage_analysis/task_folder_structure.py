from arbitrage_analysis.config import BLD

# Define the subdirectories to create within BLD
subdirectories = {
    "data": BLD / "data",
    "figures": BLD / "figures",
    "models": BLD / "models",
    "predictions": BLD / "predictions",
    "tables": BLD / "tables"
}

def task_create_directories(
    produces=subdirectories.values(),
):
    for directory in subdirectories.values():
        directory.mkdir(parents=True, exist_ok=True)