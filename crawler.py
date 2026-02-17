import requests
from bs4 import BeautifulSoup
import re
import pathlib

def crawl_transcript_links(base_url: str, output_file: pathlib.Path) -> None:
    """
    Crawl the base URL for episode transcript links and generate scraping instructions.
    Args:
        base_url (str): The URL to crawl for transcript links.
        output_file (Path): File to write scraping instructions.
    """
    response = requests.get(base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    instructions = []
    # Example: Find links to episode transcripts (adjust selector as needed)
    for link in soup.find_all('a', href=True):
        href = link['href']
        text = link.get_text(strip=True)
        # Heuristic: Look for links containing 'Transcript:'
        if re.search(r'Transcript:', href) or re.search(r'Transcript:', text):
            episode_name = text if text else href
            episode_url = href if href.startswith('http') else base_url.rstrip('/') + '/' + href.lstrip('/')
            instructions.append(f"{episode_name}|{episode_url}")

    with open(output_file, 'w', encoding='utf-8') as f:
        for instruction in instructions:
            f.write(instruction + '\n')
    print(f"Scraping instructions written to {output_file}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        prog='Episode Transcript Crawler',
        description='Crawl a base URL for episode transcript links and generate scraping instructions.',
        epilog='Example: python crawler.py https://theinfosphere.org/Transcripts transcripts.txt'
    )
    parser.add_argument('base_url', help='URL to crawl for episode transcript links')
    parser.add_argument('output_file', type=pathlib.Path, help='File to write scraping instructions')
    parser.add_argument('-f', '--filter', type=str, default='Transcript:', help='Regex to filter transcript links (default: Transcript:)')
    parser.add_argument('--format', choices=['txt', 'csv'], default='txt', help='Output format for instructions (default: txt)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--max-links', type=int, default=0, help='Maximum number of transcript links to crawl (0 = unlimited)')

    args = parser.parse_args()

    def crawl_transcript_links_cli(base_url: str, output_file: pathlib.Path, filter_regex: str, output_format: str, verbose: bool, max_links: int) -> None:
        try:
            response = requests.get(base_url)
            response.raise_for_status()
        except Exception as e:
            print(f"ERROR: Failed to fetch {base_url}: {e}")
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        instructions = []
        link_count = 0
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text(strip=True)
            if re.search(filter_regex, href) or re.search(filter_regex, text):
                episode_name = text if text else href
                episode_url = href if href.startswith('http') else base_url.rstrip('/') + '/' + href.lstrip('/')
                instructions.append((episode_name, episode_url))
                link_count += 1
                if verbose:
                    print(f"Found: {episode_name} | {episode_url}")
                if max_links and link_count >= max_links:
                    break
        if not instructions:
            print("WARNING: No transcript links found.")
        with open(output_file, 'w', encoding='utf-8') as f:
            if output_format == 'csv':
                f.write('episode_name,episode_url\n')
                for name, url in instructions:
                    f.write(f'"{name}","{url}"\n')
            else:
                for name, url in instructions:
                    f.write(f'{name}|{url}\n')
        print(f"Scraping instructions written to {output_file} ({len(instructions)} links)")

    crawl_transcript_links_cli(
        args.base_url,
        args.output_file,
        args.filter,
        args.format,
        args.verbose,
        args.max_links
    )
