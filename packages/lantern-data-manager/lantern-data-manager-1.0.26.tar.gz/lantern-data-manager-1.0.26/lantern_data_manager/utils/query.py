from lantern_data_manager.utils.logger import logger

TYPE_FLOAT = "float"
TYPE_INT = "int"
TYPE_BOOL = "bool"
TYPE_STRING = "string"
TYPE_DURATION = "duration"
TYPE_TIME = "time"
TYPE_UINT = "uint"
TYPES = [
    TYPE_FLOAT, TYPE_INT, TYPE_BOOL,
    TYPE_STRING, TYPE_DURATION, TYPE_TIME,
    TYPE_UINT,
]


def make_query(bucket, start_range, device_ids, measurement=None, type=None,
               stop_range=None, field=None, fields=[], filters=None, groupers=None, first=None, last=None,
               functions=None, multiple_queries=False):
    """ Query InfluxDB using input parameters

    Arguments:
        bucket {str} -- bucket name to perform query
        start {str} -- flux start format string(-2d, -1m, -10w, etc)
        device_ids {List of str} -- device id (filter) to perform query

    Keyword Arguments:
        stop {str} -- flux stop format string(-2d, -1m, -10w, etc)
        measurement {str} -- '_measurement' value in influxdb (metric type) ex: watermeter
        field {str} -- '_field' value in influxdb (metric name), ex: counter, temperature, humidity, etc
        field [{str}} -- '_field' value in influxdb (metric name), ex: counter, temperature, humidity, etc (But a list)
        filters {list} -- List of {name: 'str', value: 'str'}, which is a list of filters to be added to query. 
        groupers {list} -- Which is the grouper to be used, with the form: {every: 'str', fn: 'str', type: 'str'(None)}, ex: {every: '10s', fn: 'sum', type: 'float'}, where type is optional and will cast data to that type.
        functions {list} -- List with objects to request a aggregate function from influx.
        multiple_queries {boolean} -- It indicates that the query is part of a multiple query.
    """

    query_str = ""

    def add_q(query_str, _str):
        return query_str + ' \n ' + _str

    # base bucket
    query_str = f'from(bucket: "{bucket}")'

    # ranges
    if not stop_range:
        query_str = add_q(query_str, "|> range(start: {})".format(start_range))
    else:
        query_str = add_q(query_str, "|> range(start: {}, stop: {})".format(start_range, stop_range))

    # device ids
    if device_ids and len(device_ids):
        _ff = '|> filter(fn: (r) =>'
        for idx, d_id in enumerate(device_ids):
            if idx != 0:
                _ff = _ff + " or" 
            _ff = _ff + ' r.device_id == "{value}"'.format(value=d_id)
        _ff = _ff + ')'
        query_str = add_q(query_str, _ff)

    # measurement
    if measurement:
        query_str = add_q(query_str, '|> filter(fn: (r) => r._measurement == "{}")'.format(measurement))

    # field
    if field:
        query_str = add_q(query_str, '|> filter(fn: (r) => r._field == "{}")'.format(field))

    # fields
    if fields and len(fields):
        conditions = ""
        for idx, field_name in enumerate(fields):
            op = " or " if idx > 0 else ""
            conditions = '{conditions} {op} r._field == "{val}"'.format(
                conditions=conditions, op=op, val=field_name
            )
        query_str = add_q(query_str, '|> filter(fn: (r) => {conditions})'.format(conditions=conditions))

    # functions
    if functions and len(functions):
        for fn in functions:
            str_function = '|> {}('.format(fn["name"])
            params = fn.get("params", None)
            if params:
                for key_param in params.keys():
                    str_function += '{}:"{}"'.format(key_param, params[key_param])
            str_function += ")"
            query_str = add_q(query_str, str_function)
        query_str = add_q(query_str, '|> duplicate(column: "{}", as: "{}")'.format("_stop", "_time"))


    # filters (OR, we have one or the other)
    if filters and len(filters):
        _ff = '|> filter(fn: (r) =>'
        for idx, f in enumerate(filters):
            if idx != 0:
                _ff = _ff + " or" 
            _ff = _ff + ' r.{name} == "{value}"'.format(name=f["name"], value=f["value"])
        _ff = _ff + ')'
        query_str = add_q(query_str, _ff)

    # casting global type if defined
    if type:
        query_str = add_q(query_str, _cast_type(type))

    if last and not first:
        query_str = add_q(query_str, "|> top(n: {}, columns: [\"_time\"])".format(last))
        query_str = add_q(query_str, "|> sort(columns:[\"_time\"], desc:false)".format(last))

    if first and not last:
        query_str = add_q(query_str, "|> bottom(n: {}, columns: [\"_time\"])".format(first))
        
    logger.debug("query_str: {}".format(query_str))
    # List of queries to execute
    list_query_str = []
    if not groupers:
        """ no groupers, so we add the original query 1 time """
        list_query_str.append(query_str)
    if groupers and len(groupers):
        """ We have groupers, so we add 1 query for each grouper """
        for g in groupers:
            _type = ""
            if "type" in g:
                _type = _cast_type(g["type"])
                g_q_str = ''' {q} \n {type} \n |> aggregateWindow(every: {every}, fn: {fn})'''.format(
                    type=_type, q=query_str, every=g["every"], fn=g["fn"]
                )

                if not multiple_queries:
                    g_q_str = f'{g_q_str} \n |> yield(name: "{g["fn"]}")'
                    
            list_query_str.append(g_q_str)
    logger.info("*** BEGİNNİNG *** queries to be executed")
    return list_query_str


