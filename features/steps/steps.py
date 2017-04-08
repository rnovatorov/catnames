import os
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys


@given(u'non authorized user')
def step_impl(context):
    pass


@given(u'authorized user "{username}"')
def step_impl(context, username):
    context.execute_steps(u'''
        When user proceeds to login page
         And user clicks login via vk oauth
         And user submits vk credentials
    ''')
    

@when(u'user proceeds to login page')
def step_impl(context):
    context.execute_steps(u'''
        When user visits Sovyak index page
         And user clicks login button
    ''')


@when(u'user clicks login button')
def step_impl(context):
    context.wait.until(lambda x: x.find_element_by_name("login"))
    elem = context.driver.find_element_by_name("login")
    # context.logger.info(elem.text)
    elem.click()

@when(u'user clicks login via vk oauth')
def step_impl(context):
    context.wait.until(lambda x: x.find_element_by_name("vk_oauth"))
    elem = context.driver.find_element_by_name("vk_oauth")
    # context.driver.get_screenshot_as_file(os.path.join(context.screenshot_dir, "foo.png"))
    elem.click()

@when(u'user submits vk credentials')
def step_impl(context):
    context.wait.until(lambda x: x.find_element_by_id("login_submit"))
    
    phone_input = context.driver.find_element_by_name("email")
    phone_input.clear()
    phone_input.send_keys(context.vk_test_user_credentials["phone"])
    
    pass_input = context.driver.find_element_by_name("pass")
    pass_input.clear()
    pass_input.send_keys(context.vk_test_user_credentials["password"])

    submit_input = context.driver.find_element_by_id("install_allow")
    submit_input.click()

    try:
        context.wait.until(lambda x: x.find_element_by_class_name("box_error"))
        box_error = context.driver.find_element_by_class_name("box_error")
        context.logger.error("Login failed: %s", box_error.text)
        raise Exception
    except TimeoutException:
        context.logger.info("Login succeed")


@when(u'user visits Sovyak index page')
def step_impl(context):
    context.driver.get(context.index_page)


@then(u'"{text}" is seen in "{tag_name}"')
def step_impl(context, text, tag_name):
    elem = context.driver.find_element_by_tag_name(tag_name)
    assert elem.text == text, "Text in '%s' must be '%s', not '%s'" % (tag_name, text, elem.text)
