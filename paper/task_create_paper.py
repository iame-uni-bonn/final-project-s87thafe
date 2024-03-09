import subprocess
from arbitrage_analysis.config import PAPER_DIR, BLD_figures, BLD_tables

def _compile_tex_document(tex_file_path):
    """
    Compiles a LaTeX document into a PDF using pdflatex.

    Parameters:
    - tex_file_path: str, the path to the .tex file to be compiled.

    Returns:
    - None. However, it prints out a success message upon successful compilation
      or an error message if the compilation fails.

    Raises:
    - subprocess.CalledProcessError: If pdflatex encounters an error during compilation.

    Example usage:
    >>> compile_tex_document("path/to/document.tex")
    """
    try:
        # Execute the pdflatex command
        subprocess.run(["pdflatex", tex_file_path], check=True)
        
        # Print success message
        print(f"Successfully compiled {tex_file_path} into PDF.")
    except subprocess.CalledProcessError as e:
        # Print error message
        print(f"Failed to compile {tex_file_path}. Error: {e}")

depends_on_compile_tex = {
    "tex_figure": BLD_tables / "arbitrage_opportunities.tex",
    "kde_figure": BLD_figures / 'kde_with_arbitrage_opportunities.png',
    "arb_opp_figure": BLD_figures / "arbitrage_opportunities.png",
    "yield_figure": BLD_figures / "investment_growth.png"
}

def task_compile_paper(
    depends_on = depends_on_compile_tex,
    produces =  PAPER_DIR / "arbitrage_analysis.pdf"
    ):
    _compile_tex_document(produces)