def make_queries(bucket, start_range, device_ids, measurement=None, type=None,
               stop_range=None, field=None, fields=[], filters=None, groupers=None, first=None, last=None,
               functions=None, bucket_list=[], imports=[], extra_queries=[]):
    """ Query InfluxDB using input parameters

    Arguments:
        bucket {str} -- bucket name to perform query
        start {str} -- flux start format string(-2d, -1m, -10w, etc)
        device_ids {List of str} -- device id (filter) to perform query

    Keyword Arguments:
        stop {str} -- flux stop format string(-2d, -1m, -10w, etc)
        measurement {str} -- '_measurement' value in influxdb (metric type) ex: watermeter
        field {str} -- '_field' value in influxdb (metric name), ex: counter, temperature, humidity, etc
        field [{str}} -- '_field' value in influxdb (metric name), ex: counter, temperature, humidity, etc (But a list)
        filters {list} -- List of {name: 'str', value: 'str'}, which is a list of filters to be added to query. 
        groupers {list} -- Which is the grouper to be used, with the form: {every: 'str', fn: 'str', type: 'str'(None)}, ex: {every: '10s', fn: 'sum', type: 'float'}, where type is optional and will cast data to that type.
        functions {list} -- List with objects to request a aggregate function from influx.
        bucket_list {List of str} -- buckets name to perform query (create an union of the data)
        imports {List of str} -- imports needed in extra queries
        extra_queries {List of str with Flux structure} -- additional queries, Note: these queries will be added at the end of the general query
    """
    def add_queries(query_str, _list_str):
        for _str in _list_str:
            query_str += ' \n ' + _str
        return query_str

    if bucket_list and len(bucket_list) > 1:
        general_query = f"{add_queries('', imports)}" if imports else ''
        union_tables = []
        for index, bucket_name in enumerate(bucket_list):
            query_str = make_query(
                            bucket=bucket_name,
                            start_range=start_range,
                            device_ids=device_ids,
                            measurement=measurement,
                            type=type,
                            stop_range=stop_range,
                            field=field,
                            fields=fields,
                            filters=filters,
                            groupers=groupers,
                            first=first,
                            last=last,
                            functions=functions,
                            multiple_queries=True
                        )
            general_query = f'{general_query} \n table{index} = {query_str[0]}'
            general_query = f'{general_query} {add_queries("", extra_queries)}' if extra_queries else general_query
            general_query = f'{general_query} \n |> group()'
            union_tables.append(f"table{index}")

        
        general_query = general_query = f"{general_query} \n union(tables: {union_tables})"
        return [general_query]
    elif bucket_list:
        raise Exception("bucket_list needs to have at least 2 buckets")
    else: 
        query_str = make_query(
            bucket=bucket,
            start_range=start_range,
            device_ids=device_ids,
            measurement=measurement,
            type=type,
            stop_range=stop_range,
            field=field,
            fields=fields,
            filters=filters,
            groupers=groupers,
            first=first,
            last=last,
            functions=functions)[0]
        
        query_str = f'{add_queries("", imports)} \n {query_str}' if imports else query_str
        query_str = add_queries(query_str, extra_queries) if extra_queries else query_str
        return [query_str]
    



def _cast_type(type):
    """ will return casting line based on input type """
    if type not in TYPES:
        raise Exception("{} not implemented, it should be one of: {}".format(type, TYPES))
    if type == TYPE_FLOAT:
        return '|> toFloat()'
    elif type == TYPE_INT:
        return '|> toInt()'
    elif type == TYPE_BOOL:
        return '|> toBool()'
    elif type == TYPE_STRING:
        return '|> toString()'
    elif type == TYPE_DURATION:
        return '|> toDuration()'
    elif type == TYPE_TIME:
        return '|> toTime()'
    elif type == TYPE_UINT:
        return '|> toUInt()'
    else:
        raise Exception("{} not implemented".format(type))
