# Overrideable SQL templates
sql_create_table = "CREATE TABLE %(table)s (%(definition)s)"
sql_check_table = "SELECT %(name)s FROM sqlite_master WHERE type='table' AND name='%(table)s'"
sql_rename_table = "ALTER TABLE %(old_table)s RENAME TO %(new_table)s"
sql_retablespace_table = "ALTER TABLE %(table)s SET TABLESPACE %(new_tablespace)s"
sql_delete_table = "DROP TABLE %(table)s CASCADE"

sql_create_column = "ALTER TABLE %(table)s ADD COLUMN %(column)s %(definition)s"
sql_alter_column = "ALTER TABLE %(table)s %(changes)s"
sql_alter_column_type = "ALTER COLUMN %(column)s TYPE %(type)s"
sql_alter_column_null = "ALTER COLUMN %(column)s DROP NOT NULL"
sql_alter_column_not_null = "ALTER COLUMN %(column)s SET NOT NULL"
sql_alter_column_default = "ALTER COLUMN %(column)s SET DEFAULT %(default)s"
sql_alter_column_no_default = "ALTER COLUMN %(column)s DROP DEFAULT"
sql_alter_column_no_default_null = sql_alter_column_no_default
sql_alter_column_collate = "ALTER COLUMN %(column)s TYPE %(type)s%(collation)s"
sql_delete_column = "ALTER TABLE %(table)s DROP COLUMN %(column)s CASCADE"
sql_rename_column = "ALTER TABLE %(table)s RENAME COLUMN %(old_column)s TO %(new_column)s"
sql_update_with_default = "UPDATE %(table)s SET %(column)s = %(default)s WHERE %(column)s IS NULL"

sql_unique_constraint = "UNIQUE (%(columns)s)%(deferrable)s"
sql_check_constraint = "CHECK (%(check)s)"
sql_delete_constraint = "ALTER TABLE %(table)s DROP CONSTRAINT %(name)s"
sql_constraint = "CONSTRAINT %(name)s %(constraint)s"

sql_create_check = "ALTER TABLE %(table)s ADD CONSTRAINT %(name)s CHECK (%(check)s)"
sql_delete_check = sql_delete_constraint

sql_create_unique = "ALTER TABLE %(table)s ADD CONSTRAINT %(name)s UNIQUE (%(columns)s)%(deferrable)s"
sql_delete_unique = sql_delete_constraint

sql_create_fk = (
    "ALTER TABLE %(table)s ADD CONSTRAINT %(name)s FOREIGN KEY (%(column)s) "
    "REFERENCES %(to_table)s (%(to_column)s)%(deferrable)s"
)
sql_create_inline_fk = None
sql_create_column_inline_fk = None
sql_delete_fk = sql_delete_constraint

sql_create_index = "CREATE INDEX %(name)s ON %(table)s (%(columns)s)%(include)s%(extra)s%(condition)s"
sql_create_unique_index = "CREATE UNIQUE INDEX %(name)s ON %(table)s (%(columns)s)%(include)s%(condition)s"
sql_delete_index = "DROP INDEX %(name)s"

sql_create_pk = "ALTER TABLE %(table)s ADD CONSTRAINT %(name)s PRIMARY KEY (%(columns)s)"
sql_delete_pk = sql_delete_constraint

sql_delete_procedure = 'DROP PROCEDURE %(procedure)s'