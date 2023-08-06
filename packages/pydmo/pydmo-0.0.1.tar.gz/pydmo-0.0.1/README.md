![coverage](https://gitlab.com/gitlab-org/gitlab/badges/main/coverage.svg?job=tests)

# pydmo

**Documentation**: [https://strayMat.gitlab.io/pydmo](https://strayMat.gitlab.io/pydmo)

**Source Code**: [https://gitlab.com/strayMat/pydmo](https://gitlab.com/strayMat/pydmo)

This projects implements the creation of [pydantic] data models from a collection of dataset (eg. pandas dataset). 


## Motivation

Having typed data models in python files is very useful for :

- Code testing thanks to dummy data generation
- Data validation
- Documentation generation

These usages are motivated by the [data templates with pydantic](https://ianwhitestone.work/data-templates-with-pydantic/) blog post.

## Links with other projects

The [Table-schema-translator](https://framagit.org/interhop/library/table-schema-translator/-/tree/master) takes yaml as input to generate scala data models for spark.  

We use the [pydantic code generation package](https://koxudaxi.github.io/datamodel-code-generator/jsonschema/).

The python API should be installed with pip as [recommanded in the documentation](https://koxudaxi.github.io/datamodel-code-generator/using_as_module/). 


# 📝 **Note**
- Might be useful if we want to integrate some features existing only on table schema: [Pandas api for table schema](https://pandas.pydata.org/docs/reference/api/pandas.io.json.build_table_schema.html)
