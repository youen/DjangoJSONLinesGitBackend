# DjangoJSONLinesGitBackend

A backend for the Django ORM that uses Git to persist data and serializes tables in JSONLines format.

## Prerequisites

- Python 3.6 or later
- Django 4.0 or later

## Installation

To install DjangoJSONLinesGitBackend, run the following command:

```console
pip install git+https://github.com/youen/DjangoJSONLinesGitBackend.git
```

## Configuration

To use the JSONLines Git backend, set ENGINE to 'JSONLinesGitBackend.read' or 'JSONLinesGitBackend.write' in your Django settings. The NAME setting should be set to the directory where the data will be stored.

### Settings.py

Here is an example of how to set up the 'default', 'json-git-read' and 'json-git' databases:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'json-git-read': {
        'ENGINE': 'DjangoJSONLinesGitBackend.read',
        'NAME': BASE_DIR / 'data',

    },

    'json-git': {
        'ENGINE': 'DjangoJSONLinesGitBackend.write',
        'NAME': BASE_DIR / 'data',

    }
}

# Database router
DATABASE_ROUTERS = ['myapp.routers.JsonGitDbRouter']
```

## Router

You will also need to set up a database router to route certain models to the JSONLines Git backend.

To route database read and write operations to the 'json-git-read' and 'json-git' databases for specific models, you can use a database router.

Here is an example of a router that routes database operations for models in the 'application' app to the 'json-git-read' and 'json-git' databases:

```python
class JsonGitDbRouter:
    """
    A router to control all database operations on models in the 'application' app.
    """
    route_app_labels = {'application'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read models from the 'application' app go to the 'json-git-read' database.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'json-git-read'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write models from the 'application' app go to the 'json-git' database.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'json-git'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the 'application' app is involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None
```

## UUID Primary Keys

In order to properly store and retrieve data from JSONLines files, it is important to use UUID fields as primary keys for your models. This ensures that the primary keys will remain unique and consistent across exports and imports of the database. To specify a UUID field as the primary key for a model, use the following code:

```python
import uuid

class MyModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
```

## Migration

To apply migrations to the 'json-git' database for the 'application' app, run the following command:

```console
$ python manage.py migrate --database json-git application
Operations to perform:
  Apply all migrations: application
Running migrations:
  Applying application.0001_initial... OK
```

This will apply any pending migrations to the 'json-git' database for the models in the 'application' app.

## Contribution

We welcome contributions to this project. If you have an idea for how to improve the project, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
