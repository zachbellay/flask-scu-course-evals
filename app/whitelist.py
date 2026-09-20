import os


class Whitelist:
    def __init__(self, app, whitelist_txt_abs_path):

        self.whitelist = set()

        if not os.path.exists(whitelist_txt_abs_path):
            return

        with open(whitelist_txt_abs_path) as f:
            for email in f:
                email = email.strip()
                self.whitelist.add(email)
