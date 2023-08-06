from importlib import import_module
from inspect import getmembers
from inspect import isclass
from os import listdir
from os import path
from sys import modules

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2.exceptions import TemplateNotFound
from toml import load as toml_load


class BigApp(object):
    smtp = dict()
    structures = dict()
    model_classes = dict()

    _app = None
    _jinja_env = Environment()

    db = SQLAlchemy()
    sql_do = db.session

    def __init__(self, flask_app=None, app_config_file: str = None):
        if flask_app is not None:
            self.init_app(flask_app, app_config_file)

    def init_app(self, flask_app, app_config_file: str):
        if flask_app is None:
            raise ImportError("No app passed into the FlaskLaunchpad app")
        self._app = flask_app

        _file = app_config_file

        if app_config_file is None:
            _file = "app_config.toml"

        with self._app.app_context():
            if not path.isfile(f"{current_app.root_path}/{_file}"):
                raise ImportError("""Flask app has no valid config file, must be like app_config.toml and be in the root of the app.""")

            _config = toml_load(f"{current_app.root_path}/{_file}")

            if "smtp" in _config:
                _smtp = _config["smtp"]
                del _config["smtp"]

            current_app.config["SQLALCHEMY_BINDS"] = {}
            if "flask" in _config:
                if "static_folder" in _config['flask']:
                    current_app.static_folder = f"{current_app.root_path}/{_config['flask']['static_folder']}"
                    del _config["flask"]["static_folder"]

                if "template_folder" in _config['flask']:
                    current_app.template_folder = f"{current_app.root_path}/{_config['flask']['template_folder']}"
                    del _config["flask"]["template_folder"]

                for key, value in _config['flask'].items():
                    current_app.config[key.upper()] = value
                del _config["flask"]

            if "database" in _config:
                if "main" in _config["database"]:
                    if _config['database']['main']['type'] == "sqlite":
                        current_app.config[
                            "SQLALCHEMY_DATABASE_URI"
                        ] = f"sqlite:////{current_app.root_path}/{_config['database']['main']['database_name']}.sqlite"
                    else:
                        type_user_pass = f"{_config['database']['main']['type']}://{_config['database']['main']['username']}:{_config['database']['main']['password']}"
                        server_database = f"@{_config['database']['main']['server']}/{_config['database']['main']['database_name']}"
                        current_app.config["SQLALCHEMY_DATABASE_URI"] = type_user_pass + server_database
                    del _config["database"]["main"]

                for key, value in _config["database"].items():
                    if value["enabled"]:
                        if value["type"] == "sqlite":
                            database = f"sqlite:////{current_app.root_path}/{value['database_name']}.sqlite"
                            current_app.config["SQLALCHEMY_BINDS"].update({key: database})
                        else:
                            type_user_pass = f"{value['type']}://{value['username']}:{value['password']}"
                            server_database = f"@{value['server']}/{value['database_name']}"
                            current_app.config["SQLALCHEMY_BINDS"].update({key: type_user_pass + server_database})
                del _config["database"]

    def import_builtins(self, folder: str = "routes") -> None:
        from .utilities import contains_illegal_chars

        with self._app.app_context():
            routes_raw, routes_clean = listdir(f"{current_app.root_path}/{folder}"), []
            for route in routes_raw:
                if contains_illegal_chars(route, exception=[".py"]):
                    continue
                routes_clean.append(route.replace(".py", ""))

            for route in routes_clean:
                try:
                    import_module(f"{current_app.name}.{folder.replace('/', '.')}.{route}")
                except ImportError as e:
                    print("Error importing builtin: ", e, f"in {folder}/{route}")
                    continue

    def import_blueprints(self, folder: str) -> None:
        from .utilities import contains_illegal_chars

        with self._app.app_context():
            blueprints_raw, blueprints_clean = listdir(f"{current_app.root_path}/{folder}/"), []
            for blueprint in blueprints_raw:
                _path = f"{current_app.root_path}/{folder}/{blueprint}"
                if path.isdir(_path):
                    if not contains_illegal_chars(blueprint):
                        blueprints_clean.append(blueprint)

            for blueprint in blueprints_clean:
                _bp_root_folder = f"{current_app.root_path}/{folder}/{blueprint}"

                try:
                    blueprint_module = import_module(f"{current_app.name}.{folder.replace('/', '.')}.{blueprint}")
                    blueprint_object = getattr(blueprint_module, "bp")
                    if blueprint_object.enabled:
                        current_app.register_blueprint(blueprint_object)
                except AttributeError as e:
                    print("Error importing blueprint: ", e, f" from {_bp_root_folder}")
                    continue

    def import_models(self, file: str = None, folder: str = None) -> None:
        from .utilities import contains_illegal_chars

        if file is None and folder is None:
            raise ImportError("You must pass in a file or folder located at the root of the app.")

        with self._app.app_context():
            if folder is not None:
                _folder = f"{current_app.root_path}/{folder}"
                if path.isdir(_folder):
                    folder_models_raw, folder_modules_clean = listdir(_folder), []
                    for model in folder_models_raw:
                        if contains_illegal_chars(model, exception=[".py"]):
                            continue
                        folder_modules_clean.append(model.replace(".py", ""))

                    for folder_model in folder_modules_clean:
                        split_folder = _folder.split("/")
                        strip_folder = split_folder[split_folder.index(current_app.name):]
                        folder_import_path = f"{'.'.join(strip_folder)}.{folder_model}"
                        try:
                            _folder_model_module = import_module(folder_import_path)
                            _folder_model_object = getattr(_folder_model_module, "db")

                        except ImportError as e:
                            print("Error importing model: ", e, f" from {folder_import_path}")
                            continue
                        except AttributeError as e:
                            print("Error importing model: ", e, f" from {folder_import_path}")
                            continue

                        folder_model_members = getmembers(modules[folder_import_path], isclass)
                        for folder_member in folder_model_members:
                            class_name = folder_member[0]
                            class_object = folder_member[1]
                            if current_app.name in str(class_object):
                                self.model_classes.update({class_name: class_object})
                else:
                    print("Folder not found: ", f"{current_app.root_path}/{folder}")

            if file is not None:
                _file = f"{current_app.root_path}/{file}"
                if path.isfile(_file):
                    split_file = _file.split("/")
                    strip_file = split_file[split_file.index(current_app.name):]
                    file_import_path = f"{'.'.join(strip_file)}.{file}"
                    try:
                        _file_model_module = import_module(file_import_path)
                        _file_model_object = getattr(_file_model_module, "db")

                    except ImportError as e:
                        print("Error importing model: ", e, f" from {file_import_path}")
                    except AttributeError as e:
                        print("Error importing model: ", e, f" from {file_import_path}")

                    file_model_members = getmembers(modules[file_import_path], isclass)
                    for file_member in file_model_members:
                        class_name = file_member[0]
                        class_object = file_member[1]
                        if current_app.name in str(class_object):
                            self.model_classes.update({class_name: class_object})

                else:
                    print("File not found: ", f"{current_app.root_path}/{file}")

            self.db.init_app(current_app)

    def smtp_settings(self, email_address: str):
        if email_address in self.smtp:
            return self.smtp[email_address]

    def model_class(self, class_name: str):
        return self.model_classes[class_name]

    def create_all_models(self):
        SQLAlchemy.create_all(self.db)

    def import_structures(self, structures_folder: str) -> None:
        from flask import send_from_directory, abort

        with self._app.app_context():
            if not path.isdir(f"{current_app.root_path}/{structures_folder}"):
                raise NotADirectoryError(f"{current_app.root_path}/{structures_folder} was not found")

            current_app.jinja_loader.searchpath.append(f"{current_app.root_path}/{structures_folder}")

            @current_app.route("/<structure>/static/<folder>/<file>", endpoint="__static", methods=["GET"])
            def structure_static(structure, folder, file):
                if path.isdir(f"{current_app.root_path}/{structures_folder}/{structure}/static/"):
                    if folder == "root":
                        return send_from_directory(f"{current_app.root_path}/{structures_folder}/{structure}/static/", f"{file}")
                    return send_from_directory(f"{current_app.root_path}/{structures_folder}/{structure}/static/{folder}/", f"{file}")
                return abort(404)

    def from_folder(self, file: str, structure: str, folder: str = None):
        if folder is None:
            return f"{structure}/templates/{file}"
        return f"{structure}/templates/{folder}/{file}"

    def extend(self, structure: str, file: str):
        return f"{structure}/templates/extends/{file}"

    def include(self, structure: str, file: str):
        return f"{structure}/templates/includes/{file}"

    def errors(self, structure: str, file: str):
        return f"{structure}/templates/errors/{file}"

    def render(self, structure: str, file: str):
        return f"{structure}/templates/renders/{file}"
