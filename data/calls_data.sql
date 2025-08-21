-- Insert sample calls data
-- Run in SQLite: .read calls_data.sql
-- Note: This assumes carriers and loads tables are already populated

INSERT INTO calls (carrier_mc_number, load_id, call_start_time, call_end_time, call_duration, outcome, sentiment, initial_rate_offered, final_rate_agreed, negotiation_rounds, notes, call_transcript, transferred_to_rep) VALUES
('MC123456', 'LD001', datetime('2025-08-20 09:15:00'), datetime('2025-08-20 09:22:00'), 420, 'accepted', 'positive', 1250.00, 1250.00, 0, 'Carrier accepted rate immediately', 'Agent: Hello, this is Sarah from LoadMatch. I have a load from LA to Phoenix... Carrier: That works for us, we can take it at your rate.', 0),
('MC789012', 'LD002', datetime('2025-08-20 10:30:00'), datetime('2025-08-20 10:45:00'), 900, 'negotiating', 'neutral', 2100.00, NULL, 2, 'Carrier wants higher rate for reefer load', 'Agent: We have a reefer load Chicago to Dallas... Carrier: We need at least $2300 for that route with current fuel prices.', 0),
('MC345678', 'LD003', datetime('2025-08-20 11:00:00'), datetime('2025-08-20 11:08:00'), 480, 'rejected', 'negative', 1800.00, NULL, 1, 'Carrier not interested in Florida runs', 'Agent: Load available Atlanta to Miami... Carrier: We dont do Florida runs, too much traffic and delays.', 0),
('MC901234', 'LD004', datetime('2025-08-20 13:20:00'), datetime('2025-08-20 13:35:00'), 900, 'accepted', 'positive', 2800.00, 2750.00, 1, 'Small negotiation but deal closed', 'Agent: Flatbed load Denver to Seattle... Carrier: Can you do $2750? Agent: Yes, thats acceptable.', 0),
('MC567890', 'LD005', datetime('2025-08-20 14:45:00'), datetime('2025-08-20 15:02:00'), 1020, 'transferred', 'neutral', 3200.00, NULL, 0, 'High value load, transferred to senior rep', 'Agent: High value medical equipment load... Carrier: This needs special handling, can I speak to a manager?', 1),
('MC111222', 'LD006', datetime('2025-08-20 15:30:00'), datetime('2025-08-20 15:38:00'), 480, 'accepted', 'positive', 1650.00, 1650.00, 0, 'Quick acceptance, regular customer', 'Agent: Portland to Vegas load available... Carrier: Perfect, we run that route weekly. Book us.', 0),
('MC333444', 'LD007', datetime('2025-08-20 16:10:00'), datetime('2025-08-20 16:25:00'), 900, 'negotiating', 'neutral', 1950.00, NULL, 1, 'Discussing reefer requirements', 'Agent: Frozen food load Tampa to Nashville... Carrier: We need confirmation on temperature requirements and loading procedures.', 0),
('MC555666', 'LD008', datetime('2025-08-20 16:45:00'), datetime('2025-08-20 16:52:00'), 420, 'rejected', 'neutral', 1400.00, NULL, 0, 'Rate too low for current market', 'Agent: Phoenix to San Antonio load... Carrier: That rate is below our minimum for that lane, sorry.', 0),
('MC777888', 'LD009', datetime('2025-08-20 17:20:00'), datetime('2025-08-20 17:28:00'), 480, 'accepted', 'positive', 1100.00, 1150.00, 1, 'Small rate increase negotiated', 'Agent: Kansas City to Minneapolis... Carrier: Can you do $1150? Agent: Yes, thats fine.', 0),
('MC999000', 'LD010', datetime('2025-08-20 17:50:00'), datetime('2025-08-20 18:05:00'), 900, 'negotiating', 'positive', 2200.00, NULL, 1, 'Discussing permit and route details', 'Agent: Oversized load Sacramento to Salt Lake... Carrier: What are the exact dimensions and do you have permits ready?', 0);

SELECT 'Calls data inserted successfully!' as message;
