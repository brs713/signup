#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re


html_opener = """
<!DOCTYPE html>
<html>
    <head>
            <style>
                .error {
                    color: red;
                }
            </style>
        </head>
        <body>
        <h1>Signup</h1>
"""

form_open_html = """
    <form method="post">
        <table><tbody>
"""

row = """
    <tr>
        <td><label for="{0}">{1}</label></td>
        <td>
            <input name="{0}" value="{2}" type="{3}">
            <span class="error">{4}</span>
        </td>
    </tr>
"""

form_close_html = """
        </tbody></table>
        <input type="submit">
    </form>
"""


html_closer = """
</body>
</html>
"""


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PWD_RE = re.compile("^.{3,20}$")
def valid_password(password):
    return PWD_RE.match(password)
                    
                    
EML_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return EML_RE.match(email)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        
        form_html = """
            <form method="post">
                <table>
                    <tbody><tr>
                        <td><label for="username">Username</label></td>
                        <td>
                            <input name="username" value="" required="" type="text">
                            <span class="error"></span>
                        </td>
                    </tr>
                    <tr>
                        <td><label for="password">Password</label></td>
                        <td>
                            <input name="password" required="" type="password">
                            <span class="error"></span>
                        </td>
                    </tr>
                    <tr>
                        <td><label for="verify">Verify Password</label></td>
                        <td>
                            <input name="verify" required="" type="password">
                            <span class="error"></span>
                        </td>
                    </tr>
                    <tr>
                        <td><label for="email">Email (optional)</label></td>
                        <td>
                            <input name="email" value="" type="email">
                            <span class="error"></span>
                        </td>
                    </tr>
                </tbody></table>
                <input type="submit">
            </form>
        """
                
        html = html_opener + form_html + html_closer
        self.response.write(html)
        
    def post(self):       
                
        usr = self.request.get("username")
        pwd = self.request.get("password")
        ver = self.request.get("verify")
        eml = self.request.get("email")

        user_error = "Need a valid user name." if (valid_username(usr) == None) else ""
    
        pwd_error = "That's a crappy password; I can't let you use that." if (valid_password(pwd) == None) else ""
        
        pwdver_error = "Check your typing.  &quot*****&quot isn't the same as &quot*****&quot." if (pwd != ver) else ""
        
        email_error = "No.   Just...   no." if (valid_email(eml) == None) else ""

        
        form_username = row.format("username", "Username", usr, "text", user_error)
        
        form_pwd1 = row.format("password", "Password", "", "password", pwd_error)

        form_pwd2 = row.format("verify", "Verify Password", "", "password", pwdver_error)
        
        form_email = row.format("email", "Email", eml, "email", email_error)
        
        
        form_html = form_username + form_pwd1 + form_pwd2 + form_email
        html = html_opener + form_open_html + form_html + form_close_html + html_closer
        if (user_error == "" and pwd_error == "" and pwdver_error == "" and email_error == ""):
            self.redirect('/welcome?username=' + usr)
        else:
            self.response.write(html)
            
            
class Welcome(webapp2.RequestHandler):
    def get(self):
        usr = self.request.get("username")
        html = """
            <h1>Hello, {0}!</h1>
        """.format(usr)
        self.response.write(html)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
