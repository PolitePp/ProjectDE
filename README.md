# ProjectDE

Проект посвящён работе с медицинскими данными, а именно документами и их услугами. По одному документу (болезни), может быть несколько услуг. Данная информация хранится в разных таблицах. Примеры строк указаны в файлах iemk_iemk_op_doc_reg.sql и iemk_iemk_op_rendered_service.sql

Схема процесса [здесь](https://drive.google.com/file/d/13JRANqyTh8cPzndjeIC_n5-PV8M5g487/view?usp=sharing)

На текущий момент проект содержит в себе:
1. Apache Airflow для управления процессами получения данных
2. Streamsets для выгрузки данных
3. Vertica для хранения данных
4. Spark для обработки данных

Для работоспособности Streamset с Vertica необходимо зайти внутрь контейнера Streamsets пройти по следующему пути - /opt/streamsets-datacollector/streamsets-libs/streamsets-datacollector-jdbc-lib/lib
и через wget скачать драйвер
Полную инструкцию по созданию JDBC с вертика можно посмотреть [здесь](https://www.vertica.com/kb/StreamSetsCG/Content/Partner/StreamSetsCG.htm)

В streamsets созданы два pipelines - op_doc_reg и op_rendered_service. Оба трансформируют информацию таким образом, чтобы она могла быть загружена в цхд, построенное по архитектуре Data Vault 2.0

