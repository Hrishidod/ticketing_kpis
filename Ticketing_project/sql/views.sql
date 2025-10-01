/*!50001 CREATE VIEW `v_avg_handling_by_priority` AS SELECT 
 1 AS `priority`,
 1 AS `closed_tickets`,
 1 AS `avg_handling_hours`*/;
/*!50001 CREATE VIEW `v_backlog` AS SELECT 
 1 AS `backlog_tickets`,
 1 AS `total_tickets`,
 1 AS `backlog_pct`*/;
/*!50001 CREATE VIEW `v_backlog_aging` AS SELECT 
 1 AS `priority`,
 1 AS `h_0_24`,
 1 AS `h_24_48`,
 1 AS `h_49_72`,
 1 AS `h_gt_72`*/;
/*!50001 CREATE VIEW `v_backlog_by_priority` AS SELECT 
 1 AS `priority`,
 1 AS `total`,
 1 AS `backlog`,
 1 AS `backlog_pct`*/;
/*!50001 CREATE VIEW `v_channel_status` AS SELECT 
 1 AS `channel`,
 1 AS `status`,
 1 AS `ticket_count`*/;
/*!50001 CREATE VIEW `v_closed_with_duration` AS SELECT 
 1 AS `ticket_id`,
 1 AS `ticket_type`,
 1 AS `channel`,
 1 AS `priority`,
 1 AS `status`,
 1 AS `first_response_at`,
 1 AS `resolved_at`,
 1 AS `handling_hours_after_first_response`,
 1 AS `sla_target_hours`,
 1 AS `sla_breached`,
 1 AS `satisfaction`,
 1 AS `product`,
 1 AS `purchase_date`,
 1 AS `ticket_subject`,
 1 AS `ticket_description`,
 1 AS `resolution_text`*/;
/*!50001 CREATE VIEW `v_data_quality_coverage` AS SELECT 
 1 AS `closed_total`,
 1 AS `closed_with_duration`,
 1 AS `pct_closed_with_duration`*/;
/*!50001 CREATE VIEW `v_frt_by_channel` AS SELECT 
 1 AS `channel`,
 1 AS `tickets_with_frt`,
 1 AS `avg_frt_hours`,
 1 AS `frt_breach_rate_pct`*/;
/*!50001 CREATE VIEW `v_frt_summary` AS SELECT 
 1 AS `priority`,
 1 AS `tickets_with_frt`,
 1 AS `avg_frt_hours`,
 1 AS `frt_breaches`,
 1 AS `frt_breach_rate_pct`*/;
/*!50001 CREATE VIEW `v_null_duration_by_status` AS SELECT 
 1 AS `status`,
 1 AS `total`,
 1 AS `null_duration`,
 1 AS `pct_null`*/;
/*!50001 CREATE VIEW `v_open_age_buckets` AS SELECT 
 1 AS `priority`,
 1 AS `d_lt_1`,
 1 AS `d_1_2`,
 1 AS `d_3_7`,
 1 AS `d_gt_7`*/;
/*!50001 CREATE VIEW `v_open_over_sla` AS SELECT 
 1 AS `ticket_id`,
 1 AS `priority`,
 1 AS `status`,
 1 AS `channel`,
 1 AS `ticket_type`,
 1 AS `first_response_at`,
 1 AS `hours_open_since_first_response`,
 1 AS `sla_target_hours`*/;
/*!50001 CREATE VIEW `v_open_ticket_age` AS SELECT 
 1 AS `priority`,
 1 AS `open_ticket_count`,
 1 AS `avg_age_days`,
 1 AS `max_age_days`*/;
/*!50001 CREATE VIEW `v_priority_channel` AS SELECT 
 1 AS `priority`,
 1 AS `channel`,
 1 AS `ticket_count`*/;
/*!50001 CREATE VIEW `v_satisfaction_by_priority` AS SELECT 
 1 AS `priority`,
 1 AS `closed_with_rating`,
 1 AS `avg_csats`*/;
/*!50001 CREATE VIEW `v_sla_by_channel` AS SELECT 
 1 AS `channel`,
 1 AS `closed_tickets`,
 1 AS `breaches`,
 1 AS `breach_rate_pct`*/;
/*!50001 CREATE VIEW `v_sla_by_type` AS SELECT 
 1 AS `ticket_type`,
 1 AS `closed_tickets`,
 1 AS `breaches`,
 1 AS `breach_rate_pct`*/;
/*!50001 CREATE VIEW `v_sla_summary` AS SELECT 
 1 AS `priority`,
 1 AS `closed_tickets`,
 1 AS `breaches`,
 1 AS `breach_rate_pct`*/;
/*!50001 CREATE VIEW `v_status_mix` AS SELECT 
 1 AS `status`,
 1 AS `ticket_count`*/;
/*!50001 CREATE VIEW `v_type_status` AS SELECT 
 1 AS `ticket_type`,
 1 AS `status`,
 1 AS `ticket_count`*/;
/*!50001 CREATE VIEW `v_weekly_sla_breach_trend` AS SELECT 
 1 AS `yearweek_iso`,
 1 AS `closed_tickets`,
 1 AS `breaches`,
 1 AS `breach_rate_pct`*/;
/*!50001 CREATE VIEW `v_weekly_trend` AS SELECT 
 1 AS `yearweek_iso`,
 1 AS `responded_count`,
 1 AS `closed_count`*/;
