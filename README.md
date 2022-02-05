# Generic Poster

### **How to run:**

On root folder run:
```
python main.py
```


### **How to use:**

After running this command a por will be open to connect:
```
http://localhost:5000
```

Send a body POST request to the endpoints and fields configuration below.



### **Endpoints available:**
```
POST - /dynamo
POST - /sqs
```



### **Fields:**

### **Main body:**

Fields:
```
(REQUIRED)
"amount": (Integer) Amount of objects to be generate

(REQUIRED)
"table":  (String) Table name on dynamo. Exclusive for /dynamo request

(REQUIRED)
"queue":  (String) Queue name on SQS. Exclusive for /sqs request

(REQUIRED)
"data":   (Array) Fields configurations to be created
```
Json example:
```
{
    "amount": 10,
    "table": "table_name", -- Exclusive for dynamo request
    "queue": "queue_name", -- Exclusive for sqs request
    "data": [FieldArray]
}
```



### **Common fields:**

```
(REQUIRED)
"name":          (String) Field name   

(REQUIRED)
"type":          (String) Field type - Accepted types: 'str','string','int','integer','number','bool','boolean,'float','double','date','object','array'  

(NO REQUIRED)
"field_config":  (Object) Field configuration

(NO REQUIRED)
"default":       (Field_type) Default value for field

(NO REQUIRED)
"possibilities": (Array) Possible values for this field   
```



### **Field Configuration:**

**String:**

Fieds:
```
"lower_case":     (Boolean) Lowercase string if true and uppercase otherwise
"amount_chars":   (Integer) Characters amount in string
```

Default value:
Random lowercase string 50 characteres

Json Example: (with possibility value)

```
        {
            "name": "CHVE_PK",
            "type": "str",
            "field_config": {
                "lower_case": false,
                "amount_chars": 10
            },
            "default": null,
            "possibilities": ["First String", "Second String", "Third String"]
        },
```



**Integer:**

Fields:
```
"min":   (Integer) Min Value
"max":   (Integer) Max value
```

Default value:
Min = 0 | Max = 1000000

Json Example:

```
        {
            "name": "idade",
            "type": "int",
            "field_config": {
                "min": 0,
                "max": 110
            },
            "default": null,
            "possibilities": []
        }
```

Boolean:

Fields:
```
No Configuration/Possibilities needed
```

Default:
No default value

Json Example: (with default value)

```
        {
            "name": "isActive",
            "type": "bool",
            "field_config": {},
            "default": true,
            "possibilities": []
        }
```

**Double:**

```
"min":   (Integer) Min Value
"max":   (Integer) Max value
```

Json Example: 

```
        {
            "name": "valor",
            "type": "double",
            "field_config": {
                "min": 0,
                "max": 2000
            },
            "default": null,
            "possibilities": []
        }
```


**Object:**

Fields:

```
(REQUIRED)
"fields": Configuration of all fields mentioned above
```

Default:
No default value

Json Example: 

```
        {
            "name": "endereco",
            "type": "object",
            "field_config": {
                "fields": [
                    {
                        "name": "street",
                        "type": "str",
                        "field_config": {
                            "lower_case": true,
                            "amount_chars": 50
                        },
                        "default": null,
                        "possibilities": []
                    },
                    {
                        "name": "number",
                        "type": "int",
                        "field_config": {
                            "min": 0,
                            "max": 0
                        },
                        "default": null,
                        "possibilities": [500, 600, 700, 1500, 2100]
                    },
                    {
                        "name": "city",
                        "type": "str",
                        "field_config": {
                            "lower_case": false,
                            "amount_chars": 15
                        },
                        "default": "São Paulo",
                        "possibilities": []
                    }
                ]
            },
            "default": null,
            "possibilities": []
        }
```

**Array:**

Fields:
```
(REQUIRED)
"amount": Amount of fields to be generated

(REQUIRED)
"array_data_config": Field configuration mentioned above
```

Default:
No default value

Json Example: 

```
{
            "name": "users",
            "type": "array",
            "field_config": {
                "amount": 10,
                "array_data_config": {
                    "type": "object",
                    "fields": [
                        {
                            "name": "nome",
                            "type": "str",
                            "field_config": {
                                "lower_case": false,
                                "amount_chars": 10
                            },
                            "default": null,
                            "possibilities": []
                        },
                        {
                            "name": "birthday",
                            "type": "date",
                            "field_config": {
                                "as_string": true,
                                "with_time": true,
                                "format": null,
                                "date": {
                                    "day": {
                                        "min": 1,
                                        "max": 30
                                    },
                                    "month": {
                                        "min": 1,
                                        "max": 12
                                    },
                                    "year": {
                                        "min": 1990,
                                        "max": 2010
                                    }
                                },
                                "time": {
                                    "hours": {
                                        "min": 20,
                                        "max": 24
                                    },
                                    "minutes": {
                                        "min": 15,
                                        "max": 30
                                    },
                                    "seconds": {
                                        "min": 0,
                                        "max": 59
                                    }
                                }
                            },
                            "default": null,
                            "possibilities": []
                        },
                        {
                            "name": "isActive",
                            "type": "bool",
                            "field_config": {},
                            "default": null,
                            "possibilities": []
                        },
                        {
                            "name": "idade",
                            "type": "int",
                            "field_config": {
                                "min": 0,
                                "max": 110
                            },
                            "default": null,
                            "possibilities": []
                        },
                        {
                            "name": "valor",
                            "type": "double",
                            "field_config": {
                                "min": 0,
                                "max": 2000
                            },
                            "default": null,
                            "possibilities": []
                        },
                        {
                            "name": "endereco",
                            "type": "object",
                            "field_config": {
                                "fields": [
                                    {
                                        "name": "street",
                                        "type": "str",
                                        "field_config": {
                                            "lower_case": true,
                                            "amount_chars": 50
                                        },
                                        "default": null,
                                        "possibilities": []
                                    },
                                    {
                                        "name": "number",
                                        "type": "int",
                                        "field_config": {
                                            "min": 1,
                                            "max": 500
                                        },
                                        "default": null,
                                        "possibilities": []
                                    },
                                    {
                                        "name": "city",
                                        "type": "str",
                                        "field_config": {
                                            "lower_case": false,
                                            "amount_chars": 15
                                        },
                                        "default": null,
                                        "possibilities": []
                                    }
                                ]
                            },
                            "default": null,
                            "possibilities": []
                        }
                    ]
                }
            },
            "default": null,
            "possibilities": []
        }
```


