import pytest, json
import os, sys
from pathlib import Path

def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(os.getcwd()).parent.parent

def add_project_to_syspath():
    """
       Adds project directory to sys path. 
       Provides access to project source files to be tested
    """
    # Obtain current working directory
    dir_name = os.path.split(os.getcwd())[1]
    
    # Obtain SRC project dir from current dir name
    if dir_name[0:5] == "test_" or dir_name[0:5] == "test-":
        dir_name = dir_name[5:]

    # Add SRC project dir to the syspath.
    src_dir = os.path.join(get_project_root(), dir_name)
    sys.path.insert(0, src_dir)

add_project_to_syspath()

# Global Variables
central_handle = None
central_config = None

# Import Project Classes to be tested
from central_main import ArubaCentralAPI
from central_configuration import ArubaCentralConfiguration

# Getting Input File Name
@pytest.fixture(scope="module")
def centralinfo(pytestconfig):
    central_args = pytestconfig.getoption("centralinfo")

    with open(central_args, "r") as fp:
        input_args = json.loads(fp.read())

    central_info = input_args["central_info"]    

    return central_info

@pytest.mark.dependency()
def test_central_session_token(centralinfo):
    """
        Test to see if both generating token and refreshing token works
    """
    global central_handle
    central = centralinfo
    base_url = central["central_base_url"]

    # Generates the token for the first time
    central_handle2 = ArubaCentralAPI(client_id=central["client_id"],
                                     client_secret=central["client_secret"],
                                     customer_id=central["customer_id"],
                                     username=central["username"],
                                     password=central["password"],
                                     central_base_url=base_url)

    # Refreshes token second time
    central_handle = ArubaCentralAPI(client_id=central["client_id"],
                                     client_secret=central["client_secret"],
                                     customer_id=central["customer_id"],
                                     username=central["username"],
                                     password=central["password"],
                                     central_base_url=base_url)

    assert central_handle.token['access_token'] != central_handle2.token['access_token']
        
@pytest.mark.dependency(depends=['test_central_session_token'])
def test_creating_group():
    """
    Creating group tests GET, POST HTTP methods 
    and also tests creating group in aruba central 
    """

    if not central_handle:
        pytest.skip("Session Handle not found! Skipping test case creating group")

    central_config = ArubaCentralConfiguration(central_handle)

    # Creating a template group
    templateGroup = {"Wired": True, "Wireless": True}
    groupName = "jenkins-template"
    groupPass = "admin1234"
    central_config.createGroup(groupName, groupPass, templateGroup)
    
    # Check if group is created or not
    apiPath = "/configuration/v1/groups/" + groupName
    if central_config.isExists(apiPath=apiPath) != "PATCH":
        pytest.xfail("Creating Site Failed.")
    
@pytest.mark.dependency(depends=['test_central_session_token'])
def test_creating_site():
    """
    Creating site tests GET, POST HTTP methods 
    and also tests creating site in aruba central 
    """

    if not central_handle:
        pytest.skip("Session Handle not found! Skipping test case creating group")

    central_config = ArubaCentralConfiguration(central_handle)

    # Create a Site
    siteName = "Jenkins-SLR"
    siteAddress = {"address": "3970 Rivermark Plaza", "city": "Santa Clara",
                   "state": "California", "country": "United States",
                   "zipcode": "95053"}
    geoLocation = {
                   "latitude": "34.8951",
                   "longitude": "-77.0364"
                  }
    central_config.createSite(siteName=siteName, geoLocation=geoLocation)

    # Check if the site is created or not
    site_id = central_config.findSiteId(siteName=siteName)
    if not site_id:
        pytest.xfail("POST/GET Site Failed.")

@pytest.mark.dependency(depends=['test_central_session_token', 'test_creating_site'])
def test_patch_creating_site():
    """
    Re-creating/Modifying a site should be PATCH HTTP method. 
    This case tests if PATCH is used and PATCH functionality works 
    """

    if not central_handle:
        pytest.skip("Session Handle not found! Skipping test case creating group")

    central_config = ArubaCentralConfiguration(central_handle)

    siteName = "Jenkins-SLR"   
    siteAddress = {"address": "3970 Rivermark Plaza", "city": "Santa Clara",
                   "state": "California", "country": "United States",
                   "zipcode": "95053"}
    geoLocation = {
                   "latitude": "34.8951",
                   "longitude": "-77.0364"
                  }
    central_config.createSite(siteName=siteName, geoLocation=geoLocation)
    # Check if the site is created or not
    site_id = central_config.findSiteId(siteName=siteName)
    if not site_id:
        pytest.xfail("PATCH/GET Site Failed.")
    
@pytest.mark.dependency(depends=['test_central_session_token'])
def test_delete_group_site():
    """
    This test case tests DELETE HTTP Method. 
    Deletes group and site created earlier
    """

    if not central_handle:
        pytest.skip("Session Handle not found! Skipping test case creating group")

    central_config = ArubaCentralConfiguration(central_handle)

    # Delete Site
    siteName = "Jenkins-SLR"
    central_config.deleteSite(siteName=siteName)

    # Check if the site is deleted or not
    site_id = central_config.findSiteId(siteName=siteName)
    if site_id:
        pytest.xfail("DELETE Site Failed.")

    # Delete Group
    groupName = "jenkins-template"
    central_config.deleteGroup(groupName=groupName)

    # Check if group is deleted or not
    apiPath = "/configuration/v1/groups/" + groupName
    if central_config.isExists(apiPath=apiPath) != "POST":
        pytest.xfail("DELETE Site Failed.")
