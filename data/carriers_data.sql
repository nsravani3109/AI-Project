-- Insert sample carriers data
-- Run in SQLite: .read carriers_data.sql

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

SELECT 'Carriers data inserted successfully!' as message;
