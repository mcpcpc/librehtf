INSERT INTO user (role_id, username, password) VALUES (2, 'test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f');
INSERT INTO device (name, description) VALUES ('name1', 'description1');
INSERT INTO test (name, description, device_id) VALUES
  ('name1', 'description1', 1),
  ('name2', 'description2', 1);
INSERT INTO task (name, command, test_id, operator_id, datatype_id) VALUES
  ('name1', 'measured = 42', 1, 1, 1), 
  ('name2', 'measured = 42', 1, 1, 1);
