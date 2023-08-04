from flask import Flask, render_template

from StorageBot import StorageBot

import threading


class App:
    def __init__(self):
        self.bot = StorageBot()

        self.webserver = Flask(
            __name__,
            template_folder='resources/templates/',
            static_folder='resources/static/'
        )

        self.register_routes()

        # Need to run both application concurrently
        webserver_thread = threading.Thread(target=self.webserver.run)
        bot_thread = threading.Thread(target=self.bot.run)

        webserver_thread.start()
        bot_thread.start()

        webserver_thread.join()
        bot_thread.join()

    def register_routes(self) -> None:
        self.webserver.add_url_rule('/', 'index', self.index)
        self.webserver.add_url_rule('/login', 'login', self.login)

    def login(self):
        pass

    def index(self):
        return render_template('index.html', variable="12345")


if __name__ == "__main__":
    app = App()




