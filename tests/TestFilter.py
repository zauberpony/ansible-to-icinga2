import unittest
from textwrap import dedent

from filter_plugins import to_icinga2


class ToIcinga2ExpressionTest(unittest.TestCase):
    def _p(self, t):
        return dedent(t).strip()

    def test_string_value(self):
        self.assertEqual("vars.os = \"Linux\"", to_icinga2.to_icinga2_expression(dict(os="Linux")))

    def test_multiple_values(self):
        expected = """
        vars.smtp = 1
        vars.os_family = "RedHat"
        vars.os = "Linux"
        """
        self.assertEqual(self._p(expected), to_icinga2.to_icinga2_expression(dict(os="Linux", os_family="RedHat", smtp=1)))

    def test_with_list(self):
        expected = """
        vars.notification["mail"] = {
            groups = [ "icingaadmins" ]
        }
        """

        self.assertEqual(self._p(expected), to_icinga2.to_icinga2_expression({
            "notification": {
                "mail": {
                    "groups": ["icingaadmins"]
                }
            }
        }))

    def test_empty_dict(self):
        expected = """
        vars.disks["disk"] = {

        }
        """
        self.assertEqual(self._p(expected), to_icinga2.to_icinga2_expression({
            "disks": {"disk": {}}
        }))

    def test_multiple_dicts(self):
        expected = """\
        vars.http_vhosts["Syncthing https redirect"] = {
            http_port = 8384
            http_expect = 302
        }
        vars.http_vhosts["Syncthing"] = {
            http_port = 8384
            http_expect = 401
            http_ssl = 1
        }
        """

        configuration = {
            "http_vhosts": {
                "Syncthing https redirect": {
                    "http_port": 8384,
                    "http_expect": 302
                },
                "Syncthing": {
                    "http_port": 8384,
                    "http_ssl": 1,
                    "http_expect": 401
                }
            }
        }

        self.assertEquals(self._p(expected), to_icinga2.to_icinga2_expression(configuration))

    def test_nested_dict(self):
        expected = dedent("""\
        vars.http_vhosts["Default page"] = {
            http_string = "the string"
            http_port = 8384
            http_uri = "/"
        }""")
        configuration = {
            "http_vhosts": {
                "Default page": {
                    "http_string": "the string",
                    "http_uri": "/",
                    "http_port": 8384
                }
            }
        }


        self.assertEqual(expected, to_icinga2.to_icinga2_expression(configuration))


if __name__ == '__main__':
    unittest.main()
