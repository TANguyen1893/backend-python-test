INSERT INTO users (username, password) VALUES
('user1', '$2b$12$7hQVQYJDxW/GhwIoIQYefelXiUBpCFPw9IS6CcuzjEznMnZ5yc0HC'),
('user2', '$2b$12$gJHfzIMZKxtiEp8ccatceu96J6QBvNqjQ.V33tpw9PDn/ikDpTybK'),
('user3', '$2b$12$XrD.NZyzDH1EWfTFCJ3q6.nQGxZVfYYPCJ/igG4g1CmBsMp2idy0a');

INSERT INTO todos (user_id, description) VALUES
(1, 'Vivamus tempus'),
(1, 'lorem ac odio'),
(1, 'Ut congue odio'),
(1, 'Sodales finibus'),
(1, 'Accumsan nunc vitae'),
(2, 'Lorem ipsum'),
(2, 'In lacinia est'),
(2, 'Odio varius gravida');