import requests

sdg_urls = [
    "https://metadata.un.org/sdg/1",
    "https://metadata.un.org/sdg/2",
    "https://metadata.un.org/sdg/3",
    "https://metadata.un.org/sdg/4",
    "https://metadata.un.org/sdg/5",
    "https://metadata.un.org/sdg/6",
    "https://metadata.un.org/sdg/7",
    "https://metadata.un.org/sdg/8",
    "https://metadata.un.org/sdg/9",
    "https://metadata.un.org/sdg/10",
    "https://metadata.un.org/sdg/11",
    "https://metadata.un.org/sdg/12",
    "https://metadata.un.org/sdg/13",
    "https://metadata.un.org/sdg/14",
    "https://metadata.un.org/sdg/15",
    "https://metadata.un.org/sdg/16",
    "https://metadata.un.org/sdg/17",
]


output_file = "sdgs-metadata.ttl"


def fetch_and_write_sdg_data(url, output_file):
    """
    Fetch the content at a URL with Turtle content type and write the result to an output file
    """
    response = requests.get(url, headers={"Accept": "text/turtle"})
    response.raise_for_status()

    with open(output_file, "a", encoding="utf-8") as f:
        f.write(response.text)
        f.write("\n\n")


# Remove the previous content if any
with open(output_file, "w", encoding="utf-8") as f:
    f.write("")

# Fectch the data for each SDG
for url in sdg_urls:
    fetch_and_write_sdg_data(url, output_file)

print(f"Data for SDGs saved in '{output_file}'.")
