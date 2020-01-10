def pytest_addoption(parser):
    parser.addoption("--centralinfo", action="store", default="input_file.json")
