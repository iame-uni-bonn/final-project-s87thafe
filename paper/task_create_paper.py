import subprocess
from arbitrage_analysis.config import PAPER_DIR, BLD_figures, BLD_tables

def compile_tex_document(tex_file_path):
    """
    Compiles a LaTeX document into a PDF file using pdflatex.

    This function takes the path to a .tex file as input and uses the pdflatex command to compile
    it into a PDF. It outputs a success message upon successful compilation or an error message
    if the compilation fails. In case of a compilation error, a subprocess.CalledProcessError is
    raised.

    Args:
        tex_file_path (str): The file path of the .tex LaTeX document to be compiled.

    Returns:
        None: Upon successful completion, prints a success message. If an error occurs during
              compilation, an error message is printed and a subprocess.CalledProcessError is raised.

    Raises:
        subprocess.CalledProcessError: Indicates an error occurred during the compilation process.
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
    compile_tex_document(produces)