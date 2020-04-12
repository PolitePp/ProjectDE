from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('PythonETL').master('spark://vladimir-VirtualBox:7077').\
    getOrCreate()
    #config('spark.driver.extraClassPath', '/home/vladimir/ProjectDE/PythonScripts/jdbc/postgresql-42.2.12.jar').\

properties = {
    'driver': 'org.postgresql.Driver',
    'url': 'jdbc:postgresql://10.0.2.15:5432/project',
    'user': 'postgres',
    'password': '123456',
}
query = '(select * from op_doc_reg where idmu = 263) odr'

df2 = spark.read \
    .format('jdbc') \
    .option('driver', properties['driver']) \
    .option('url', properties['url']) \
    .option('user', properties['user']) \
    .option('password', properties['password']) \
    .option('dbtable', query) \
    .load()

df2.createOrReplaceTempView("op_doc_reg")
df2_hub = spark.sql('select id as id_doc_reg'
          ', md5(id) as hk_doc_reg'
          ', now() as load_date'
          ', 1 as record_source '
          'from op_doc_reg')

df2_hub.write.format('com.vertica.spark.datasource.DefaultSource')\
    .option('db', 'docker')\
    .option('user', 'dbadmin')\
    .option('password', '123456')\
    .option('table', 'hub_doc_reg')\
    .option('host', '172.24.0.7')\
    .option('hdfs_url', 'hdfs://172.24.0.4:9000/user/hadoop')\
    .option('web_hdfs_url', 'webhdfs://172.24.0.4:9870/user/hadoop')\
    .mode('append') \
    .save()
