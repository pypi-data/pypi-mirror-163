# Panther Config SDK
The Panther Config module allows you to configure detections for your [Panther](https://panther.com) instance.

## Install
The Panther Config SDK can be installed using PIP.

```sh
pip3 install panther_config==0.0.4
```


## query module

### Query
A saved or scheduled query

| Field | Type | Description |
| ----- | ---- | ----------- |
| `name` | `str` | Unique name for the query |

## detection module


### PythonFilter
Custom python filter

| Field | Type | Description |
| ----- | ---- | ----------- |
| `func` | `typing.Callable[[typing.Any], bool]` | Custom python filter |



### JSONUnitTest
Unit test with json content

| Field | Type | Description |
| ----- | ---- | ----------- |
| `name` | `str` | name of the unit test |
| `data` | `str` | json data |


### DictUnitTest
Unit test with python dict content

| Field | Type | Description |
| ----- | ---- | ----------- |
| `data` | `typing.Dict[str, typing.Any]` | json data |


### Rule
Define a rule

| Field | Type | Description |
| ----- | ---- | ----------- |
| `rule_id` | `str` | ID for the rule |
| `severity` | `str` | Severity for the rule |
| `title` | `typing.Optional[str]` | Severity for the rule |
| `log_types` | `typing.Union[str, typing.List[str]]` | Severity for the rule |
| `filters` | `typing.Union[_BaseFilter, typing.List[_BaseFilter]]` | Define event filters for the rule |
| `unit_tests` | `typing.Optional[typing.Union[_BaseFilter, typing.List[_BaseFilter]]]` | Define event filters for the rule |
