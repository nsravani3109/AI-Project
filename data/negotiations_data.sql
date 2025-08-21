-- Insert sample negotiations data
-- Run in SQLite: .read negotiations_data.sql
-- Note: This assumes calls table is already populated

INSERT INTO negotiations (call_id, round_number, carrier_offer, system_response, timestamp) VALUES
-- Negotiation for call_id 2 (MC789012, LD002 - Chicago to Dallas reefer)
(2, 1, 2300.00, 'I understand fuel costs are high. Our rate of $2100 is competitive for this reefer lane. Can we work with that?', datetime('2025-08-20 10:35:00')),
(2, 2, 2250.00, 'Let me check with my supervisor. Would $2150 work for you?', datetime('2025-08-20 10:42:00')),

-- Negotiation for call_id 3 (MC345678, LD003 - Atlanta to Miami)
(3, 1, NULL, 'I understand your concern about Florida. Would a higher rate of $1900 change your mind?', datetime('2025-08-20 11:05:00')),

-- Negotiation for call_id 4 (MC901234, LD004 - Denver to Seattle flatbed)
(4, 1, 2750.00, 'That works for us. $2750 is acceptable for this flatbed load.', datetime('2025-08-20 13:32:00')),

-- Negotiation for call_id 7 (MC333444, LD007 - Tampa to Nashville reefer)
(7, 1, NULL, 'The load must be kept at -10F throughout transport. We provide temperature monitoring. Is your equipment capable?', datetime('2025-08-20 16:18:00')),

-- Negotiation for call_id 9 (MC777888, LD009 - Kansas City to Minneapolis)
(9, 1, 1150.00, 'Yes, we can do $1150 for this load. I will book you now.', datetime('2025-08-20 17:25:00')),

-- Negotiation for call_id 10 (MC999000, LD010 - Sacramento to Salt Lake City oversized)
(10, 1, NULL, 'Load dimensions are 48x8.5x11 feet. All permits are ready and will be provided before pickup.', datetime('2025-08-20 17:58:00'));

SELECT 'Negotiations data inserted successfully!' as message;
