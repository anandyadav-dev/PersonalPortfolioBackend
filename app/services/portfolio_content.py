import os
import glob

class PortfolioContentService:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def get_site_content(self) -> str:
        """
        Reads all .tsx files in src/sections to simulate 'scraping' the portfolio.
        Returns a single string with all relevant content.
        """
        # Adjust path to find src/sections relative to backend or absolute
        # Assuming base_path provided is root of repo
        sections_dir = os.path.join(self.base_path, "src", "sections")
        content = []

        if not os.path.exists(sections_dir):
            return "Portfolio sections directory not found."

        files = glob.glob(os.path.join(sections_dir, "*.tsx"))
        
        content.append("=== PORTFOLIO WEBSITE CONTENT (Simulated Scraping) ===")
        
        for file_path in files:
            filename = os.path.basename(file_path)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
                    content.append(f"\n--- SECTION: {filename} ---\n")
                    content.append(file_content)
            except Exception as e:
                content.append(f"\nError reading {filename}: {str(e)}\n")

        return "\n".join(content)
