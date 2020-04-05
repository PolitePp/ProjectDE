drop table if exists lnk_doc_reg_rendered_service;
drop table if exists sat_doc_reg;
drop table if exists sat_rendered_service;
drop table if exists hub_doc_reg;
drop table if exists hub_rendered_service;

create table ref_sources
(
    id smallint
    , name varchar
);

create table hub_doc_reg
(
    id_doc_reg varchar(36) unique
    , hk_doc_reg varchar(32) primary key
    , load_date timestamp
    , record_source smallint
);


create table sat_doc_reg
(
    hk_doc_reg varchar(32)
    , load_date timestamp
    , hash_diff varchar(32)
    , record_source smallint
    , idmu numeric,
	document_id varchar(36),
	idmedicaldoctype numeric,
	doc_date timestamp,
	confident_id numeric,
	patient_confident_id numeric,
	assignee_confident_id numeric,
	patient_id numeric,
	idprofessional numeric,
	idrole numeric,
	post_guid numeric,
	spec_guid numeric,
	card_number varchar(50),
	case_begin timestamp,
	case_end timestamp,
	structured_body_id numeric,
	create_date timestamp,
	change_date timestamp,
	log_id numeric,
	csg_mes_id numeric,
	hightech_medical_assist_id numeric,
	subdiv_id numeric,
	deleted_mark numeric(38),
	case_id varchar(36),
	prof_podrazdel_id numeric,
	prof_otdel varchar(64),
	fed_00365_guid bigint,
	fed_33001_guid bigint,
	id_ref_specialist numeric,
	constraint pk_sat_doc_reg primary key (hk_doc_reg, load_date),
	constraint fk_hk_doc_reg foreign key (hk_doc_reg) references hub_doc_reg(hk_doc_reg)
);

create table hub_rendered_service
(
    id_rendered_service bigint unique
    , hk_rendered_service varchar(32) primary key
    , load_date timestamp
    , record_source smallint
);

create table sat_rendered_service
(
    hk_rendered_service varchar(32),
    load_date timestamp
    , hash_diff varchar(32)
    , record_source smallint,
	sst365_guid numeric,
	idtypeservice numeric,
	dms_service_name varchar(255),
	idmcunit numeric not null,
	services_count numeric not null,
	idtypepayment numeric not null,
	polis_number varchar(255),
	polis_series varchar(255),
	mdn366_guid numeric,
	specialist_id numeric,
	tariff numeric,
	service_date timestamp,
	service_start_date timestamp,
	service_end_date timestamp,
	policy_type numeric(38),
	diagnoses_id numeric,
	profile_id numeric,
	children_profile numeric(38,1),
	id_researched_materials numeric,
	hst0444_id numeric,
	refusal_sign smallint,
	medical_intervention varchar(255),
	id_hst0494 bigint,
	id_fed00045 bigint,
	id_hst0491 bigint,
	constraint pk_sat_rendered_service primary key (hk_rendered_service, load_date),
	constraint fk_hk_rendered_service foreign key (hk_rendered_service) references hub_rendered_service(hk_rendered_service)
);

create table lnk_doc_reg_rendered_service
(
    hk_doc_reg_rendered_service varchar(32) primary key
    , hk_rendered_service varchar(32)
    , hk_doc_reg varchar(32)
    , load_date timestamp
    , record_source smallint
    , constraint fk_hk_op_doc_reg foreign key (hk_rendered_service) references hub_rendered_service(hk_rendered_service)
	, constraint fk_hk_doc_reg foreign key (hk_doc_reg) references hub_doc_reg(hk_doc_reg)
);

insert into ref_sources values (1, 'PostgreSQL DB first');