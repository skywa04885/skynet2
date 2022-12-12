import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

ABOUT_TITLE = 'SkyNet Log Viewer Info'
ABOUT_AUTHORS = ['Luke A.C.A. Rieff (Skywa04885)']
ABOUT_DOCUMENTERS = ['Luke A.C.A. Rieff (Skywa04885)']
ABOUT_COMMENTS = 'Simple program for viewing the logs of Skynet.'
ABOUT_PROGRAM_NAME = 'SkyNet Log Viewer'
ABOUT_COPYRIGHT = 'Copyright 2022 Luke A.C.A. Rieff (Skywa04885)'
ABOUT_VERSION = '1.0'
ABOUT_WEBSITE = 'https://pornhub.com/'
ABOUT_WEBSITE_LABEL = 'Website (Do not click)'
ABOUT_LICENSE_TYPE = Gtk.License.APACHE_2_0
ABOUT_LICENSE = '''Copyright 2022 Luke A.C.A. Rieff

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.'''


class AboutDialog(Gtk.AboutDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_title(ABOUT_TITLE)
        self.set_authors(ABOUT_AUTHORS)
        self.set_documenters(ABOUT_DOCUMENTERS)
        self.set_comments(ABOUT_COMMENTS)
        self.set_program_name(ABOUT_PROGRAM_NAME)
        self.set_copyright(ABOUT_COPYRIGHT)
        self.set_version(ABOUT_VERSION)
        self.set_website(ABOUT_WEBSITE)
        self.set_website_label(ABOUT_WEBSITE_LABEL)
        self.set_license_type(ABOUT_LICENSE_TYPE)
        self.set_license(ABOUT_LICENSE)
