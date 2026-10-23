import os
from src.config_parser import ConfigParser
from src.scraper_agent import ScraperAgent


def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(project_dir, "configs", "example_site_config.json")

    try:
        config = ConfigParser(config_path).load_config()
        config["output_directory"] = os.path.join(project_dir, "data")
        agent = ScraperAgent(config, headless=True)
        products = agent.run()
        print("\n--- Scraping Summary ---")
        print(f"Products collected: {len(products)}")
        print(f"Output folder: {os.path.join(project_dir, 'data')}")
        print("------------------------")
    except (FileNotFoundError, ValueError, OSError) as error:
        print(f"Unable to run scraper: {error}")


if __name__ == "__main__":
    main()
