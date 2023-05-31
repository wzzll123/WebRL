# read in the Python script from a file
import os
import pickle
import re

from exp import make_website

with open('web2url_exp.pkl', 'rb') as f:
    web2url = pickle.load(f)

# set up the Java code template for each test class
java_template = """package resources.{package};

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import java.util.concurrent.TimeUnit;

public class Test{test_num} {{
    WebDriver driver;
    private StringBuffer verificationErrors = new StringBuffer();
    private boolean acceptNextAlert = true;

    @Before
    public void setUp() {{
        System.setProperty("webdriver.chrome.driver", "/Users/wzz/Desktop/chromedriver");
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless");
        options.addArguments("--force-device-scale-factor=1");
        driver = new ChromeDriver(options);
        driver.manage().timeouts().implicitlyWait(1, TimeUnit.SECONDS);
        driver.get("{url}");
    }}

    {test_methods}

    public WebDriver getDriver() {{
        return this.driver;
    }}

    @After
    public void tearDown() {{
        driver.quit();
    }}
}}\n"""


def converter(script_name, url, package):
    with open(script_name, 'r') as f:
        script_text = f.read()
    test_names = []
    # split the script into individual test steps
    test_steps = script_text.split('\n')

    # iterate over the test steps and generate a Java test class for each one
    test_classes = []
    j = 0
    for i, test_step in enumerate(test_steps):
        # if 'driver.get' in test_step:
        #     url_regex = r'driver.get\("(.+?)"\)'
        #     match = re.search(url_regex, test_step)
        #     url = match.group(1)
        # skip non test lines
        if not ('el = driver.find_element_by' in test_step):
            continue
        j += 1

        attr_dict = {
            "xpath": {
                "python_regex": r'el = driver.find_element_by_xpath\("(.+?)"\)',
                "java_template": 'driver.findElement(By.xpath("{}")).click();'
            },
            "id": {
                "python_regex": r'el = driver.find_element_by_id\("(.+?)"\)',
                "java_template": 'driver.findElement(By.id("{}")).click();'
            },
            "name": {
                "python_regex": r'el = driver.find_element_by_name\("(.+?)"\)',
                "java_template": 'driver.findElement(By.name("{}")).click();'
            },
            "link_text": {
                "python_regex": r'el = driver.find_element_by_link_text\("(.+?)"\)',
                "java_template": 'driver.findElement(By.linkText("{}")).click();'
            }
        }
        for attr in attr_dict:
            match = re.search(attr_dict[attr]["python_regex"], test_step)
            if match is not None:
                attr_value = match.group(1)
                java_test_step = attr_dict[attr]['java_template'].format(attr_value)
                break
        # match = re.search(xpath_regex, test_step)
        # xpath = match.group(1)
        # java_test_step = 'driver.findElement(By.xpath("{}")).click();'.format(xpath)
        # set up the Java code for the test method corresponding to this test step
        test_method_name = f"test_step_{j}"
        test_method_code = f"""@Test
    public void {test_method_name}() throws Exception {{
        {java_test_step}
    }}"""

        # generate the Java code for the test class
        test_class_code = java_template.format(package=package, test_num=j, url=url, test_methods=test_method_code)
        test_names.append(f"Test{j}")

        # write out the Java test classes to individual files
        with open(f"Test{j}.java", "w") as f:
            f.write(test_class_code)
    return test_names

for web in web2url:
    old_url = web2url[web]['old_url']
    new_url = web2url[web]['new_url']
    old_package_name = f'{web}SimiloOld'
    new_package_name = f'{web}SimiloNew'
    print(f'put("{web}Similo", new String[]{{', end='')
    os.mkdir(old_package_name)
    os.mkdir(new_package_name)
    os.chdir(old_package_name)
    test_names = converter(f'/Users/wzz/Desktop/Research/scriptRepair/WebRL/webTestScript/{web}_similo.py', old_url,
                           old_package_name)
    for test_name in test_names:
        print(f'"{test_name}",', end='')
    print('});')
    os.chdir(f'../{new_package_name}')
    converter(f'/Users/wzz/Desktop/Research/scriptRepair/WebRL/webTestScript/{web}_similo.py', new_url,
              new_package_name)
    os.chdir('..')
