.. _installation:

Установка
=========

1. Установите `django-fias`::

        pip install django-fias

2. Добавьте `fias` и `django_select2` в ваш список `INSTALLED_APPS`.
3. Добавьте `url(r'^fias/', include('fias.urls', namespace='fias')),` в ваш urlpatterns
4. Любым доступным способом подключите к админке приложения, в котором будете использовать поле FiasAddress свежую версию jQuery::

    # например так:
    class ItemAdmin(admin.ModelAdmin):
        class Media:
            js = ['//ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.js']
    admin.site.register(Item, ItemAdmin)

5. Если вы желаете использовать отдельную БД под данные ФИАС, выполните следующее

* Создайте БД и подключите её к Джанго обычным способом
* Добавьте в ваш `settings.py` параметр::

        FIAS_DATABASE_ALIAS = 'fias'

где `fias` - имя БД

* Добавьте в список `DATABASE_ROUTERS`::

        fias.routers.FIASRouter

* Выполните::


        python manage.py migrate --database=fias

где `fias` - имя БД ФИАС

5. Выполните::

        python manage.py migrate

6. Выполните::

        python manage.py collectstatic

Настройка полнотекстового поиска
================================

**NOTE**: поддерживаются только 2 СУБД: PostgreSQL и MySQL.
**NOTE2**: для индексации базы в MySQL может потребоваться до 2-2.5ГБ свободного места во временном каталоге MySQL.
**NOTE3**: нет необходимости слишком часто пересоздавать поисковый индекс базы ФИАС. Это требуется делать только после обновления базы.

1. Установите:

* `Sphinx Search Engine <http://sphinxsearch.com>`_ Для Debian, Ubuntu, RHEL, Windows есть `пакеты <http://sphinxsearch.com/downloads/release/>`_


3. Сгенерируйте конфигурацию `sphinx`:

Если у вы уже используете `sphinx` в проекте, то вам нужен только конфиг индекса. Выполните::

    python manage.py fias_suggest --path=PATH > sphinx.conf

где `PATH` - путь до каталога с индексами sphinx.

Иначе выполните::

    python manage.py fias_suggest --path=PATH --full > sphinx.conf

чтобы получить полный конфиг sphinx.

Замените конфиг sphinx полученными настройками (для **Gentoo** это файл `/etc/sphinx/sphinx.conf`, для **Ubuntu**: `/etc/sphinxsearch/sphinx.conf`)

4. Псоле того, как данные **импортированы** и обновлены выполните::

    indexer -c /etc/sphinx/sphinx.conf --all

*NOTE*: для повторной переиндексации при запущенном Sphinx следует выполнять::

    indexer -c /etc/sphinx/sphinx.conf --all --rotate

5. Запустите sphinx::

    # для Gentoo
    /etc/init.d/searchd start
    # для Ubuntu
    /etc/init.d/sphinxsearch start

**NOTE** Если Sphinx работает на другом хосте или на другом порту, добавьте в `settings.py` словарь соответствующими параметрами::

    FIAS_SEARCHD_CONNECTION = {
        'host': '127.0.0.1',
        'port': 9306,
    }

Настройка весов
===============
Из-за особенностей организации БД ФИАС, сортировка результатов поиска происходит не так, как хотелось бы.
Поэтому, начиная с версии 0.4 добавлена возможность настроить веса типов адресных объектов по своему усмотрению.
Для этого в `settings.py` добавьте словарь `FIAS_SB_WEIGHTS` вида::

        FIAS_SB_WEIGHTS = {
            # СОКРАЩЕНИЕ: ВЕС
            'г': 128,
            'с': 100,
        }
        
где 
 * СОКРАЩЕНИЕ - сокращённое наименование вида объекта из таблицы SocrBase
 * ВЕС - число от 0 до 128
 
*NOTE*: по-умолчанию вес всех типов равен 64
*NOTE*: пример заполнения можно посмотреть в weights.py - там перечислены предустановленные веса.

Чтобы применить свои изменения, выполните::

        python manage.py fias --fill-weights
        
Кроме того изменить веса можно в панели администрирования Django.
Но помните, что эти изменения будут **перезаписаны** при следующем вызове упомянутой команды!
После внесения изменений обязательно нужно переиндексировать базу.

Выбор импортируемых таблиц
==========================

Таблицы SOCRBASE и ADDROBJ импортируются всегда. Таблицы NORMDOC, LANDMARK, HOUSEINT и HOUSE по-умолчанию не импортируются.

Добавьте в ваш `settings.py` список названий таблиц, которые вы хотели бы импортировать::

    FIAS_TABLES = ('normdoc', 'landmark', 'houseint', 'house')
