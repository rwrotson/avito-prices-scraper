# Avito Prices Scraper

Web scraper app for getting and parsing prices of products from [Avito.ru](https://avito.ru)

## Supports  🚀
✅ **Extract product prices & status** (`SOLD` / `BOOKED` / etc.) directly from ads  
✅ **Flexible search options**:  
    - Search by keywords or use a `JSON` / `YAML` config file  
    - Extract prices from multi-product ad descriptions  
✅ **Powerful filtering & sorting** by price and status  
✅ **Multiple output formats**:  
    - `table`  
    - `json`  
    - `csv`  
    - and more  
✅ **Save results to `MongoDB`** for persistence (*optional*)  
✅ **Access saved data easily**:  
    - query via CLI commands  
    - view results in `MongoExpress` web interface  
✅ **Easy to deploy**:  
    - can be installed via `uv` package manager  
    - containerized with `docker` and `docker-compose` secure configurations 

## Why Use This? 💡
✅ **For vendors:**  
    - find competitive pricing for items you want to sell  
    - regularly monitor competitors' prices  
    - track the status of your competitors' products  

✅ **For buyers**:   
    - find the best deals  
    - regularly monitor prices to be informed when the price drops

## Prepare for installation  🛠️
1. Clone the repository

```bash
git clone https://github.com/rwrotson/avito-prices-scraper
```

2. Provide the necessary environment variables in the `.env`-files or 
in `.env`-files and secrets-file for `Docker` deployment.
See examples in the `.env/example`-files.  
  
For full version with `MongoDB` support, you need to provide the following files:
- `.mongodb`
- `.mongoexpress`
- `.parser` *(optional)*

For minimal version with just a scraper itself you can provide no files at all.  
Although you can optionally provide this one:
- `.parser` *(optional)*

## Install locally 📦
1. **Install `uv` package manager**

```bash
pip install uv
```

2. **Install the app**

For minimal version without `MongoDB` support:
```bash
uv pip install .
```
For full version with `MongoDB` support:
```bash
uv pip install ".[db-libs]"
```

3. **Run the app**

```bash
avito-prices-scraper --help
avito-prices-scraper search_on_avito --help
avito-prices-scraper search_on_avito_from_file --help
avito-prices-scraper search_in_db --help
```


## Install with Docker  🐳

1. **Build images**: 
```
docker compose -f docker/{version}.compose.yml build```, where `{version}` is either `full` or `minimal`.
```

2. **Run containers**:  
```docker compose -f docker/{version}.compose.yml up```, where `{version}` is either `full` or `minimal`.

  *You can configure the app by modifying `{version}.compose.yml` file, especially `command` instructions of `parser` service and also by providing different configs in`request-entries` directory.*
  

## Usage  🚀

```shell
~/Dev/we/avito-prices-scraper main !1 ❯ avito-prices-scraper --help                             avito-prices-scraper 04:26:00
                                                                                                                               
 Usage: avito-prices-scraper [OPTIONS] COMMAND [ARGS]...                                                                       
                                                                                                                               
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                     │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.              │
│ --help                        Show this message and exit.                                                                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ search-on-avito             Search for products on Avito by given queries.                                                  │
│ search-on-avito-from-file   Search for products on Avito by given queries from a file.                                      │
│ search-in-db                Search for product_requests and resulting products.                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

```shell
~/Dev/we/avito-prices-scraper main !1 ❯ avito-prices-scraper search-on-avito --help             avito-prices-scraper 04:25:54
                                                                                                                               
 Usage: avito-prices-scraper search-on-avito [OPTIONS] SEARCH_QUERIES...                                                       
                                                                                                                               
 Search for products on Avito by given queries.                                                                                
 For 'title_queries' and 'description_queries' options:                                                                        
 - when list of values is provided, it should be of the same length as 'search_queries', as each value will be used for        
 corresponding search query   - when None values are provided, they default to 'search_queries'                                
                                                                                                                               
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    search_queries      SEARCH_QUERIES...  A query string(s) to search for a product with Avito search service [required]  │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --title-queries                                    TEXT                               An additional query string(s) to      │
│                                                                                       search for in product titles for      │
│                                                                                       better prices detection. If not       │
│                                                                                       provided, search in titles will be    │
│                                                                                       performed with 'search_queries'       │
│                                                                                       strings.Use '_' to skip this option   │
│                                                                                       for some of queries and use           │
│                                                                                       'search_queries' instead.             │
│                                                                                       [default: <class 'list'>]             │
│ --description-queries                              TEXT                               An additional query string(s) to      │
│                                                                                       search for in product descriptions,   │
│                                                                                       when there are several products in    │
│                                                                                       one product card at one URL. If not   │
│                                                                                       provided, search in descriptions will │
│                                                                                       be performed with 'search_queries'    │
│                                                                                       strings. Use '_' to skip this option  │
│                                                                                       for some of queries and use           │
│                                                                                       'search_queries' instead.             │
│                                                                                       [default: <class 'list'>]             │
│ --max-pages                                        INTEGER RANGE [x>=0]               Maximum number of pages to scrape.    │
│                                                                                       Use '0' to scrape all pages.          │
│                                                                                       [default: 0]                          │
│ --min-price                                        INTEGER RANGE [x>=0]               Minimum price to filter by. Use '0'   │
│                                                                                       to not filter.                        │
│                                                                                       [default: 0]                          │
│ --max-price                                        INTEGER RANGE [x>=0]               Maximum price to filter by. Use '0'   │
│                                                                                       to not filter.                        │
│                                                                                       [default: 0]                          │
│ --include-unknown        --no-include-unknown                                         Include products with unknown prices. │
│                                                                                       [default: include-unknown]            │
│ --include-ambiguous      --no-include-ambiguous                                       Include products with ambiguous       │
│                                                                                       prices.                               │
│                                                                                       [default: include-ambiguous]          │
│ --include-multiple       --no-include-multiple                                        Include products with multiple prices │
│                                                                                       found in description.                 │
│                                                                                       [default: include-multiple]           │
│ --include-booked         --no-include-booked                                          Include products marked as booked.    │
│                                                                                       [default: include-booked]             │
│ --include-sold           --no-include-sold                                            Include products marked as sold.      │
│                                                                                       [default: include-sold]               │
│ --sort-by                                          [price|page]                       Sort products by price or page.       │
│                                                                                       [default: price]                      │
│ --sort-order                                       [asc|desc]                         Sort products in ascending or         │
│                                                                                       descending order.                     │
│                                                                                       [default: asc]                        │
│ --template                                         [list|table|dataclasses|json|csv]  Choose a template for printing found  │
│                                                                                       products and prices.                  │
│                                                                                       [default: table]                      │
│ --save-to-db             --no-save-to-db                                              Whether to save products to the       │
│                                                                                       database or not.                      │
│                                                                                       [default: no-save-to-db]              │
│ --help                                                                                Show this message and exit.           │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

```shell
~/Dev/we/avito-prices-scraper main !1 ❯ avito-prices-scraper search-on-avito-from-file --help   avito-prices-scraper 04:25:13
                                                                                                                               
 Usage: avito-prices-scraper search-on-avito-from-file [OPTIONS] FILE_PATH                                                     
                                                                                                                               
 Search for products on Avito by given queries from a file.                                                                    
 The file in YAML or JSON format should contain a list of dictionaries with request params, where each dictionary represents   
 query and params for a single search request.                                                                                 
 You can find examples of this file in 'request-entries' directory.                                                            
 Other options provide fallback values for all params, when they are not provided in the file.                                 
                                                                                                                               
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    file_path      PATH  Path to a JSON or YAML text file with search queries and options. [required]                      │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --max-pages                                      INTEGER RANGE [x>=0]               Maximum number of pages to scrape. Use  │
│                                                                                     '0' to scrape all pages.                │
│                                                                                     [default: 0]                            │
│ --min-price                                      INTEGER RANGE [x>=0]               Minimum price to filter by. Use '0' to  │
│                                                                                     not filter.                             │
│                                                                                     [default: 0]                            │
│ --max-price                                      INTEGER RANGE [x>=0]               Maximum price to filter by. Use '0' to  │
│                                                                                     not filter.                             │
│                                                                                     [default: 0]                            │
│ --include-unknown      --no-include-unknown                                         Include products with unknown prices.   │
│                                                                                     [default: include-unknown]              │
│ --include-ambiguous    --no-include-ambiguous                                       Include products with ambiguous prices. │
│                                                                                     [default: include-ambiguous]            │
│ --include-multiple     --no-include-multiple                                        Include products with multiple prices   │
│                                                                                     found in description.                   │
│                                                                                     [default: include-multiple]             │
│ --include-booked       --no-include-booked                                          Include products marked as booked.      │
│                                                                                     [default: include-booked]               │
│ --include-sold         --no-include-sold                                            Include products marked as sold.        │
│                                                                                     [default: include-sold]                 │
│ --sort-by                                        [price|page]                       Sort products by price or page.         │
│                                                                                     [default: price]                        │
│ --sort-order                                     [asc|desc]                         Sort products in ascending or           │
│                                                                                     descending order.                       │
│                                                                                     [default: asc]                          │
│ --template                                       [list|table|dataclasses|json|csv]  Choose a template for printing found    │
│                                                                                     products and prices.                    │
│                                                                                     [default: table]                        │
│ --save-to-db           --no-save-to-db                                              Whether to save products to the         │
│                                                                                     database or not.                        │
│                                                                                     [default: no-save-to-db]                │
│ --help                                                                              Show this message and exit.             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

```shell
~/Dev/we/avito-prices-scraper main !1 ❯ avito-prices-scraper search-in-db --help            5s  avito-prices-scraper 04:24:42
                                                                                                                               
 Usage: avito-prices-scraper search-in-db [OPTIONS]                                                                            
                                                                                                                               
 Search for product_requests and resulting products.                                                                           
                                                                                                                               
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --search-queries                                   TEXT                               A query string(s) to search for a     │
│                                                                                       product with Avito search service     │
│                                                                                       [default: <class 'list'>]             │
│ --title-queries                                    TEXT                               An additional query string(s) to      │
│                                                                                       search for in product titles for      │
│                                                                                       better prices detection. If not       │
│                                                                                       provided, search in titles will be    │
│                                                                                       performed with 'search_queries'       │
│                                                                                       strings.Use '_' to skip this option   │
│                                                                                       for some of queries and use           │
│                                                                                       'search_queries' instead.             │
│                                                                                       [default: <class 'list'>]             │
│ --description-queries                              TEXT                               An additional query string(s) to      │
│                                                                                       search for in product descriptions,   │
│                                                                                       when there are several products in    │
│                                                                                       one product card at one URL. If not   │
│                                                                                       provided, search in descriptions will │
│                                                                                       be performed with 'search_queries'    │
│                                                                                       strings. Use '_' to skip this option  │
│                                                                                       for some of queries and use           │
│                                                                                       'search_queries' instead.             │
│                                                                                       [default: <class 'list'>]             │
│ --request-ids                                      TEXT                               Filter by request ID.                 │
│                                                                                       [default: <class 'list'>]             │
│ --datetime-lte                                     FROMISOFORMAT                      Filter by max timestamp.              │
│                                                                                       [default: None]                       │
│ --datetime-gte                                     FROMISOFORMAT                      Filter by min timestamp.              │
│                                                                                       [default: None]                       │
│ --min-price                                        INTEGER RANGE [x>=0]               Minimum price to filter by. Use '0'   │
│                                                                                       to not filter.                        │
│                                                                                       [default: 0]                          │
│ --max-price                                        INTEGER RANGE [x>=0]               Maximum price to filter by. Use '0'   │
│                                                                                       to not filter.                        │
│                                                                                       [default: 0]                          │
│ --include-unknown        --no-include-unknown                                         Include products with unknown prices. │
│                                                                                       [default: include-unknown]            │
│ --include-ambiguous      --no-include-ambiguous                                       Include products with ambiguous       │
│                                                                                       prices.                               │
│                                                                                       [default: include-ambiguous]          │
│ --include-multiple       --no-include-multiple                                        Include products with multiple prices │
│                                                                                       found in description.                 │
│                                                                                       [default: include-multiple]           │
│ --include-booked         --no-include-booked                                          Include products marked as booked.    │
│                                                                                       [default: include-booked]             │
│ --include-sold           --no-include-sold                                            Include products marked as sold.      │
│                                                                                       [default: include-sold]               │
│ --sort-by                                          [price|page]                       Sort products by price or page.       │
│                                                                                       [default: price]                      │
│ --sort-order                                       [asc|desc]                         Sort products in ascending or         │
│                                                                                       descending order.                     │
│                                                                                       [default: asc]                        │
│ --template                                         [list|table|dataclasses|json|csv]  Choose a template for printing found  │
│                                                                                       products and prices.                  │
│                                                                                       [default: table]                      │
│ --help                                                                                Show this message and exit.           │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```