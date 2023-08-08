import logging

from django.conf import settings
from django.db import connections, reset_queries

logger = logging.getLogger(__name__)


class PrintRawQueryMiddleware:
    """
    Middleware which prints out a list of all SQL queries done
    for each view that is processed.  This is only useful for debugging.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Return the response no matter what so we will do that
        """
        response = self.get_response(request)

        indentation = 2
        for conn_name in settings.DATABASES.keys():
            connection = connections[conn_name]
            if len(connection.queries) > 0 and settings.DEBUG:
                total_time = 0.0
                count =0
                for query in connection.queries:
                    nice_sql = query["sql"].replace('"', "").replace(",", ", ")
                    logger.info(
                        "\033[1;31m[TIME: {} seconds] - \033[1;32m['CONN': {}] \033[0m \033[1;31m[{}]\033[0m {}".format(
                            query["time"], conn_name, query["time"], nice_sql
                        )
                    )
                    total_time = total_time + float(query["time"])
                    count += 1
                logger.info("{}\033[1;32m[TOTAL TIME: {} seconds]\033[0m".format(" " * indentation, str(total_time)))
                logger.info(f"TOTAL COUNT OF DB CALLS: {count} counts")

        # finally return the response post all the required things are Done.
        return response


class PrintQueriesInTerminal:
    def __call__(self, *args, **kwargs):
        for conn_name in settings.DATABASES.keys():
            connection = connections[conn_name]
            if len(connection.queries) > 0 and settings.DEBUG:
                total_time = 0.0
                for query in connection.queries:
                    nice_sql = query["sql"].replace('"', "").replace(",", ", ")
                    print(
                        "\033[1;31m[TIME: {} seconds] - \033[1;32m['CONN': {}] \033[0m \033[1;31m[{}]\033[0m {}".format(
                            query["time"], conn_name, query["time"], nice_sql
                        )
                    )
                    total_time = total_time + float(query["time"])
                print("{}\033[1;32m[TOTAL TIME: {} seconds]\033[0m".format(" " * 2, str(total_time)))
        reset_queries()
