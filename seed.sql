INSERT INTO roles(name)
VALUES
('ADMIN'),
('MANAGER'),
('EMPLOYEE');

INSERT INTO categories(name, description)
VALUES
('Laptop', 'Ordinateurs portables'),
('Monitor', 'Écrans'),
('Printer', 'Imprimantes');

/* Mot de passe : admin123 */
INSERT INTO users(firstname, lastname, email, password, role_id)
VALUES ('Admin', 'System', 'admin@stock.local', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 1);

/* 
ID : admin@stock.local
Mot de passe : admin123

ID : alice@alexnder.local
Mot de passe : alice123 

ID : benjamin@garault.local
Mot de passe : benjamin123

ID : aurele@martin.local
Mot de passe : aurele123
*/
