-- Sample data insertion scripts for Inbound Sales AI Agent Database
-- Run these commands in SQLite to populate your tables with test data

-- Insert sample carriers
INSERT INTO carriers (mc_number, company_name, status, address, phone, email, is_verified, created_at, updated_at) VALUES
('MC123456', 'Swift Transportation', 'Active', '2200 S 75th Ave, Phoenix, AZ 85043', '(602) 269-9700', 'dispatch@swift.com', 1, datetime('now'), datetime('now')),
('MC789012', 'J.B. Hunt Transport', 'Active', '615 J.B. Hunt Corporate Dr, Lowell, AR 72745', '(479) 820-0000', 'loads@jbhunt.com', 1, datetime('now'), datetime('now')),
('MC345678', 'Schneider National', 'Active', '3101 S Packerland Dr, Green Bay, WI 54313', '(920) 592-2000', 'freight@schneider.com', 1, datetime('now'), datetime('now')),
('MC901234', 'Werner Enterprises', 'Active', '14507 Frontier Rd, Omaha, NE 68138', '(402) 895-6640', 'dispatch@werner.com', 1, datetime('now'), datetime('now')),
('MC567890', 'Prime Inc', 'Active', '2740 N Mayfair Ave, Springfield, MO 65803', '(417) 866-8300', 'loads@primeinc.com', 1, datetime('now'), datetime('now')),
('MC111222', 'Maverick Transportation', 'Active', '10 Maverick Way, Little Rock, AR 72210', '(501) 570-1100', 'freight@maverickusa.com', 1, datetime('now'), datetime('now')),
('MC333444', 'Heartland Express', 'Active', '901 North Kansas Ave, North Liberty, IA 52317', '(319) 626-3600', 'dispatch@heartlandexpress.com', 1, datetime('now'), datetime('now')),
('MC555666', 'USA Truck', 'Active', '3200 Industrial Blvd, Van Buren, AR 72956', '(479) 471-2500', 'loads@usa-truck.com', 1, datetime('now'), datetime('now')),
('MC777888', 'Knight-Swift Transportation', 'Active', '5601 W Buckeye Rd, Phoenix, AZ 85043', '(602) 606-6200', 'dispatch@knight-swift.com', 1, datetime('now'), datetime('now')),
('MC999000', 'Covenant Transport', 'Active', '400 Birmingham Hwy, Chattanooga, TN 37419', '(423) 821-1212', 'freight@covenanttransport.com', 1, datetime('now'), datetime('now'));

