USE tailor_admin_db;

INSERT INTO adminpanel_service (service_name, service_description, gender_type, is_active, created_at) VALUES
('Shirt Stitching', 'Custom men shirt stitching', 'Men', 1, NOW()),
('Pant Stitching', 'Custom men pant stitching', 'Men', 1, NOW()),
('Suit Stitching', 'Men suit stitching', 'Men', 1, NOW()),
('Blouse Stitching', 'Ladies blouse stitching', 'Ladies', 1, NOW()),
('Chudidar Stitching', 'Ladies chudidar stitching', 'Ladies', 1, NOW()),
('Kurti Stitching', 'Ladies kurti stitching', 'Ladies', 1, NOW()),
('Saree Fall & Pico', 'Saree fall and pico service', 'Ladies', 1, NOW()),
('Alteration', 'Dress alteration service', 'Common', 1, NOW());

INSERT INTO adminpanel_serviceprice (service_id, price, effective_from, is_active, created_at) VALUES
(1, 500.00, CURDATE(), 1, NOW()),
(2, 700.00, CURDATE(), 1, NOW()),
(3, 2500.00, CURDATE(), 1, NOW()),
(4, 600.00, CURDATE(), 1, NOW()),
(5, 900.00, CURDATE(), 1, NOW()),
(6, 800.00, CURDATE(), 1, NOW()),
(7, 200.00, CURDATE(), 1, NOW()),
(8, 150.00, CURDATE(), 1, NOW());

INSERT INTO adminpanel_sitesetting (shop_name, phone, email, address, whatsapp_number, instagram_url, facebook_url, updated_at) VALUES
('Smart Tailors', '9876543210', 'smarttailors@gmail.com', 'Chennai, Tamil Nadu', '9876543210', '', '', NOW());
