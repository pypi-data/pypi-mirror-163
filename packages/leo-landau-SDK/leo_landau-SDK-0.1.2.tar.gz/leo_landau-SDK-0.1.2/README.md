# leo_landau-SDK
Python SDK for the-one-api

The One API to rule them all: https://the-one-api.dev/

### API access

To access The One API, we need an account.

Sign up here: 
https://the-one-api.dev/sign-up

Then login to get your access token: 
https://the-one-api.dev/login

Include the access_token as an environment variable. In the `main.py` file we give an example of how to load the access_token from a `.env` file. The format is shown in `.env.example`. Just paste in the access_token into "my_access_token" and rename the file to .env. Or include the access_token in your project in any other way you see fit.

### SDK Usage

- Install the SDK. e.g. `pip install leo-landau-SDK` (🤞)
- Import the SDK files. e.g. `from leo_landau_SDK.api_request import ApiRequest` and `from leo_landau_SDK.movie import Movie`
- Create an `ApiRequest`, specifying the desired result object type and the access_token
- (optionally) add filters, limits, pagination or sort_by to the `ApiRequest` the available features are included as methods to the `ApiRequest` object and are further documented in the [api docs]("https://the-one-api.dev/documentation").
- If you are using a method that requires an object_id, call the `ApiRequest.get(obj_id)` method. If you are calling a method that returns a list of objects, call the `ApiRequest.get_all()` method. These both return an instance of the `ApiResult` class.
- If the call to the API was successful, the `ApiResult.docs` object will be populated with a list of objects of the expected type -- the type passed into the `ApiRequest`.


A simple sample workflow is found in the `main.py` file like:
```
    # access token is in .env file
    access_token = os.environ.get("ACCESS_TOKEN")
    api_request = ApiRequest(Movie, access_token)
    api_request.filter("academyAwardWins>5")
    api_result = api_request.get_all()
    for movie in api_result.docs:
        print(vars(movie))
```

- Additional examples of the SDK usage can be found in the files in the 'test' dir.

### SDK development

Project development using Python 3.8.

Keeping track of the project Python dependencies in `requirements.txt` via:
`pip freeze > requirements.txt`

Keeping project in a `virtualenv`. Setup is something like:
```
cd {here}
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the tests:
```
python -m unittest discover -s src/test -p '*_test.py'
```