-- Insert sample loads
INSERT INTO loads (load_id, origin, destination, pickup_datetime, delivery_datetime, equipment_type, loadboard_rate, notes, weight, commodity_type, num_of_pieces, miles, dimensions, status, created_at, updated_at) VALUES
('LD001', 'Los Angeles, CA', 'Phoenix, AZ', datetime('2025-08-21 08:00:00'), datetime('2025-08-21 18:00:00'), 'Dry Van', 1250.00, 'Urgent delivery required', 45000, 'Electronics', 15, 372, '53'' x 8.5'' x 9''', 'available', datetime('now'), datetime('now')),
('LD002', 'Chicago, IL', 'Dallas, TX', datetime('2025-08-22 06:00:00'), datetime('2025-08-23 14:00:00'), 'Refrigerated', 2100.00, 'Temperature sensitive cargo', 48000, 'Food Products', 32, 925, '53'' x 8.5'' x 9''', 'available', datetime('now'), datetime('now')),
('LD003', 'Atlanta, GA', 'Miami, FL', datetime('2025-08-23 10:00:00'), datetime('2025-08-24 08:00:00'), 'Dry Van', 1800.00, 'No weekend delivery', 38000, 'Clothing', 28, 663, '53'' x 8.5'' x 9''', 'available', datetime('now'), datetime('now')),
('LD004', 'Denver, CO', 'Seattle, WA', datetime('2025-08-24 12:00:00'), datetime('2025-08-26 10:00:00'), 'Flatbed', 2800.00, 'Tarping required', 46000, 'Machinery', 5, 1318, '48'' x 8.5'' x 11''', 'available', datetime('now'), datetime('now')),
('LD005', 'Houston, TX', 'New York, NY', datetime('2025-08-25 14:00:00'), datetime('2025-08-27 16:00:00'), 'Dry Van', 3200.00, 'High value load', 42000, 'Medical Equipment', 18, 1628, '53'' x 8.5'' x 9''', 'available', datetime('now'), datetime('now')),
('LD006', 'Portland, OR', 'Las Vegas, NV', datetime('2025-08-26 09:00:00'), datetime('2025-08-27 15:00:00'), 'Dry Van', 1650.00, 'Standard delivery', 40000, 'Consumer Goods', 22, 869, '53'' x 8.5'' x 9''', 'booked', datetime('now'), datetime('now')),
('LD007', 'Tampa, FL', 'Nashville, TN', datetime('2025-08-27 11:00:00'), datetime('2025-08-28 17:00:00'), 'Refrigerated', 1950.00, 'Keep frozen at -10F', 44000, 'Frozen Foods', 35, 461, '53'' x 8.5'' x 9''', 'available', datetime('now'), datetime('now')),
('LD008', 'Phoenix, AZ', 'San Antonio, TX', datetime('2025-08-28 07:00:00'), datetime('2025-08-29 13:00:00'), 'Dry Van', 1400.00, 'Weekend pickup OK', 36000, 'Automotive Parts', 12, 853, '53'' x 8.5'' x 9''', 'available', datetime('now'), datetime('now')),
('LD009', 'Kansas City, MO', 'Minneapolis, MN', datetime('2025-08-29 13:00:00'), datetime('2025-08-30 19:00:00'), 'Dry Van', 1100.00, 'Easy loading/unloading', 32000, 'Paper Products', 40, 464, '53'' x 8.5'' x 9''', 'available', datetime('now'), datetime('now')),
('LD010', 'Sacramento, CA', 'Salt Lake City, UT', datetime('2025-08-30 08:00:00'), datetime('2025-08-31 14:00:00'), 'Flatbed', 2200.00, 'Oversized load permit included', 48000, 'Construction Materials', 8, 652, '48'' x 8.5'' x 11''', 'available', datetime('now'), datetime('now'));

