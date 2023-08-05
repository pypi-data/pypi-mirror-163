SELECT
    1 AS visit_occurrence_id,
    1 AS person_id,
    0 AS visit_concept_id,
    0 AS visit_type_concept_id,
    1 AS provider_id,
    1 AS care_site_id,
    '' AS visit_source_value,
    0 AS visit_source_concept_id,
    0 AS admitted_from_concept_id,
    '' AS admitted_from_source_value,
    0 AS discharged_to_concept_id,
    '' AS discharged_to_source_value,
    now()::DATE AS visit_start_date,
    now()::TIMESTAMP AS visit_start_datetime,
    now()::DATE AS visit_end_date,
    now()::TIMESTAMP AS visit_end_datetime,
    NULL::int AS preceding_visit_occurrence_id
