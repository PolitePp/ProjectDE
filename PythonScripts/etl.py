from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('PythonETL').master('spark://vladimir-VirtualBox:7077'). \
    getOrCreate()

properties = {
    'driver': 'org.postgresql.Driver',
    'url': 'jdbc:postgresql://10.0.2.15:5432/project',
    'user': 'postgres',
    'password': '123456',
}
query = '(select * from op_doc_reg) odr'

df2 = spark.read \
    .format('jdbc') \
    .option('driver', properties['driver']) \
    .option('url', properties['url']) \
    .option('user', properties['user']) \
    .option('password', properties['password']) \
    .option('dbtable', query) \
    .load()

df2.createOrReplaceTempView("op_doc_reg")

doc_hub = spark.sql('select id as id_doc_reg'
                    ', md5(id) as hk_doc_reg'
                    ', now() as load_date'
                    ', 1 as record_source '
                    'from op_doc_reg')

doc_hub.write.format('com.vertica.spark.datasource.DefaultSource') \
    .option('db', 'docker') \
    .option('user', 'dbadmin') \
    .option('password', '123456') \
    .option('table', 'hub_doc_reg') \
    .option('host', '172.24.0.7') \
    .option('hdfs_url', 'hdfs://172.24.0.4:9000/user/hadoop') \
    .option('web_hdfs_url', 'webhdfs://172.24.0.4:9870/user/hadoop') \
    .mode('append') \
    .save()

doc_sat = spark.sql('''select md5(id) as hk_doc_reg
                    , now() as load_date
                    , md5(concat_ws(',', idmu, document_id, idmedicaldoctype, doc_date, confident_id, patient_confident_id
                    , assignee_confident_id, patient_id, idprofessional, idrole, post_guid, spec_guid, card_number
                    , case_begin, case_end, structured_body_id, create_date, change_date, log_id, csg_mes_id
                    , hightech_medical_assist_id, subdiv_id, deleted_mark, case_id, prof_podrazdel_id, prof_otdel
                    , fed_00365_guid, fed_33001_guid, id_ref_specialist)) as hash_diff
                    , 1 as record_source
                    , idmu
                    , document_id
                    , idmedicaldoctype
                    , doc_date
                    , confident_id
                    , patient_confident_id
                    , assignee_confident_id
                    , patient_id
                    , idprofessional
                    , idrole
                    , post_guid
                    , spec_guid
                    , card_number
                    , case_begin
                    , case_end
                    , structured_body_id
                    , create_date
                    , change_date
                    , log_id
                    , csg_mes_id
                    , hightech_medical_assist_id
                    , subdiv_id
                    , deleted_mark
                    , case_id
                    , prof_podrazdel_id
                    , prof_otdel
                    , fed_00365_guid
                    , fed_33001_guid
                    , id_ref_specialist
                    from op_doc_reg''')

doc_sat.write.format('com.vertica.spark.datasource.DefaultSource') \
    .option('db', 'docker') \
    .option('user', 'dbadmin') \
    .option('password', '123456') \
    .option('table', 'sat_doc_reg') \
    .option('host', '172.24.0.7') \
    .option('hdfs_url', 'hdfs://172.24.0.4:9000/user/hadoop') \
    .option('web_hdfs_url', 'webhdfs://172.24.0.4:9870/user/hadoop') \
    .mode('append') \
    .save()

query = '(select * from op_rendered_service) ors'

df2 = spark.read \
    .format('jdbc') \
    .option('driver', properties['driver']) \
    .option('url', properties['url']) \
    .option('user', properties['user']) \
    .option('password', properties['password']) \
    .option('dbtable', query) \
    .load()

df2.createOrReplaceTempView("op_rendered_service")

ors_hub = spark.sql('''select cast(id as int) as id_rendered_service
                    , md5(cast(id as String)) as hk_rendered_service
                    , now() as load_date
                    , 1 as record_source
                    from op_rendered_service''')

ors_hub.printSchema()

ors_hub.write.format('com.vertica.spark.datasource.DefaultSource') \
    .option('db', 'docker') \
    .option('user', 'dbadmin') \
    .option('password', '123456') \
    .option('table', 'hub_rendered_service') \
    .option('host', '172.24.0.7') \
    .option('hdfs_url', 'hdfs://172.24.0.4:9000/user/hadoop') \
    .option('web_hdfs_url', 'webhdfs://172.24.0.4:9870/user/hadoop') \
    .mode('append') \
    .save()

ors_sat = spark.sql('''select md5(cast(id as String)) as hk_rendered_service
                    , now() as load_date
                    , md5(concat_ws(',', sst365_guid, idtypeservice, dms_service_name, idmcunit, services_count
                    , idtypepayment, polis_number, polis_series, mdn366_guid, specialist_id, tariff
                    , service_date, service_start_date, service_end_date, policy_type, diagnoses_id
                    , profile_id, children_profile, id_researched_materials, hst0444_id, refusal_sign
                    , medical_intervention, id_hst0494, id_fed00045, id_hst0491)) as hash_diff
                    , 1 as record_source
                    , sst365_guid
                    , idtypeservice
                    , dms_service_name
                    , idmcunit
                    , services_count
                    , idtypepayment
                    , polis_number
                    , polis_series
                    , mdn366_guid
                    , specialist_id
                    , tariff
                    , service_date
                    , service_start_date
                    , service_end_date
                    , policy_type
                    , diagnoses_id
                    , profile_id
                    , children_profile
                    , id_researched_materials
                    , hst0444_id
                    , refusal_sign
                    , medical_intervention
                    , id_hst0494
                    , id_fed00045
                    , id_hst0491
                    from op_rendered_service''')

ors_sat.write.format('com.vertica.spark.datasource.DefaultSource') \
    .option('db', 'docker') \
    .option('user', 'dbadmin') \
    .option('password', '123456') \
    .option('table', 'sat_rendered_service') \
    .option('host', '172.24.0.7') \
    .option('hdfs_url', 'hdfs://172.24.0.4:9000/user/hadoop') \
    .option('web_hdfs_url', 'webhdfs://172.24.0.4:9870/user/hadoop') \
    .mode('append') \
    .save()

doc_ors_lnk = spark.sql('''select md5(concat(id, reg_doc_id)) as hk_doc_reg_rendered_service
                        , md5(cast(id as String)) as hk_rendered_service
                        , md5(reg_doc_id) as hk_doc_reg
                        , now() as load_date
                        , 1 as record_source
                        from op_rendered_service''')

doc_ors_lnk.write.format('com.vertica.spark.datasource.DefaultSource') \
    .option('db', 'docker') \
    .option('user', 'dbadmin') \
    .option('password', '123456') \
    .option('table', 'lnk_doc_reg_rendered_service') \
    .option('host', '172.24.0.7') \
    .option('hdfs_url', 'hdfs://172.24.0.4:9000/user/hadoop') \
    .option('web_hdfs_url', 'webhdfs://172.24.0.4:9870/user/hadoop') \
    .mode('append') \
    .save()