-- Insert sample calls
INSERT INTO calls (carrier_mc_number, load_id, call_start_time, call_end_time, call_duration, outcome, sentiment, initial_rate_offered, final_rate_agreed, negotiation_rounds, notes, call_transcript, transferred_to_rep, created_at, updated_at) VALUES
('MC123456', 'LD001', datetime('2025-08-20 09:15:00'), datetime('2025-08-20 09:22:00'), 420, 'accepted', 'positive', 1250.00, 1250.00, 0, 'Carrier accepted rate immediately', 'Agent: Hello, this is Sarah from LoadMatch. I have a load from LA to Phoenix... Carrier: That works for us, we can take it at your rate.', 0, datetime('now'), datetime('now')),
('MC789012', 'LD002', datetime('2025-08-20 10:30:00'), datetime('2025-08-20 10:45:00'), 900, 'negotiating', 'neutral', 2100.00, NULL, 2, 'Carrier wants higher rate for reefer load', 'Agent: We have a reefer load Chicago to Dallas... Carrier: We need at least $2300 for that route with current fuel prices.', 0, datetime('now'), datetime('now')),
('MC345678', 'LD003', datetime('2025-08-20 11:00:00'), datetime('2025-08-20 11:08:00'), 480, 'rejected', 'negative', 1800.00, NULL, 1, 'Carrier not interested in Florida runs', 'Agent: Load available Atlanta to Miami... Carrier: We dont do Florida runs, too much traffic and delays.', 0, datetime('now'), datetime('now')),
('MC901234', 'LD004', datetime('2025-08-20 13:20:00'), datetime('2025-08-20 13:35:00'), 900, 'accepted', 'positive', 2800.00, 2750.00, 1, 'Small negotiation but deal closed', 'Agent: Flatbed load Denver to Seattle... Carrier: Can you do $2750? Agent: Yes, thats acceptable.', 0, datetime('now'), datetime('now')),
('MC567890', 'LD005', datetime('2025-08-20 14:45:00'), datetime('2025-08-20 15:02:00'), 1020, 'transferred', 'neutral', 3200.00, NULL, 0, 'High value load, transferred to senior rep', 'Agent: High value medical equipment load... Carrier: This needs special handling, can I speak to a manager?', 1, datetime('now'), datetime('now')),
('MC111222', 'LD006', datetime('2025-08-20 15:30:00'), datetime('2025-08-20 15:38:00'), 480, 'accepted', 'positive', 1650.00, 1650.00, 0, 'Quick acceptance, regular customer', 'Agent: Portland to Vegas load available... Carrier: Perfect, we run that route weekly. Book us.', 0, datetime('now'), datetime('now')),
('MC333444', 'LD007', datetime('2025-08-20 16:10:00'), datetime('2025-08-20 16:25:00'), 900, 'negotiating', 'neutral', 1950.00, NULL, 1, 'Discussing reefer requirements', 'Agent: Frozen food load Tampa to Nashville... Carrier: We need confirmation on temperature requirements and loading procedures.', 0, datetime('now'), datetime('now')),
('MC555666', 'LD008', datetime('2025-08-20 16:45:00'), datetime('2025-08-20 16:52:00'), 420, 'rejected', 'neutral', 1400.00, NULL, 0, 'Rate too low for current market', 'Agent: Phoenix to San Antonio load... Carrier: That rate is below our minimum for that lane, sorry.', 0, datetime('now'), datetime('now')),
('MC777888', 'LD009', datetime('2025-08-20 17:20:00'), datetime('2025-08-20 17:28:00'), 480, 'accepted', 'positive', 1100.00, 1150.00, 1, 'Small rate increase negotiated', 'Agent: Kansas City to Minneapolis... Carrier: Can you do $1150? Agent: Yes, thats fine.', 0, datetime('now'), datetime('now')),
('MC999000', 'LD010', datetime('2025-08-20 17:50:00'), datetime('2025-08-20 18:05:00'), 900, 'negotiating', 'positive', 2200.00, NULL, 1, 'Discussing permit and route details', 'Agent: Oversized load Sacramento to Salt Lake... Carrier: What are the exact dimensions and do you have permits ready?', 0, datetime('now'), datetime('now'));

-- Insert sample negotiations
INSERT INTO negotiations (call_id, round_number, carrier_offer, system_response, timestamp) VALUES
-- Negotiation for call_id 2 (MC789012, LD002)
(2, 1, 2300.00, 'I understand fuel costs are high. Our rate of $2100 is competitive for this reefer lane. Can we work with that?', datetime('2025-08-20 10:35:00')),
(2, 2, 2250.00, 'Let me check with my supervisor. Would $2150 work for you?', datetime('2025-08-20 10:42:00')),

-- Negotiation for call_id 3 (MC345678, LD003)
(3, 1, NULL, 'I understand your concern about Florida. Would a higher rate of $1900 change your mind?', datetime('2025-08-20 11:05:00')),

-- Negotiation for call_id 4 (MC901234, LD004)
(4, 1, 2750.00, 'That works for us. $2750 is acceptable for this flatbed load.', datetime('2025-08-20 13:32:00')),

-- Negotiation for call_id 7 (MC333444, LD007)
(7, 1, NULL, 'The load must be kept at -10F throughout transport. We provide temperature monitoring. Is your equipment capable?', datetime('2025-08-20 16:18:00')),

-- Negotiation for call_id 9 (MC777888, LD009)
(9, 1, 1150.00, 'Yes, we can do $1150 for this load. Ill book you now.', datetime('2025-08-20 17:25:00')),

-- Negotiation for call_id 10 (MC999000, LD010)
(10, 1, NULL, 'Load dimensions are 48x8.5x11 feet. All permits are ready and will be provided before pickup.', datetime('2025-08-20 17:58:00'));

-- Display confirmation message
SELECT 'Sample data insertion completed successfully!' as message;
