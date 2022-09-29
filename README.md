# VCF Manipulator

VCF Manipulator is an online REST API that allows the easier editing of Variant Call Format (VCF) files.

## Installation

Installation is fairly straightforward and can be completed in a few steps.

Steps:

0. (Optional)
    * Create a local directory for the project files
    * Inside this directory create a virtual environment using `virtualenv virtualenv`.
    * Activate your virtual environment using `source ./virtualenv/bin/activate`.
1. Clone this repo on your local working environment.
2. Install required packages with `pip install -r requirements.txt`.
3. Run migrations using `python manage.py migrate`.
4. Copy `.env.example` to `.env`.
5. Make sure to change the values of the environment variables, especially the value of the working VCF file.
6. Run `python manage.py runserver` to start the application
7. You can access the API on http://localhost:8000/api. Use the documentation below to work with your VCF file.



## API

All API calls fall under the /api/ prefix. All requests are parsed using JSON and can be rendered as JSON or XML responses. All other types are not allowed.

**GET /data/list**

Returns a paginated set of results from the selected VCF file.

Arguments:
- (optional) **id**: String with prefix *rs* followed by an integer, eg *rs1000*. 
Defines the id of the data row in the VCF File. 
- (optional) **page**: Integer, eg *2*. Defines the number of the page for the paginated results.
- (optional) **page_size**: Integer, eg *20*. Defaults to *100*. Defines the total number of paginated results per page. 

*Example Request*

```bash
$ curl GET http://localhost:8000/api/data/list?id=rs1000&page_size=100 \
    -H 'Accept: application/json' \
    -H 'Accept-Encoding: gzip, deflate' \
    -H 'Cache-Control: no-cache' \
    -H 'Connection: keep-alive' \
    -H 'Referer: http://localhost:8000/api/data?id=rs1' \
    -H 'cache-control: no-cache'
```

*Example Response*

```bash
{
    "count": 1000,
    "next": "http://localhost:8000/api/data/list?id=rs1000&page=2&page_size=100",
    "previous": null,
    "results": [
        {
            "ID": "rs1000",
            "CHROM": "chr1",
            "POS": 1000,
            "ALT": "A",
            "REF": "G"
        },
        ...
    ]
}
```

**POST /data/row**

Creates a new row in the VCF file. Returns a **201 Created** status along with the validated row data.

*Example Request*

```bash
$ curl POST http://localhost:8000/api/data/row \
  -H 'Accept: application/json' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Authorization: secretkey' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -d '{
	"CHROM": "chr10", 
	"POS": 1000, 
	"ALT": "A", 
	"REF": "G",
	"ID": "rs1000"
}'
```

*Example Response*

```bash
{
    "ID": "rs1000",
    "CHROM": "chr10",
    "POS": 1000,
    "ALT": "A",
    "REF": "G"
}
```

**PUT /data/row**

Updates an existing row in the VCF file, identified by the request parameter *id*. 
Returns a **200 OK** status along with the validated row data.

Arguments:
- (required) **id**: String with prefix *rs* followed by an integer, eg *rs1000*. 
Defines the id of the data row in the VCF File. 

*Example Request*

```bash
$ curl PUT http://localhost:8000/api/data/row?id=rs1000 \
  -H 'Accept: application/json' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Authorization: secretkey' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -d '{
	"CHROM": "chr10", 
	"POS": 1000, 
	"ALT": "A", 
	"REF": "G",
	"ID": "rs1"
}'
```

*Example Response*

```bash
{
    "ID": "rs1000",
    "CHROM": "chr10",
    "POS": 1000,
    "ALT": "A",
    "REF": "G"
}
```

**DELETE /data/row**

Deletes an existing row in the VCF file, identified by the request parameter *id*. 
Returns a **204 No Content** status.

Arguments:
- (required) **id**: String with prefix *rs* followed by an integer, eg *rs1000*. 
Defines the id of the data row in the VCF File. 

*Example Request*

```bash
$ curl DELETE http://localhost:8000/api/data/row?id=rs1000 \
  -H 'Accept: application/json' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Authorization: secretkey' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' 
```

## Testing

Testing is being handled with *pytest*. All tests are stored in the *tests* directory and split among files per each Python class, eg `tests/test_services/test_some_service.py`.
To run all tests in the test suite, you can simply run 
```bash
$ pytest -q tests
```
in the root directory, or you can run each test class on its own, ie
```bash
$ pytest -q tests/test_services/test_some_service.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## License

[MIT](https://choosealicense.com/licenses/mit/)