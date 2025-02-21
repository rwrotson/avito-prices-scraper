# Avito Prices Scraper

Web scraper app for getting and parsing prices of products from [Avito.ru](https://avito.ru)

## Supports  🚀
✅ **Extract product prices & status** (`SOLD` / `BOOKED` / etc.) directly from ads  

✅ **Flexible search options**:  
    - Search by keywords or use a `JSON` / `YAML` config file  
    - Extract prices from multi-product ad descriptions  

✅ **Powerful filtering & sorting** by **price** and **status**  

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

For **minimal version** without `MongoDB` support:
```bash
uv pip install .
```
For **full version** with `MongoDB` support:
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

*You can configure the app by modifying `{version}.compose.yml` file, especially `command` instructions of `parser` service and also by providing different requests in`request-entries` directory.*
  
Also you can use `docker build` and `docker run` commands to build and run the app with custom provided params for more specific cases.

## Usage  🚀

There are three CLI subcommands: `search-on-avito`, `search-on-avito-from-file`, `search-in-db`.
  
All of them are well-documented, so you can get help by running `--help` option with the command.

```shell
~/ main !1 ❯ avito-prices-scraper --help                                                                  avito-prices-scraper
                                                                                                                               
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

### search-on-avito  🔎
```bash
~/ main !1 ❯ avito-prices-scraper search-on-avito --help                                                 avito-prices-scraper
                                                                                                                               
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

### search-on-avito-from-file 📄
```shell
~/ main !1 ❯ avito-prices-scraper search-on-avito-from-file --help                                        avito-prices-scraper
                                                                                                                               
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
### search-in-db  🛢️
```shell
~/ main !1 ❯ avito-prices-scraper search-in-db --help                                                     avito-prices-scraper
                                                                                                                               
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

### MongoExpress

You can also access the saved data in the `MongoDB` via the `MongoExpress` web interface. 
By default, it is available at `http://localhost:8081`.


## Examples  📚

### Search for products on Avito by provided parameters

```shell
~/ main !1 ❯ avito-prices-scraper search-on-avito "джеймс джойс дублинцы" \
                                  --title-queries "дублинцы" \
                                  --description-queries "дублинцы" \
                                  --max-pages 1 \
                                  --min-price 50 \
                                  --max-price 2000 \
                                  --sort-by price 
                                  --sort-order desc \
                                  --template table \
                                  --no-save-to-db
                                  --debug
Creating browser interface...
  Using undetected-chrome webdriver...
  Adding options...
  Options added:     --headless
                     --no-sandbox
                     --window-size=1920,1080
                     --disable-gpu
                     --disable-dev-shm-usage
                     --user-data-dir=/var/folders/wp/27mq51wx25b8l5g3hg1h73t40000gn/T/tmpfh0mvuxa
  Adding user agent...
  User agent added:  --browsers=['Chrome']
                     --os=['Linux']
                     --platforms=['desktop']
  Creating driver...
  Driver created: chrome
  Window size set to 1920x1080

Browser interface created!

Searching for <джеймс джойс дублинцы> on Avito...
Pages: 1... MAX!

Found 28 products: ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃    ┃                                                                                              ┃ Price  ┃              ┃       ┃                           ┃           ┃
┃    ┃                                                                                              ┃ from   ┃ Prices from  ┃       ┃                           ┃           ┃
┃  № ┃ Title                                                                                        ┃ title  ┃ description  ┃ Price ┃ Statuses from description ┃ Status    ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│  1 │ ✔ Джеймс Джойс Дублинцы. Портрет художника в юности в Санкт-Петербурге                       │ 2000   │              │ 2000  │                           │ OK        │
│    │ https://www.avito.ru/sankt-peterburg/knigi_i_zhurnaly/dzheyms_dzhoys_dublintsy._portret_hud… │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│  2 │ ✔ Дублинцы. Джойс в Москве                                                                   │ 2000   │              │ 2000  │                           │ OK        │
│    │ https://www.avito.ru/moskva/knigi_i_zhurnaly/dublintsy._dzhoys_714183358                     │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│  3 │ ✘ Витухновская, Уэлш, Селби и др в Москве                                                    │ 1075   │ 2000         │ 2000  │ OK                        │ OK        │
│    │ https://www.avito.ru/moskva/knigi_i_zhurnaly/vituhnovskaya_uelsh_selbi_i_dr_752585713        │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│  4 │ ✘ Редкие книги, комиксы, артбуки в Москве                                                    │ 650    │ 1900         │ 1900  │ OK                        │ OK        │
│    │ https://www.avito.ru/moskva/knigi_i_zhurnaly/redkie_knigi_komiksy_artbuki_3237801152         │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│  5 │ ✘ Новые книги, цены от в Москве                                                              │ 400    │ 1200         │ 1200  │ SOLD                      │ SOLD      │
│    │ https://www.avito.ru/moskva/knigi_i_zhurnaly/novye_knigi_tseny_ot_2391846083                 │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│  6 │ ✔ Джеймс Джойс. Дублинцы на французском языке в Нижнем Новгороде                             │ 950    │              │ 950   │                           │ OK        │
│    │ https://www.avito.ru/nizhniy_novgorod/knigi_i_zhurnaly/dzheyms_dzhoys._dublintsy_na_frantsu… │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│  7 │ ✔ Джеймс Джойс - Дублинцы в Кумертау                                                         │ 850    │              │ 850   │                           │ OK        │
│    │ https://www.avito.ru/kumertau/knigi_i_zhurnaly/dzheyms_dzhoys_-_dublintsy_4905937968         │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│  8 │ ✔ Джеймс Джойс. Дублинцы. Портрет художника в юности в Звенигороде                           │ 850    │              │ 850   │ NOT_FOUND                 │ OK        │
│    │ https://www.avito.ru/zvenigorod/knigi_i_zhurnaly/dzheyms_dzhoys._dublintsy._portret_hudozhn… │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│  9 │ ✔ Дублинцы. Портрет художника в юности в Москве                                              │ 812    │              │ 812   │                           │ OK        │
│    │ https://www.avito.ru/moskva/knigi_i_zhurnaly/dublintsy._portret_hudozhnika_v_yunosti_460430… │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│ 10 │ ✘ М.Уэльбек, Ф. О'Брайен, Ж. Перек в Санкт-Петербурге                                        │ 535    │ 660          │ 660   │ OK                        │ OK        │
│    │ https://www.avito.ru/sankt-peterburg/knigi_i_zhurnaly/m.uelbek_f._obrayen_zh._perek_6906681… │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│ 11 │ ✘ Ж. Перек, Д. Джойс, Д. Бойн в Санкт-Петербурге                                             │ 660    │ 660          │ 660   │ OK                        │ OK        │
│    │ https://www.avito.ru/sankt-peterburg/knigi_i_zhurnaly/zh._perek_d._dzhoys_d._boyn_687018285  │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│ 12 │ ✔ Джеймс Джойс Дублинцы Вагриус в Ярославле                                                  │ 600    │ 125          │ 600   │ OK, NOT_FOUND             │ AMBIGUOUS │
│    │ https://www.avito.ru/yaroslavl/knigi_i_zhurnaly/dzheyms_dzhoys_dublintsy_vagrius_4429200468  │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│ 13 │ ✘ Joyce James. Джойс Джеймс в Москве                                                         │ 1250   │ 588          │ 588   │ OK, NOT_FOUND             │ AMBIGUOUS │
│    │ https://www.avito.ru/moskva/knigi_i_zhurnaly/joyce_james._dzhoys_dzheyms_3832310176          │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│ 14 │ ✘ Книги разные в Москве                                                                      │ 50     │ 530          │ 530   │ OK                        │ OK        │
│    │ https://www.avito.ru/moskva/knigi_i_zhurnaly/knigi_raznye_1971159635                         │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│ 15 │ ✔ Dubliners. A Portrait of the Artist as a Young Man. Дублинцы. Портрет художника в юности в │ 530    │              │ 530   │ NOT_FOUND                 │ OK        │
│    │ Щелково                                                                                      │        │              │       │                           │           │
│    │ https://www.avito.ru/schelkovo/knigi_i_zhurnaly/dubliners._a_portrait_of_the_artist_as_a_yo… │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│ 16 │ ✔ Джеймс Джойс "Дублинцы" (на английском) в Москве                                           │ 500    │              │ 500   │                           │ OK        │
│    │ https://www.avito.ru/moskva/knigi_i_zhurnaly/dzheyms_dzhoys_dublintsy_na_angliyskom_3571840… │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│ 17 │ ✔ Джеймс Джойс Дублинцы (на английском языке) в Москве                                       │ 500    │              │ 500   │ NOT_FOUND                 │ OK        │
│    │ https://www.avito.ru/moskva/knigi_i_zhurnaly/dzheyms_dzhoys_dublintsy_na_angliyskom_yazyke_… │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│ 18 │ ✔ Джеймс Джойс "Дублинцы" (на английском) в Москве                                           │ 400    │              │ 400   │                           │ OK        │
│    │ https://www.avito.ru/moskva/knigi_i_zhurnaly/dzheyms_dzhoys_dublintsy_na_angliyskom_4786324… │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│ 19 │ ✘ Витгенштейн в Москве                                                                       │ 376    │ 350          │ 350   │ OK                        │ OK        │
│    │ https://www.avito.ru/moskva/knigi_i_zhurnaly/vitgenshteyn_4057334827                         │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│ 20 │ ✔ Джеймс Джойс Дублинцы на английском в Москве                                               │ 329    │              │ 329   │ NOT_FOUND                 │ OK        │
│    │ https://www.avito.ru/moskva/knigi_i_zhurnaly/dzheyms_dzhoys_dublintsy_na_angliyskom_4842262… │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│ 21 │ ✘ Книги в Ярославле                                                                          │ 220    │ 200          │ 200   │ OK                        │ OK        │
│    │ https://www.avito.ru/yaroslavl/knigi_i_zhurnaly/knigi_4057371697                             │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│ 22 │ ✔ Джеймс Джойс Дублинцы в Кумертау                                                           │ 200    │              │ 200   │                           │ OK        │
│    │ https://www.avito.ru/kumertau/knigi_i_zhurnaly/dzheyms_dzhoys_dublintsy_4553607380           │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│ 23 │ ✘ Просто книги в Дзержинске                                                                  │ 39     │ 190          │ 190   │ OK                        │ OK        │
│    │ https://www.avito.ru/dzerzhinsk/knigi_i_zhurnaly/prosto_knigi_4014677630                     │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│ 24 │ ✔ Джеймс Джойс Дублинцы в Казани                                                             │ 180    │              │ 180   │                           │ OK        │
│    │ https://www.avito.ru/kazan/knigi_i_zhurnaly/dzheyms_dzhoys_dublintsy_4582770669              │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│ 25 │ ✔ Джеймс Джойс Дублинцы в Мосрентген                                                         │ 150    │              │ 150   │                           │ OK        │
│    │ https://www.avito.ru/mosrentgen/knigi_i_zhurnaly/dzheyms_dzhoys_dublintsy_4874387756         │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│ 26 │ ✘ Книги в Москве                                                                             │ 100    │ 100          │ 100   │ OK                        │ OK        │
│    │ https://www.avito.ru/moskva/knigi_i_zhurnaly/knigi_2573916991                                │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│ 27 │ ✘ Книги в Курске                                                                             │ 50     │ 100          │ 100   │ OK                        │ OK        │
│    │ https://www.avito.ru/kursk/knigi_i_zhurnaly/knigi_4555282158                                 │        │              │       │                           │           │
├────┼──────────────────────────────────────────────────────────────────────────────────────────────┼────────┼──────────────┼───────┼───────────────────────────┼───────────┤
│ 28 │ ✘ Зарубежная литература в Москве                                                             │ 60     │ 100          │ 100   │ OK                        │ OK        │
│    │ https://www.avito.ru/moskva/knigi_i_zhurnaly/zarubezhnaya_literatura_1164966417              │        │              │       │                           │           │
└────┴──────────────────────────────────────────────────────────────────────────────────────────────┴────────┴──────────────┴───────┴───────────────────────────┴───────────┘
```

### Requesting several products in one command

```shell
~/ main !1 ❯ avito-prices-scraper search-on-avito "набоков бледный огонь" \
                                                  "бунин жизнь арсеньева" \
                                                  --template list

Searching for <набоков бледный огонь> on Avito...
Pages: 1... MAX!

Found 13 products: ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
1. 1938 руб.: Истинная жизнь Севастьяна Найта в Москве (https://www.avito.ru/moskva/knigi_i_zhurnaly/istinnaya_zhizn_sevastyana_nayta_4635577287)
2. 1920 руб.: Книга Трагедия господина Морна в Москве (https://www.avito.ru/moskva/knigi_i_zhurnaly/kniga_tragediya_gospodina_morna_4773949018)
3. 1500 руб.: Набоков «Бледный огонь» в Стерлитамаке (https://www.avito.ru/sterlitamak/knigi_i_zhurnaly/nabokov_blednyy_ogon_4685479984)
4. 630 руб.: Владимир Набоков Бледный огонь и Другие берега в Москве (https://www.avito.ru/moskva/knigi_i_zhurnaly/vladimir_nabokov_blednyy_ogon_i_drugie_berega_4810366182)
5. 610 руб.: Владимир Набоков: Бледный огонь в Санкт-Петербурге (https://www.avito.ru/sankt-peterburg/knigi_i_zhurnaly/vladimir_nabokov_blednyy_ogon_4001350457)
6. 600 руб.: Бледный огонь (Владимир Набоков) в Мурманске (https://www.avito.ru/murmansk/knigi_i_zhurnaly/blednyy_ogon_vladimir_nabokov_4279168542)
7. 600 руб.: Книги справочники в Казани (https://www.avito.ru/kazan/kollektsionirovanie/knigi_spravochniki_4197186236)
8. 599 руб.: Книги в ассортименте в Воронеже (https://www.avito.ru/voronezh/knigi_i_zhurnaly/knigi_v_assortimente_4558769949)
9. 500 руб.: Книги по психологии философии классика 23 шт в Краснодаре 
(https://www.avito.ru/krasnodar/knigi_i_zhurnaly/knigi_po_psihologii_filosofii_klassika_23_sht_4514907492)
10. 400 руб.: Новые книги в Майкопе (https://www.avito.ru/maykop/knigi_i_zhurnaly/novye_knigi_4605927252)
11. 370 руб.: Книги новые и б/у в Краснодаре (https://www.avito.ru/krasnodar/knigi_i_zhurnaly/knigi_novye_i_bu_4601628483)
12. 200 руб.: Книги сломленные ангелы, набоков, булгаков в Перми (https://www.avito.ru/perm/knigi_i_zhurnaly/knigi_slomlennye_angely_nabokov_bulgakov_4566709501)
13. 100 руб.: Книги Фрай,Ахматова, Рыжий,Рубина, Булгаков в Ярославле (https://www.avito.ru/yaroslavl/knigi_i_zhurnaly/knigi_frayahmatova_ryzhiyrubina_bulgakov_4795224902)

Searching for <бунин жизнь арсеньева> on Avito...
Pages: 1... MAX!

Found 33 products: ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
1. 2000 руб.: Собрание сочинений Бунина И.А в Москве (https://www.avito.ru/moskva/knigi_i_zhurnaly/sobranie_sochineniy_bunina_i.a_3489399209)
2. 1953 руб.: Бунин И. А. Избранные произведения. 1991 в Москве (https://www.avito.ru/moskva/knigi_i_zhurnaly/bunin_i._a._izbrannye_proizvedeniya._1991_4429618424)
3. 1940 руб.: Жизнь Арсеньева. Темные аллеи в Щелково (https://www.avito.ru/schelkovo/knigi_i_zhurnaly/zhizn_arseneva._temnye_allei_4081195994)
4. 900 руб.: Жизнь Арсеньева - Бунин в Екатеринбурге (https://www.avito.ru/ekaterinburg/knigi_i_zhurnaly/zhizn_arseneva_-_bunin_3676975934)
5. 890 руб.: Антоновские яблоки. Жизнь Арсеньева Бунин Иван Але в Санкт-Петербурге 
(https://www.avito.ru/sankt-peterburg/knigi_i_zhurnaly/antonovskie_yabloki._zhizn_arseneva_bunin_ivan_ale_4677240692)
6. 830 руб.: Библиотека всемирной литературы (отечеств. лит-ра) в Краснодаре 
(https://www.avito.ru/krasnodar/knigi_i_zhurnaly/biblioteka_vsemirnoy_literatury_otechestv._lit-ra_3537334383)
7. 750 руб.: И.Бунин Избранные сочинения в Волгограде (https://www.avito.ru/volgograd/knigi_i_zhurnaly/i.bunin_izbrannye_sochineniya_4469621334)
8. 550 руб.: Иван Бунин. Жизнь Арсеньева в Туле (https://www.avito.ru/tula/knigi_i_zhurnaly/ivan_bunin._zhizn_arseneva_4159995952)
9. 500 руб.: Искандер, Гафт, Рубина, Бунин, Залотуха, Чхартишви в Москве 
(https://www.avito.ru/moskva/knigi_i_zhurnaly/iskander_gaft_rubina_bunin_zalotuha_chhartishvi_2889145228)
10. 470 руб.: Иван бунин, жизнь Арсеньева, 1982 в Электростали (https://www.avito.ru/elektrostal/knigi_i_zhurnaly/ivan_bunin_zhizn_arseneva_1982_4478726662)
11. 450 руб.: Жизнь Арсеньева / Окаянные дни, Иван Бунин в Москве (https://www.avito.ru/moskva/knigi_i_zhurnaly/zhizn_arseneva_okayannye_dni_ivan_bunin_4364788882)
12. 450 руб.: Бунин Иван. Жизнь Арсеньева в Москве (https://www.avito.ru/moskva/knigi_i_zhurnaly/bunin_ivan._zhizn_arseneva_3836966073)
13. 350 руб.: Бунин Иван. Жизнь Арсеньева в Москве (https://www.avito.ru/moskva/knigi_i_zhurnaly/bunin_ivan._zhizn_arseneva_4230969460)
14. 336 руб.: Классики и современники 7 в Рязани (https://www.avito.ru/ryazan/knigi_i_zhurnaly/klassiki_i_sovremenniki_7_3736855114)
15. 300 руб.: Шишков Серкин Рерих Орлов Толстой в Москве (https://www.avito.ru/moskva/knigi_i_zhurnaly/shishkov_serkin_rerih_orlov_tolstoy_2377118711)
16. 300 руб.: Иван Бунин Жизнь Арсеньева. Стих-я в Москве (https://www.avito.ru/moskva/knigi_i_zhurnaly/ivan_bunin_zhizn_arseneva._stih-ya_3905210656)
17. 280 руб.: Книги Жизнь Арсеньева Бунин Иван Алексеевич в Москве (https://www.avito.ru/moskva/knigi_i_zhurnaly/knigi_zhizn_arseneva_bunin_ivan_alekseevich_2822287586)
18. 250 руб.: Бунин И. А. Жизнь Арсеньева в Москве (https://www.avito.ru/moskva/knigi_i_zhurnaly/bunin_i._a._zhizn_arseneva_4453325606)
19. 250 руб.: И. Бунин Жизнь Арсеньева. Рассказы в Тольятти (https://www.avito.ru/tolyatti/knigi_i_zhurnaly/i._bunin_zhizn_arseneva._rasskazy_2200299247)
20. 200 руб.: Книги в Москве (https://www.avito.ru/moskva/knigi_i_zhurnaly/knigi_4559360730)
21. 160 руб.: И. Бунин Жизнь Арсеньева 1996 в Москве (https://www.avito.ru/moskva/knigi_i_zhurnaly/i._bunin_zhizn_arseneva_1996_4525677916)
22. 160 руб.: Бунин Иван, "Жизнь Арсеньева, Суходол, рассказы" в Ростове-на-Дону 
(https://www.avito.ru/rostov-na-donu/knigi_i_zhurnaly/bunin_ivan_zhizn_arseneva_suhodol_rasskazy_2125281493)
23. 150 руб.: Бунин жизнь Арсеньева в Липецке (https://www.avito.ru/lipetsk/knigi_i_zhurnaly/bunin_zhizn_arseneva_4136055583)
24. 150 руб.: И. А. Бунин Жизнь Арсеньева в Самаре (https://www.avito.ru/samara/knigi_i_zhurnaly/i._a._bunin_zhizn_arseneva_4939905359)
25. 130 руб.: И. А бунин жизнь арсеньева советская россия 1982 в Дмитрове 
(https://www.avito.ru/dmitrov/knigi_i_zhurnaly/i._a_bunin_zhizn_arseneva_sovetskaya_rossiya_1982_4189601078)
26. 120 руб.: Бунин жизнь арсеньева в Ставрополе (https://www.avito.ru/stavropol/knigi_i_zhurnaly/bunin_zhizn_arseneva_4691246761)
27. 120 руб.: Книги в Сызрани (https://www.avito.ru/syzran/knigi_i_zhurnaly/knigi_3766774592)
28. 100 руб.: Книги разное в Москве (https://www.avito.ru/moskva/knigi_i_zhurnaly/knigi_raznoe_3760637250)
29. 100 руб.: И.Бунин жизнь Арсеньева в Туле (https://www.avito.ru/tula/knigi_i_zhurnaly/i.bunin_zhizn_arseneva_3157519415)
30. 100 руб.: Книги в Казани (https://www.avito.ru/kazan/knigi_i_zhurnaly/knigi_4646442358)
31. 77 руб.: И.А.Бунин суходол, жизнь арсеньева, рассказы в Самаре (https://www.avito.ru/samara/knigi_i_zhurnaly/i.a.bunin_suhodol_zhizn_arseneva_rasskazy_4328427570)
32. 50 руб.: Книги в Москве (https://www.avito.ru/moskva/knigi_i_zhurnaly/knigi_4503439161)
33. 50 руб.: Бунин 2 тома в Москве (https://www.avito.ru/moskva/knigi_i_zhurnaly/bunin_2_toma_4567667393)
```