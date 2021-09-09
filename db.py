import databases
import sqlalchemy


metadata = sqlalchemy.MetaData()
database = databases.Database('mysql://root:35739517@192.168.0.51:3307/InOut2')