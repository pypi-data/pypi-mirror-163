# mini urls
A library to short urls with [shrtco.de](https://shrtco.de) api

## Installation

```bash
pip install miniurls
```

## Example

```python
import miniurls

url = "https://example.com"
shorten = miniurls.Short()
shorten_url = shorten.shortUrl(url=url)

print(shorten_url)
```