### **Example:**

**Full json example:**
```
{
    "amount": 10,
    "table": "TABLE_GEN", (or "queue: "SQS_QUEU")
    "data": [
        {
            "name": "CHVE_PK",
            "type": "str",
            "field_config": {
                "lower_case": false,
                "amount_chars": 10
            },
            "default": null,
            "possibilities": []
        },
        {
            "name": "CHVE_SK",
            "type": "date",
            "field_config": {
                "as_string": true,
                "with_time": true,
                "format": null,
                "date": {
                    "day": {
                        "min": 1,
                        "max": 30
                    },
                    "month": {
                        "min": 1,
                        "max": 12
                    },
                    "year": {
                        "min": 2000,
                        "max": 2021
                    }
                },
                "time": {
                    "hours": {
                        "min": 20,
                        "max": 24
                    },
                    "minutes": {
                        "min": 15,
                        "max": 30
                    },
                    "seconds": {
                        "min": 0,
                        "max": 59
                    }
                }
            },
            "default": null,
            "possibilities": []
        },
        {
            "name": "users",
            "type": "array",
            "field_config": {
                "amount": 10,
                "array_data_config": {
                    "type": "object",
                    "fields": [
                        {
                            "name": "nome",
                            "type": "str",
                            "field_config": {
                                "lower_case": false,
                                "amount_chars": 10
                            },
                            "default": null,
                            "possibilities": []
                        },
                        {
                            "name": "birthday",
                            "type": "date",
                            "field_config": {
                                "as_string": true,
                                "with_time": true,
                                "format": null,
                                "date": {
                                    "day": {
                                        "min": 1,
                                        "max": 30
                                    },
                                    "month": {
                                        "min": 1,
                                        "max": 12
                                    },
                                    "year": {
                                        "min": 1990,
                                        "max": 2010
                                    }
                                },
                                "time": {
                                    "hours": {
                                        "min": 20,
                                        "max": 24
                                    },
                                    "minutes": {
                                        "min": 15,
                                        "max": 30
                                    },
                                    "seconds": {
                                        "min": 0,
                                        "max": 59
                                    }
                                }
                            },
                            "default": null,
                            "possibilities": []
                        },
                        {
                            "name": "isActive",
                            "type": "bool",
                            "field_config": {},
                            "default": null,
                            "possibilities": []
                        },
                        {
                            "name": "idade",
                            "type": "int",
                            "field_config": {
                                "min": 0,
                                "max": 110
                            },
                            "default": null,
                            "possibilities": []
                        },
                        {
                            "name": "valor",
                            "type": "double",
                            "field_config": {
                                "min": 0,
                                "max": 2000
                            },
                            "default": null,
                            "possibilities": []
                        },
                        {
                            "name": "endereco",
                            "type": "object",
                            "field_config": {
                                "fields": [
                                    {
                                        "name": "street",
                                        "type": "str",
                                        "field_config": {
                                            "lower_case": true,
                                            "amount_chars": 50
                                        },
                                        "default": null,
                                        "possibilities": []
                                    },
                                    {
                                        "name": "number",
                                        "type": "int",
                                        "field_config": {
                                            "min": 1,
                                            "max": 500
                                        },
                                        "default": null,
                                        "possibilities": []
                                    },
                                    {
                                        "name": "city",
                                        "type": "str",
                                        "field_config": {
                                            "lower_case": false,
                                            "amount_chars": 15
                                        },
                                        "default": null,
                                        "possibilities": []
                                    }
                                ]
                            },
                            "default": null,
                            "possibilities": []
                        }
                    ]
                }
            },
            "default": null,
            "possibilities": []
        }
    ]
}

```

**Simple Json Example:**

```
{
    "amount": 2,
    "table": "TABLE_GEN",
    "data": [
        {
            "name": "CHVE_PK",
            "type": "str"
        },
        {
            "name": "CHVE_SK",
            "type": "str"
        },
        {
            "name": "age",
            "type": "int"
        },
        {
            "name": "male",
            "type": "boolean"
        },
        {
            "name": "birthday",
            "type": "date",
            "field_config": {
                "as_string": true
            }
        },
        {
            "name": "endereco",
            "type": "object",
            "field_config":{
                "fields":[
                    {
                        "name": "street",
                        "type": "string"
                    },
                    {
                        "name": "city",
                        "type": "string"
                    },
                    {
                        "name": "numbers",
                        "type": "array",
                        "field_config": {
                            "amount": 2,
                            "array_data_config": {
                                "type": "int"
                            }
                        }
                    }
                ]
            }
        }
    ]
}
```
