INSERT INTO device (name, description) VALUES ('name1', 'description1');
INSERT INTO test (name, description, device_id) VALUES
  ('name1', 'description1', 1),
  ('name2', 'description2', 1);
INSERT INTO task (name, command, test_id, operator_id, datatype_id) VALUES
  ('name1', 'measured = 42', 1, 1, 1), 
  ('name2', 'measured = 42', 1, 1, 1);
