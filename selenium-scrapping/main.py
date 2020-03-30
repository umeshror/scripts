import os
import smtplib
import textwrap
import time

from selenium import webdriver


class TestLogin():
    def __init__(self):
        # web url endpoint to test
        self.url = os.environ.get('LOGIN_URL')
        self.driver = self.get_driver()

    def get_driver(self):
        """
        Create instance of Chrome webdriver for given url
        :return: webdriver instance
        """
        driver = webdriver.Chrome(executable_path=os.environ.get('EXECUTABLE_PATH'))
        driver.get(self.url)
        return driver

    @property
    def current_url(self):
        """
        retruns current url of driver
        :return: URL <string>
        """
        return self.driver.current_url

    def test_login(self):
        """
        Test if login get successful with correct username anf password
        """
        username = self.driver.current_url
        username.send_keys(os.environ.get('USERNAME'))

        password = self.driver.find_element_by_name('password')
        password.send_keys(os.environ.get('PASSWORD'))

        start_time = time.time()
        password.submit()

        time_taken = time.process_time() - start_time

        self.close_driver()
        if time_taken > 120:
            if self.current_url != self.url:
                print('login was successful, but took {} seconds'.format(time_taken))
            else:
                print('login failed, took more {} seconds'.format(time_taken))
            return False
        return True

    def send_mail(self, to_email_id, content):
        """
        Sends email to about status of login report
        :param to_email_id: Reciever's mail id
        :param content: content of the mail
        """

        from_email = os.environ.get('FROM_EMAIL_ID')
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(from_email, os.environ.get('EMAIL_PWD'))

        email_txt = textwrap.dedent("""\
            From: %s
            To: %s
            Subject: %s
            %s
            """ % (from_email, ", ".join(to_email_id), "Login report", content))
        # Send the mail
        server = smtplib.SMTP(smtpserver)
        server.sendmail(from_email, to_email_id, email_txt)
        server.quit()

    def close_driver(self):
        """
        Closes active driver
        """
        self.driver.close()


if __name__ == "__main__":
    tl = TestLogin()
    tl.test_login()
