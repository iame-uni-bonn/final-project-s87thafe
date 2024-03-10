import subprocess
from pathlib import Path
from arbitrage_analysis.config import PAPER_DIR, BLD_figures, BLD_tables

depends_on_compile_tex = {
    "tex_figure": BLD_tables / "arbitrage_opportunities.tex",
    "kde_figure": BLD_figures / 'kde_with_arbitrage_opportunities.png',
    "arb_opp_figure": BLD_figures / "arbitrage_opportunities.png",
    "yield_figure": BLD_figures / "investment_growth.png",
    "tex_file": PAPER_DIR / "arbitrage_analysis.tex"
}

def task_compile_paper(
    depends_on = depends_on_compile_tex
    ):
    # Compile the paper
    subprocess.run(["latexmk", "-pdf", depends_on["tex_file"]], check=False, cwd=depends_on["tex_file"].parent)