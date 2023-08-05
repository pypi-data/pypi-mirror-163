SELECT
    1 AS procedure_occurrence_id,
    1 AS person_id,
    0 AS procedure_concept_id,
    now()::DATE AS procedure_date,
    now()::TIMESTAMP AS procedure_datetime,
    now()::DATE AS procedure_end_date,
    now()::TIMESTAMP AS procedure_end_datetime,
    0 AS procedure_type_concept_id,
    0 AS modifier_concept_id,
    1 AS quantity,
    1 AS provider_id,
    1 AS visit_occurrence_id,
    1 AS visit_detail_id,
    '' AS procedure_source_value,
    0 AS procedure_source_concept_id,
    '' AS modifier_source_value
