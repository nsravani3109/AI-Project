-- Insert sample loads data
-- Run in SQLite: .read loads_data.sql

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

SELECT 'Loads data inserted successfully!' as message;
